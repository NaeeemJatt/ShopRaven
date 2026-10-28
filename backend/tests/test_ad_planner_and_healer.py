"""
Unit tests for Alippo Extended Growth Suite:
Ad Campaign Planner, Under-Selling SKU Detector, and Broken Image Auto-Healer.
"""

import pytest
from app.marketing.ad_campaign_planner import AdCampaignPlanner
from app.marketing.underselling_detector import UnderSellingDetector
from app.marketing.broken_image_auditor import BrokenImageAuditor
from app.marketing.product_feeds_xml import ProductFeedGenerator


def test_breakeven_roas_calculation():
    """Verifies Break-Even ROAS mathematical formula for Pakistani COD."""
    planner = AdCampaignPlanner()

    # Sale = 1399, Cost = 780, RTO = 15% (buffer = Rs. 37.5) -> Net = 581.5 -> ROAS = 1399 / 581.5 = 2.41
    roas = planner.calculate_breakeven_roas(1399.0, 780.0, rto_rate=0.15)
    assert 2.30 <= roas <= 2.50

    # 7-Day Strategy Generation
    plan = planner.generate_7_day_meta_ad_plan(
        daily_budget_pkr=2500.0,
        target_orders=15,
        products=[{
            "id": 1042,
            "title": "Ultrasonic Skin Scrubber",
            "sale_price": 1399,
            "wholesale_cost": 780
        }]
    )
    assert plan["daily_budget_pkr"] == 2500.0
    assert plan["metrics"]["breakeven_roas"] == roas
    assert plan["metrics"]["target_scale_roas"] > roas
    assert len(plan["creative_hooks"]) >= 5
    assert len(plan["seven_day_schedule"]) == 5
    assert "Karachi" in plan["targeting"]["cities"]


def test_underselling_sku_detection():
    """Verifies that high-traffic low-converting SKUs are correctly identified and diagnosed."""
    detector = UnderSellingDetector()

    snapshots = [
        {
            "product_id": 1043,
            "title": "Underperforming Car Charger",
            "views": 250,
            "orders": 1,  # 0.4% CR -> Under-selling!
            "sale_price": 1899,
            "wholesale_cost": 1000,
            "market_avg": 1699,
            "bounce_rate": 55.0
        },
        {
            "product_id": 1042,
            "title": "Winning Skin Scrubber",
            "views": 300,
            "orders": 24,  # 8.0% CR -> Healthy
            "sale_price": 1399,
            "wholesale_cost": 780,
            "market_avg": 1499,
            "bounce_rate": 35.0
        }
    ]

    flagged = detector.detect_underselling_skus(snapshots)
    assert len(flagged) == 1
    assert flagged[0]["product_id"] == 1043
    assert flagged[0]["conversion_rate_pct"] == 0.4
    assert "PRICE_RESISTANCE" in flagged[0]["diagnosis"]["cause"]

    # Test 48-Hour Clearance Flash Sale
    clearance = detector.launch_clearance_flash_sale(
        wc_product_id=1043,
        product={"sale_price": 1899, "wholesale_cost": 1000}
    )
    assert clearance["status"] == "clearance_scheduled"
    assert clearance["clearance_price_pkr"] >= (1000 * 1.40)  # Must strictly respect +40% floor
    assert clearance["clearance_price_pkr"] < 1899  # Must provide discount


def test_broken_image_detection_and_xml_feed():
    """Verifies broken image auditor flagging and valid XML catalog feeds."""
    auditor = BrokenImageAuditor()

    # Product with no images attached
    test_prods = [
        {"id": 999, "name": "Broken Image Product", "images": []}
    ]
    broken = auditor.audit_storefront_product_images(test_prods)
    assert len(broken) == 1
    assert broken[0]["issue"] == "NO_IMAGES_ATTACHED"

    # Auto-heal execution
    healed = auditor.auto_heal_missing_product_images(wc_product_id=999)
    assert healed["status"] == "healed"
    assert healed["verified_resolution"] == "1080x1080"

    # XML Feed Generation
    feed_gen = ProductFeedGenerator()
    xml_data = feed_gen.build_meta_catalog_xml([
        {
            "id": 258,
            "title": "Smart Sunset Lamp",
            "sale_price": 1399,
            "regular_price": 2049,
            "permalink": "https://nnstore.shop/product/sunset-lamp/",
            "image_url": "https://images.pexels.com/photos/3785147/pexels-photo-3785147.jpeg"
        }
    ])
    assert "<rss" in xml_data
    assert 'version="2.0"' in xml_data
    assert "<g:price>2049 PKR</g:price>" in xml_data
    assert "<g:shipping>" in xml_data
    assert "150 PKR" in xml_data

