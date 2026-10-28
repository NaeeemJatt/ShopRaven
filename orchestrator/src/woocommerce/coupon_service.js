/**
 * WooCommerce Coupon Service: Creates single-use promotional coupons via REST API.
 */

const WooCommerceAPIClient = require('./wc_api_client');

class WooCommerceCouponService {
  constructor() {
    this.wcClient = new WooCommerceAPIClient();
  }

  async createSingleUseCoupon(code, amountPKR, expiryMinutes = 30) {
    const expiryDate = new Date(Date.now() + expiryMinutes * 60000).toISOString();

    const payload = {
      code: code,
      discount_type: 'fixed_cart',
      amount: String(amountPKR),
      individual_use: true,
      usage_limit: 1,
      usage_limit_per_user: 1,
      date_expires: expiryDate,
      description: `ShopRaven Automated Single-Use Coupon (Rs. ${amountPKR} OFF)`
    };

    return await this.wcClient.post('/coupons', payload);
  }
}

module.exports = WooCommerceCouponService;

