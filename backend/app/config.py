"""
Configuration management for ShopRaven Python Backend.
Enforces business rules and environment constraints for nnstore.shop.
"""

from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, HttpUrl, field_validator


NNSTORE_CATEGORIES: List[str] = [
    "Beauty & Care",
    "Kitchen Accessories",
    "Home & Living",
    "Gym Accessories",
    "Electronic Accessories",
    "Auto & Tools",
    "Accessories",
]


class Settings(BaseSettings):
    # App environment
    ENVIRONMENT: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    SECRET_KEY: str = Field(default="shopraven-secure-key-2026")
    BACKEND_HOST: str = Field(default="0.0.0.0")
    BACKEND_PORT: int = Field(default=8000)

    # Database & Redis
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/shopraven"
    )
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # Storefront settings
    WC_STORE_URL: str = Field(default="https://nnstore.shop")
    WC_CONSUMER_KEY: str = Field(default="")
    WC_CONSUMER_SECRET: str = Field(default="")
    WP_APP_USERNAME: str = Field(default="")
    WP_APP_PASSWORD: str = Field(default="")

    # Business Rules (Locked)
    DEFAULT_DELIVERY_FEE_PKR: float = Field(default=150.0)
    FREE_DELIVERY_THRESHOLD_PKR: float = Field(default=2500.0)
    PREPAID_DISCOUNT_PERCENT: float = Field(default=5.0)

    # Margins & Competitor courier benchmark
    PROFIT_MIN_PCT: float = Field(default=0.40)  # +40% profit floor
    PROFIT_MAX_PCT: float = Field(default=0.50)  # +50% profit target
    COMPETITOR_AVG_SHIPPING_PKR: float = Field(default=220.0)

    # Supplier Credentials
    HHC_BASE_URL: str = Field(default="https://member.hhcdropshipping.com")
    HHC_EMAIL: str = Field(default="")
    HHC_PASSWORD: str = Field(default="")

    OSHI_BASE_URL: str = Field(default="https://www.portal.oshidropship.com")
    OSHI_EMAIL: str = Field(default="")
    OSHI_PASSWORD: str = Field(default="")

    # AI & Communications
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash")
    DISCORD_WEBHOOK_URL: str = Field(default="")
    DISCORD_BOT_TOKEN: str = Field(default="")
    WHATSAPP_TOKEN: str = Field(default="")
    WHATSAPP_PHONE_NUMBER_ID: str = Field(default="")
    STORE_SUPPORT_WHATSAPP: str = Field(default="+923124999196")
    WASENDER_API_URL: str = Field(default="https://wasenderapi.com/api/send-message")
    WASENDER_API_TOKEN: str = Field(default="")
    ADMIN_WHATSAPP_NUMBER: str = Field(default="+923114618934")

    @field_validator("PROFIT_MIN_PCT")
    @classmethod
    def validate_min_profit(cls, v: float) -> float:
        if v < 0.30 or v > 0.60:
            raise ValueError("PROFIT_MIN_PCT must be within realistic margins (0.30 - 0.60)")
        return v

    @field_validator("PROFIT_MAX_PCT")
    @classmethod
    def validate_max_profit(cls, v: float, info) -> float:
        min_pct = info.data.get("PROFIT_MIN_PCT", 0.40)
        if v < min_pct:
            raise ValueError("PROFIT_MAX_PCT must be greater than or equal to PROFIT_MIN_PCT")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Returns cached singleton Settings instance."""
    return Settings()

