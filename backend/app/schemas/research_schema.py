"""
Pydantic v2 schemas for Pakistani market research and demand scanning.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class TrendItemSchema(BaseModel):
    id: Optional[int] = None
    keyword: str = Field(..., description="Target search query or trending product phrase")
    normalized_tokens: str = Field(..., description="Lowercase clean tokens for similarity matching")
    category_name: str = Field(..., description="One of nnstore.shop's 7 official categories")
    monthly_searches: int = Field(default=0, ge=0)
    growth_pct: float = Field(default=0.0)
    source: str = Field(default="Google PK")
    exists_in_store: bool = Field(default=False)
    matched_wc_product_id: Optional[int] = None
    opportunity_score: float = Field(default=0.0, ge=0.0, le=100.0)
    last_scanned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MarketScanRequest(BaseModel):
    category_filter: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    min_growth_pct: float = Field(default=10.0)


class MarketScanResponse(BaseModel):
    total_scanned: int
    new_opportunities_found: int
    already_in_store_count: int
    top_opportunities: List[TrendItemSchema]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

