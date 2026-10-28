/**
 * Unit tests for Zero-Dashboard WhatsApp Approval Manager.
 */

const WhatsAppApprovalManager = require('../src/whatsapp/approval_manager');

describe('WhatsApp Zero-Dashboard Approval Engine', () => {
  let approvalManager;
  let mockWhatsappClient;
  let mockPublisher;
  let sentMessages = [];

  beforeEach(() => {
    sentMessages = [];
    mockWhatsappClient = {
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

    mockPublisher = {
      publishDraftToLive: jest.fn().mockResolvedValue({ id: 258, status: 'publish' })
    };

    approvalManager = new WhatsAppApprovalManager(mockWhatsappClient, mockPublisher);
    approvalManager.adminPhone = '+923114618934';
  });

  test('requestApproval generates shortCode, quick-approve URL, and dispatches to admin phone', async () => {
    const approval = await approvalManager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 258,
      title: 'Smart Sunset Lamp RGB',
      description: 'Tested 1080x1080 canvas with Roman-Urdu tags',
      details: {
        'Sale Price': 'Rs. 1,399',
        'Wholesale': 'Rs. 720'
      },
      payload: { draftId: 258, slug: 'sunset-lamp' }
    });

    expect(approval.id).toBeDefined();
    expect(approval.status).toBe('PENDING');
    expect(sentMessages.length).toBe(1);
    expect(sentMessages[0].to).toBe('+923114618934');
    expect(sentMessages[0].text).toContain('Smart Sunset Lamp RGB');
    expect(sentMessages[0].text).toContain('REPLY DIRECTLY ON WHATSAPP');
    expect(sentMessages[0].text).toContain('quick-approve');
  });

  test('Direct reply "APPROVE" from admin executes live publish and notifies back', async () => {
    const approval = await approvalManager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 258,
      title: 'Smart Sunset Lamp RGB',
      description: 'Ready to go live',
      details: { 'Sale Price': 'Rs. 1,399' },
      payload: { draftId: 258, slug: 'sunset-lamp' }
    });

    // Admin replies "APPROVE" via WhatsApp
    const result = await approvalManager.handleIncomingWhatsAppMessage('+923114618934', 'APPROVE');

    expect(result.handled).toBe(true);
    expect(result.status).toBe('SUCCESS');
    expect(mockPublisher.publishDraftToLive).toHaveBeenCalledWith(258);
    expect(approval.status).toBe('APPROVED');

    // Should have sent confirmation WhatsApp message
    const confirmMsg = sentMessages[sentMessages.length - 1];
    expect(confirmMsg.text).toContain('APPROVED & PUBLISHED LIVE');
    expect(confirmMsg.text).toContain('nnstore.shop');
  });

  test('Direct reply with specific shortCode "APPROVE 101" targets correct approval', async () => {
    const approval = await approvalManager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 305,
      title: 'Electric Vegetable Chopper',
      description: 'Kitchen mover',
      details: {},
      payload: { draftId: 305, slug: 'vegetable-chopper' }
    });

    const result = await approvalManager.handleIncomingWhatsAppMessage('+923114618934', `APPROVE ${approval.shortCode}`);
    expect(result.handled).toBe(true);
    expect(result.status).toBe('SUCCESS');
    expect(mockPublisher.publishDraftToLive).toHaveBeenCalledWith(305);
  });

  test('Direct reply "REJECT" cancels the approval without publishing', async () => {
    const approval = await approvalManager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 400,
      title: 'Unwanted Product',
      description: 'Testing rejection',
      details: {}
    });

    const result = await approvalManager.handleIncomingWhatsAppMessage('+923114618934', 'REJECT');
    expect(result.handled).toBe(true);
    expect(result.status).toBe('REJECTED');
    expect(approval.status).toBe('REJECTED');
    expect(mockPublisher.publishDraftToLive).not.toHaveBeenCalled();

    const rejectNotice = sentMessages[sentMessages.length - 1];
    expect(rejectNotice.text).toContain('Rejected on WhatsApp');
  });

  test('Unauthorized sender phone is rejected for security', async () => {
    await approvalManager.requestApproval({
      type: 'PUBLISH_PRODUCT',
      targetId: 500,
      title: 'Security Test',
      details: {}
    });

    const result = await approvalManager.handleIncomingWhatsAppMessage('+923001234567', 'APPROVE');
    expect(result.handled).toBe(false);
    expect(result.reason).toBe('UNAUTHORIZED_SENDER');
    expect(mockPublisher.publishDraftToLive).not.toHaveBeenCalled();
  });
});

