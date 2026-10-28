"""
Model for tracking customer segmentation and deal hunter behavior (Alippo Features #5 & #12).
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class CustomerSegment(Base):
    __tablename__ = "customer_segments"

    id = Column(Integer, primary_key=True, index=True)
    phone_or_email = Column(String(100), unique=True, nullable=False, index=True)
    city = Column(String(100), nullable=True)
    total_orders = Column(Integer, default=0)
    delivered_orders = Column(Integer, default=0)
    rto_orders = Column(Integer, default=0)
    total_spent_pkr = Column(Float, default=0.0)
    segment_tag = Column(
        String(50), default="NEW_VISITOR", index=True
    )  # 'NEW_VISITOR', 'RETURNING_VIP', 'DEAL_HUNTER', 'CART_ABANDONER', 'HIGH_RTO_RISK'
    last_coupon_code = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CustomerSegment({self.phone_or_email} - {self.segment_tag})>"

