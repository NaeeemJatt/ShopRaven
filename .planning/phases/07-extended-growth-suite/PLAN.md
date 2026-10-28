# Phase 7 Plan: Alippo Extended Growth Suite (Features #14 to #21)

## Phase Objective
Implement the 8 advanced growth and scaling features specified in `ShopRaven_Complete_Project_Specification_and_Codebase_Manual 02.pdf` (v2.0.0 Complete Edition). This completes 100% full parity (21 of 21 Alippo features) across AI video reels, seasonal banners, 7-day Meta ad planning, CAPI retargeting, review protection, dead-stock clearance, broken image self-healing, and storefront speed/heatmap tracking.

---

## Execution Waves & Task Breakdown

### Wave 1: Visual & Creative Studio Engine (Features #14 & #14B)

#### Task 07-01-A: Multi-Slide Carousel & Video Reel Studio (Feature #14)
- **Target File:** `backend/app/studio/video_carousel_generator.py`
- **Specification:**
  - `class VideoAndCarouselStudio`:
    - `generate_5_slide_instagram_carousel(product: dict, pricing: dict) -> list[str]`:
      Creates a 5-slide 1080x1080 square graphic set (`Slide 1: Hook`, `Slide 2: Problem`, `Slide 3: Solution`, `Slide 4: Key Specifications`, `Slide 5: PKR COD Offer + Rs. 150 Flat Delivery Badge`).
    - `render_vertical_product_reel_mp4(slides: list[str], audio_track: str = None) -> str`:
      Compiles slides into a 9:16 vertical MP4 format with caption transitions. Gracefully falls back to high-res animated sequence/GIF if ffmpeg is unavailable in minimal environments.
- **Verification:** Unit test confirms 5 slides generated at exact 1080x1080 dimensions with `#FAFAFC` background.

#### Task 07-01-B: Localized Pakistani Festival Sale Banner Maker (Feature #14B)
- **Target File:** `backend/app/studio/festival_banner_maker.py`
- **Specification:**
  - `class FestivalBannerGenerator`:
    - `render_festival_campaign_banner(product: dict, festival_theme: str) -> str`:
      Generates localized festive banner overlays for:
      - `ramzan`: "Ramzan Mega Mubarak Sale — Upto 50% Off"
      - `eid`: "Eid-ul-Fitr Special Deals — Nationwide COD"
      - `azadi`: "14 August Azadi Mubarak Sale — Flat Rs. 150 Delivery"
      - `11_11`: "11.11 Biggest Shopping Festival of Pakistan"
      - `blessed_friday`: "Blessed Friday Mega Savings"
      - Draws strikethrough regular price and bold sale price in PKR.
- **Verification:** Generates test banner with valid dimensions and returns file path.

---

### Wave 2: Marketing, Ad Planning & Live Feeds (Features #15, #16A, #18, #19)

#### Task 07-02-A: 7-Day Meta Ad Campaign Planner (Feature #15)
- **Target File:** `backend/app/marketing/ad_campaign_planner.py`
- **Specification:**
  - `class AdCampaignPlanner`:
    - `calculate_breakeven_roas(sale_price_pkr: float, wholesale_cost_pkr: float, rto_rate: float = 0.15) -> float`:
      Formula: `BE_ROAS = Sale_Price / (Sale_Price - Wholesale_Cost - (rto_rate * 250))`
    - `generate_7_day_meta_ad_plan(daily_budget_pkr: float, target_orders: int, products: list[dict]) -> dict`:
      Generates:
      1. Target Audience & City Clustering (Karachi, Lahore, Rawalpindi/Islamabad, Faisalabad, Multan).
      2. 5 High-Conversion Urdu/English Hooks (e.g. "Abhi mangwaein aur check kar ke payment karein!").
      3. Paste-ready Instagram captions with hashtags.
      4. 7-Day Optimization Schedule ("Kill ad set if CPP > X after 48 hours; Scale budget +20% if ROAS > Y").
- **Verification:** `calculate_breakeven_roas(1499, 750, 0.15)` matches expected mathematical value.

#### Task 07-02-B: Live Meta Catalog & Google Shopping PK XML Feeds (Feature #16A)
- **Target File:** `backend/app/marketing/product_feeds_xml.py`
- **Specification:**
  - `class ProductFeedGenerator`:
    - `build_meta_catalog_xml(products: list[dict]) -> str`:
      Generates Facebook/Meta Catalog RSS 2.0 XML with `<g:id>`, `<g:title>`, `<g:price>PKR ...</g:price>`, `<g:shipping><g:price>150 PKR</g:price></g:shipping>`.
    - `build_google_merchant_pk_xml(products: list[dict]) -> str`:
      Generates Google Merchant Center compliant XML with ISO 4217 PKR currency and Pakistan targeted delivery.
