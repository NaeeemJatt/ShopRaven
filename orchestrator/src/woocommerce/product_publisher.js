/**
 * WooCommerce Product Publisher for nnstore.shop.
 * Creates Draft listings with complete SEO/AEO metadata and handles 1-click publishing.
 */

const WooCommerceAPIClient = require('./wc_api_client');

class WooCommerceProductPublisher {
  constructor() {
    this.wcClient = new WooCommerceAPIClient();
  }

  async createDraftListing(agentPackage) {
    const payload = {
      name: agentPackage.title,
      slug: agentPackage.slug,
      type: 'simple',
      status: 'draft', // Created as Draft first for safety
      regular_price: String(agentPackage.regular_price),
      sale_price: String(agentPackage.sale_price),
      short_description: agentPackage.short_description,
      description: agentPackage.description,
      categories: agentPackage.categories || [],
      tags: agentPackage.tags || [],
      images: agentPackage.images || [],
      meta_data: agentPackage.meta_data || [],
      manage_stock: false,
      stock_status: 'instock'
    };

    const createdProduct = await this.wcClient.post('/products', payload);
    return createdProduct;
  }

  async publishDraftToLive(wcProductId) {
    const updated = await this.wcClient.put(`/products/${wcProductId}`, {
      status: 'publish'
    });

    // Instant Google Search Console & Bing Sitemap Ping for rapid indexation
    try {
      const sitemapUrl = encodeURIComponent('https://nnstore.shop/sitemap_index.xml');
      fetch(`https://www.google.com/ping?sitemap=${sitemapUrl}`).catch(() => {});
      fetch(`https://www.bing.com/ping?sitemap=${sitemapUrl}`).catch(() => {});
    } catch (e) {
      // Best-effort ping
    }

    return updated;
  }
}

module.exports = WooCommerceProductPublisher;

