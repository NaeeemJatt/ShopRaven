"""
Prompts and templates for Gemini 2.5 Flash Structured Outputs for nnstore.shop.
"""

NNSTORE_SEO_AEO_SYSTEM_PROMPT = """You are the Senior Pakistani E-Commerce Merchandiser and AI Organic SEO/AEO Specialist for nnstore.shop.
Your objective is to maximize FREE ORGANIC SEARCH TRAFFIC from Google PK, Google Shopping Free Listings, Perplexity, and Gemini AI Search.

Strict Guidelines:
1. Brand Voice: Premium yet approachable, reliable, authentic, and tailored for Pakistani shoppers.
2. Short Description: Exactly 1 bold catchy hook line followed by 3 to 4 concise bullet points highlighting key specifications and problem-solving benefits.
3. Logistics & Trust: Emphasize 3-5 days nationwide Cash on Delivery (COD) across Pakistan for a flat delivery fee of Rs. 150.
4. Support: Mention 24/7 dedicated customer assistance on WhatsApp at +92 311 4618934.
5. Answer Engine Optimization (AEO): Provide a concise ~45-word direct answer summary answering 'What is this product, why should a Pakistani customer buy it, and what is its delivered price?'.
6. Schema FAQ: Provide 3 practical FAQs addressing high-intent commercial doubts: (1) Pricing in PKR, (2) COD Delivery timeline & shipping fee (Rs. 150), and (3) 7-day checking warranty & WhatsApp support.
7. Return valid JSON adhering strictly to the required schema.
"""


def build_product_seo_prompt(offer_data: dict, pricing_data: dict, category: str) -> str:
    """Builds the user instruction prompt for Gemini 2.5 Flash."""
    title = offer_data.get("product_title", "")
    cost = pricing_data.get("wholesale_cost_pkr", 0)
    sale_pkr = pricing_data.get("recommended_sale_price", 0)
    reg_pkr = pricing_data.get("recommended_regular_price", 0)
    specs = offer_data.get("specs", {})

    return f"""Analyze this wholesale product offer and generate the complete Organic SEO, AEO, and WooCommerce listing package:

Product Title: {title}
Category: {category}
Wholesale PKR: Rs. {cost:,.0f}
Recommended Sale Price: Rs. {sale_pkr:,.0f}
Strikethrough Regular Price: Rs. {reg_pkr:,.0f}
Delivery Fee: Flat Rs. 150 Cash-on-Delivery nationwide
Official Store Support: WhatsApp +92 311 4618934
Specifications: {specs}

Generate:
1. catchy_headline_hook (1 bold line)
2. key_bullet_points (3-4 concise benefit bullets)
3. persuasive_description_html (clean HTML markup, with <h2>, <p>, <ul> tags)
4. aeo_direct_answer_summary (~45 words for Google AEO/AI Overviews)
5. roman_urdu_synonyms (5+ colloquial Pakistani phrases)
6. phonetic_misspellings (3+ common typos)
7. rankmath_title (under 60 chars, including price & 'nnstore.shop')
8. rankmath_meta_description (under 155 chars, including Rs. 150 COD and WhatsApp support)
9. faqs (3 Q&A pairs covering Price, Rs. 150 COD Shipping, and Support)
"""

