/**
 * WooCommerce Product Publisher for nnstore.shop.
 * Creates Draft listings with complete SEO/AEO metadata and handles 1-click publishing.
 */

const WooCommerceAPIClient = require('./wc_api_client');

function resolveCategory(catInput, title = '') {
  const clean = (typeof catInput === 'string' ? catInput : (catInput?.name || title || '')).toLowerCase();
  if (clean.includes('beauty') || clean.includes('skin') || clean.includes('scrub') || clean.includes('pore') || clean.includes('face') || clean.includes('derma')) return [{ id: 17 }];
  if (clean.includes('kitchen') || clean.includes('chopper') || clean.includes('cutter') || clean.includes('blender') || clean.includes('garlic')) return [{ id: 30 }];
  if (clean.includes('home') || clean.includes('lamp') || clean.includes('sunset') || clean.includes('diffuser') || clean.includes('living') || clean.includes('humidifier') || clean.includes('shaver') || clean.includes('pillow') || clean.includes('mop')) return [{ id: 41 }];
  if (clean.includes('gym') || clean.includes('fitness') || clean.includes('grip') || clean.includes('band') || clean.includes('skipping')) return [{ id: 50 }];
  if (clean.includes('electronic') || clean.includes('earbud') || clean.includes('audio') || clean.includes('watch') || clean.includes('charger') || clean.includes('tws') || clean.includes('gadget') || clean.includes('stand')) return [{ id: 51 }];
  if (clean.includes('auto') || clean.includes('car') || clean.includes('tool') || clean.includes('screwdriver') || clean.includes('hardware')) return [{ id: 131 }];
  if (clean.includes('bag') || clean.includes('wallet') || clean.includes('ring') || clean.includes('bracelet') || clean.includes('accessories')) return [{ id: 132 }];
  return [{ id: 41 }];
}

class WooCommerceProductPublisher {
  constructor() {
    this.wcClient = new WooCommerceAPIClient();
  }

  async createDraftListing(agentPackage) {
    let categories = agentPackage.categories || [];
    if (!categories.length || !categories[0].id) {
      categories = resolveCategory(categories[0] || agentPackage.category, agentPackage.title);
    }

    const payload = {
      name: agentPackage.title,
      slug: agentPackage.slug,
      type: 'simple',
      status: 'draft', // Created as Draft first for safety
      regular_price: String(agentPackage.regular_price),
      sale_price: String(agentPackage.sale_price),
      short_description: agentPackage.short_description,
      description: agentPackage.description,
      categories,
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
      await this.wcClient.put('/system_status/tools/clear_transients');
    } catch (e) {
      // Best-effort ping
    }

    return updated;
  }
}

module.exports = WooCommerceProductPublisher;

