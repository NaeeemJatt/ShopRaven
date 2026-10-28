"""
Competitive Pricing Engine & +40%–50% Margin Guard.
Implements exact Pakistani COD landed cost equations and psychological rounding.
"""

import json
from typing import Optional
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models.pricing_audit import PricingAudit
from app.schemas.supplier_schema import SupplierOfferSchema
from app.schemas.pricing_schema import CompetitivePricingResponseSchema
from app.pricing.rounding import round_to_nnstore_ending, compute_strikethrough_regular_price
from app.pricing.competitor_scraper import CompetitorPriceScraper

settings = get_settings()


class CompetitivePricingEngine:
    """Calculates doorstep competitive landed pricing with strict margin safety."""

    def __init__(self):
        self.scraper = CompetitorPriceScraper()

    def calculate_optimal_price(
        self, offer: SupplierOfferSchema, db: Optional[Session] = None
    ) -> CompetitivePricingResponseSchema:
        """
        Executes landed cost formula:
        1. Wholesale Cost: W
        2. Floor (+40%): W * 1.40
        3. Ceiling (+50%): W * 1.50
        4. Competitor Landed: Market_Avg + Rs. 220
        5. Position NN Store Landed (Sale + Rs. 150) <= Competitor Landed
        6. Round to *49 or *99
        """
        w_cost = offer.wholesale_cost_pkr
        floor_40 = w_cost * (1.0 + settings.PROFIT_MIN_PCT)
        target_50 = w_cost * (1.0 + settings.PROFIT_MAX_PCT)

        # Scrape competitor market prices
        market_prices = self.scraper.fetch_pk_retail_prices(offer.product_title, w_cost)
        market_avg = self.scraper.compute_trimmed_market_average(market_prices, w_cost)

        # Doorstep Landed Courier comparison
        competitor_landed = market_avg + settings.COMPETITOR_AVG_SHIPPING_PKR  # Rs. 220
        nn_shipping = settings.DEFAULT_DELIVERY_FEE_PKR  # Rs. 150

        # Ideal price to beat competitor at doorstep:
        # NN Store Landed = Sale + 150 <= Competitor Landed
        # Sale <= Competitor Landed - 150
        ideal_competitive_sale = competitor_landed - nn_shipping

        # Position inside profit corridor [floor_40, target_50]
        if ideal_competitive_sale >= target_50:
            # Market allows full 50% target profit while staying cheaper than competitor!
            target_raw = target_50
            strategy_note = "High Margin: Market allows full +50% profit while beating competitor landed cost."
        elif ideal_competitive_sale >= floor_40:
            # Competitively undercut inside the 40%-50% corridor
            target_raw = ideal_competitive_sale
            strategy_note = "Competitive Undercut: Positioned just below competitor landed cost within +40%-50% profit."
        else:
            # Competitor is dumping or selling below margin floor; strictly protect +40% profit floor!
            target_raw = floor_40
            strategy_note = "Margin Protected: Locked at +40% minimum profit floor. Will not match irrational pricing."

        # Apply psychological rounding to *49 or *99
        recommended_sale = round_to_nnstore_ending(target_raw, min_floor=floor_40)
        recommended_regular = compute_strikethrough_regular_price(recommended_sale)

        # Final net metrics
        nnstore_landed = recommended_sale + nn_shipping
        net_profit = recommended_sale - w_cost
        profit_margin = net_profit / w_cost
        discount_saving = round(((recommended_regular - recommended_sale) / recommended_regular) * 100.0, 1)

        # Save audit to DB if session provided
        if db is not None:
            audit = PricingAudit(
                supplier_offer_id=offer.id or 1,
                wholesale_cost_pkr=w_cost,
                min_40_pkr=round(floor_40, 2),
                max_50_pkr=round(target_50, 2),
                competitor_prices_json=json.dumps(market_prices),
                market_avg_pkr=round(market_avg, 2),
                recommended_sale_pkr=recommended_sale,
                recommended_regular_pkr=recommended_regular,
                net_profit_pkr=round(net_profit, 2),
                profit_margin_pct=round(profit_margin, 4),
                strategy_note=strategy_note,
            )
            try:
                db.add(audit)
                db.commit()
            except Exception:
                db.rollback()

        return CompetitivePricingResponseSchema(
            wholesale_cost_pkr=w_cost,
            min_40_profit_price=round(floor_40, 2),
            max_50_profit_price=round(target_50, 2),
            market_average_price=round(market_avg, 2),
            competitor_landed_total=round(competitor_landed, 2),
            recommended_sale_price=recommended_sale,
            recommended_regular_price=recommended_regular,
            nnstore_landed_total=round(nnstore_landed, 2),
            net_profit_pkr=round(net_profit, 2),
            profit_margin_pct=round(profit_margin * 100.0, 2),
            discount_saving_pct=discount_saving,
            is_margin_safe=profit_margin >= 0.395,  # Allow floating point boundary
            strategy_note=strategy_note,
        )

