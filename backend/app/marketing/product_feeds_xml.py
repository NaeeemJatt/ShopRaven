"""
Live Meta Catalog & Google Merchant Center XML Feeds (Alippo Feature #16A).
Generates compliant RSS/XML product feeds for Meta Dynamic Product Ads (DPA)
and Google Shopping Pakistan.
"""

from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from xml.dom import minidom
from app.config import get_settings


class ProductFeedGenerator:
    """Generates standardized XML product catalogs for Meta Ads and Google Merchant Center."""

    def __init__(self):
        self.settings = get_settings()
        self.store_url = "https://nnstore.shop"

    def _prettify_xml(self, elem: ET.Element) -> str:
        """Returns pretty-printed XML string."""
        rough_string = ET.tostring(elem, "utf-8")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def build_meta_catalog_xml(self, products: List[Dict[str, Any]]) -> str:
        """
        Builds Facebook/Meta Catalog XML feed:
        <rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
        """
        rss = ET.Element("rss", {"version": "2.0", "xmlns:g": "http://base.google.com/ns/1.0"})
        channel = ET.SubElement(rss, "channel")

        title = ET.SubElement(channel, "title")
        title.text = "nnstore.shop Meta Product Catalog"
        link = ET.SubElement(channel, "link")
        link.text = self.store_url
        desc = ET.SubElement(channel, "description")
        desc.text = "Live product feed for Meta Dynamic Product Ads (Pakistan)"

        for prod in products:
            p_id = str(prod.get("id") or prod.get("wc_product_id") or "1001")
            p_title = prod.get("title") or prod.get("name", "Product")
            p_desc = prod.get("short_description") or prod.get("description") or "Online shopping in Pakistan with flat Rs. 150 COD."
            p_price = f"{int(prod.get('regular_price') or prod.get('sale_price', 1499))} PKR"
            p_sale_price = f"{int(prod.get('sale_price', 1399))} PKR"
            p_link = prod.get("permalink") or f"{self.store_url}/product/{prod.get('slug', p_id)}/"
            p_image = prod.get("image_url") or prod.get("image") or "https://images.pexels.com/photos/3785147/pexels-photo-3785147.jpeg"

            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "g:id").text = f"nnstore_{p_id}"
            ET.SubElement(item, "g:title").text = p_title
            ET.SubElement(item, "g:description").text = p_desc[:250]
            ET.SubElement(item, "g:link").text = p_link
            ET.SubElement(item, "g:image_link").text = p_image
            ET.SubElement(item, "g:brand").text = "NN Store"
            ET.SubElement(item, "g:condition").text = "new"
            ET.SubElement(item, "g:availability").text = "in stock"
            ET.SubElement(item, "g:price").text = p_price
            ET.SubElement(item, "g:sale_price").text = p_sale_price

            # Pakistan separate delivery configuration
            shipping = ET.SubElement(item, "g:shipping")
            ET.SubElement(shipping, "g:country").text = "PK"
            ET.SubElement(shipping, "g:service").text = "Flat Cash on Delivery"
            ET.SubElement(shipping, "g:price").text = "150 PKR"

        return self._prettify_xml(rss)

    def build_google_merchant_pk_xml(self, products: List[Dict[str, Any]]) -> str:
        """
        Builds Google Merchant Center Pakistan shopping feed:
        Target country: PK, Currency: PKR, ISO 4217 compliant.
        """
        rss = ET.Element("rss", {"version": "2.0", "xmlns:g": "http://base.google.com/ns/1.0"})
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = "NN Store Google Shopping Pakistan Feed"
        ET.SubElement(channel, "link").text = self.store_url
        ET.SubElement(channel, "description").text = "Automated Google Merchant Center Feed for nnstore.shop"

        for prod in products:
            p_id = str(prod.get("id") or prod.get("wc_product_id") or "1001")
            p_title = prod.get("title") or prod.get("name", "Product")
            p_desc = prod.get("description") or "Genuine products on nnstore.shop with 7-day replacement warranty in Pakistan."
            p_sale_price = f"{int(prod.get('sale_price', 1399))}.00 PKR"
            p_link = prod.get("permalink") or f"{self.store_url}/product/{prod.get('slug', p_id)}/"
            p_image = prod.get("image_url") or prod.get("image") or "https://images.pexels.com/photos/3785147/pexels-photo-3785147.jpeg"

            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "g:id").text = f"nn_{p_id}"
            ET.SubElement(item, "g:title").text = p_title
            ET.SubElement(item, "g:description").text = p_desc[:500]
            ET.SubElement(item, "g:link").text = p_link
            ET.SubElement(item, "g:image_link").text = p_image
            ET.SubElement(item, "g:condition").text = "new"
            ET.SubElement(item, "g:availability").text = "in_stock"
            ET.SubElement(item, "g:price").text = p_sale_price
            ET.SubElement(item, "g:identifier_exists").text = "no"

            shipping = ET.SubElement(item, "g:shipping")
            ET.SubElement(shipping, "g:country").text = "PK"
            ET.SubElement(shipping, "g:service").text = "Standard COD"
            ET.SubElement(shipping, "g:price").text = "150.00 PKR"

        return self._prettify_xml(rss)

