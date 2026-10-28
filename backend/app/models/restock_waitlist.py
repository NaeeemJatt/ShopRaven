"""
Model for tracking out-of-stock WhatsApp waitlist subscribers (Alippo Feature #8).
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class RestockWaitlist(Base):
    __tablename__ = "restock_waitlists"

    id = Column(Integer, primary_key=True, index=True)
    wc_product_id = Column(Integer, nullable=False, index=True)
    product_title = Column(String(300), nullable=False)
    customer_whatsapp = Column(String(50), nullable=False, index=True)
    notified = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    checkout_link_sent_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<RestockWaitlist(Product {self.wc_product_id}, WhatsApp: {self.customer_whatsapp}, Notified: {self.notified})>"

