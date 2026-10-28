/**
 * Discord Rich Embed Notifier.
 * Broadcasts real-time color-coded alerts to Discord for all autonomous pipeline steps.
 */

const axios = require('axios');
const { CONFIG } = require('../config/env');

const STEP_COLORS = {
  MARKET_RESEARCH: 0x8B5CF6,  // Purple
  CATALOG_GAP_CHECK: 0x3B82F6, // Blue
  SUPPLIER_CHECK: 0xF59E0B,    // Amber
  PRICE_RESEARCH: 0x10B981,    // Emerald
  IMAGE_STUDIO: 0xEC4899,      // Pink
  SEO_AEO_ENGINE: 0x06B6D4,    // Cyan
  WOOCOMMERCE_DRAFT: 0x22C55E, // Green
  COD_RTO_GUARD: 0xEF4444      // Red
};

class DiscordNotifier {
  constructor() {
    this.webhookUrl = CONFIG.DISCORD_WEBHOOK_URL;
  }

  async sendEmbed(step, status, message, fieldsObj = {}) {
    if (!this.webhookUrl) {
      return { skipped: true, reason: 'No webhook URL configured' };
    }

    const color = STEP_COLORS[step] || 0x64748B;
    const fields = Object.entries(fieldsObj).map(([key, val]) => ({
      name: key,
      value: String(val),
      inline: true
    }));

    const embed = {
      title: `[ShopRaven] ${step.replace(/_/g, ' ')} — ${status}`,
      description: message,
      color: color,
      fields: fields,
      footer: {
        text: 'ShopRaven Autonomous Engine • nnstore.shop'
      },
      timestamp: new Date().toISOString()
    };

    try {
      const resp = await axios.post(this.webhookUrl, { embeds: [embed] }, { timeout: 6000 });
      return { success: true, status: resp.status };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }
}

module.exports = DiscordNotifier;