- **Verification:** XML parses cleanly with `xml.etree.ElementTree` without syntax errors.

#### Task 07-02-C: Under-Selling / Dead-Stock Detector & Flash Sales (Feature #18)
- **Target File:** `backend/app/marketing/underselling_detector.py`
- **Specification:**
  - `class UnderSellingDetector`:
    - `detect_underselling_skus(snapshots: list[dict]) -> list[dict]`:
      Identifies SKUs with >150 views and <0.5% conversion rate.
    - `diagnose_conversion_bottleneck(product: dict) -> dict`:
      Diagnoses whether drop-off is caused by: Price vs Market Average, Weak Hook, or High Checkout Drop.
    - `launch_clearance_flash_sale(wc_product_id: int) -> dict`:
      Creates 48-hour clearance discount respecting +40% floor or generates BOGO bundle coupon.
- **Verification:** Correctly classifies low-converting SKUs and calculates clearance price above floor.

#### Task 07-02-D: Broken Product Image & Missing Gallery Auto-Healer (Feature #19)
- **Target File:** `backend/app/marketing/broken_image_auditor.py`
- **Specification:**
  - `class BrokenImageAuditor`:
    - `audit_storefront_product_images(wc_products: list[dict]) -> list[dict]`:
      Crawls product image URLs to detect HTTP 404/500, non-image content types, or missing galleries.
    - `auto_heal_missing_product_images(wc_product_id: int) -> dict`:
      Re-renders 1080x1080 image from supplier raw cache and triggers WooCommerce image re-attachment.
- **Verification:** Flags mock broken image and triggers auto-heal payload.

#### Task 07-02-E: Marketing API Router & Endpoints
- **Target Files:** `backend/app/marketing/__init__.py`, `backend/app/api/routes/marketing.py`, `backend/app/api/router.py`
- **Specification:**
  - Expose:
    - `POST /api/v1/marketing/ad-plan`
    - `POST /api/v1/marketing/generate-creatives`
    - `GET /api/v1/marketing/feeds/meta.xml`
    - `GET /api/v1/marketing/feeds/google-shopping-pk.xml`
    - `POST /api/v1/marketing/audit-underselling`
    - `POST /api/v1/marketing/heal-broken-images`
- **Verification:** FastAPI test client returns 200 OK across all marketing endpoints.

---

### Wave 3: WhatsApp Engagement, Rating Shield & Creator Outreach (Features #17 & #20)

#### Task 07-03-A: Post-Delivery Rating & Review Protection Shield (Feature #17)
- **Target File:** `orchestrator/src/whatsapp/review_rating_shield.js`
- **Specification:**
  - `class StoreRatingProtectionShield`:
    - `triggerPostDeliveryRatingCheck(orderPayload)`:
      Dispatches WhatsApp check-in 24 hours after courier delivery.
    - `handleBuyerRatingReply(phonePK, starRating, feedbackText)`:
      - If 4–5 Stars: Responds with a 1-tap direct link to post a verified review on `nnstore.shop` (optimizes Google SERP 4.8★ rating).
      - If 1–3 Stars: Intercepts the complaint privately, notifies VIP customer support on WhatsApp (+92 312 4999196), and prevents public negative review.
- **Verification:** Unit tests confirm 5-star rating returns public review link; 2-star rating routes to private support.

#### Task 07-03-B: Influencer & UGC Creator Outreach Bot (Feature #20)
- **Target File:** `orchestrator/src/whatsapp/creator_associate_outreach.js`
- **Specification:**
  - `class CreatorAndAssociateOutreachBot`:
    - `onboardUGCCreator(creatorName, phonePK, instagramHandle, productId)`:
      Generates custom affiliate coupon code via `coupon_service.js` and sends product brief with commission terms.
    - `dispatchSalesAssociateTask(associatePhone, taskSummary)`:
      Dispatches daily operational reminders (COD verification calls, pending dispatches).
- **Verification:** Successful coupon creation and task message formatting.

---

### Wave 4: Meta Conversions API (CAPI) & Server-Side Retargeting (Feature #16B)

