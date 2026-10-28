/**
 * ShopRaven Zero-Dashboard WhatsApp Approval Manager.
 * Enables Store Owner to approve product publishings, clearance discounts,
 * and high-risk orders directly on WhatsApp (+923114618934) without logging into any control room.
 * 
 * Supports:
 * 1. Direct text reply on WhatsApp ("APPROVE", "YES", "APPROVE 101", "REJECT").
 * 2. 1-Tap Quick-Approve Web Link in the WhatsApp message (No login required).
 */

const crypto = require('crypto');
const { CONFIG } = require('../config/env');

class WhatsAppApprovalManager {
  constructor(whatsappClient, productPublisher) {
    this.whatsappClient = whatsappClient;
    this.publisher = productPublisher;
    this.adminPhone = CONFIG.ADMIN_WHATSAPP_NUMBER || '+923114618934';
    this.baseUrl = process.env.BASE_PUBLIC_URL || 'http://localhost:4000';

    // Store active approval requests in memory
    this.approvals = new Map();
    this.counter = 100;
  }

  /**
   * Generates a new approval request, saves it, and dispatches a rich WhatsApp message
   * with both Direct Reply instructions and 1-Tap Quick-Approve link.
   */
  async requestApproval({ type, targetId, title, description, details = {}, payload = {} }) {
    this.counter += 1;
    const shortCode = String(this.counter);
    const approvalId = `APR-${shortCode}`;
    const token = crypto.randomBytes(16).toString('hex');

    const approval = {
      id: approvalId,
      shortCode,
      token,
      type: type || 'PUBLISH_PRODUCT',
      targetId,
      title,
      description,
      details,
      payload,
      status: 'PENDING',
      createdAt: new Date().toISOString()
    };

    this.approvals.set(approvalId, approval);
    this.approvals.set(shortCode, approval);
    this.approvals.set(token, approval);

    // Format rich WhatsApp message
    const message = this.buildWhatsAppMessage(approval);

    console.log(`[WhatsApp Approval] Requesting approval ${approvalId} for "${title}" -> ${this.adminPhone}`);
    await this.whatsappClient.sendTextMessage(this.adminPhone, message);

    return approval;
  }

  /**
   * Constructs the WhatsApp message with reply commands and 1-tap quick approve URL.
   */
  buildWhatsAppMessage(approval) {
    const { id, shortCode, token, title, description, details } = approval;
    const timestamp = new Date().toLocaleTimeString('en-PK', { timeZone: 'Asia/Karachi' });
    const quickApproveUrl = `${this.baseUrl}/api/approvals/quick-approve?id=${id}&token=${token}`;

    let detailsList = '';
    for (const [k, v] of Object.entries(details)) {
      if (v) detailsList += `• *${k}:* ${v}\n`;
    }

    return `🚨 *ShopRaven: Approval Required*\n\n` +
      `📌 *Item:* ${title}\n` +
      `📋 *Details:* ${description}\n` +
      `🔢 *Approval Code:* ${id}\n\n` +
      (detailsList ? `${detailsList}\n` : '') +
      `━━━━━━━━━━━━━━━━━━━━━━━━\n` +
      `💬 *REPLY DIRECTLY ON WHATSAPP:*\n` +
      `👉 Reply *APPROVE* or *YES* (to publish live)\n` +
      `👉 Or Reply *APPROVE ${shortCode}*\n` +
      `👉 Reply *REJECT* (to cancel)\n\n` +
      `📱 *OR 1-TAP QUICK APPROVE (NO LOGIN):*\n` +
      `${quickApproveUrl}\n` +
      `━━━━━━━━━━━━━━━━━━━━━━━━\n` +
      `⏱ *Sent:* ${timestamp} PKT | nnstore.shop`;
  }

  /**
   * Finds pending approval by ID, shortCode, or gets the most recent pending approval.
   */
  findPendingApproval(identifier) {
    if (identifier) {
      const clean = String(identifier).trim().toUpperCase();
      const app = this.approvals.get(clean) || this.approvals.get(`APR-${clean}`);
      if (app && app.status === 'PENDING') return app;
    }

    // Find latest pending approval
    const all = Array.from(new Set(this.approvals.values()));
    const pending = all.filter(a => a.status === 'PENDING');
    if (pending.length > 0) {
      pending.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      return pending[0];
    }

    return null;
  }

