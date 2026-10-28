/**
 * Discord Bot Slash Commands Controller.
 * Allows controlling ShopRaven from mobile or desktop Discord.
 * Commands: /scan-now, /publish <wc_product_id>, /price-check <keyword>, /pnl-report, /reorder-menu.
 */

const axios = require('axios');
const WooCommerceProductPublisher = require('../woocommerce/product_publisher');
const StorefrontMenuOptimizer = require('../woocommerce/menu_reorder');
const { CONFIG } = require('../config/env');

class ShopRavenDiscordBot {
  constructor() {
    this.publisher = new WooCommerceProductPublisher();
    this.menuOptimizer = new StorefrontMenuOptimizer();
  }

  async handleCommand(commandName, args = {}) {
    switch (commandName) {
      case '/scan-now':
        return await this.scanNow();
      case '/publish':
        return await this.publishDraft(args.productId);
      case '/price-check':
        return await this.priceCheck(args.keyword);
      case '/pnl-report':
        return await this.pnlReport();
      case '/reorder-menu':
        return await this.reorderMenu();
      default:
        return { error: `Unknown slash command: ${commandName}` };
    }
  }

  async scanNow() {
    try {
      const resp = await axios.post(`${CONFIG.PYTHON_BACKEND_URL}/api/v1/research/scan`);
      return {
        message: '🚀 Market Research Scan Triggered!',
        details: resp.data
      };
    } catch (err) {
      return { message: 'Failed to trigger scan on backend', error: err.message };
    }
  }

  async publishDraft(wcProductId) {
    if (!wcProductId) {
      return { message: 'Please provide a valid WooCommerce Product ID, e.g. /publish 1245' };
    }
    try {
      const result = await this.publisher.publishDraftToLive(wcProductId);
      return {
        message: `✅ Product #${wcProductId} is now LIVE on https://nnstore.shop!`,
        result
      };
    } catch (err) {
      return { message: `Failed to publish product #${wcProductId}`, error: err.message };
    }
  }

  async priceCheck(keyword) {
    if (!keyword) {
      return { message: 'Please specify a product keyword, e.g. /price-check skin scrubber' };
    }
    try {
      const resp = await axios.post(`${CONFIG.PYTHON_BACKEND_URL}/api/v1/suppliers/compare`, { keyword });
      return {
        message: `🔍 Sourcing & Price Check for "${keyword}":`,
        data: resp.data
      };
    } catch (err) {
      return { message: 'Price check query failed', error: err.message };
    }
  }

  async pnlReport() {
    try {
      const resp = await axios.get(`${CONFIG.PYTHON_BACKEND_URL}/api/v1/analytics/forecast`);
      return {
        message: '📊 Current Month Realized PnL Digest:',
        digest: resp.data.executive_digest
      };
    } catch (err) {
      return { message: 'Could not fetch PnL report', error: err.message };
    }
  }

  async reorderMenu() {
    try {
      const result = await this.menuOptimizer.reorderCatalogByVelocity();
      return {
        message: '🔄 Storefront Menu Reordered by Sales Velocity!',
        result
      };
    } catch (err) {
      return { message: 'Menu reorder failed', error: err.message };
    }
  }
}

module.exports = ShopRavenDiscordBot;

