"""
Session Vault: Manages authenticated session cookies and CSRF tokens in Redis.
Prevents repetitive login overhead and handles automated re-authentication.
"""

import json
from typing import Optional, Dict, Any
from bs4 import BeautifulSoup
import redis
from app.config import get_settings

settings = get_settings()


class SupplierSessionVault:
    """Stores and retrieves session cookies from Redis with CSRF token extraction."""

    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception:
            self.redis_client = None

    def save_cookies(self, supplier_key: str, cookies: Dict[str, Any], ttl_seconds: int = 86400) -> None:
        """Saves session cookies to Redis with a 24-hour expiration."""
        if not self.redis_client:
            return
        key = f"supplier_session:{supplier_key}"
        try:
            self.redis_client.setex(key, ttl_seconds, json.dumps(cookies))
        except Exception:
            pass

    def load_cookies(self, supplier_key: str) -> Dict[str, Any]:
        """Loads cached session cookies from Redis if valid."""
        if not self.redis_client:
            return {}
        key = f"supplier_session:{supplier_key}"
        try:
            val = self.redis_client.get(key)
            if val:
                return json.loads(val)
        except Exception:
            pass
        return {}

    def extract_csrf_token(self, html_text: str) -> Optional[str]:
        """Parses HTML for standard Laravel/Django/PHP CSRF tokens."""
        if not html_text:
            return None
        soup = BeautifulSoup(html_text, "html.parser")
        token_input = soup.find("input", {"name": ["_token", "csrf_token", "csrfmiddlewaretoken"]})
        if token_input and token_input.get("value"):
            return token_input["value"]
        meta_token = soup.find("meta", {"name": "csrf-token"})
        if meta_token and meta_token.get("content"):
            return meta_token["content"]
        return None

