"""
Unit tests for Schema.org JSON-LD & SEO/AEO Builder.
"""

from app.seo_aeo.json_ld_builder import JSONLDSchemaBuilder


def test_schema_org_json_ld_structure():
    """Verifies that generated @graph conforms to Product, Shipping, and FAQ standards."""
    builder = JSONLDSchemaBuilder()
    graph = builder.build_product_and_faq_schema(
        slug="ultrasonic-skin-scrubber",
        title="Ultrasonic Skin Scrubber Pore Cleaner",
        sku="HHC-58421",
        sale_price=1399.0,
        images=["https://nnstore.shop/image.jpg"],
        aeo_summary="Direct answer summary for test product.",
        faqs=[
            {"question": "What is delivery fee?", "answer": "Flat Rs. 150 across Pakistan."}
        ],
    )

    assert "@context" in graph
    assert graph["@context"] == "https://schema.org"
    assert "@graph" in graph

    entities = {e["@type"]: e for e in graph["@graph"]}
    assert "Product" in entities
    assert "FAQPage" in entities

    product = entities["Product"]
    assert product["name"] == "Ultrasonic Skin Scrubber Pore Cleaner"
    assert product["offers"]["priceCurrency"] == "PKR"
    assert product["offers"]["price"] == "1399.0"

    # Verify flat Rs. 150 COD shipping detail
    shipping = product["offers"]["shippingDetails"]
    assert shipping["shippingRate"]["value"] == "150"
    assert shipping["shippingRate"]["currency"] == "PKR"
    assert shipping["shippingDestination"]["addressCountry"] == "PK"

