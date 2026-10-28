/**
 * WhatsApp Abandoned Cart Recovery (Alippo Feature #12).
 * Triggers 20 minutes after checkout abandonment with a pre-filled recovery link.
 */

const WhatsAppCloudClient = require('./cloud_client');

class AbandonedCartRecoveryEngine {
  constructor() {
    this.whatsappClient = new WhatsAppCloudClient();
  }

  buildPreFilledRecoveryUrl(cartItems = [], couponCode = '') {
    const storeUrl = 'https://nnstore.shop/cart';
    const params = new URLSearchParams();

    if (cartItems.length > 0 && cartItems[0].id) {
      params.append('fill_cart', cartItems.map(i => `${i.id}:${i.quantity || 1}`).join(','));
    }
    if (couponCode) {
      params.append('coupon_code', couponCode);
    }

    const queryStr = params.toString();
    return queryStr ? `${storeUrl}?${queryStr}` : storeUrl;
  }

  async handleAbandonedCheckout(checkoutPayload) {
    const phone = checkoutPayload.billing_phone || checkoutPayload.phone;
    const name = checkoutPayload.billing_first_name || 'Customer';
    const items = checkoutPayload.items || [];
    const coupon = checkoutPayload.deal_hunter_coupon || '';

    if (!phone) {
      return { status: 'skipped', reason: 'No phone number provided' };
    }

    const recoveryLink = this.buildPreFilledRecoveryUrl(items, coupon);

    const couponNotice = coupon
      ? `\n🎁 We reserved a special discount code *${coupon}* to give you extra savings on your order!`
      : '';

    const message = `Assalam-o-Alaikum ${name}! 👋\n\nWe noticed you left items in your cart at *nnstore.shop*.\n${couponNotice}\n\nTap below to complete your order with flat Rs. 150 Cash-on-Delivery anywhere in Pakistan:\n👉 ${recoveryLink}\n\nNeed help with sizing or delivery? Reply right here on WhatsApp!`;

    const dispatchResult = await this.whatsappClient.sendTextMessage(phone, message);

    return {
      status: 'dispatched',
      recipient: phone,
      recoveryLink,
      dispatchResult
    };
  }
}

module.exports = AbandonedCartRecoveryEngine;

