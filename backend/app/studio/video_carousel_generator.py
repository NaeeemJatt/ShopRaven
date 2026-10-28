"""
AI Video Ad, UGC Reel & Multi-Slide Carousel Studio (Alippo Feature #14).
Transforms a single supplier product photo into a 5-slide 1080x1080 Meta carousel
and a 9:16 vertical product video reel.
"""

import os
import io
from typing import List, Dict, Any, Optional
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from app.studio.image_processor import ProductImageStudio


class VideoAndCarouselStudio:
    """Generates high-converting 5-slide Instagram/Meta carousels and vertical video reels."""

    def __init__(self, output_dir: str = "temp_studio_output/carousel"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.image_studio = ProductImageStudio(output_dir=self.output_dir)

    def _get_base_image(self, product: Dict[str, Any]) -> Image.Image:
        """Fetches or renders base product image on 1080x1080 studio canvas."""
        img_url = product.get("image_url") or product.get("image")
        if img_url and img_url.startswith("http"):
            try:
                resp = requests.get(img_url, timeout=10)
                if resp.status_code == 200:
                    raw_img = Image.open(io.BytesIO(resp.content)).convert("RGB")
                    return self.image_studio.standardize_to_square_canvas(raw_img)
            except Exception as e:
                pass

        # Fallback studio canvas
        canvas = Image.new("RGB", (1080, 1080), (250, 250, 252))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([100, 200, 980, 880], fill=(240, 243, 248), outline=(220, 226, 235), width=2)
        return canvas

    def generate_5_slide_instagram_carousel(
        self, product: Dict[str, Any], pricing: Dict[str, Any]
    ) -> List[str]:
        """
        Creates a 5-slide 1080x1080 square graphic set:
        Slide 1: Hook & Brand Hero
        Slide 2: Problem & Frustration
        Slide 3: Solution & Transformation
        Slide 4: Key Specifications
        Slide 5: Irresistible PKR COD Offer + Rs. 150 Flat Delivery Badge
        """
        title = product.get("title") or product.get("name", "Exclusive Product")
        category = product.get("category", "Trending Collection")
        sale_price = pricing.get("sale_price") or pricing.get("recommended_sale_price", 1499)
        regular_price = pricing.get("regular_price") or pricing.get("recommended_regular_price", 2199)

        base_img = self._get_base_image(product)
        slug = product.get("slug") or title.lower().replace(" ", "_")[:20]
        slide_paths = []

        slides_config = [
            {
                "number": 1,
                "badge": "🔥 TOP SELLING IN PAKISTAN",
                "badge_color": (225, 29, 72),
                "headline": title[:45],
                "subtext": "Upgrade your daily lifestyle with verified 100% authentic quality.",
                "cta": "Swipe to see how it works 👉",
            },
            {
                "number": 2,
                "badge": "⚠️ THE DAILY PROBLEM",
                "badge_color": (234, 88, 12),
                "headline": "Tired of Cheap Copies & Disappointment?",
                "subtext": "Low-quality alternatives break in days and waste your hard-earned money. You deserve something that actually works reliably.",
                "cta": "Here is the proven solution 👉",
            },
            {
                "number": 3,
                "badge": "✨ THE REVOLUTIONARY SOLUTION",
                "badge_color": (16, 185, 129),
                "headline": "Engineered for Long-Lasting Performance",
                "subtext": "Designed with premium materials, trusted by hundreds of Pakistani shoppers across Karachi, Lahore & Islamabad.",
                "cta": "Check the specs next 👉",
            },
            {
                "number": 4,
                "badge": "⚙️ KEY SPECIFICATIONS",
                "badge_color": (37, 99, 235),
                "headline": "Premium Quality You Can Feel",
                "subtext": "• Durable & ergonomic structure\n• Tested for daily rigorous usage\n• 7-Day easy replacement guarantee\n• 100% customer satisfaction guaranteed",
                "cta": "Special Offer Inside 👉",
            },
            {
                "number": 5,
                "badge": "🇵🇰 SPECIAL COD OFFER",
                "badge_color": (13, 148, 136),
                "headline": f"Rs. {int(sale_price):,} Only (Save Rs. {int(regular_price - sale_price):,})",
                "subtext": "Order now on nnstore.shop with Flat Rs. 150 Cash-on-Delivery nationwide!\n\nPay cash only when TCS/Leopard delivers to your doorstep.",
                "cta": "Tap Link in Bio to Order Now 🛒",
            },
        ]

        for s in slides_config:
            slide_canvas = base_img.copy()
            draw = ImageDraw.Draw(slide_canvas)

            # Top Header Card Banner
            draw.rectangle([0, 0, 1080, 140], fill=(15, 23, 42))
            draw.text((40, 45), "nnstore.shop", fill=(255, 255, 255))
            draw.text((880, 45), f"Slide {s['number']}/5", fill=(148, 163, 184))

            # Category / Pill Badge
            badge_text = s["badge"]
            draw.rounded_rectangle([40, 160, 460, 210], radius=8, fill=s["badge_color"])
            draw.text((55, 172), badge_text, fill=(255, 255, 255))

            # Bottom Content Overlay Card
            draw.rounded_rectangle([40, 780, 1040, 1040], radius=16, fill=(15, 23, 42, 240), outline=(51, 65, 85), width=2)

            # Headline & Subtext
            draw.text((65, 805), s["headline"], fill=(255, 255, 255))
            
            # Format subtext lines
            y_offset = 855
            for line in s["subtext"].split("\n")[:3]:
                draw.text((65, y_offset), line[:75], fill=(203, 213, 225))
                y_offset += 32

            # Bottom CTA banner
            draw.text((65, 985), s["cta"], fill=(56, 189, 248))

            out_path = os.path.join(self.output_dir, f"{slug}_slide_{s['number']}.jpg")
            slide_canvas.save(out_path, "JPEG", quality=92)
            slide_paths.append(out_path)

        return slide_paths

    def render_vertical_product_reel_mp4(
        self, slides: List[str], audio_track: Optional[str] = None
    ) -> str:
        """
        Assembles slides into a 9:16 vertical (1080x1920) presentation.
        If moviepy is installed, renders MP4; otherwise compiles an animated sequence.
        """
        if not slides:
            raise ValueError("No slides provided to render reel.")

        slug = os.path.splitext(os.path.basename(slides[0]))[0].replace("_slide_1", "")
        out_mp4 = os.path.join(self.output_dir, f"{slug}_vertical_reel.mp4")

        try:
            from moviepy.editor import ImageClip, concatenate_videoclips

            clips = []
            for slide_path in slides:
                # Load square slide and center onto 1080x1920 vertical canvas
                slide_img = Image.open(slide_path).convert("RGB")
                vertical_bg = Image.new("RGB", (1080, 1920), (15, 23, 42))
                # Paste centered vertically
                vertical_bg.paste(slide_img, (0, 420))
                
                temp_v_slide = slide_path.replace(".jpg", "_vert.jpg")
                vertical_bg.save(temp_v_slide, "JPEG")

                clip = ImageClip(temp_v_slide).set_duration(2.5)
                clips.append(clip)

            video = concatenate_videoclips(clips, method="compose")
            video.write_videofile(out_mp4, fps=24, codec="libx264", logger=None)
            return out_mp4
        except Exception:
            # Graceful lightweight fallback: Generate animated GIF / sequence descriptor
            gif_path = os.path.join(self.output_dir, f"{slug}_reel_preview.gif")
            images = [Image.open(p).convert("RGB").resize((540, 540)) for p in slides]
            if images:
                images[0].save(
                    gif_path,
                    save_all=True,
                    append_images=images[1:],
                    duration=2000,
                    loop=0,
                )
            return gif_path

