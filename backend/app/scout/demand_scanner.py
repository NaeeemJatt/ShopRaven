"""
Search Demand Scanner: Aggregates signals from Google PK, Daraz, PriceOye, and Meta Ads
into a unified composite demand score (0-100).
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.trend_keyword import TrendKeyword
from app.models.wc_product_sync import WCProductSync
from app.scout.google_trends_pk import GoogleTrendsPKCollector
from app.scout.daraz_priceoye_movers import MarketplaceVelocityScanner
from app.scout.meta_ads_pk_verifier import MetaAdLibraryVerifier


class SearchDemandScanner:
    """Combines multi-channel signals and computes composite demand score."""

    def __init__(self):
        self.google_collector = GoogleTrendsPKCollector()
        self.marketplace_scanner = MarketplaceVelocityScanner()
        self.meta_verifier = MetaAdLibraryVerifier()

    def rank_candidates_by_opportunity(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Computes composite opportunity score:
        - Search Volume & Organic Growth (40%)
        - Marketplace Velocity (35%)
        - Commercial Buyer Intent & Social Validation (25%)
        """
        ranked = []
        for item in candidates:
            growth = min(item.get("growth_pct", 0.0) / 100.0, 1.0) * 40.0
            velocity = item.get("velocity_score", 65.0) * 0.35
            ads_info = self.meta_verifier.check_active_pk_ads(item["keyword"])
            ad_score = ads_info["longevity_score"] * 0.25

            # High-intent organic buyer modifier boost (+10 points)
            kw_lower = item["keyword"].lower()
            intent_boost = 0.0
            if any(term in kw_lower for term in ["price in pakistan", "cash on delivery", "online", "sasta", "daraz"]):
                intent_boost = 10.0

            composite_score = round(growth + velocity + ad_score + intent_boost, 1)
            item["opportunity_score"] = min(composite_score, 100.0)
            item["meta_ads"] = ads_info
            ranked.append(item)

        # Sort descending by opportunity score
        ranked.sort(key=lambda x: x["opportunity_score"], reverse=True)
        return ranked

    def run_full_market_scan(self, db: Session) -> List[TrendKeyword]:
        """Runs multi-source discovery across open categories, checks catalog gap, and updates DB."""
        raw_candidates = []

        # 1. Google Trends & Autocomplete PK across all categories
        google_items = self.google_collector.fetch_rising_shopping_queries_pk()
        raw_candidates.extend(google_items)

        # 2. Daraz Movers across all top consumer categories
        daraz_categories = ["kitchen", "beauty", "electronics", "home", "accessories", "baby", "fitness", "tools"]
        for cat_slug in daraz_categories:
            daraz_items = self.marketplace_scanner.scan_daraz_category_leaders(cat_slug)
            raw_candidates.extend(daraz_items)

        # 3. PriceOye Movers
        priceoye_items = self.marketplace_scanner.scan_priceoye_accessories()
        raw_candidates.extend(priceoye_items)

        # Rank candidates with organic intent prioritization
        scored_candidates = self.rank_candidates_by_opportunity(raw_candidates)

        # Fetch existing store products for Token Similarity Catalog Gap Analysis
        existing_products = db.query(WCProductSync).all()
        existing_tokens_map = {
            p.wc_product_id: set(p.title.lower().split()) for p in existing_products
        }

        saved_keywords: List[TrendKeyword] = []
        seen_keywords = set()

        for candidate in scored_candidates:
            keyword_str = candidate.get("keyword", "").strip()
            if not keyword_str:
                continue

            normalized_key = keyword_str.lower()
            if normalized_key in seen_keywords:
                continue
            seen_keywords.add(normalized_key)

            tokens_str = candidate.get("normalized_tokens", "")
            candidate_tokens = set(tokens_str.split())

            # Check if exists in DB already (case-insensitive)
            existing_kw = db.query(TrendKeyword).filter(
                func.lower(TrendKeyword.keyword) == normalized_key
            ).first()

            if not existing_kw:
                # Perform Catalog Gap Check
                is_in_store = False
                matched_id = None

                for prod_id, p_tokens in existing_tokens_map.items():
                    if candidate_tokens and len(candidate_tokens.intersection(p_tokens)) >= 2:
                        is_in_store = True
                        matched_id = prod_id
                        break

                new_record = TrendKeyword(
                    keyword=keyword_str,
                    normalized_tokens=tokens_str,
                    category_name=candidate.get("category_name", "General"),
                    monthly_searches=candidate.get("monthly_searches", 1000),
                    growth_pct=candidate.get("growth_pct", 20.0),
                    source=candidate.get("source", "Google PK"),
                    exists_in_store=is_in_store,
                    matched_wc_product_id=matched_id,
                )
                try:
                    db.add(new_record)
                    db.commit()
                    db.refresh(new_record)
                    saved_keywords.append(new_record)
                except IntegrityError:
                    db.rollback()
                    # Concurrent worker or collision safety: load existing record and update
                    existing_kw = db.query(TrendKeyword).filter(
                        func.lower(TrendKeyword.keyword) == normalized_key
                    ).first()
                    if existing_kw:
                        try:
                            existing_kw.last_scanned_at = datetime.utcnow()
                            existing_kw.growth_pct = candidate.get("growth_pct", existing_kw.growth_pct)
                            existing_kw.monthly_searches = candidate.get("monthly_searches", existing_kw.monthly_searches)
                            db.commit()
                        except Exception:
                            db.rollback()
                        saved_keywords.append(existing_kw)
            else:
                # Refresh metrics for existing keyword
                try:
                    existing_kw.last_scanned_at = datetime.utcnow()
                    existing_kw.growth_pct = candidate.get("growth_pct", existing_kw.growth_pct)
                    existing_kw.monthly_searches = candidate.get("monthly_searches", existing_kw.monthly_searches)
                    db.commit()
                except Exception:
                    db.rollback()
                saved_keywords.append(existing_kw)

        return saved_keywords


class PakistanMarketScout(SearchDemandScanner):
    """Facade for market discovery."""
    pass

