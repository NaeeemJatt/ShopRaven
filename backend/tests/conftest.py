"""
Pytest configuration and test fixtures for ShopRaven backend test suite.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.schemas.supplier_schema import SupplierOfferSchema

# In-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh in-memory database schema for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden get_db dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_supplier_offer():
    """Returns a realistic wholesale product offer from HHC."""
    return SupplierOfferSchema(
        id=101,
        supplier_name="HHC",
        supplier_url="https://member.hhcdropshipping.com/en/products/view/ultrasonic-skin-scrubber",
        supplier_sku="HHC-58421",
        product_title="Ultrasonic Skin Scrubber Pore Cleaner",
        wholesale_cost_pkr=850.0,
        in_stock=True,
        raw_description="Deep facial cleansing ultrasound device for blackheads.",
        specs={"battery": "600mAh", "modes": "Cleansing, Moisturizing, Lifting"},
        image_urls=[
            "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800",
            "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800",
        ],
    )

