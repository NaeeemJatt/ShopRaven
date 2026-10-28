"""
Model for tracking Pakistani trending keywords and catalog gap analysis.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base


class TrendKeyword(Base):
    __tablename__ = "trend_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), unique=True, nullable=False, index=True)
    normalized_tokens = Column(String(255), nullable=False)
    category_name = Column(String(100), nullable=False, index=True)
    monthly_searches = Column(Integer, default=0)
    growth_pct = Column(Float, default=0.0)
    source = Column(String(50), default="Google PK")  # 'Google PK', 'Daraz', 'Meta Ads'
    exists_in_store = Column(Boolean, default=False, index=True)
    matched_wc_product_id = Column(Integer, nullable=True)
    last_scanned_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TrendKeyword(keyword='{self.keyword}', exists={self.exists_in_store})>"

