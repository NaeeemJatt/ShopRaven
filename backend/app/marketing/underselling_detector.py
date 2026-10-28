"""
Under-Selling / Dead-Stock Detector & Automated Clearance Flash Sales (Alippo Feature #18).
Identifies high-traffic but low-converting SKUs (>150 views, <0.5% CR), diagnoses root causes,
and auto-schedules 48-hour clearance pricing or BOGO bundles.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.coupons.deal_hunter import DealHunterCouponEngine


class UnderSellingDetector:
    """Detects underperforming SKUs and deploys automated clearance countermeasures."""

    def __init__(self):
        self.coupon_engine = DealHunterCouponEngine()

    def detect_underselling_skus(self, snapshots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Flags products with significant traffic (>150 views) but critically low conversion (<0.5%).
        """
        underselling = []
        for s in snapshots:
            views = int(s.get("views") or s.get("total_views", 0))
            orders = int(s.get("orders") or s.get("total_orders", 0))
            cr = (orders / float(views)) * 100 if views > 0 else 0.0

            if views >= 150 and cr < 0.5:
                diagnosis = self.diagnose_conversion_bottleneck(s)
                underselling.append({
                    "product_id": s.get("product_id") or s.get("id"),
                    "title": s.get("title") or s.get("name", "Product"),
                    "views": views,
                    "orders": orders,
                    "conversion_rate_pct": round(cr, 2),
                    "diagnosis": diagnosis,
                    "recommended_action": diagnosis.get("countermeasure")
                })
        return underselling

    def diagnose_conversion_bottleneck(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Diagnoses why shoppers are not converting:
        1. High Price vs Market Average
        2. Unclear / Weak 1-Line Hook
        3. Delivery Friction on Checkout
        """
        sale_price = float(product.get("sale_price", 1399))
        market_avg = float(product.get("market_avg", sale_price + 100))
        bounce_rate = float(product.get("bounce_rate", 45.0))

        if sale_price > market_avg:
            return {
                "cause": "PRICE_RESISTANCE",
                "reason": f"Sale price (Rs. {int(sale_price)}) is higher than Pakistani market average (Rs. {int(market_avg)}).",
                "countermeasure": "48-Hour Clearance Flash Sale (Cut price to market average respecting +40% floor)"
            }
        elif bounce_rate > 65.0:
            return {
                "cause": "WEAK_HERO_OR_IMAGE",
                "reason": f"High bounce rate ({bounce_rate}%). Shoppers are leaving product page within 5 seconds.",
                "countermeasure": "Trigger 1080x1080 studio image re-render with high-contrast benefit badge"
            }
        else:
            return {
                "cause": "CHECKOUT_COD_HESITATION",
                "reason": "Shoppers viewing specifications but hesitating on cash delivery credibility.",
                "countermeasure": "Inject WhatsApp Verified Trust Badge + BOGO Bundle Coupon"
            }

    def launch_clearance_flash_sale(self, wc_product_id: int, product: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generates a 48-hour clearance price payload respecting the +40% profit floor.
        """
        prod = product or {}
        sale_price = float(prod.get("sale_price", 1499))
        wholesale_cost = float(prod.get("wholesale_cost", 800))

        # Respect +40% floor
        floor_price = wholesale_cost * 1.40
        discount_candidate = self.coupon_engine.compute_margin_safe_discount(sale_price, wholesale_cost)
        clearance_price = max(sale_price - discount_candidate.get("max_discount_pkr", 150), floor_price)

        # Round to *49 or *99
        rounded_clearance = max(math.ceil(clearance_price / 100) * 100 - 1, floor_price)

        expiry = (datetime.utcnow() + timedelta(hours=48)).isoformat() + "Z"

        return {
            "status": "clearance_scheduled",
            "product_id": wc_product_id,
            "original_sale_price": sale_price,
            "clearance_price_pkr": rounded_clearance,
            "wholesale_floor_pkr": floor_price,
            "savings_pkr": round(sale_price - rounded_clearance, 0),
            "duration": "48 Hours",
            "expires_at": expiry,
            "coupon_code": f"CLEARANCE-{wc_product_id}"
        }


import math

