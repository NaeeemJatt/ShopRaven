"""
Pydantic v2 schemas for Gemini 2.5 Flash Structured Outputs and WooCommerce listings.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FAQItemSchema(BaseModel):
    question: str
    answer: str


class GeminiSEOAEOOutputSchema(BaseModel):
    catchy_headline_hook: str = Field(..., description="1-line bold hook tailored for Pakistani shoppers")
    key_bullet_points: List[str] = Field(..., min_length=3, max_length=5, description="3-5 concise selling points")
    persuasive_description_html: str = Field(..., description="Full conversion-focused product description")
    aeo_direct_answer_summary: str = Field(..., description="~45-word direct answer summary for AI engines")
    roman_urdu_synonyms: List[str] = Field(..., min_length=5, description="Localized Roman-Urdu search phrases")
    phonetic_misspellings: List[str] = Field(..., description="Common Pakistani typos for WooCommerce tags")
    rankmath_title: str
    rankmath_meta_description: str
    faqs: List[FAQItemSchema] = Field(..., min_length=3, max_length=4)


class WooCommerceReadyPackageSchema(BaseModel):
    title: str
    slug: str
    regular_price: str
    sale_price: str
    short_description: str
    description: str
    categories: List[Dict[str, Any]]
    tags: List[Dict[str, str]]
    images: List[Dict[str, str]]
    meta_data: List[Dict[str, Any]]
    json_ld_schema: Dict[str, Any]

