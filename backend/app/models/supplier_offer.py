"""
Model for storing raw and normalized offers scraped from HHC and Oshi dropshipping.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class SupplierOfferRecord(Base):
    __tablename__ = "supplier_offers"

    id = Column(Integer, primary_key=True, index=True)
    trend_keyword_id = Column(Integer, ForeignKey("trend_keywords.id", ondelete="SET NULL"), nullable=True)
    supplier_name = Column(String(50), nullable=False)  # 'HHC' or 'OSHI'
    supplier_url = Column(String(500), nullable=False)
    supplier_sku = Column(String(100), nullable=False, index=True)
    product_title = Column(String(300), nullable=False)
    wholesale_cost_pkr = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True, index=True)
    raw_description = Column(Text, nullable=True)
    specs_json = Column(Text, nullable=True)  # JSON string of specifications dict
    image_urls_json = Column(Text, nullable=True)  # JSON list of raw image URLs
    scraped_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    trend_keyword = relationship("TrendKeyword", backref="supplier_offers")

    def __repr__(self):
        return f"<SupplierOfferRecord({self.supplier_name}:{self.supplier_sku} - PKR {self.wholesale_cost_pkr})>"

