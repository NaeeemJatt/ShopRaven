"""
Festival & Seasonal Sale Banner Maker (Alippo Feature #14B).
Renders localized Pakistani campaign banners (Ramzan, Eid-ul-Fitr, 14 August Azadi,
11.11, Blessed Friday) with bold strikethrough PKR pricing.
"""

import os
import io
from typing import Dict, Any, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
from app.studio.image_processor import ProductImageStudio


class FestivalBannerGenerator:
    """Generates localized festival campaign banners with strikethrough pricing."""

    THEMES = {
        "ramzan": {
            "title": "🌙 RAMZAN MUBARAK MEGA SALE",
            "tagline": "Special Discounts for the Holy Month • Flat Rs. 150 Nationwide COD",
            "header_color": (15, 66, 42),       # Deep Islamic emerald
            "accent_color": (217, 119, 6),      # Warm gold
            "badge": "UPTO 50% OFF"
        },
        "eid": {
            "title": "✨ EID-UL-FITR SPECIAL DEALS",
            "tagline": "Celebrate in Style • Guaranteed Delivery Before Eid!",
            "header_color": (30, 27, 75),       # Deep festive indigo
            "accent_color": (234, 179, 8),      # Radiant gold
            "badge": "EID GIFT SPECIAL"
        },
        "azadi": {
            "title": "🇵🇰 14 AUGUST AZADI MUBARAK SALE",
            "tagline": "Celebrating 79 Years of Independence • Flat Rs. 150 COD Shipping",
            "header_color": (4, 120, 87),       # Pakistan flag green
            "accent_color": (255, 255, 255),    # Clean white
            "badge": "AZADI SAVINGS"
        },
        "11_11": {
            "title": "⚡ 11.11 MEGA SHOPPING FESTIVAL",
            "tagline": "The Biggest Online Sale in Pakistan • Lowest Prices of the Year",
            "header_color": (159, 18, 57),      # Bold ruby red
            "accent_color": (251, 191, 36),     # Yellow gold
            "badge": "11.11 EXCLUSIVE"
        },
        "blessed_friday": {
            "title": "🕌 BLESSED FRIDAY MEGA DISCOUNTS",
            "tagline": "Unbeatable Pakistani Prices • 100% Cash-on-Delivery Guarantee",
            "header_color": (17, 24, 39),       # Premium obsidian
            "accent_color": (16, 185, 129),     # Emerald green
            "badge": "BLESSED FRIDAY"
        }
    }

    def __init__(self, output_dir: str = "temp_studio_output/banners"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.image_studio = ProductImageStudio(output_dir=self.output_dir)

    def render_festival_campaign_banner(
        self, product: Dict[str, Any], festival_theme: str = "ramzan"
    ) -> str:
        """
        Creates a 1080x1080 festive promotional creative:
        - Festive decorative banner header
        - Centered product imagery
        - Strikethrough regular price + bold sale price
        - Trust COD badges
        """
        theme_key = festival_theme.lower().replace("-", "_")
        theme = self.THEMES.get(theme_key, self.THEMES["ramzan"])

        title = product.get("title") or product.get("name", "Exclusive Product")
        sale_price = product.get("sale_price") or product.get("recommended_sale_price", 1399)
        regular_price = product.get("regular_price") or product.get("recommended_regular_price", 2049)

        # 1. Base 1080x1080 Canvas
        canvas = Image.new("RGB", (1080, 1080), (250, 250, 252))

        # 2. Try pasting product image in center
        img_url = product.get("image_url") or product.get("image")
        if img_url and img_url.startswith("http"):
            try:
                resp = requests.get(img_url, timeout=10)
                if resp.status_code == 200:
                    raw_img = Image.open(io.BytesIO(resp.content)).convert("RGB")
                    centered = self.image_studio.standardize_to_square_canvas(raw_img)
                    canvas.paste(centered, (0, 0))
            except Exception:
                pass

        draw = ImageDraw.Draw(canvas)

        # 3. Top Festival Header Banner
        header_color = theme["header_color"]
        accent_color = theme["accent_color"]
        draw.rectangle([0, 0, 1080, 180], fill=header_color)

        # Store Branding + Festival Title
        draw.text((40, 25), "nnstore.shop", fill=(203, 213, 225))
        draw.text((40, 65), theme["title"], fill=accent_color)
        draw.text((40, 125), theme["tagline"], fill=(241, 245, 249))

        # 4. Corner Promotional Ribbon / Badge
        draw.rounded_rectangle([780, 200, 1040, 260], radius=10, fill=theme["header_color"], outline=accent_color, width=2)
        draw.text((800, 220), theme["badge"], fill=accent_color)

        # 5. Bottom Pricing Card with Strikethrough
        draw.rounded_rectangle([40, 840, 1040, 1040], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)

        # Product Title
        draw.text((70, 865), title[:55], fill=(255, 255, 255))

        # Price Display: Strikethrough Regular + Bold Green Sale Price
        reg_text = f"Was: Rs. {int(regular_price):,}"
        sale_text = f"NOW: Rs. {int(sale_price):,}"
        draw.text((70, 915), reg_text, fill=(148, 163, 184))
        # Draw strikethrough red line over regular price
        draw.line([68, 925, 215, 925], fill=(239, 68, 68), width=3)

        draw.text((245, 910), sale_text, fill=(16, 185, 129))

        # Separate Delivery Badge
        draw.rounded_rectangle([70, 970, 480, 1015], radius=6, fill=(30, 41, 59))
        draw.text((85, 982), "🚚 Flat Rs. 150 Nationwide COD Delivery", fill=(56, 189, 248))

        # Order CTA Button
        draw.rounded_rectangle([800, 960, 1010, 1015], radius=8, fill=(16, 185, 129))
        draw.text((830, 978), "ORDER NOW ↗", fill=(255, 255, 255))

        slug = title.lower().replace(" ", "_")[:20]
        out_path = os.path.join(self.output_dir, f"{slug}_{theme_key}_banner.jpg")
        canvas.save(out_path, "JPEG", quality=92)
        return out_path