#### Task 07-04-A: Server-Side Meta CAPI Dispatcher
- **Target File:** `orchestrator/src/tracking/meta_capi_dispatcher.js`
- **Specification:**
  - `class MetaCAPIDispatcher`:
    - `sendServerEvent(eventName, eventId, userData, customData)`:
      Hashes user phone and city with SHA-256 according to Meta Conversions API requirements.
      Sends server-side event payload with shared `event_id` to Meta Graph API (`/v19.0/{pixel_id}/events`).
- **Verification:** Test event generates correct SHA-256 hash and formatted Graph API body.

#### Task 07-04-B: WordPress Browser CAPI Pixel Bridge
- **Target File:** `wordpress-plugin/shopraven-bridge/includes/class-meta-capi-pixel.php`
- **Specification:**
  - `class ShopRaven_Meta_CAPI_Pixel`:
    - `inject_pixel_head_script()`: Injects browser-side pixel with shared `event_id`.
    - `forward_wc_purchase_to_capi($order_id)`: Dispatches purchase event with identical `event_id` to server dispatcher for 100% deduplication.
- **Verification:** PHP syntax check validates cleanly without errors.

---

### Wave 5: Storefront Speed Optimizer & Heatmap Tracker (Features #21A & #21B)

#### Task 07-05-A: Built-In Storefront Speed Optimizer (Feature #21A)
- **Target File:** `wordpress-plugin/shopraven-bridge/includes/class-speed-optimizer.php`
- **Specification:**
  - `class ShopRaven_Speed_Optimizer`:
    - `optimize_lcp_product_images($attr, $attachment)`: Adds `fetchpriority="high"` and removes `loading="lazy"` on primary hero images.
    - `defer_non_critical_assets($tag, $handle)`: Adds `defer` to non-essential JavaScript assets.
- **Verification:** PHP syntax and filter hooks validated.

#### Task 07-05-B: Click, Scroll & Behavior Heatmap Tracker (Feature #21B)
- **Target File:** `wordpress-plugin/shopraven-bridge/includes/class-heatmap-tracker.php`
- **Specification:**
  - `class ShopRaven_Heatmap_Tracker`:
    - `register_telemetry_beacon_endpoint()`: Registers REST route `/wp-json/shopraven/v1/telemetry/heatmap`.
    - Collects scroll depths (25%, 50%, 75%, 100%), rage clicks, and "Add to Cart" vs "Buy via WhatsApp" coordinates.
- **Verification:** REST endpoint callback registered cleanly.

#### Task 07-05-C: WordPress Plugin Integration
- **Target File:** `wordpress-plugin/shopraven-bridge/shopraven-bridge.php`
- **Specification:**
  - Require and instantiate:
    - `ShopRaven_Meta_CAPI_Pixel`
    - `ShopRaven_Speed_Optimizer`
    - `ShopRaven_Heatmap_Tracker`
- **Verification:** Plugin main file loads all classes cleanly.

---

### Wave 6: Frontend Control Room Integration & Comprehensive Test Suite

#### Task 07-06-A: React Ad Planner & Creative View
- **Target File:** `frontend/src/components/AdPlannerAndCreativeView.tsx`
- **Specification:**
  - Control room view supporting:
    - 7-Day Meta Ad Plan generator with Break-Even ROAS calculator.
    - Festival Sale Banner preview and generator.
    - Storefront Scroll & Click Heatmap analytics.
- **Verification:** Component compiles with TypeScript and React.

#### Task 07-06-B: Control Room Single-File Dashboard Integration
- **Target Files:** `frontend/nnstore_ai_dashboard.html`, `frontend/index.html`
- **Specification:**
  - Add navigation tab: **"📢 Ad Planner & Creatives"**.
  - Mount interactive 7-Day Ad Planner, Banner Studio, and Heatmap visualizer.
  - Wire actions to orchestrator and backend APIs.
- **Verification:** Dashboard renders all 6 tabs without console errors.

#### Task 07-06-C: Unit Test Suite for Extended Growth Suite
- **Target File:** `backend/tests/test_ad_planner_and_healer.py`
- **Specification:**
  - `test_breakeven_roas_calculation()`: Verifies Break-Even ROAS math.
  - `test_underselling_sku_detection()`: Verifies dead-stock detection logic.
  - `test_broken_image_detection()`: Verifies image auditor flags broken links.
- **Verification:** `pytest -v tests/` executes and passes 100%.

