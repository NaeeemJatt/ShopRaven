"""
Pydantic v2 validation contracts and structured output schemas.
"""

from app.schemas.research_schema import (
    TrendItemSchema,
    MarketScanRequest,
    MarketScanResponse,
)
from app.schemas.supplier_schema import (
    SupplierOfferSchema,
    DualSupplierCompareResponse,
)
from app.schemas.pricing_schema import (
    PricingRequestSchema,
    CompetitivePricingResponseSchema,
)
from app.schemas.seo_aeo_schema import (
    FAQItemSchema,
    GeminiSEOAEOOutputSchema,
    WooCommerceReadyPackageSchema,
)
from app.schemas.analytics_schema import (
    DashboardKPISchema,
    CityPerformanceSchema,
    SalesForecastSchema,
)

__all__ = [
    "TrendItemSchema",
    "MarketScanRequest",
    "MarketScanResponse",
    "SupplierOfferSchema",
    "DualSupplierCompareResponse",
    "PricingRequestSchema",
    "CompetitivePricingResponseSchema",
    "FAQItemSchema",
    "GeminiSEOAEOOutputSchema",
    "WooCommerceReadyPackageSchema",
    "DashboardKPISchema",
    "CityPerformanceSchema",
    "SalesForecastSchema",
]

