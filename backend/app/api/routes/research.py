"""
Endpoints for Pakistani market research and trending keyword scans.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trend_keyword import TrendKeyword
from app.schemas.research_schema import MarketScanResponse, TrendItemSchema
from app.scout.demand_scanner import SearchDemandScanner

router = APIRouter()


@router.post("/scan", response_model=MarketScanResponse)
def trigger_market_scan(db: Session = Depends(get_db)):
    """Triggers an immediate multi-source Pakistani market scan."""
    scanner = SearchDemandScanner()
    saved = scanner.run_full_market_scan(db)

    total_scanned = len(saved)
    new_opps = sum(1 for item in saved if not item.exists_in_store)
    already_store = total_scanned - new_opps

    top_items = [TrendItemSchema.model_validate(item) for item in saved[:15]]

    return MarketScanResponse(
        total_scanned=total_scanned,
        new_opportunities_found=new_opps,
        already_in_store_count=already_store,
        top_opportunities=top_items,
    )


@router.get("/trends", response_model=List[TrendItemSchema])
def list_trending_keywords(db: Session = Depends(get_db), limit: int = 50):
    """Retrieves discovered trends with catalog gap status."""
    trends = db.query(TrendKeyword).order_by(TrendKeyword.last_scanned_at.desc()).limit(limit).all()
    return [TrendItemSchema.model_validate(t) for t in trends]

