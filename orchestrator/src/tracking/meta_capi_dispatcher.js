/**
 * Server-Side Meta Conversions API (CAPI) & Retargeting Dispatcher (Alippo Feature #16B).
 * Sends deduplicated server events (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase)
 * directly to Meta Graph API with SHA-256 hashed customer parameters to bypass iOS/browser ad-blockers.
 */

const crypto = require('crypto');
const { CONFIG } = require('../config/env');

class MetaCAPIDispatcher {
  constructor() {
    this.pixelId = process.env.META_PIXEL_ID || '123456789012345';
    this.accessToken = process.env.META_CAPI_ACCESS_TOKEN || '';
    this.apiVersion = 'v19.0';
    this.graphUrl = `https://graph.facebook.com/${this.apiVersion}/${this.pixelId}/events`;
    this.storeUrl = CONFIG.WC_STORE_URL || 'https://nnstore.shop';
  }

  /**
   * Hashes a string using SHA-256 according to Meta CAPI specification.
   */
  hashValue(val) {
    if (!val) return undefined;
    return crypto.createHash('sha256').update(String(val).trim().toLowerCase()).digest('hex');
  }

  /**
   * Normalizes and hashes Pakistani phone numbers.
   */
  hashPhone(phone) {
    if (!phone) return undefined;
    let digits = phone.replace(/[^0-9]/g, '');
    if (digits.startsWith('03')) {
      digits = '92' + digits.slice(1);
    } else if (digits.startsWith('3') && digits.length === 10) {
      digits = '92' + digits;
    }
    return this.hashValue(digits);
  }

  /**
   * Dispatches server-side event to Meta Conversions API.
   */
  async sendServerEvent(eventName, eventId, userData = {}, customData = {}, sourceUrl = null) {
    const eventTime = Math.floor(Date.now() / 1000);

    const hashedUserData = {
      ph: userData.phone ? [this.hashPhone(userData.phone)] : undefined,
      em: userData.email ? [this.hashValue(userData.email)] : undefined,
      fn: userData.firstName ? [this.hashValue(userData.firstName)] : undefined,
      ln: userData.lastName ? [this.hashValue(userData.lastName)] : undefined,
      ct: userData.city ? [this.hashValue(userData.city)] : undefined,
      country: [this.hashValue('pk')],
      client_ip_address: userData.ip || '127.0.0.1',
      client_user_agent: userData.userAgent || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    };

    // Remove undefined keys
    Object.keys(hashedUserData).forEach(k => hashedUserData[k] === undefined && delete hashedUserData[k]);

    const payload = {
      data: [
        {
          event_name: eventName,
          event_time: eventTime,
          event_id: eventId, // Shared deduplication key matching client-side Pixel
          event_source_url: sourceUrl || this.storeUrl,
          action_source: 'website',
          user_data: hashedUserData,
          custom_data: {
            currency: 'PKR',
            delivery_fee: 150,
            ...customData
          }
        }
      ]
    };

    if (!this.accessToken || process.env.NODE_ENV === 'test') {
      // Mock log when CAPI token is in sandbox / development
      return {
        success: true,
        mock: true,
        eventName,
        eventId,
        hashedUserData
      };
    }

    try {
      const resp = await fetch(`${this.graphUrl}?access_token=${this.accessToken}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      return {
        success: resp.ok,
        data
      };
    } catch (err) {
      console.error('[Meta CAPI Dispatch Error]:', err.message);
      return { success: false, error: err.message };
    }
  }
}

module.exports = MetaCAPIDispatcher;

