"""
Endpoints for Pakistani market research and trending keyword scans.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.trend_keyword import TrendKeyword
from app.schemas.research_schema import MarketScanResponse, TrendItemSchema
from app.scout.demand_scanner import SearchDemandScanner

router = APIRouter()


@router.post("/scan", response_model=MarketScanResponse)
def trigger_market_scan(db: Session = Depends(get_db)):
    """Triggers an immediate multi-source Pakistani market scan and dispatches pipeline for missing items."""
    scanner = SearchDemandScanner()
    saved = scanner.run_full_market_scan(db)

    total_scanned = len(saved)
    new_opps = sum(1 for item in saved if not item.exists_in_store)
    already_store = total_scanned - new_opps

    # Automatically dispatch autonomous sourcing pipeline for top missing opportunities
    missing = [item for item in saved if not item.exists_in_store][:3]
    for m in missing:
        try:
            from app.tasks.pipeline_tasks import execute_autonomous_product_pipeline
            execute_autonomous_product_pipeline.delay(m.keyword, m.category_name)
        except Exception:
            pass

    top_items = [TrendItemSchema.model_validate(item) for item in saved[:15]]

    return MarketScanResponse(
        total_scanned=total_scanned,
        new_opportunities_found=new_opps,
        already_in_store_count=already_store,
        top_opportunities=top_items,
    )


@router.post("/hunt")
def trigger_product_hunt(payload: Dict[str, Any] = Body(...)):
    """Dispatches an on-demand autonomous product hunting and sourcing pipeline."""
    keyword = payload.get("keyword") or payload.get("target")
    category = payload.get("category", "General Store")
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")

    from app.tasks.pipeline_tasks import execute_autonomous_product_pipeline
    task = execute_autonomous_product_pipeline.delay(keyword, category)
    return {
        "status": "DISPATCHED",
        "task_id": task.id,
        "keyword": keyword,
        "category": category
    }


@router.get("/trends", response_model=List[TrendItemSchema])
def list_trending_keywords(db: Session = Depends(get_db), limit: int = 50):
    """Retrieves discovered trends with catalog gap status."""
    trends = db.query(TrendKeyword).order_by(TrendKeyword.last_scanned_at.desc()).limit(limit).all()
    return [TrendItemSchema.model_validate(t) for t in trends]

