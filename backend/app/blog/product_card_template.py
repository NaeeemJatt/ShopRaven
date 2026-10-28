"""
Template renderer for responsive inline WooCommerce product cards in blog posts.
"""


def render_inline_product_card_html(product: dict) -> str:
    """
    Renders a responsive, conversion-optimized HTML product card
    with image, title, PKR pricing, and 1-click 'Add to Cart' button.
    """
    p_id = product.get("id", "0")
    title = product.get("title", "Featured Product")
    sale_price = product.get("sale_price", "0")
    regular_price = product.get("regular_price", "")
    image_src = product.get("image_url", "https://nnstore.shop/wp-content/uploads/placeholder.jpg")
    store_url = "https://nnstore.shop"

    regular_price_html = f'<span style="text-decoration: line-through; color: #94a3b8; font-size: 14px; margin-left: 8px;">Rs. {regular_price}</span>' if regular_price else ""

    return f"""
<div class="shopraven-blog-product-card" style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin: 24px 0; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; flex-direction: row; gap: 16px; align-items: center; max-width: 640px;">
  <div style="flex-shrink: 0; width: 110px; height: 110px; border-radius: 8px; overflow: hidden; background: #f8fafc;">
    <img src="{image_src}" alt="{title}" style="width: 100%; height: 100%; object-fit: cover;" />
  </div>
  <div style="flex-grow: 1;">
    <span style="background: #fef3c7; color: #b45309; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 9999px; text-transform: uppercase;">Top Seller</span>
    <h4 style="margin: 6px 0; font-size: 16px; font-weight: 700; color: #0f172a; line-height: 1.3;">{title}</h4>
    <div style="margin: 6px 0; font-size: 18px; font-weight: 800; color: #16a34a;">
      Rs. {sale_price} {regular_price_html}
    </div>
    <div style="font-size: 12px; color: #64748b; margin-bottom: 8px;">Flat Rs. 150 Cash-on-Delivery nationwide</div>
    <a href="{store_url}/?add-to-cart={p_id}" style="display: inline-block; background: #2563eb; color: #ffffff; font-weight: 600; font-size: 13px; padding: 8px 18px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
      Add to Cart — Quick COD
    </a>
  </div>
</div>
"""