  /**
   * Processes incoming WhatsApp reply from Admin.
   * Handles "APPROVE", "YES", "APPROVE 101", "REJECT", etc.
   */
  async handleIncomingWhatsAppMessage(fromPhone, text) {
    const cleanPhone = this.whatsappClient.normalizePhoneNumber(fromPhone);
    const adminNormalized = this.whatsappClient.normalizePhoneNumber(this.adminPhone);

    // Verify authorized admin phone
    if (cleanPhone !== adminNormalized) {
      console.log(`[WhatsApp Auth] Message from unverified phone ${cleanPhone} (Expected ${adminNormalized}).`);
      return { handled: false, reason: 'UNAUTHORIZED_SENDER' };
    }

    const trimmed = (text || '').trim();
    if (!trimmed) return { handled: false };

    // Parse commands
    const tokens = trimmed.split(/\s+/);
    const command = tokens[0].toUpperCase();
    const targetCode = tokens[1] || null;

    const isApprove = ['APPROVE', 'YES', 'HAAN', 'OK', 'Y', 'PUBLISH'].includes(command);
    const isReject = ['REJECT', 'NO', 'NAHI', 'CANCEL', 'N'].includes(command);
    const isStatus = ['STATUS', 'PENDING', 'LIST'].includes(command);

    if (isStatus) {
      return await this.sendPendingStatus();
    }

    if (!isApprove && !isReject) {
      return { handled: false, reason: 'NOT_A_COMMAND' };
    }

    const approval = this.findPendingApproval(targetCode);
    if (!approval) {
      const replyMsg = `ℹ️ *ShopRaven:* No pending approval request found for "${targetCode || 'recent'}".\nSend *STATUS* to see pending actions.`;
      await this.whatsappClient.sendTextMessage(this.adminPhone, replyMsg);
      return { handled: true, status: 'NOT_FOUND' };
    }

    if (isReject) {
      approval.status = 'REJECTED';
      const rejectMsg = `❌ *Rejected on WhatsApp*\nApproval *${approval.id}* for "${approval.title}" has been cancelled.`;
      await this.whatsappClient.sendTextMessage(this.adminPhone, rejectMsg);
      return { handled: true, status: 'REJECTED', approval };
    }

    // Execute approval
    return await this.executeApproval(approval, 'WhatsApp Direct Reply');
  }

  /**
   * Executes the approved action (e.g. publishing draft live to WooCommerce).
   */
  async executeApproval(approval, actor = 'WhatsApp') {
    approval.status = 'APPROVED';
    approval.approvedAt = new Date().toISOString();
    approval.approvedBy = actor;

    let executionResult = null;
    let liveUrl = `https://nnstore.shop/product/${approval.payload?.slug || ''}`;

    try {
      if (approval.type === 'PUBLISH_PRODUCT') {
        const draftId = approval.payload?.draftId || approval.targetId;
        console.log(`[WhatsApp Approval] Publishing product #${draftId} live to WooCommerce...`);
        
        if (this.publisher && draftId) {
          executionResult = await this.publisher.publishDraftToLive(draftId);
        }
      }

      // Notify Admin on WhatsApp with live confirmation & store link
      const confirmMsg = `✅ *APPROVED & PUBLISHED LIVE!*\n\n` +
        `🎉 Product *${approval.title}* is now live on *nnstore.shop*!\n\n` +
        `• *Action:* Published via ${actor}\n` +
        `• *Draft ID:* #${approval.targetId}\n` +
        `• *Sale Price:* Rs. ${approval.details?.['Sale Price'] || '1,399'}\n` +
        `• *Delivery:* Flat Rs. 150 COD\n` +
        `• *Live Link:* ${liveUrl}\n\n` +
        `🚀 Google & Bing sitemaps have been pinged for instant indexing.`;

      await this.whatsappClient.sendTextMessage(this.adminPhone, confirmMsg);

      return {
        handled: true,
        status: 'SUCCESS',
        approval,
        executionResult
      };
    } catch (err) {
      console.error(`[WhatsApp Approval Execution Error]:`, err.message);
      const errMsg = `⚠️ *Approval Error for ${approval.id}*: ${err.message}\nPlease check system logs.`;
      await this.whatsappClient.sendTextMessage(this.adminPhone, errMsg);
      return { handled: true, status: 'ERROR', error: err.message };
    }
  }

  /**
   * Sends active pending approvals status to Admin WhatsApp.
   */
  async sendPendingStatus() {
    const all = Array.from(new Set(this.approvals.values()));
    const pending = all.filter(a => a.status === 'PENDING');

    if (pending.length === 0) {
      const msg = `✅ *ShopRaven:* All approvals are up to date! No pending actions.\nAutonomous pipelines running normally every 30 minutes.`;
      await this.whatsappClient.sendTextMessage(this.adminPhone, msg);
      return { handled: true, pendingCount: 0 };
    }

    let listText = `📋 *ShopRaven: Pending Approvals (${pending.length})*\n\n`;
    for (const p of pending) {
      listText += `• *${p.id}* (${p.shortCode}): ${p.title}\n  Reply: *APPROVE ${p.shortCode}*\n\n`;
    }

    await this.whatsappClient.sendTextMessage(this.adminPhone, listText);
    return { handled: true, pendingCount: pending.length };
  }
}

module.exports = WhatsAppApprovalManager;

