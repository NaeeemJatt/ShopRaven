/**
 * Post-Delivery Rating & Review Protection Shield (Alippo Feature #17).
 * Sends a WhatsApp check-in 24 hours after courier delivery.
 * - 4-5 Star ratings: Dispatches a 1-tap link to post a verified photo review on nnstore.shop (boosts 4.8★ Google snippets).
 * - 1-3 Star ratings: Privately intercepts complaints, alerts VIP customer support (+92 312 4999196), and prevents negative public reviews.
 */

const WhatsAppCloudClient = require('./cloud_client');
const WooCommerceAPIClient = require('../woocommerce/wc_api_client');
const { CONFIG } = require('../config/env');

class StoreRatingProtectionShield {
  constructor() {
    this.whatsapp = new WhatsAppCloudClient();
    this.wcClient = new WooCommerceAPIClient();
    this.storeUrl = CONFIG.WC_STORE_URL || 'https://nnstore.shop';
    this.supportWhatsApp = CONFIG.STORE_SUPPORT_WHATSAPP || '+923124999196';
  }

  /**
   * Dispatches WhatsApp check-in message 24 hours after courier delivers order.
   */
  async triggerPostDeliveryRatingCheck(orderPayload) {
    const customerPhone = orderPayload.billing?.phone || orderPayload.phone;
    const customerName = orderPayload.billing?.first_name || orderPayload.customer_name || 'Customer';
    const orderId = orderPayload.id || orderPayload.order_id || 'Order';
    const productName = orderPayload.line_items?.[0]?.name || 'your order';

    if (!customerPhone) {
      return { success: false, reason: 'No phone number provided' };
    }

    const checkInMessage = 
      `Assalam-o-Alaikum ${customerName}! 📦✨\n\n` +
      `We hope you are enjoying your *${productName}* (Order #${orderId}) from *nnstore.shop*!\n\n` +
      `How was your delivery and product experience?\n\n` +
      `Please reply with a number (1 to 5):\n` +
      `⭐⭐⭐⭐⭐ (5) — Excellent! Loved it\n` +
      `⭐⭐⭐⭐ (4) — Good\n` +
      `⭐⭐⭐ (3) — Average\n` +
      `⭐⭐ (2) — Below expectations\n` +
      `⭐ (1) — Terrible / Issues with item\n\n` +
      `Your honest feedback helps us serve you better across Pakistan! 🙏`;

    return await this.whatsapp.sendTextMessage(customerPhone, checkInMessage);
  }

  /**
   * Processes the buyer's star reply and routes accordingly.
   */
  async handleBuyerRatingReply(phonePK, starRating, feedbackText = '') {
    const stars = parseInt(starRating, 10);

    if (stars >= 4) {
      // 4-5 Stars: Direct to public review page to boost 4.8★ Google Rich Snippet
      const reviewUrl = `${this.storeUrl}/reviews/?rate=5&verified=true`;
      const thankYouMsg = 
        `JazakAllah Khair! 🎉 We are thrilled you loved your order!\n\n` +
        `Could you take 30 seconds to share a quick photo review on our store? ` +
        `As a thank-you, you'll receive a *Rs. 150 discount coupon* on your next purchase!\n\n` +
        `👉 Tap here to post your review:\n${reviewUrl}\n\n` +
        `Team nnstore.shop ❤️`;

      await this.whatsapp.sendTextMessage(phonePK, thankYouMsg);
      return {
        action: 'PUBLIC_REVIEW_PROMOTED',
        stars,
        reviewUrl
      };
    } else {
      // 1-3 Stars: Intercept privately before public negative review
      const apologyMsg = 
        `We are genuinely sorry to hear that your experience was not 100% satisfactory. 💔\n\n` +
        `At nnstore.shop, we provide a *7-Day Money-Back & Free Exchange Guarantee*.\n\n` +
        `Our Senior Support Manager is reviewing this immediately and will contact you shortly to replace your item or issue a full refund.\n\n` +
        `You can also chat directly with our manager on WhatsApp: ${this.supportWhatsApp}`;

      await this.whatsapp.sendTextMessage(phonePK, apologyMsg);

      // Alert Admin on WhatsApp
      await this.whatsapp.notifyAdminApproval(
        `🚨 Negative Review Intercepted (${stars}★)`,
        `Customer expressed dissatisfaction. Intercepted privately before public review.`,
        {
          'Customer Phone': phonePK,
          'Rating Given': `${stars} / 5 Stars`,
          'Feedback': feedbackText || 'No comment provided',
          'Status': 'Awaiting Support Contact'
        }
      );

      return {
        action: 'PRIVATE_RESOLUTION_INTERCEPTED',
        stars,
        escalatedTo: this.supportWhatsApp
      };
    }
  }
}

module.exports = StoreRatingProtectionShield;

