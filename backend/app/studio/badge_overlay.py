"""
Badge and promotional callout renderer for secondary product gallery images.
"""

import os
from PIL import Image, ImageDraw, ImageFont


class StudioBadgeRenderer:
    """Renders clean promotional and feature badges onto product images."""

    def apply_feature_callout(self, image_path: str, headline: str = "CASH ON DELIVERY") -> str:
        """
        Draws a modern badge on the top-left or bottom of the image.
        Returns the path to the updated badge image.
        """
        if not os.path.exists(image_path):
            return image_path

        try:
            img = Image.open(image_path).convert("RGBA")
            draw = ImageDraw.Draw(img)

            # Badge dimensions
            badge_w = 420
            badge_h = 70
            margin = 40

            # Draw soft pill container (Dark sleek aesthetic: #1E293B)
            draw.rounded_rectangle(
                [(margin, margin), (margin + badge_w, margin + badge_h)],
                radius=16,
                fill=(30, 41, 59, 230),  # Slate 800 with 90% opacity
                outline=(245, 158, 11, 255),  # Amber border
                width=3,
            )

            # Try loading default font or PIL fallback
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

            # Render text
            draw.text(
                (margin + 30, margin + 22),
                f"★ {headline.upper()}",
                fill=(255, 255, 255, 255),
                font=font,
            )

            # Save back to RGB JPEG
            final_img = img.convert("RGB")
            badge_path = image_path.replace(".jpg", "-badged.jpg")
            final_img.save(badge_path, "JPEG", quality=92)
            return badge_path
        except Exception:
            return image_path

