/**
 * ShopRaven WhatsApp Messaging Client.
 * Integrated with WasenderAPI (https://wasenderapi.com/api/send-message)
 * with graceful fallback to Meta WhatsApp Cloud API.
 * 
 * Supports:
 * 1. Admin notifications to +923114618934 whenever an action is performed or approval is required.
 * 2. Customer transactional notifications (COD confirmations, cart recovery, restock alerts).
 */

const { CONFIG } = require('../config/env');

class WhatsAppCloudClient {
  constructor() {
    this.wasenderUrl = CONFIG.WASENDER_API_URL || 'https://wasenderapi.com/api/send-message';
    this.wasenderToken = CONFIG.WASENDER_API_TOKEN || CONFIG.WHATSAPP_TOKEN || '';
    this.adminPhone = CONFIG.ADMIN_WHATSAPP_NUMBER || '+923114618934';

    // Meta Cloud API Fallback
    this.metaToken = CONFIG.WHATSAPP_TOKEN;
    this.phoneId = CONFIG.WHATSAPP_PHONE_NUMBER_ID;
    this.metaBaseURL = this.phoneId ? `https://graph.facebook.com/v20.0/${this.phoneId}/messages` : '';
  }

  normalizePhoneNumber(phone) {
    if (!phone) return '';
    let cleaned = phone.replace(/[^0-9]/g, '');
    if (cleaned.startsWith('03')) {
      cleaned = '92' + cleaned.slice(1);
    } else if (cleaned.startsWith('3') && cleaned.length === 10) {
      cleaned = '92' + cleaned;
    }
    return '+' + cleaned;
  }

  /**
   * Primary method to send a WhatsApp message (with optional product image) to any Pakistani or international number.
   * If imageUrl is provided, Wasender dispatches the image directly with bodyText as the caption.
   */
  async sendTextMessage(recipientPhonePK, bodyText, imageUrl = null) {
    const to = this.normalizePhoneNumber(recipientPhonePK);
    if (!to) {
      throw new Error('Invalid phone number provided');
    }

    // 1. Prioritize WasenderAPI
    if (this.wasenderToken) {
      try {
        const payload = { to, text: bodyText };
        if (imageUrl && typeof imageUrl === 'string' && imageUrl.startsWith('http')) {
          payload.imageUrl = imageUrl;
        }

        const resp = await fetch(this.wasenderUrl, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.wasenderToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload),
          signal: AbortSignal.timeout(12000)
        });

        const data = await resp.json();
        return {
          success: resp.ok,
          provider: 'wasender',
          data
        };
      } catch (err) {
        console.warn(`[WhatsApp] Wasender dispatch warning (${err.message}). Checking Meta fallback...`);
      }
    }

    // 2. Fallback to Meta Cloud API if configured
    if (this.metaBaseURL && this.metaToken && this.metaToken.startsWith('EAAG')) {
      try {
        const payload = {
          messaging_product: 'whatsapp',
          recipient_type: 'individual',
          to: to.replace('+', '')
        };

        if (imageUrl && typeof imageUrl === 'string' && imageUrl.startsWith('http')) {
          payload.type = 'image';
          payload.image = { link: imageUrl, caption: bodyText };
        } else {
          payload.type = 'text';
          payload.text = { preview_url: true, body: bodyText };
        }

        const resp = await fetch(this.metaBaseURL, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.metaToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload),
          signal: AbortSignal.timeout(10000)
        });

        const data = await resp.json();
        return {
          success: resp.ok,
          provider: 'meta_cloud',
          data
        };
      } catch (metaErr) {
        console.error('[WhatsApp] Meta Cloud dispatch error:', metaErr.message);
      }
    }

    // 3. Fallback mock for local development/test
    if (process.env.NODE_ENV === 'test' || !this.wasenderToken) {
      return {
        success: true,
        mock: true,
        to,
        message: bodyText
      };
    }

    throw new Error('Failed to dispatch WhatsApp message via all configured providers.');
  }

  /**
   * Send instant action alert to Admin (+923114618934)
   */
  async notifyAdminAction(actionTitle, summary, details = {}) {
    let fieldsText = '';
    for (const [key, val] of Object.entries(details)) {
      if (val !== undefined && val !== null && val !== '') {
        fieldsText += `• *${key}:* ${val}\n`;
      }
    }

    const timestamp = new Date().toLocaleTimeString('en-PK', { timeZone: 'Asia/Karachi' });
    const message = `⚡ *ShopRaven Action Executed*\n\n📌 *Action:* ${actionTitle}\n📝 *Summary:* ${summary}\n${fieldsText ? '\n' + fieldsText : ''}⏱ *Time:* ${timestamp} PKT\n🌐 *Store:* ${CONFIG.WC_STORE_URL}\n🎛 *Dashboard:* http://localhost:4000/`;

    try {
      console.log(`[WhatsApp Admin] Alerting ${this.adminPhone}: ${actionTitle}`);
      return await this.sendTextMessage(this.adminPhone, message);
    } catch (err) {
      console.error('[WhatsApp Admin Alert Error]:', err.message);
      return { success: false, error: err.message };
    }
  }

  /**
   * Send approval-required request to Admin (+923114618934)
   */
  async notifyAdminApproval(approvalTitle, description, approvalData = {}) {
    let fieldsText = '';
    for (const [key, val] of Object.entries(approvalData)) {
      if (val !== undefined && val !== null && val !== '') {
        fieldsText += `• *${key}:* ${val}\n`;
      }
    }

    const timestamp = new Date().toLocaleTimeString('en-PK', { timeZone: 'Asia/Karachi' });
    const message = `🚨 *ShopRaven: Approval Required*\n\n📌 *Item:* ${approvalTitle}\n📋 *Details:* ${description}\n${fieldsText ? '\n' + fieldsText : ''}\n👉 *Action Required:* Open Control Room to review and approve.\n🎛 *Dashboard:* http://localhost:4000/\n⏱ *Time:* ${timestamp} PKT`;

    try {
      console.log(`[WhatsApp Approval] Alerting ${this.adminPhone}: ${approvalTitle}`);
      return await this.sendTextMessage(this.adminPhone, message);
    } catch (err) {
      console.error('[WhatsApp Approval Alert Error]:', err.message);
      return { success: false, error: err.message };
    }
  }
}

module.exports = WhatsAppCloudClient;
