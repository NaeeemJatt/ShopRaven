"""
Model auditing every calculation from CompetitivePricingEngine.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PricingAudit(Base):
    __tablename__ = "pricing_audits"

    id = Column(Integer, primary_key=True, index=True)
    supplier_offer_id = Column(Integer, ForeignKey("supplier_offers.id", ondelete="CASCADE"), nullable=False)
    wholesale_cost_pkr = Column(Float, nullable=False)
    min_40_pkr = Column(Float, nullable=False)
    max_50_pkr = Column(Float, nullable=False)
    competitor_prices_json = Column(Text, nullable=True)  # JSON array of float prices scraped
    market_avg_pkr = Column(Float, nullable=False)
    recommended_sale_pkr = Column(Float, nullable=False)
    recommended_regular_pkr = Column(Float, nullable=False)
    net_profit_pkr = Column(Float, nullable=False)
    profit_margin_pct = Column(Float, nullable=False)
    strategy_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    supplier_offer = relationship("SupplierOfferRecord", backref="pricing_audits")

    def __repr__(self):
        return f"<PricingAudit(Sale PKR {self.recommended_sale_pkr}, Margin: {self.profit_margin_pct:.1%})>"

