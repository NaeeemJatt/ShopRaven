# ShopRaven Roadmap

## Completed Milestones

### Phase 1: Core Scaffolding & Configuration (Sprint 1) — ✅ COMPLETED
- Docker Compose multi-container setup (Postgres 16, Redis 7, Backend, Celery, Orchestrator).
- FastAPI backend initialization, SQLAlchemy 2.0 Base, Pydantic v2 schemas.
- Alembic database migration setup (001–007).

### Phase 2: Market Demand Scout & Dual-Supplier Vault (Sprint 2) — ✅ COMPLETED
- Google Trends PK, Daraz.pk movers, PriceOye scraper, Meta Ads verifier.
- HHC & Oshi Dropshipping session vault & comparator.
- Automated token similarity catalog gap check on `nnstore.shop`.

### Phase 3: Competitive Pricing & 1080x1080 Studio (Sprint 3) — ✅ COMPLETED
- +40% to +50% margin guard with flat Rs. 150 COD delivery math.
- 1080x1080 square studio canvas generator with `#FAFAFC` background.
- Localized Roman-Urdu mapper & Gemini 2.5 Flash SEO/AEO engine.

### Phase 4: Alippo Core Parity Modules (Sprint 4) — ✅ COMPLETED
- Deal Hunter price-hesitation coupon engine (capped at +40% floor).
- Autonomous SEO Blog generator with embedded product cards.
- 30-Day sales forecaster & true net profit accounting.

### Phase 5: Node.js Orchestrator & Live Storefront Automation (Sprint 5) — ✅ COMPLETED
- WooCommerce REST API v3 client with IPv4 forced resolution.
- Live catalog sync & 1-click draft-to-live product publisher.
- Menu reordering by sales velocity, 301 smart redirects, and WhatsApp cart recovery.

### Phase 6: Mission Control Dashboard & WordPress Bridge (Sprint 6) — ✅ COMPLETED
- `nnstore_ai_dashboard.html` / `index.html` with real-time 5-engine pipeline monitor.
- Live Storefront Product Preview modal.
- `shopraven-bridge` WordPress plugin with Cart Progress Bar and COD/Prepaid incentive.

---

## Active Milestone: v2.0.0 Complete Edition

### Phase 7: Alippo Extended Growth Suite (Features #14 to #21) — ✅ COMPLETED
**Goal:** Implement the 8 remaining growth features from *ShopRaven Complete Project Specification 02.pdf* to achieve 100% full parity (21/21 features) across AI video reels, ad planning, Meta CAPI, review shield, dead-stock clearance, broken image healing, and storefront speed/heatmaps.

- **Plan 07-01: Creative & Visual Studio Engine (Features #14 & #14B)**
  - `backend/app/studio/video_carousel_generator.py` (5-slide 1080x1080 Meta carousel + 9:16 vertical MP4 product reel)
  - `backend/app/studio/festival_banner_maker.py` (Ramzan, Eid, 14 August, 11.11, Blessed Friday sale banners)
- **Plan 07-02: Marketing, Ad Planning & Live Feeds (Features #15, #16A, #18, #19)**
  - `backend/app/marketing/ad_campaign_planner.py` (7-Day Meta ad planner with Break-Even ROAS & kill/scale rules)
  - `backend/app/marketing/product_feeds_xml.py` (Live Meta Catalog XML & Google Shopping PK XML feeds)
  - `backend/app/marketing/underselling_detector.py` (Dead-stock detector & 48h clearance flash sales)
  - `backend/app/marketing/broken_image_auditor.py` (Broken image crawler & auto-healer)
  - `backend/app/api/routes/marketing.py` & router registration
- **Plan 07-03: WhatsApp Engagement, Rating Shield & Creator Outreach (Features #17 & #20)**
  - `orchestrator/src/whatsapp/review_rating_shield.js` (Post-delivery WhatsApp check-in: 4-5★ to public photo reviews, 1-3★ to private WhatsApp)
  - `orchestrator/src/whatsapp/creator_associate_outreach.js` (Influencer / UGC Creator outreach & sales tasks)
- **Plan 07-04: Meta Conversions API (CAPI) & Server-Side Tracking (Feature #16B)**
  - `orchestrator/src/tracking/meta_capi_dispatcher.js` (Server-side CAPI events with SHA-256 hashed data)
  - `wordpress-plugin/shopraven-bridge/includes/class-meta-capi-pixel.php` (Browser-side pixel with deduplication keys)
- **Plan 07-05: Storefront Speed Optimizer & Heatmap Tracker (Features #21A & #21B)**
  - `wordpress-plugin/shopraven-bridge/includes/class-speed-optimizer.php` (LCP high-priority, script deferral, WebP compression)
  - `wordpress-plugin/shopraven-bridge/includes/class-heatmap-tracker.php` (Scroll depth, rage clicks, click coordinates beacon)
  - `wordpress-plugin/shopraven-bridge/shopraven-bridge.php` (Hook registration)
- **Plan 07-06: Control Room Frontend Integration & Verification (Frontend & Tests)**
  - `frontend/src/components/AdPlannerAndCreativeView.tsx`
  - `frontend/nnstore_ai_dashboard.html` & `frontend/index.html` (Ad Planner tab & controls)
  - `backend/tests/test_ad_planner_and_healer.py` (Unit tests verifying Break-Even ROAS, Underselling & Healer)

