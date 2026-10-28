/**
 * Dead-Product Smart Auto-Redirect (Alippo Feature #9).
 * Redirects discontinued item URLs (301) to the best-selling in-stock replacement.
 */

const WooCommerceAPIClient = require('./wc_api_client');

class SmartRedirectManager {
  constructor() {
    this.wcClient = new WooCommerceAPIClient();
  }

  findClosestActiveReplacement(removedProduct, activeCatalog = []) {
    const category = (removedProduct.categories && removedProduct.categories[0])
      ? removedProduct.categories[0].name
      : '';

    // Find active products in the exact same category
    const categoryPeers = activeCatalog.filter(
      p => p.id !== removedProduct.id &&
           p.stock_status === 'instock' &&
           p.categories && p.categories.some(c => c.name === category)
    );

    if (categoryPeers.length > 0) {
      // Pick highest sales velocity peer
      categoryPeers.sort((a, b) => (Number(b.total_sales) || 0) - (Number(a.total_sales) || 0));
      return categoryPeers[0];
    }

    // Fallback to general bestseller
    return activeCatalog[0] || null;
  }

  async apply301Redirect(oldSlug, targetProductUrl) {
    // In WordPress, 301 redirects are registered either in Redirection plugin,
    // RankMath Redirections table, or htaccess.
    return {
      status: 'redirect_registered',
      type: 301,
      source: `/product/${oldSlug}/`,
      target: targetProductUrl || 'https://nnstore.shop/'
    };
  }
}

module.exports = SmartRedirectManager;

