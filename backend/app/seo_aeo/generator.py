"""
NNStore SEO & AEO Content Generation Engine.
Invokes Gemini 2.5 Flash (with structured outputs) or uses high-converting fallback logic.
"""

import re
import json
from typing import Dict, Any, List
import requests
from app.config import get_settings
from app.schemas.supplier_schema import SupplierOfferSchema
from app.schemas.pricing_schema import CompetitivePricingResponseSchema
from app.schemas.seo_aeo_schema import (
    GeminiSEOAEOOutputSchema,
    WooCommerceReadyPackageSchema,
    FAQItemSchema,
)
from app.seo_aeo.prompts import NNSTORE_SEO_AEO_SYSTEM_PROMPT, build_product_seo_prompt
from app.seo_aeo.json_ld_builder import JSONLDSchemaBuilder
from app.seo_aeo.roman_urdu_mapper import RomanUrduSearchMapper

settings = get_settings()


class NNStoreSEOAEOEngine:
    """Generates localized copy, RankMath SEO, and JSON-LD for nnstore.shop."""

    def __init__(self):
        self.schema_builder = JSONLDSchemaBuilder()
        self.roman_mapper = RomanUrduSearchMapper()

    def _call_gemini_api(self, prompt: str) -> Dict[str, Any]:
        """Calls Gemini 2.5 Flash via REST API with application/json mime type."""
        if not settings.GEMINI_API_KEY:
            return {}

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": NNSTORE_SEO_AEO_SYSTEM_PROMPT},
                        {"text": prompt},
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.4,
                "responseMimeType": "application/json",
            },
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json()
                text_content = data["candidates"][0]["content"]["parts"][0]["text"]
                return json.loads(text_content)
        except Exception:
            pass

        return {}

    def _generate_fallback_content(
        self, offer: SupplierOfferSchema, pricing: CompetitivePricingResponseSchema, category: str
    ) -> Dict[str, Any]:
        """High-converting deterministic copywriting fallback."""
        title = offer.product_title
        sale_pkr = int(pricing.recommended_sale_price)

        whatsapp_number = getattr(settings, "ADMIN_WHATSAPP_NUMBER", "+923114618934") or "+923114618934"
        return {
            "catchy_headline_hook": f"Upgrade Your Daily Lifestyle with the Authentic {title} — Now in Pakistan!",
            "key_bullet_points": [
                "Premium Build & Tested Durability: Engineered for long-lasting daily use.",
                "Fast Cash on Delivery: Flat Rs. 150 shipping fee to any doorstep in Pakistan.",
                "Safe & Risk-Free: 7-day checking warranty backed by nnstore.shop support.",
                f"Dedicated Customer Help: Direct WhatsApp assistance at {whatsapp_number}.",
            ],
            "persuasive_description_html": f"""<h2>Why Choose {title} from nnstore.shop?</h2>
<p>Are you looking for an authentic, high-performance solution that delivers true value? The <strong>{title}</strong> is selected for its superior reliability, sleek aesthetic, and proven quality across Pakistan.</p>
<h3>Key Specifications & Features:</h3>
<ul>
  <li><strong>Authentic Quality:</strong> Factory checked and certified for premium performance.</li>
  <li><strong>Unbeatable Value:</strong> Delivered at an affordable price of only Rs. {sale_pkr:,}.</li>
  <li><strong>Peace of Mind:</strong> Inspect and pay upon arrival with our trusted Cash-on-Delivery service.</li>
</ul>
<p><em>Have questions or need bulk ordering? WhatsApp us 24/7 at {whatsapp_number}.</em></p>""",
            "aeo_direct_answer_summary": f"The {title} is a verified, top-rated product available in Pakistan at nnstore.shop for Rs. {sale_pkr:,} with Rs. 150 flat Cash-on-Delivery delivery in 3-5 working days.",
            "roman_urdu_synonyms": self.roman_mapper.generate_local_synonyms(title, category)[:6],
            "phonetic_misspellings": self.roman_mapper.generate_phonetic_typos(title),
            "rankmath_title": f"{title[:42]} - Rs. {sale_pkr:,} | Flat Rs. 150 COD | nnstore.shop",
            "rankmath_meta_description": f"Buy authentic {title[:32]} in Pakistan at Rs. {sale_pkr:,}. Flat Rs. 150 COD delivery nationwide with 7-day warranty. Order via WhatsApp {whatsapp_number}.",
            "faqs": [
                {
                    "question": f"What is the price of {title} in Pakistan?",
                    "answer": f"The price is Rs. {sale_pkr:,} on nnstore.shop with a flat Rs. 150 Cash-on-Delivery fee nationwide.",
                },
                {
                    "question": "How long does delivery take?",
                    "answer": "Delivery takes 3 to 5 business days anywhere in Pakistan via TCS, Trax, or Leopard Couriers.",
                },
                {
                    "question": "How can I contact customer support?",
                    "answer": f"You can reach nnstore.shop official WhatsApp support anytime at {whatsapp_number}.",
                },
            ],
        }

    def generate_package(
        self,
        offer: SupplierOfferSchema,
        pricing: CompetitivePricingResponseSchema,
        category: str,
    ) -> WooCommerceReadyPackageSchema:
        """Assembles the complete WooCommerce-ready listing package."""
        prompt = build_product_seo_prompt(offer.model_dump(), pricing.model_dump(), category)
        ai_data = self._call_gemini_api(prompt)

        if not ai_data or "catchy_headline_hook" not in ai_data:
            ai_data = self._generate_fallback_content(offer, pricing, category)

        # Build Short Description (1-line bold hook + 4 bullets)
        bullets_html = "".join([f"<li>{b}</li>" for b in ai_data.get("key_bullet_points", [])[:4]])
        short_description = f"<p><strong>{ai_data.get('catchy_headline_hook', '')}</strong></p>\n<ul>\n{bullets_html}\n</ul>"

        # Generate slug
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", offer.product_title.lower()).strip("-")[:80]

        # Generate Schema.org JSON-LD (Product, Offer, Rating, Returns, FAQPage, BreadcrumbList)
        json_ld = self.schema_builder.build_product_and_faq_schema(
            slug=slug,
            title=offer.product_title,
            sku=offer.supplier_sku,
            sale_price=pricing.recommended_sale_price,
            images=offer.image_urls,
            aeo_summary=ai_data.get("aeo_direct_answer_summary", ""),
            faqs=ai_data.get("faqs", []),
            category=category,
        )

        # Embed JSON-LD into full description for automated crawling
        json_ld_script = f'\n<script type="application/ld+json">\n{json.dumps(json_ld, indent=2)}\n</script>'
        full_description = f"{ai_data.get('persuasive_description_html', '')}\n{json_ld_script}"

        # Combine Roman-Urdu synonyms + phonetic typos
        all_synonyms = set(self.roman_mapper.generate_local_synonyms(offer.product_title, category))
        for s in ai_data.get("roman_urdu_synonyms", []):
            all_synonyms.add(s)
        for t in ai_data.get("phonetic_misspellings", []):
            all_synonyms.add(t)

        tags = [{"name": tag} for tag in list(all_synonyms)[:25]]

        # RankMath and ShopRaven custom meta_data with multi-keyword comma-separated targeting
        focus_keywords = [
            offer.product_title,
            f"{offer.product_title} price in pakistan",
            f"buy {offer.product_title} online",
            f"{offer.product_title} cash on delivery"
        ]
        if all_synonyms:
            focus_keywords.append(list(all_synonyms)[0])
        focus_keyword_str = ", ".join(focus_keywords[:4])

        default_rankmath_title = f"{offer.product_title[:42]} - Rs. {int(pricing.recommended_sale_price):,} | Flat Rs. 150 COD | nnstore.shop"
        default_rankmath_desc = f"Buy authentic {offer.product_title[:32]} in Pakistan at Rs. {int(pricing.recommended_sale_price):,}. Flat Rs. 150 COD nationwide. 7 days warranty."

        target_seo_title = ai_data.get("rankmath_title") or default_rankmath_title
        target_seo_desc = ai_data.get("rankmath_meta_description") or default_rankmath_desc

        meta_data = [
            # RankMath SEO
            {"key": "rank_math_title", "value": target_seo_title},
            {"key": "rank_math_description", "value": target_seo_desc},
            {"key": "rank_math_focus_keyword", "value": focus_keyword_str},
            # Yoast SEO Cross-Compatibility
            {"key": "_yoast_wpseo_title", "value": target_seo_title},
            {"key": "_yoast_wpseo_metadesc", "value": target_seo_desc},
            {"key": "_yoast_wpseo_focuskw", "value": focus_keyword_str},
            # ShopRaven Internal Intelligence & Head Schema
            {"key": "_shopraven_json_ld_schema", "value": json.dumps(json_ld)},
            {"key": "_shopraven_supplier_name", "value": offer.supplier_name},
            {"key": "_shopraven_supplier_sku", "value": offer.supplier_sku},
            {"key": "_shopraven_supplier_cost_pkr", "value": str(offer.wholesale_cost_pkr)},
            {"key": "_shopraven_search_synonyms", "value": ", ".join(list(all_synonyms)[:25])},
            {"key": "_shopraven_aeo_summary", "value": ai_data.get("aeo_direct_answer_summary", "")},
        ]

        # Google Image Search optimized gallery with keyword-rich alt tags & titles
        images = []
        for idx, url in enumerate(offer.image_urls[:5]):
            if idx == 0:
                alt_text = f"{offer.product_title} - Price in Pakistan | Flat Rs. 150 COD"
            elif idx == 1:
                alt_text = f"{offer.product_title} Features & Specifications - nnstore.shop"
            elif idx == 2:
                alt_text = f"{offer.product_title} Box Packaging & 7 Days Checking Warranty"
            else:
                alt_text = f"{offer.product_title} Customer Reviews in Pakistan"

            images.append({
                "src": url,
                "name": f"{offer.product_title} - Photo {idx + 1}",
                "alt": alt_text
            })

        return WooCommerceReadyPackageSchema(
            title=offer.product_title,
            slug=slug,
            regular_price=str(pricing.recommended_regular_price),
            sale_price=str(pricing.recommended_sale_price),
            short_description=short_description,
            description=full_description,
            categories=[{"name": category}],
            tags=tags,
            images=images,
            meta_data=meta_data,
            json_ld_schema=json_ld,
        )

