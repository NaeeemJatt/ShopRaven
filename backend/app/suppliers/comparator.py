"""
Dual Supplier Comparator: Evaluates HHC vs. Oshi Dropshipping in parallel,
selects the lower wholesale PKR cost, saves to database, and triggers pipeline.
"""

import json
from typing import Optional
from sqlalchemy.orm import Session
from app.models.supplier_offer import SupplierOfferRecord
from app.models.trend_keyword import TrendKeyword
from app.schemas.supplier_schema import SupplierOfferSchema, DualSupplierCompareResponse
from app.suppliers.hhc_client import HHCDropshippingClient
from app.suppliers.oshi_client import OshiDropshippingClient


class DualSupplierComparator:
    """Compares offers from HHC and Oshi to pick the winning wholesale source."""

    def __init__(self):
        self.hhc_client = HHCDropshippingClient()
        self.oshi_client = OshiDropshippingClient()

    def compute_title_similarity(self, query: str, candidate_title: str) -> float:
        """Computes Jaccard token similarity between search query and supplier product title."""
        query_tokens = set(query.lower().split())
        title_tokens = set(candidate_title.lower().split())
        if not query_tokens or not title_tokens:
            return 0.0
        intersection = query_tokens.intersection(title_tokens)
        union = query_tokens.union(title_tokens)
        return float(len(intersection)) / float(len(union))

    def compare_and_select_winner(self, keyword: str, db: Session) -> Optional[SupplierOfferSchema]:
        """
        Searches HHC and Oshi simultaneously.
        Filters out out-of-stock items, selects the supplier with lowest wholesale PKR cost,
        and saves both offers to the database.
        """
        hhc_offer = self.hhc_client.search_product(keyword)
        oshi_offer = self.oshi_client.search_product(keyword)

        # Get parent trend keyword if registered
        trend_rec = db.query(TrendKeyword).filter(TrendKeyword.keyword == keyword).first()
        trend_id = trend_rec.id if trend_rec else None

        # Persist HHC Offer
        if hhc_offer:
            hhc_rec = SupplierOfferRecord(
                trend_keyword_id=trend_id,
                supplier_name="HHC",
                supplier_url=hhc_offer.supplier_url,
                supplier_sku=hhc_offer.supplier_sku,
                product_title=hhc_offer.product_title,
                wholesale_cost_pkr=hhc_offer.wholesale_cost_pkr,
                in_stock=hhc_offer.in_stock,
                raw_description=hhc_offer.raw_description,
                specs_json=json.dumps(hhc_offer.specs),
                image_urls_json=json.dumps(hhc_offer.image_urls),
            )
            db.add(hhc_rec)

        # Persist Oshi Offer
        if oshi_offer:
            oshi_rec = SupplierOfferRecord(
                trend_keyword_id=trend_id,
                supplier_name="OSHI",
                supplier_url=oshi_offer.supplier_url,
                supplier_sku=oshi_offer.supplier_sku,
                product_title=oshi_offer.product_title,
                wholesale_cost_pkr=oshi_offer.wholesale_cost_pkr,
                in_stock=oshi_offer.in_stock,
                raw_description=oshi_offer.raw_description,
                specs_json=json.dumps(oshi_offer.specs),
                image_urls_json=json.dumps(oshi_offer.image_urls),
            )
            db.add(oshi_rec)

        db.commit()

        # Selection logic
        candidates = []
        if hhc_offer and hhc_offer.in_stock:
            candidates.append(hhc_offer)
        if oshi_offer and oshi_offer.in_stock:
            candidates.append(oshi_offer)

        if not candidates:
            # Fallback to whatever is available
            candidates = [o for o in [hhc_offer, oshi_offer] if o]

        if not candidates:
            return None

        # Select lowest wholesale cost
        candidates.sort(key=lambda x: x.wholesale_cost_pkr)
        winner = candidates[0]
        return winner

