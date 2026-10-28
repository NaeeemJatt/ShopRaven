/**
 * Restock Waitlist Dispatcher (Alippo Feature #8).
 * Notifies waitlisted buyers on WhatsApp when out-of-stock items return to stock.
 */

const WhatsAppCloudClient = require('../whatsapp/cloud_client');

class RestockWaitlistDispatcher {
  constructor() {
    this.whatsappClient = new WhatsAppCloudClient();
    this.waitlists = new Map(); // In-memory/DB map of productId -> Set of phone numbers
  }

  registerWaitlistSubscriber(wcProductId, whatsappNumber) {
    if (!this.waitlists.has(wcProductId)) {
      this.waitlists.set(wcProductId, new Set());
    }
    this.waitlists.get(wcProductId).add(whatsappNumber);
    return {
      success: true,
      productId: wcProductId,
      subscriberPhone: whatsappNumber
    };
  }

  async dispatchRestockLinksForProduct(wcProductId, productTitle) {
    const subscribers = this.waitlists.get(wcProductId);
    if (!subscribers || subscribers.size === 0) {
      return { dispatchedCount: 0 };
    }

    let sent = 0;
    const checkoutLink = `https://nnstore.shop/?add-to-cart=${wcProductId}`;

    for (const phone of subscribers) {
      const msg = `🎉 Good News from nnstore.shop!\n\nThe product you were waiting for, *"${productTitle || 'Item'}"*, is finally BACK IN STOCK!\n\nTap below to order now before it sells out again (Flat Rs. 150 COD delivery nationwide):\n👉 ${checkoutLink}\n\nQuestions? Reply directly to this WhatsApp!`;
      try {
        await this.whatsappClient.sendTextMessage(phone, msg);
        sent++;
      } catch (err) {
        // Continue notifying remaining waitlist
      }
    }

    // Clear waitlist after successful notification
    this.waitlists.delete(wcProductId);

    return {
      dispatchedCount: sent,
      productId: wcProductId
    };
  }
}

module.exports = RestockWaitlistDispatcher;

