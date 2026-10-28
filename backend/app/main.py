"""
FastAPI application entrypoint for ShopRaven AI Engine.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import Base, engine
from app.api.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist in dev/test mode
    if settings.ENVIRONMENT in ["development", "test"]:
        Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic if any


app = FastAPI(
    title="ShopRaven Engine",
    description="Autonomous E-Commerce AI Cofounder Platform for nnstore.shop",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware for Control Room Dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for container orchestrators."""
    return {
        "status": "healthy",
        "service": "ShopRaven Engine",
        "environment": settings.ENVIRONMENT,
        "storefront": settings.WC_STORE_URL,
    }


# Mount API v1 router
app.include_router(api_router)

