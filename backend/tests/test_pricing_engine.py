"""
Unit tests for Competitive Pricing Engine & Margin Guard.
"""

from app.pricing.engine import CompetitivePricingEngine
from app.pricing.rounding import round_to_nnstore_ending, compute_strikethrough_regular_price


def test_rounding_psychological_endings():
    """Verifies that all prices end in 49 or 99 and respect min floor."""
    # Test target 1420 with floor 1400 -> Should round to 1449 or 1399 (if >= floor)
    res = round_to_nnstore_ending(1420.0, min_floor=1400.0)
    assert res in [1449.0, 1399.0] or (res % 100 in [49, 99])
    assert res >= 1400.0

    # Test regular price strikethrough
    regular = compute_strikethrough_regular_price(1399.0)
    assert regular % 100 in [49, 99]
    assert regular > 1399.0


def test_pricing_engine_profit_corridor(sample_supplier_offer, db_session):
    """Verifies that pricing engine maintains >= +40% profit margin."""
    engine = CompetitivePricingEngine()
    result = engine.calculate_optimal_price(sample_supplier_offer, db_session)

    w_cost = sample_supplier_offer.wholesale_cost_pkr
    min_floor = w_cost * 1.40

    assert result.recommended_sale_price >= min_floor
    assert result.recommended_sale_price % 100 in [49, 99]
    assert result.recommended_regular_price % 100 in [49, 99]
    assert result.recommended_regular_price > result.recommended_sale_price
    assert result.is_margin_safe is True
    assert result.net_profit_pkr >= (w_cost * 0.395)

