const test = require('node:test');
const assert = require('node:assert');
const WhatsAppApprovalManager = require('../src/whatsapp/approval_manager');

test('WhatsApp Approval Manager Test Suite', async (t) => {
  let sentMessages = [];
  const mockWhatsappClient = {
    normalizePhoneNumber: (p) => {
      if (!p) return '';
      let c = p.replace(/[^0-9]/g, '');
      if (c.startsWith('03')) c = '92' + c.slice(1);
      return '+' + c;
    },
    sendTextMessage: async (to, text) => {
      sentMessages.push({ to, text });
      return { success: true };
    }
  };

  let publishedDraftId = null;
  const mockPublisher = {
    publishDraftToLive: async (id) => {
      publishedDraftId = id;
      return { id, status: 'publish' };
    }
  };

  const manager = new WhatsAppApprovalManager(mockWhatsappClient, mockPublisher);
  manager.adminPhone = '+923114618934';

  await t.test('1. Creates approval and sends WhatsApp message to admin', async () => {
    const app = await manager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 258,
      title: 'Smart Sunset Lamp RGB',
      description: 'Studio canvas ready',
      details: { 'Sale Price': 'Rs. 1,399' },
      payload: { draftId: 258, slug: 'sunset-lamp' }
    });

    assert.strictEqual(app.status, 'PENDING');
    assert.strictEqual(sentMessages.length, 1);
    assert.strictEqual(sentMessages[0].to, '+923114618934');
    assert.ok(sentMessages[0].text.includes('Smart Sunset Lamp RGB'));
    assert.ok(sentMessages[0].text.includes('REPLY DIRECTLY ON WHATSAPP'));
    assert.ok(sentMessages[0].text.includes('quick-approve'));
  });

  await t.test('2. Admin WhatsApp reply "APPROVE" triggers live publish to WooCommerce', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'APPROVE');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'SUCCESS');
    assert.strictEqual(publishedDraftId, 258);

    const latestMessage = sentMessages[sentMessages.length - 1];
    assert.ok(latestMessage.text.includes('APPROVED & PUBLISHED LIVE'));
    assert.ok(latestMessage.text.includes('nnstore.shop'));
  });

  await t.test('3. Admin WhatsApp reply "REJECT" cancels the approval', async () => {
    publishedDraftId = null;
    const app2 = await manager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 301,
      title: 'Unwanted SKU',
      details: {}
    });

    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'REJECT');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'REJECTED');
    assert.strictEqual(publishedDraftId, null); // Did NOT publish

    const rejectMsg = sentMessages[sentMessages.length - 1];
    assert.ok(rejectMsg.text.includes('Rejected on WhatsApp'));
  });

  await t.test('4. Blocks unauthorized sender numbers', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923009999999', 'APPROVE');
    assert.strictEqual(result.handled, false);
    assert.strictEqual(result.reason, 'UNAUTHORIZED_SENDER');
  });

  await t.test('5. 1-Tap Quick-Approve executes without dashboard login', async () => {
    publishedDraftId = null;
    const app3 = await manager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 444,
      title: 'Quick Tap Product',
      details: { 'Sale Price': 'Rs. 2,199' }
    });

    const pending = manager.findPendingApproval(app3.token);
    assert.ok(pending);
    const result = await manager.executeApproval(pending, '1-Tap Quick-Approve Link');
    assert.strictEqual(result.status, 'SUCCESS');
    assert.strictEqual(publishedDraftId, 444);
    assert.strictEqual(pending.status, 'APPROVED');
  });
});

