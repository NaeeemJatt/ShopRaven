/**
 * Automated test suite for ShopRaven Node.js Orchestrator.
 */

const CatalogGapChecker = require('../src/woocommerce/catalog_sync');
const CODRTOGuard = require('../src/whatsapp/cod_rto_guard');
const AbandonedCartRecoveryEngine = require('../src/whatsapp/cart_recovery');

describe('ShopRaven Orchestrator Core Suite', () => {
  let catalogChecker;
  let rtoGuard;
  let cartRecovery;

  beforeEach(() => {
    catalogChecker = new CatalogGapChecker();
    rtoGuard = new CODRTOGuard();
    cartRecovery = new AbandonedCartRecoveryEngine();
  });

  describe('Catalog Gap Analysis', () => {
    test('checkCatalogGap flags existing product when tokens match', async () => {
      // Mock catalog in memory
      catalogChecker.catalogCache = [
        { id: 101, name: 'Ultrasonic Skin Scrubber Pore Cleaner' },
        { id: 102, name: 'Electric Vegetable Cutter 4 in 1' }
      ];
      catalogChecker.lastFetched = Date.now();

      const res = await catalogChecker.checkProductExistsInStore('Skin Scrubber Ultrasonic Cleaner');
      expect(res.exists).toBe(true);
      expect(res.matchedProduct.id).toBe(101);
      expect(res.similarityScore).toBeGreaterThanOrEqual(60);
    });

    test('checkCatalogGap identifies missing opportunities correctly', async () => {
      catalogChecker.catalogCache = [
        { id: 101, name: 'Ultrasonic Skin Scrubber' }
      ];
      catalogChecker.lastFetched = Date.now();

      const res = await catalogChecker.checkProductExistsInStore('Wireless Tire Inflator Digital Pump');
      expect(res.exists).toBe(false);
      expect(res.matchedProduct).toBeNull();
    });
  });

  describe('COD RTO Risk Scorer', () => {
    test('scoreOrderRTORisk flags incomplete address as HIGH risk', () => {
      const highRiskOrder = {
        id: 901,
        billing_first_name: 'Ahmed',
        phone: '03120000000',
        shipping_address: 'Near main bazar', // Missing house/street number and under 15 chars
        shipping_city: 'Lahore'
      };

      const result = rtoGuard.scoreOrderRTORisk(highRiskOrder);
      expect(result.riskScore).toBeGreaterThanOrEqual(35);
      expect(result.reasons.length).toBeGreaterThan(0);
      expect(result.riskLevel).not.toBe('LOW');
    });

    test('scoreOrderRTORisk validates complete address as LOW risk', () => {
      const validOrder = {
        id: 902,
        billing_first_name: 'Hamza',
        phone: '03124999196',
        shipping_address: 'House 42, Street 8, Sector F-7/2',
        shipping_city: 'Islamabad'
      };

      const result = rtoGuard.scoreOrderRTORisk(validOrder);
      expect(result.riskLevel).toBe('LOW');
      expect(result.riskScore).toBeLessThan(35);
    });
  });

  describe('Cart Recovery URL Builder', () => {
    test('buildPreFilledRecoveryUrl formats correct link with coupon', () => {
      const url = cartRecovery.buildPreFilledRecoveryUrl([{ id: 105, quantity: 1 }], 'DEAL-A1B2');
      expect(url).toContain('https://nnstore.shop/cart');
      expect(url).toContain('fill_cart=105%3A1');
      expect(url).toContain('coupon_code=DEAL-A1B2');
    });
  });
});

