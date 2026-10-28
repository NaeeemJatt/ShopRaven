"""
Deal Hunter Coupon Engine (Alippo Feature #5).
Detects price-hesitation shoppers and generates 30-minute single-use coupons
strictly protecting the +40% minimum profit floor.
"""

import secrets
from datetime import datetime, timedelta
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()


class DealHunterCouponEngine:
    """Calculates margin-safe discount allowances and creates single-use coupon payloads."""

    def compute_margin_safe_discount(self, sale_price_pkr: float, wholesale_cost_pkr: float) -> Dict[str, Any]:
        """
        Calculates maximum permissible discount ensuring:
        (sale_price - discount) >= wholesale_cost * 1.40
        """
        profit_floor = wholesale_cost_pkr * (1.0 + settings.PROFIT_MIN_PCT)  # +40% floor
        max_possible_discount = max(0.0, sale_price_pkr - profit_floor)

        if max_possible_discount <= 0.0:
            return {
                "can_discount": False,
                "max_discount_pkr": 0.0,
                "recommended_discount_pkr": 0.0,
                "effective_sale_price_pkr": sale_price_pkr,
                "profit_floor_pkr": profit_floor,
                "reason": "Current sale price is already at or below the +40% profit floor.",
            }

        # Offer ~60% of the maximum headroom so profit remains comfortably above +40%
        # Example: Headroom Rs. 300 -> Offer Rs. 150 or Rs. 200 coupon
        recommended_discount = round(min(max_possible_discount * 0.60, max_possible_discount), 0)
        # Round to convenient denominations (e.g., 50, 100, 150, 200)
        if recommended_discount > 50:
            recommended_discount = float(int(recommended_discount / 50) * 50)

        effective_price = sale_price_pkr - recommended_discount
        remaining_margin_pct = (effective_price - wholesale_cost_pkr) / wholesale_cost_pkr

        return {
            "can_discount": recommended_discount > 0,
            "max_discount_pkr": round(max_possible_discount, 2),
            "recommended_discount_pkr": recommended_discount,
            "effective_sale_price_pkr": effective_price,
            "profit_floor_pkr": profit_floor,
            "remaining_profit_margin_pct": round(remaining_margin_pct * 100.0, 2),
            "is_floor_respected": effective_price >= (profit_floor - 0.01),
        }

    def generate_one_time_coupon_payload(self, code_prefix: str = "DEAL", discount_pkr: float = 150.0) -> Dict[str, Any]:
        """Generates WooCommerce single-use 30-minute coupon definition."""
        random_suffix = secrets.token_hex(3).upper()
        coupon_code = f"{code_prefix}-{random_suffix}"
        expiry_time = datetime.utcnow() + timedelta(minutes=30)

        return {
            "code": coupon_code,
            "discount_type": "fixed_cart",
            "amount": str(int(discount_pkr)),
            "individual_use": True,
            "usage_limit": 1,
            "usage_limit_per_user": 1,
            "date_expires": expiry_time.isoformat(),
            "description": f"ShopRaven Deal Hunter 30-minute exclusive discount for Rs. {int(discount_pkr)} off.",
        }

