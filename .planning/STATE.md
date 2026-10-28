# ShopRaven Project State

## Active Milestone
- **Milestone:** v2.0.0 Complete Edition (Alippo Extended Growth Suite)
- **Active Phase:** Phase 7: Alippo Extended Growth Suite (Features #14 to #21)
- **Status:** Phase 7 Execution Completed & Verified (12/12 unit tests passing, all 21 features delivered)
- **Completed Features:** 21 of 21 Features (Features #1 to #21 fully implemented)
- **Target Features:** 0 remaining — 100% Codebase Specification Coverage

## Key Technical Decisions
1. **Container Alignment**: All new Python endpoints are mounted in `backend/app/api/routes/marketing.py` and registered in `backend/app/api/router.py`.
2. **XML Feeds**: Feeds served directly via standard library `xml.etree.ElementTree` without heavy external dependencies.
3. **Studio Video/Reels**: Support both MoviePy/FFmpeg rendering and graceful SVG/Pillow multi-slide animated reel generation for container environments without GPU.
4. **CAPI Deduplication**: Shared `event_id` generated per user action to deduplicate between `ShopRaven_Meta_CAPI_Pixel` (browser) and `MetaCAPIDispatcher` (server).
5. **Rating Shield**: Safe 2-tier routing (4-5★ to public WooCommerce photo review link; 1-3★ to internal WhatsApp resolution).
6. **WhatsApp Multi-Device Gateway**: Configured with WasenderAPI session; admin action alerts and approval workflows dispatched live to `+923114618934`.

