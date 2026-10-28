"""
Model tracking WooCommerce synchronized products on nnstore.shop.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.database import Base


class WCProductSync(Base):
    __tablename__ = "wc_products_sync"

    id = Column(Integer, primary_key=True, index=True)
    wc_product_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), nullable=False, index=True)
    category_name = Column(String(100), nullable=False, index=True)
    supplier_name = Column(String(50), nullable=True)  # 'HHC' or 'OSHI'
    supplier_sku = Column(String(100), nullable=True)
    wholesale_cost_pkr = Column(Float, nullable=True)
    sale_price_pkr = Column(Float, nullable=False)
    regular_price_pkr = Column(Float, nullable=False)
    net_profit_pkr = Column(Float, nullable=True)
    status = Column(String(50), default="draft", index=True)  # 'draft', 'publish', 'outofstock', 'redirected'
    menu_order = Column(Integer, default=0, index=True)
    total_views = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    redirect_target_url = Column(String(500), nullable=True)
    json_ld_schema = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<WCProductSync(ID={self.wc_product_id}, Title='{self.title}', Status='{self.status}')>"

