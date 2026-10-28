"""
Main API Router aggregating all v1 sub-routers.
"""

from fastapi import APIRouter
from app.api.routes import (
    research,
    suppliers,
    pricing,
    seo_aeo,
    blog,
    marketing,
    analytics,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(research.router, prefix="/research", tags=["Research & Scout"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Dual Suppliers"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["Pricing & Margin Guard"])
api_router.include_router(seo_aeo.router, prefix="/seo-aeo", tags=["SEO & AEO Engine"])
api_router.include_router(blog.router, prefix="/blog", tags=["Auto Blogger"])
api_router.include_router(marketing.router, tags=["Extended Growth Suite & Marketing"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Control Room Analytics"])

