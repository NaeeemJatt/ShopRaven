const test = require('node:test');
const assert = require('node:assert');
const WhatsAppApprovalManager = require('../src/whatsapp/approval_manager');

test('WhatsApp Approval Manager & Status Dashboard Test Suite', async (t) => {
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

  let allTriggered = false;
  let huntedKeyword = null;
  const mockStateProvider = () => ({
    automationState: {
      cadenceMinutes: 30,
      nextRunTimestamp: new Date(Date.now() + 20 * 60 * 1000).toISOString(),
      totalCyclesExecuted: 49,
      totalProductsHunted: 145
    },
    tasksRegistry: [
      {
        engineName: '🎯 Product Hunting Scout',
        target: 'Google PK + Daraz Movers: Smart Gadgets',
        progress: 82,
        stageName: 'Phase 2: Live Catalog Gap Similarity Check (2 Winners)',
        supplier: 'Scraping wholesale catalogs',
        salePrice: 1599,
        status: 'RUNNING'
      },
      {
        engineName: '⚡ Sourcing & Listing Creator',
        target: 'Mini Portable Washing Machine',
        progress: 65,
        stageName: 'Phase 5: 1080x1080 Studio Canvas Standardization',
        supplier: 'HHC (PKR 1,150) vs Oshi (PKR 1,220) -> Winner: HHC',
        salePrice: 2199,
        status: 'RUNNING'
      }
    ],
    executionHistory: [
      {
        target: 'Wireless Smart Sensor Car Charger Mount',
        category: 'Auto & Tools',
        summary: 'Discovered high review velocity on Daraz PK -> Winner Oshi (Rs. 820) -> Draft #1043 on nnstore.shop (Sale Rs. 1,899, Profit +58%)',
        status: 'DRAFT_CREATED',
        durationSeconds: 42
      }
    ],
    triggerAll: (source) => {
      allTriggered = true;
      return true;
    },
    triggerHunt: (kw) => {
      huntedKeyword = kw;
      return { target: kw, status: 'RUNNING' };
    }
  });

  const manager = new WhatsAppApprovalManager(mockWhatsappClient, mockPublisher, mockStateProvider);
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

  await t.test('2. Admin WhatsApp reply "STATUS" sends full executive dashboard with actions, running searches, upcoming runs, and results', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'STATUS');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'STATUS_SENT');

    const statusMsg = sentMessages[sentMessages.length - 1].text;

    // Check actions described first
    assert.ok(statusMsg.includes('ACTIONS YOU CAN PERFORM VIA WHATSAPP'));
    assert.ok(statusMsg.includes('APPROVE'));
    assert.ok(statusMsg.includes('REJECT'));
    assert.ok(statusMsg.includes('HUNT [ITEM]'));
    assert.ok(statusMsg.includes('TRIGGER ALL'));
    assert.ok(statusMsg.includes('STATUS'));

    // Check running searches
    assert.ok(statusMsg.includes('CURRENTLY RUNNING SEARCHES & PIPELINES'));
    assert.ok(statusMsg.includes('Product Hunting Scout'));
    assert.ok(statusMsg.includes('Mini Portable Washing Machine'));

    // Check upcoming searches
    assert.ok(statusMsg.includes('UPCOMING SCHEDULED SEARCHES'));
    assert.ok(statusMsg.includes('every 30 minutes'));

    // Check recent searches & results
    assert.ok(statusMsg.includes('RECENT SEARCHES & RESULTS'));
    assert.ok(statusMsg.includes('Wireless Smart Sensor Car Charger Mount'));
    assert.ok(statusMsg.includes('Sale Rs. 1,899, Profit +58%'));

    // Check pending approvals
    assert.ok(statusMsg.includes('PENDING APPROVALS'));
    assert.ok(statusMsg.includes('Smart Sunset Lamp RGB'));
  });

  await t.test('3. Admin WhatsApp command "HUNT Sunset Lamp" dispatches hunting pipeline', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'HUNT Sunset Lamp RGB');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'HUNT_DISPATCHED');
    assert.strictEqual(huntedKeyword, 'Sunset Lamp RGB');

    const huntReply = sentMessages[sentMessages.length - 1].text;
    assert.ok(huntReply.includes('Product Hunt Dispatched'));
    assert.ok(huntReply.includes('Sunset Lamp RGB'));
    assert.ok(huntReply.includes('+40% Net Profit Calculation'));
  });

  await t.test('4. Admin WhatsApp command "TRIGGER ALL" triggers all 5 autonomous engines', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'TRIGGER ALL');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'TRIGGERED_ALL');
    assert.strictEqual(allTriggered, true);

    const triggerReply = sentMessages[sentMessages.length - 1].text;
    assert.ok(triggerReply.includes('All 5 Autonomous Engines Dispatched'));
    assert.ok(triggerReply.includes('Scout Engine'));
    assert.ok(triggerReply.includes('Sourcing Engine'));
    assert.ok(triggerReply.includes('SEO & AEO Engine'));
  });

  await t.test('5. Admin WhatsApp reply "APPROVE" triggers live publish to WooCommerce', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'APPROVE');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'SUCCESS');
    assert.strictEqual(publishedDraftId, 258);

    const latestMessage = sentMessages[sentMessages.length - 1];
    assert.ok(latestMessage.text.includes('APPROVED & PUBLISHED LIVE'));
    assert.ok(latestMessage.text.includes('nnstore.shop'));
  });

  await t.test('6. Admin WhatsApp reply "REJECT" cancels the approval', async () => {
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

  await t.test('7. Blocks unauthorized sender numbers', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923009999999', 'APPROVE');
    assert.strictEqual(result.handled, false);
    assert.strictEqual(result.reason, 'UNAUTHORIZED_SENDER');
  });

  await t.test('8. 1-Tap Quick-Approve executes without dashboard login', async () => {
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

  await t.test('9. Unrecognized text sends friendly Co-Founder guide', async () => {
    const result = await manager.handleIncomingWhatsAppMessage('+923114618934', 'Salam kya haal hai');
    assert.strictEqual(result.handled, true);
    assert.strictEqual(result.status, 'HELP_SENT');

    const helpMsg = sentMessages[sentMessages.length - 1].text;
    assert.ok(helpMsg.includes('Salam! I am your ShopRaven AI Co-Founder'));
    assert.ok(helpMsg.includes('STATUS'));
    assert.ok(helpMsg.includes('HUNT'));
    assert.ok(helpMsg.includes('TRIGGER ALL'));
  });
});
