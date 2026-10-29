# ShopRaven — Autonomous E-Commerce AI Cofounder for nnstore.shop

ShopRaven is a comprehensive autonomous e-commerce operations, product research, dual-supplier sourcing, dynamic pricing, SEO/AEO publishing, and real-time analytics platform built specifically for [nnstore.shop](https://nnstore.shop) in the Pakistani Cash-on-Delivery (COD) market.

---

## ⚡ Architecture Overview

```
ShopRaven Platform
├── 1. Pakistani Market Scout (Google Autocomplete PK, Google Trends PK, Daraz, Meta Ads)
├── 2. Dual-Supplier Vault (Authenticated HHC & Oshi Dropshipping scrapers + comparator)
├── 3. Competitive Pricing & Margin Guard (+40% to +50% profit, Rs. 150 COD delivery, *49/*99 endings)
├── 4. 1080x1080 Image Studio (Soft-studio canvas, contrast/sharpness enhancement, WP media upload)
├── 5. Localized Roman-Urdu SEO/AEO Engine (Gemini 2.5 Flash, RankMath meta, JSON-LD Schema)
├── 6. Node.js Orchestrator & Webhooks (WooCommerce REST API v3, cron scheduler, auto menu reorder)
├── 7. Alippo 13-Feature Parity (Waitlists, Deal Hunter, COD-to-Prepaid, Auto-Blogger, Sales Predictor)
└── 8. Control Room Dashboard & Discord Command Center (/scan-now, /publish, Rich Embeds)
```

---

## 🔒 Locked Business Rules & Mathematical Formulas

1. **Storefront**: `https://nnstore.shop` (WooCommerce REST API v3)
2. **7 Official Categories**:
   - Beauty & Care
   - Kitchen Accessories
   - Home & Living
   - Gym Accessories
   - Electronic Accessories
   - Auto & Tools
   - Accessories
3. **Delivery & Landed Math**:
   - nnstore.shop charges a flat **Rs. 150** delivery fee separately at checkout.
   - Competitor benchmark courier fee: **Rs. 220** (Market Landed = $M_{avg} + 220$).
   - NN Store Landed = $\text{Sale Price} + 150$.
4. **Profit Corridor**:
   $$\text{Profit Margin} \in [+40\%, +50\%] \implies \text{Sale Price} \in [\text{Wholesale Cost} \times 1.40, \text{Wholesale Cost} \times 1.50]$$
5. **Psychological Endings**:
   - Every sale and regular price ends in `*49` or `*99` (e.g., Rs. 649, Rs. 1,399).
6. **Support & Customer Contact**:
   - Official WhatsApp Support: `+92 312 4999196`

---

## 🚀 Quickstart

### Prerequisites
- Docker Engine 24+ & Docker Compose v2
- Python 3.11+
- Node.js 20+

### Setup & Run
```bash
# 1. Clone & prepare environment
cp .env.example .env

# 2. Start full stack via Docker Compose
make dev

# 3. Run database migrations
make migrate

# 4. Trigger manual research scan
make scan-now

# 5. Run test suites
make test
```

---

## 📂 Project Structure

```
ShopRaven/
├── .env.example
├── docker-compose.yml
├── Makefile
├── skills-lock.json
├── backend/                  # FastAPI & Celery Worker Core
│   ├── app/
│   │   ├── config.py         # Settings & environment validation
│   │   ├── database.py       # SQLAlchemy 2.0 async engine & sessionmaker
│   │   ├── celery_app.py     # Distributed worker queue & beat schedules
│   │   ├── models/           # 7 Database Models
│   │   ├── schemas/          # 5 Pydantic v2 validation contracts
│   │   ├── scout/            # Market demand discovery engine
│   │   ├── suppliers/        # Authenticated HHC & Oshi scrapers
│   │   ├── pricing/          # Competitive landed pricing engine
│   │   ├── studio/           # 1080x1080 image processor & WP uploader
│   │   ├── seo_aeo/          # Roman-Urdu & Gemini 2.5 Flash AEO engine
│   │   ├── coupons/          # Margin-guarded Deal Hunter coupon bot
│   │   ├── blog/             # Auto-blogger with embedded product cards
│   │   ├── forecasting/      # PnL accounting & 30-day sales demand
│   │   └── api/              # REST routes & endpoints
│   └── tests/                # Pytest verification suite
├── orchestrator/             # Node.js 20 Orchestrator & Integrations
│   ├── src/
│   │   ├── server.js         # Webhook receiver & REST gateway
│   │   ├── woocommerce/      # WooCommerce REST API v3 sync & publish
│   │   ├── whatsapp/         # Meta WhatsApp Cloud API & COD-to-Prepaid
│   │   └── discord/          # Rich Embed notifier & slash commands
│   └── tests/                # Jest orchestrator test suite
├── wordpress-plugin/         # shopraven-bridge WordPress plugin
└── frontend/                 # Control Room Dashboard (Single-file & React)
```

---

## 🏆 Alippo 13-Feature Parity Matrix

| Feature # | Module Name | Description & Formula |
|:---:|:---|:---|
| **#01** | Bulk Photo-to-Draft | Standardizes supplier gallery to 1080x1080 and maps to 7 categories |
| **#02** | True Net Profit Accounting | $\text{Net Profit} = \text{Delivered} - \text{Cost} - \text{Packaging} - (\text{RTO} \times \text{Courier})$ |
| **#03** | Built-In AI SEO & AEO | RankMath meta + Schema.org Product, OfferShippingDetails (Rs. 150) & FAQ |
| **#04** | Roman-Urdu Search Mapping | 15–20 Roman-Urdu synonyms & phonetic typos injected into search tags |
| **#05** | Deal Hunter Coupon Bot | Generates exit discounts capped at $\ge +40\%$ profit floor |
| **#06** | Menu Reorder by Sales | $\text{Velocity} = (\text{Orders} \times 3.0) + (\text{Views} \times 0.05)$; updates menu order |
| **#07** | SEO Auto-Blogger | 900-word guides with inline `/?add-to-cart=ID` cards |
| **#08** | Out-of-Stock WhatsApp Waitlist | 1-tap checkout link texted on restock |
| **#09** | Dead-Product 301 Redirect | Auto-redirects discontinued URLs to highest-converting active item |
| **#10** | Cart Progress Bar | Unlocks free shipping above Rs. 2,500 threshold |
| **#11** | COD-to-Prepaid Split | Waives Rs. 150 shipping fee when customer switches to Raast/JazzCash |
| **#12** | WhatsApp Abandoned Cart | 20-minute recovery message with pre-filled cart checkout URL |
| **#13** | 24/7 Product Q&A & Forecast | Instant on-page AI assistant + 30-day SKU demand forecasting |

---
**License**: Proprietary — Developed for **nnstore.shop** (Naeem Ashiq).
