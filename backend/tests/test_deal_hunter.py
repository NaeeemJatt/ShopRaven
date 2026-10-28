"""
Unit tests for Deal Hunter Coupon Engine (Alippo Feature #5).
"""

from app.coupons.deal_hunter import DealHunterCouponEngine


def test_coupon_respects_40pct_floor():
    """Verifies that generated coupons never reduce net profit below +40% of wholesale cost."""
    engine = DealHunterCouponEngine()
    wholesale_cost = 1000.0
    sale_price = 1699.0  # +69.9% margin initially
    floor_40 = wholesale_cost * 1.40  # 1400.0

    result = engine.compute_margin_safe_discount(sale_price, wholesale_cost)

    assert result["can_discount"] is True
    assert result["is_floor_respected"] is True
    assert result["effective_sale_price_pkr"] >= floor_40
    assert result["remaining_profit_margin_pct"] >= 40.0


def test_zero_discount_when_at_floor():
    """Verifies that if a product is already at the +40% margin floor, no coupon is issued."""
    engine = DealHunterCouponEngine()
    wholesale_cost = 1000.0
    sale_price = 1400.0  # Exactly at +40% floor

    result = engine.compute_margin_safe_discount(sale_price, wholesale_cost)

    assert result["can_discount"] is False
    assert result["recommended_discount_pkr"] == 0.0
    assert result["effective_sale_price_pkr"] == 1400.0


def test_coupon_payload_generation():
    """Verifies format and properties of generated WooCommerce single-use coupon."""
    engine = DealHunterCouponEngine()
    payload = engine.generate_one_time_coupon_payload(code_prefix="SAVE", discount_pkr=150.0)

    assert payload["code"].startswith("SAVE-")
    assert payload["amount"] == "150"
    assert payload["usage_limit"] == 1
    assert payload["individual_use"] is True
    assert "date_expires" in payload

