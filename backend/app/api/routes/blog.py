"""
Endpoints for generating and publishing SEO buying guides with product cards.
"""

from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from app.blog.auto_blogger import SEOBlogPublisher

router = APIRouter()


class BlogPublishRequest(BaseModel):
    topic: str
    wc_products: List[Dict[str, Any]]


@router.post("/generate-and-publish")
def generate_and_publish_blog(req: BlogPublishRequest):
    """Generates 900-word buying guide embedding live WooCommerce product cards."""
    publisher = SEOBlogPublisher()
    post_payload = publisher.generate_blog_post_with_product_cards(req.topic, req.wc_products)
    published = publisher.publish_to_wordpress(post_payload)
    return {
        "status": "success",
        "topic": req.topic,
        "wordpress_post": published,
    }

