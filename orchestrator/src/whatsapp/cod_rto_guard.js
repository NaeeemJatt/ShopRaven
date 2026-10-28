/**
 * COD-to-Prepaid Split & RTO Risk Scorer (Alippo Feature #11).
 * Detects high-risk incomplete addresses and sends WhatsApp confirmations
 * offering to WAIVE the Rs. 150 shipping fee if the customer pays via Raast / EasyPaisa / JazzCash.
 */

const WhatsAppCloudClient = require('./cloud_client');

class CODRTOGuard {
  constructor() {
    this.whatsappClient = new WhatsAppCloudClient();
  }

  scoreOrderRTORisk(orderPayload) {
    let riskScore = 10; // Base score (0 - 100)
    const reasons = [];

    const address = (orderPayload.shipping_address || orderPayload.billing_address || '').trim();
    const city = (orderPayload.shipping_city || orderPayload.billing_city || '').trim().toLowerCase();
    const phone = (orderPayload.phone || orderPayload.billing_phone || '').trim();

    // 1. Check address completeness (Pakistani couriers require house/street/sector details)
    if (address.length <= 18) {
      riskScore += 35;
      reasons.push('Vague or excessively short delivery address');
    }
    if (!/\d/.test(address)) {
      riskScore += 20;
      reasons.push('Address missing house, street, or sector number');
    }

    // 2. Phone validation
    const cleanPhone = phone.replace(/[^0-9]/g, '');
    if (cleanPhone.length < 10 || cleanPhone.length > 13) {
      riskScore += 40;
      reasons.push('Suspect or malformed phone number');
    }

    // 3. Remote area / high-RTO cities
    const highRTOCities = ['rural', 'tehsil', 'village', 'chack'];
    if (highRTOCities.some(r => address.toLowerCase().includes(r))) {
      riskScore += 15;
      reasons.push('Remote village or rural tehsil route (higher courier return probability)');
    }

    let riskLevel = 'LOW';
    if (riskScore >= 60) {
      riskLevel = 'HIGH';
    } else if (riskScore >= 35) {
      riskLevel = 'MEDIUM';
    }

    return {
      riskScore: Math.min(riskScore, 100),
      riskLevel,
      reasons: reasons.length > 0 ? reasons : ['Verified complete address']
    };
  }

  async sendCODConfirmationAndPrepaidOffer(orderPayload) {
    const phone = orderPayload.phone || orderPayload.billing_phone;
    const orderId = orderPayload.id || orderPayload.order_id || 'NN-New';
    const name = orderPayload.billing_first_name || 'Valued Customer';
    const totalPkr = orderPayload.total || '0';

    if (!phone) {
      return { status: 'skipped', reason: 'Missing phone' };
    }

    const assessment = this.scoreOrderRTORisk(orderPayload);

    // WhatsApp message offering Rs. 150 shipping waiver for prepaid
    const msg = `Assalam-o-Alaikum ${name}! Shukriya for ordering at *nnstore.shop* (Order #${orderId}). 📦\n\nYour order total is *Rs. ${totalPkr}* with Cash-on-Delivery.\n\n⚡ *SPECIAL PREPAID OFFER (Save Rs. 150!):*\nIf you switch from COD to direct payment via *Raast / EasyPaisa / JazzCash*, we will *WAIVE the Rs. 150 delivery fee* completely!\n\nTo avail this:\n1. Reply *'PREPAID'* to get our official Raast ID.\n2. Or reply *'CONFIRM COD'* to dispatch with standard Cash-on-Delivery.\n\nThank you for choosing nnstore.shop!`;

    const dispatchResult = await this.whatsappClient.sendTextMessage(phone, msg);

    return {
      status: 'confirmation_sent',
      assessment,
      dispatchResult
    };
  }
}

module.exports = CODRTOGuard;

