"""
Pydantic v2 schemas for supplier offer extraction and dual-supplier comparison.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class SupplierOfferSchema(BaseModel):
    id: Optional[int] = None
    supplier_name: str = Field(..., description="'HHC' or 'OSHI'")
    supplier_url: str = Field(..., description="Direct product URL on supplier portal")
    supplier_sku: str = Field(..., description="Unique supplier SKU identifier")
    product_title: str = Field(..., description="Raw title from supplier catalog")
    wholesale_cost_pkr: float = Field(..., gt=0, description="Wholesale unit price in Pakistani Rupees")
    in_stock: bool = Field(default=True)
    raw_description: Optional[str] = None
    specs: Dict[str, Any] = Field(default_factory=dict)
    image_urls: List[str] = Field(default_factory=list)
    scraped_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DualSupplierCompareResponse(BaseModel):
    keyword: str
    hhc_offer: Optional[SupplierOfferSchema] = None
    oshi_offer: Optional[SupplierOfferSchema] = None
    winner: Optional[SupplierOfferSchema] = None
    cost_difference_pkr: float = Field(default=0.0)
    savings_pct: float = Field(default=0.0)
    selection_reason: str
    status: str = Field(default="MATCH_FOUND")  # 'MATCH_FOUND', 'OUT_OF_STOCK', 'NO_MATCH'

