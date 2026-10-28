/**
 * Catalog Gap Checker: Fetches all live & draft store items and computes token similarity.
 */

const WooCommerceAPIClient = require('./wc_api_client');

class CatalogGapChecker {
  constructor() {
    this.wcClient = new WooCommerceAPIClient();
    this.catalogCache = [];
    this.lastFetched = null;
  }

  async fetchAllStoreProducts(forceRefresh = false) {
    const now = Date.now();
    // Cache for 10 minutes
    if (!forceRefresh && this.catalogCache.length > 0 && (now - this.lastFetched < 600000)) {
      return this.catalogCache;
    }

    try {
      const products = await this.wcClient.get('/products', { per_page: 100 });
      this.catalogCache = Array.isArray(products) ? products : [];
      this.lastFetched = now;
      return this.catalogCache;
    } catch (err) {
      return this.catalogCache;
    }
  }

  async checkProductExistsInStore(trendingKeyword) {
    const products = await this.fetchAllStoreProducts();
    const queryTokens = new Set(
      trendingKeyword
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, '')
        .split(/\s+/)
        .filter(t => t.length > 2)
    );

    if (queryTokens.size === 0) {
      return { exists: false, matchedProduct: null, similarityScore: 0 };
    }

    let highestScore = 0;
    let bestMatch = null;

    for (const prod of products) {
      const prodTokens = new Set(
        prod.name
          .toLowerCase()
          .replace(/[^a-z0-9\s]/g, '')
          .split(/\s+/)
          .filter(t => t.length > 2)
      );

      let common = 0;
      for (const t of queryTokens) {
        if (prodTokens.has(t)) common++;
      }

      const score = common / Math.max(queryTokens.size, 1);
      if (score > highestScore) {
        highestScore = score;
        bestMatch = prod;
      }
    }

    // Threshold of >= 0.60 token overlap indicates item exists
    const exists = highestScore >= 0.60;

    return {
      exists,
      matchedProduct: exists ? bestMatch : null,
      similarityScore: Math.round(highestScore * 100)
    };
  }
}

module.exports = CatalogGapChecker;

