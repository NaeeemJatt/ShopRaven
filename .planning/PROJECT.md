# ShopRaven — Autonomous E-Commerce AI Cofounder for nnstore.shop

## Project Overview
ShopRaven is a production autonomous e-commerce operations, product research, dual-supplier sourcing, dynamic pricing, SEO/AEO publishing, and real-time analytics platform built specifically for `https://nnstore.shop` in the Pakistani Cash-on-Delivery (COD) market.

## Architecture Stack
- **Python 3.11+ Backend**: FastAPI, SQLAlchemy 2.0, Celery + Redis, Playwright, BeautifulSoup4, Pillow, Gemini 2.5 Flash Structured Outputs.
- **Node.js 18+ Orchestrator**: Express, Node-Cron, WooCommerce REST API v3 Client, WhatsApp Cloud API, Discord Bot Gateway.
- **WordPress Bridge Plugin (`shopraven-bridge`)**: WooCommerce hooks, Cart Progress Bar, Prepaid Discount Waiver, 24/7 Product Q&A Bot, Meta CAPI Pixel, Speed Optimizer, Heatmap Tracker.
- **Frontend Control Room**: Interactive single-page app and dashboard (`nnstore_ai_dashboard.html` / `index.html`), Tailwind CSS 3.4, Chart.js 4.4.

## Locked Business Rules
1. **Storefront**: `https://nnstore.shop` (Active WooCommerce store on Hostinger LiteSpeed).
2. **Wholesale Suppliers**: HHC Dropshipping (`member.hhcdropshipping.com`) & Oshi Dropshipping (`portal.oshidropship.com`) via authenticated session vault scraping.
3. **Pricing Rule**: +40% to +50% profit margin over wholesale PKR cost, with flat Rs. 150 COD shipping fee billed separately at checkout.
4. **Price Rounding**: Psychological endings ending in `*49` or `*99` PKR (e.g., Rs. 649, 1,399, 2,049).
5. **Image Standard**: 1080x1080 soft-studio canvas (`#FAFAFC`), +6% contrast, +12% sharpness, direct `.jpeg`/`.png` upload paths.

