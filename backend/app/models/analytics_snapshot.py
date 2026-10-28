"""
Model for daily analytics snapshot rollups (Alippo Features #2 & #13).
"""

from datetime import date, datetime
from sqlalchemy import Column, Integer, Float, Date, DateTime, Text
from app.database import Base


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(Date, unique=True, nullable=False, index=True, default=date.today)
    total_visitors = Column(Integer, default=0)
    new_visitors = Column(Integer, default=0)
    returning_visitors = Column(Integer, default=0)
    gross_sales_pkr = Column(Float, default=0.0)
    shipping_collected_pkr = Column(Float, default=0.0)
    supplier_cost_pkr = Column(Float, default=0.0)
    net_profit_pkr = Column(Float, default=0.0)
    total_orders = Column(Integer, default=0)
    delivered_orders = Column(Integer, default=0)
    in_transit_orders = Column(Integer, default=0)
    rto_orders = Column(Integer, default=0)
    aeo_referrals = Column(Integer, default=0)
    city_breakdown_json = Column(Text, nullable=True)  # JSON dict of city -> count
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AnalyticsSnapshot({self.snapshot_date}: Net PKR {self.net_profit_pkr})>"

