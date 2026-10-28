"""
Pydantic v2 schemas for Control Room KPIs, charts, and 30-day forecast.
"""

from typing import List, Dict, Any, Optional
from datetime import date
from pydantic import BaseModel, Field


class DashboardKPISchema(BaseModel):
    total_sales_revenue_pkr: float
    true_net_profit_pkr: float
    profit_margin_blended_pct: float
    total_orders_count: int
    delivered_orders_count: int
    in_transit_orders_count: int
    rto_orders_count: int
    rto_rate_pct: float
    total_store_visitors: int
    conversion_rate_pct: float
    active_published_skus: int
    drafts_in_queue_count: int


class CityPerformanceSchema(BaseModel):
    city_name: str
    order_count: int
    delivered_count: int
    rto_count: int
    total_revenue_pkr: float


class SalesForecastSchema(BaseModel):
    wc_product_id: int
    product_title: str
    supplier_sku: str
    current_stock_estimated: int
    daily_sales_velocity: float
    forecast_30_day_orders: int
    forecast_30_day_revenue_pkr: float
    days_until_stockout: int
    restock_recommended: bool
    urgency_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'

