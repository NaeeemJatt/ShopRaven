"""
Marketing & Extended Growth Suite package for ShopRaven.
"""

from app.marketing.ad_campaign_planner import AdCampaignPlanner
from app.marketing.product_feeds_xml import ProductFeedGenerator
from app.marketing.underselling_detector import UnderSellingDetector
from app.marketing.broken_image_auditor import BrokenImageAuditor

__all__ = [
    "AdCampaignPlanner",
    "ProductFeedGenerator",
    "UnderSellingDetector",
    "BrokenImageAuditor",
]

