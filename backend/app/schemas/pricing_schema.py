"""
Pydantic v2 schemas for margin-guarded competitive pricing calculations.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PricingRequestSchema(BaseModel):
    wholesale_cost_pkr: float = Field(..., gt=0, description="Winning supplier wholesale PKR cost")
    product_title: str
    category_name: str
    competitor_prices: Optional[List[float]] = Field(default=None)


class CompetitivePricingResponseSchema(BaseModel):
    wholesale_cost_pkr: float
    min_40_profit_price: float = Field(..., description="Wholesale * 1.40 margin floor")
    max_50_profit_price: float = Field(..., description="Wholesale * 1.50 margin target")
    market_average_price: float
    competitor_landed_total: float = Field(..., description="Market Avg + Rs. 220 competitor courier")
    recommended_sale_price: float = Field(..., description="Final sale price ending in *49 or *99")
    recommended_regular_price: float = Field(..., description="Strikethrough list price ending in *49 or *99")
    nnstore_landed_total: float = Field(..., description="Sale Price + Rs. 150 separate COD delivery")
    net_profit_pkr: float
    profit_margin_pct: float
    discount_saving_pct: float
    is_margin_safe: bool = True
    strategy_note: str

