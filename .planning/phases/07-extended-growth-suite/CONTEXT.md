# Phase 7 Context: Alippo Extended Growth Suite

## Context & Background
The ShopRaven codebase currently achieves complete implementation of Alippo Core Features #1 through #13 as documented in `ShopRaven_Complete_Project_Specification_and_Codebase_Manual.pdf`.

With the arrival of `ShopRaven_Complete_Project_Specification_and_Codebase_Manual 02.pdf` (v2.0.0 Complete Edition), 8 additional growth-stage capabilities (Features #14 to #21) are specified across 16 new files.

## Target Capabilities to Implement
1. **Feature #14 & #14B: Creative & Visual Studio Engine**
   - 5-slide 1080x1080 Instagram/Meta carousel maker
   - 9:16 vertical MP4/animated reel generator
   - Localized Pakistani festival sale banner maker (Ramzan, Eid, 14 August, 11.11, Blessed Friday)
2. **Feature #15: 7-Day Meta Ad Campaign Planner**
   - Break-Even ROAS formula: `Sale_Price / (Sale_Price - Wholesale_Cost - RTO_Buffer)`
   - 5 Urdu/English ad hooks, Instagram captions, city targeting
   - 7-day kill/scale rules: "Kill if CPP > X after 48h / Scale +20% if ROAS > Y"
3. **Feature #16A & #16B: Meta & Google Feeds + Server-Side CAPI**
   - Live RSS/XML feeds for Meta DPA (`/api/v1/marketing/feeds/meta.xml`) and Google Merchant PK (`/google-shopping-pk.xml`)
   - Deduplicated server-side Meta Conversions API dispatcher with SHA-256 hashed customer data
   - WordPress browser pixel with event ID synchronization
4. **Feature #17: Post-Delivery Rating & Review Protection Shield**
   - WhatsApp check-in 24h post-delivery
   - 4-5★ routed to public photo review on nnstore.shop (boosting Google 4.8★ rich snippet)
   - 1-3★ intercepted and directed to priority WhatsApp customer support (+92 312 4999196)
5. **Feature #18: Under-Selling / Dead-Stock Detector**
   - Scans products with >150 views and <0.5% conversion rate
   - Bottleneck diagnosis (price vs market average, weak hook, high bounce)
   - Auto-launches 48h Clearance Flash Sale or BOGO bundle
6. **Feature #19: Broken Product Image & Missing Gallery Auto-Healer**
   - Scans product gallery URLs for HTTP 404/500 or 0-byte images
   - Auto-re-renders and uploads clean 1080x1080 studio image from supplier cache
7. **Feature #20: Influencer / UGC Creator & Sales Associate Outreach Bot**
   - Automated onboarding with custom affiliate coupons and product seeding briefs
   - Daily operational task dispatching to sales associates via WhatsApp
8. **Feature #21A & #21B: Built-in Storefront Speed Optimizer & Heatmap Tracker**
   - LCP hero image optimization (`fetchpriority='high'`), script deferral, WebP/JPEG compression
   - Scroll depth (25/50/75/100%), rage clicks, Add-to-Cart vs Buy via WhatsApp click tracking beacon

