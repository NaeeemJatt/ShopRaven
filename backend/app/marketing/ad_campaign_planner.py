"""
7-Day Meta Ad Campaign Planner with Break-Even ROAS & Kill/Scale Rules (Alippo Feature #15).
Computes exact Break-Even ROAS, selects winning products, writes 5 Roman-Urdu/English ad hooks,
Pakistani city targeting, and automated kill/scale schedule.
"""

from typing import List, Dict, Any, Optional
import math


class AdCampaignPlanner:
    """Automates Meta ad planning, ROAS math, and targeting for Pakistani e-commerce."""

    # Top Pakistani e-commerce purchasing cities by population & purchasing power
    TIER_1_CITIES = [
        "Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad",
        "Multan", "Peshawar", "Gujranwala", "Sialkot", "Hyderabad"
    ]

    def calculate_breakeven_roas(
        self, sale_price_pkr: float, wholesale_cost_pkr: float, rto_rate: float = 0.15
    ) -> float:
        """
        Exact Break-Even ROAS formula for Pakistani COD:
        BE_ROAS = Sale_Price / Net_Margin
        Net_Margin = Sale_Price - Wholesale_Cost - RTO_Buffer (Rs. 250 avg return shipping penalty * RTO rate)
        """
        rto_buffer = rto_rate * 250.0  # Courier return fee buffer
        gross_margin = sale_price_pkr - wholesale_cost_pkr - rto_buffer

        if gross_margin <= 0:
            return 99.0  # Unprofitable unit economics

        be_roas = round(sale_price_pkr / gross_margin, 2)
        return max(be_roas, 1.20)

    def generate_7_day_meta_ad_plan(
        self, daily_budget_pkr: float, target_orders: int, products: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Builds a comprehensive 7-day Meta Ad strategy:
        - Target CPP & Budget Allocation
        - 5 High-Conversion Urdu/English Hooks
        - City & Demographic Targeting
        - 7-Day Optimization Schedule (Kill / Scale Rules)
        """
        if not products:
            products = [{
                "id": 1042,
                "title": "Ultrasonic Skin Scrubber Pore Cleaner Pro",
                "sale_price": 1399,
                "wholesale_cost": 780,
                "category": "Beauty & Care"
            }]

        featured_prod = products[0]
        sale_pkr = float(featured_prod.get("sale_price", 1399))
        cost_pkr = float(featured_prod.get("wholesale_cost", 780))
        title = featured_prod.get("title", "Featured Product")

        be_roas = self.calculate_breakeven_roas(sale_pkr, cost_pkr)
        net_profit_per_order = sale_pkr - cost_pkr - (0.15 * 250)
        max_acceptable_cpp = round(net_profit_per_order * 0.70, 0)  # Max cost per purchase for target profit
        target_roas = round(be_roas * 1.35, 2)

        # 5 High-Conversion Roman-Urdu / English hooks tested in Pakistani market
        hooks = [
            f"⚡ 'Abhi Mangwaein Aur Parcel Khol Kar Tasalli Karein!' — {title} with 100% Cash-on-Delivery.",
            f"🇵🇰 Salon jesa glow ab ghar bethe! Order today on nnstore.shop with Flat Rs. 150 delivery nationwide.",
            f"🔥 Pakistan ki No.1 Trending Beauty Deal! Limited Stock available at just Rs. {int(sale_pkr):,}.",
            f"🛒 'Price dekhiye, TCS se mangwaiye!' 7-Days Easy Exchange & Money-Back Guarantee.",
            f"📦 Zabardast quality, wholesale prices! Order {title} online in 30 seconds."
        ]

        # Instagram Caption
        caption = (
            f"✨ {title} is now available on nnstore.shop!\n\n"
            f"💰 Price: Rs. {int(sale_pkr):,} Only (Flat Rs. 150 Nationwide COD)\n"
            f"🚚 Delivery in 3-5 working days across Pakistan.\n"
            f"📲 WhatsApp Confirmation: +92 312 4999196\n\n"
            f"👉 Tap 'Shop Now' or visit nnstore.shop to order before stock runs out!\n\n"
            f"#nnstore #pakistanonlineshopping #lahore #karachi #islamabad #darazdeals #codpakistan"
        )

        schedule = [
            {"day": "Day 1-2 (Testing)", "action": "Run Broad CBO with 3 creatives. Cap daily ad set spend at Rs. 1,000."},
            {"day": "Day 3 (48-Hour Kill Check)", "action": f"KILL any ad set with Cost Per Purchase (CPP) > Rs. {int(max_acceptable_cpp)} or Zero Add-to-Carts."},
            {"day": "Day 4-5 (Audience Pruning)", "action": "Exclude low-converting cities. Focus 80% budget on Top 5 (Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad)."},
            {"day": "Day 6 (Scaling)", "action": f"SCALE budget by +20% on winning ad sets maintaining ROAS > {target_roas}."},
            {"day": "Day 7 (Retargeting Injection)", "action": "Launch Catalog Sales DPA feed targeting 7-day cart abandoners with Deal Hunter 10% coupon."}
        ]

        return {
            "campaign_name": f"ShopRaven_Meta_Advantage_{title[:25]}",
            "daily_budget_pkr": daily_budget_pkr,
            "target_orders": target_orders,
            "product": title,
            "sale_price_pkr": sale_pkr,
            "wholesale_cost_pkr": cost_pkr,
            "metrics": {
                "breakeven_roas": be_roas,
                "target_scale_roas": target_roas,
                "max_acceptable_cpp_pkr": max_acceptable_cpp,
                "estimated_net_profit_per_order_pkr": round(net_profit_per_order, 0)
            },
            "targeting": {
                "country": "Pakistan (PK)",
                "cities": self.TIER_1_CITIES,
                "age_range": "20 - 45",
                "placements": ["Instagram Feed", "Instagram Reels", "Facebook Feed", "Facebook Video Feeds"]
            },
            "creative_hooks": hooks,
            "instagram_caption": caption,
            "seven_day_schedule": schedule
        }

