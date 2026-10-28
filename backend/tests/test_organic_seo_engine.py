"""
Unit tests for ShopRaven Organic SEO & Viral Keyword Research Engine.
Verifies organic Google search dominance, Roman-Urdu tags, Schema.org rich snippets,
and commercial intent prioritization for zero-ad-spend traffic.
"""

from app.scout.google_trends_pk import GoogleTrendsPKCollector
from app.scout.demand_scanner import SearchDemandScanner
from app.seo_aeo.roman_urdu_mapper import RomanUrduSearchMapper
from app.seo_aeo.json_ld_builder import JSONLDSchemaBuilder
from app.blog.auto_blogger import SEOBlogPublisher


def test_google_trends_pk_open_categories():
    """Verifies that Google Trends PK scanner searches open categories with high-intent modifiers."""
    collector = GoogleTrendsPKCollector()
    queries = collector.fetch_rising_shopping_queries_pk(custom_categories=["Baby & Kids", "Smart Gadgets & Novelty"], max_seeds_per_cat=1)
    assert len(queries) >= 2
    keywords = [q["keyword"].lower() for q in queries]
    # Check that commercial/transactional queries are generated
    assert any("price in pakistan" in kw or "baby" in kw or "gadget" in kw or "fan" in kw for kw in keywords)


def test_demand_scanner_organic_buyer_intent_boost():
    """Verifies that candidate keywords with commercial intent get an opportunity score boost."""
    scanner = SearchDemandScanner()
    candidates = [
        {"keyword": "random gadget without intent", "growth_pct": 20.0, "velocity_score": 50.0},
        {"keyword": "sunset lamp price in pakistan", "growth_pct": 20.0, "velocity_score": 50.0},
    ]
    ranked = scanner.rank_candidates_by_opportunity(candidates)
    # The keyword with 'price in pakistan' should rank higher due to intent boost
    assert ranked[0]["keyword"] == "sunset lamp price in pakistan"
    assert ranked[0]["opportunity_score"] > ranked[1]["opportunity_score"]


def test_expanded_roman_urdu_dictionary():
    """Verifies that Roman-Urdu mapper finds colloquial phrases across modern open categories."""
    mapper = RomanUrduSearchMapper()
    # Test electronic category (e.g. neck fan)
    fan_synonyms = mapper.generate_local_synonyms("Portable Rechargeable Neck Fan", "Electronic Accessories")
    assert any("fan" in s or "garmi" in s for s in fan_synonyms)

    # Test kitchen chopper
    chopper_synonyms = mapper.generate_local_synonyms("Electric Vegetable Chopper", "Kitchen Accessories")
    assert any("chopper" in s or "tamatar" in s or "sabzi" in s for s in chopper_synonyms)


def test_schema_org_rich_snippets_star_ratings_and_returns():
    """Verifies Google SERP 5-star review rating and 7-day return policy in Product Schema."""
    builder = JSONLDSchemaBuilder()
    graph = builder.build_product_and_faq_schema(
        slug="rechargeable-mini-fan",
        title="Portable Rechargeable Mini Neck Fan",
        sku="HHC-8912",
        sale_price=1899.0,
        images=["https://nnstore.shop/fan.jpg"],
        aeo_summary="Compact hands-free cooling fan with 3 speed modes.",
        faqs=[{"question": "How long does battery last?", "answer": "Up to 6 hours on full charge."}]
    )

    entities = {e["@type"]: e for e in graph["@graph"]}
    product = entities["Product"]

    # Google Review Stars
    assert "aggregateRating" in product
    assert product["aggregateRating"]["ratingValue"] == "4.8"
    assert product["aggregateRating"]["bestRating"] == "5"

    # Google Free Returns Policy
    offer = product["offers"]
    assert "hasMerchantReturnPolicy" in offer
    assert offer["hasMerchantReturnPolicy"]["merchantReturnDays"] == 7
    assert offer["hasMerchantReturnPolicy"]["applicableCountry"] == "PK"

    # Google SERP BreadcrumbList
    assert "BreadcrumbList" in entities
    breadcrumbs = entities["BreadcrumbList"]
    assert len(breadcrumbs["itemListElement"]) == 3
    assert breadcrumbs["itemListElement"][0]["name"] == "Home"


def test_image_alt_tags_for_google_image_search():
    """Verifies that generated WooCommerce packages have keyword-rich alt tags on gallery images."""
    from app.schemas.supplier_schema import SupplierOfferSchema
    from app.schemas.pricing_schema import CompetitivePricingResponseSchema
    from app.seo_aeo.generator import NNStoreSEOAEOEngine

    engine = NNStoreSEOAEOEngine()
    offer = SupplierOfferSchema(
        supplier_name="HHC Dropshipping",
        supplier_sku="HHC-1234",
        supplier_url="https://hhcdropshipping.com/product/chopper",
        product_title="Rechargeable Mini Garlic Chopper",
        wholesale_cost_pkr=650.0,
        stock_available=25,
        rating=4.7,
        image_urls=["https://hhc.pk/img1.jpg", "https://hhc.pk/img2.jpg"]
    )
    pricing = CompetitivePricingResponseSchema(
        wholesale_cost_pkr=650.0,
        min_40_profit_price=910.0,
        max_50_profit_price=975.0,
        market_average_price=1350.0,
        competitor_landed_total=1570.0,
        recommended_sale_price=1249.0,
        recommended_regular_price=1849.0,
        nnstore_landed_total=1399.0,
        profit_margin_pct=48.0,
        net_profit_pkr=599.0,
        discount_saving_pct=32.0,
        is_margin_safe=True,
        strategy_note="Optimal profit margin corridor"
    )
    package = engine.generate_package(offer, pricing, "Kitchen Accessories")
    assert len(package.images) == 2
    assert "alt" in package.images[0]
    assert "Price in Pakistan" in package.images[0]["alt"]


def test_auto_blogger_faq_schema_and_comparison_table():
    """Verifies that the auto blogger generates Schema.org FAQPage script and price table."""
    blogger = SEOBlogPublisher()
    post = blogger.generate_blog_post_with_product_cards(
        topic="Electric Choppers",
        wc_products=[{"id": 101, "name": "Mini Chopper", "price": "1499"}]
    )
    content = post["content"]
    assert 'type="application/ld+json"' in content
    assert '"@type": "FAQPage"' in content
    assert '<table' in content
    assert 'Flat Rs. 150 Nationwide' in content

