/**
 * Influencer / UGC Creator & Sales Associate Outreach Bot (Alippo Feature #20).
 * Automates outreach and onboarding for Pakistani micro-influencers, generates custom affiliate coupons,
 * and coordinates daily dispatch/confirmation tasks with sales associates.
 */

const WhatsAppCloudClient = require('./cloud_client');
const WooCommerceCouponService = require('../woocommerce/coupon_service');
const { CONFIG } = require('../config/env');

class CreatorAndAssociateOutreachBot {
  constructor() {
    this.whatsapp = new WhatsAppCloudClient();
    this.couponService = new WooCommerceCouponService();
    this.storeUrl = CONFIG.WC_STORE_URL || 'https://nnstore.shop';
  }

  /**
   * Onboards a UGC Creator / Influencer with dedicated coupon and commission brief.
   */
  async onboardUGCCreator(creatorName, phonePK, instagramHandle, productId = null) {
    const handleClean = (instagramHandle || creatorName).replace(/[^a-zA-Z0-9]/g, '').toUpperCase().slice(0, 8);
    const affiliateCouponCode = `${handleClean}10`; // e.g. SARA10 for 10% off

    // Create 30-day affiliate coupon
    let couponCreated = false;
    try {
      await this.couponService.createSingleUseCoupon(affiliateCouponCode, 150, 43200); // 30 days
      couponCreated = true;
    } catch (e) {
      console.warn(`[Creator Outreach] Coupon creation note: ${e.message}`);
    }

    const welcomeMsg = 
      `Assalam-o-Alaikum ${creatorName}! 👋✨\n\n` +
      `We love your content on Instagram (*@${instagramHandle}*) and would love to partner with you for *nnstore.shop*!\n\n` +
      `🎁 *Your Exclusive Influencer Perks:*\n` +
      `• *Your Custom Coupon:* *${affiliateCouponCode}* (Gives your followers Flat Rs. 150 OFF + Free COD Delivery)\n` +
      `• *Your Commission:* Rs. 200 Cash per delivered order via JazzCash / EasyPaisa.\n` +
      `• *Free Sample Seeding:* We dispatch our top-selling trending products straight to your door!\n\n` +
      `👉 Reply *"YES"* to confirm your shipping address and receive your free creator PR parcel today! 📦❤️`;

    const dispatchResult = await this.whatsapp.sendTextMessage(phonePK, welcomeMsg);

    // Notify Admin on WhatsApp that a new creator is being onboarded
    await this.whatsapp.notifyAdminAction(
      'UGC Creator Outreach Dispatched',
      `Sent collaboration invitation & coupon ${affiliateCouponCode} to @${instagramHandle}`,
      {
        'Creator': creatorName,
        'Handle': `@${instagramHandle}`,
        'Phone': phonePK,
        'Coupon Code': affiliateCouponCode,
        'Commission': 'Rs. 200 / delivered COD order'
      }
    );

    return {
      success: true,
      creatorName,
      affiliateCouponCode,
      dispatchResult
    };
  }

  /**
   * Dispatches daily tasks and reminders to internal sales associates via WhatsApp.
   */
  async dispatchSalesAssociateTask(associatePhone, taskSummary, priority = 'NORMAL') {
    const timestamp = new Date().toLocaleTimeString('en-PK', { timeZone: 'Asia/Karachi' });
    const priorityIcon = priority === 'URGENT' ? '🚨' : '📋';

    const taskMsg = 
      `${priorityIcon} *ShopRaven Operational Task Assignment*\n\n` +
      `📌 *Task:* ${taskSummary}\n` +
      `⏰ *Assigned Time:* ${timestamp} PKT\n` +
      `🌐 *Admin Panel:* ${this.storeUrl}/wp-admin/\n\n` +
      `Please reply with *"DONE"* once completed or report any customer delivery issues here.`;

    return await this.whatsapp.sendTextMessage(associatePhone, taskMsg);
  }
}

module.exports = CreatorAndAssociateOutreachBot;

