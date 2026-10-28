"""
Endpoints for competitive price calculation and Deal Hunter coupon creation.
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.supplier_schema import SupplierOfferSchema
from app.schemas.pricing_schema import CompetitivePricingResponseSchema
from app.pricing.engine import CompetitivePricingEngine
from app.coupons.deal_hunter import DealHunterCouponEngine

router = APIRouter()


class DealHunterRequest(BaseModel):
    sale_price_pkr: float
    wholesale_cost_pkr: float
    code_prefix: str = "DEAL"


@router.post("/calculate", response_model=CompetitivePricingResponseSchema)
def calculate_price(offer: SupplierOfferSchema, db: Session = Depends(get_db)):
    """Calculates landed COD price adhering strictly to the +40% to +50% profit band."""
    engine = CompetitivePricingEngine()
    return engine.calculate_optimal_price(offer, db)


@router.post("/deal-hunter-coupon")
def create_deal_hunter_coupon(req: DealHunterRequest):
    """Calculates maximum margin-safe discount and generates 30-minute coupon."""
    coupon_engine = DealHunterCouponEngine()
    discount_analysis = coupon_engine.compute_margin_safe_discount(
        req.sale_price_pkr, req.wholesale_cost_pkr
    )

    if discount_analysis["can_discount"]:
        coupon_payload = coupon_engine.generate_one_time_coupon_payload(
            code_prefix=req.code_prefix,
            discount_pkr=discount_analysis["recommended_discount_pkr"],
        )
        return {
            "eligible": True,
            "analysis": discount_analysis,
            "coupon": coupon_payload,
        }

    return {
        "eligible": False,
        "analysis": discount_analysis,
        "coupon": None,
    }

