const assert = require('assert');
const WhatsAppCloudClient = require('../src/whatsapp/cloud_client');

async function testNotifyPublished() {
  process.env.NODE_ENV = 'test';
  const client = new WhatsAppCloudClient();
  
  const result = await client.notifyProductPublished({
    id: 999,
    title: 'Smart Ambient Sunset RGB Lamp',
    salePrice: 1699,
    regularPrice: 2499,
    category: 'Home & Living',
    liveUrl: 'https://nnstore.shop/product/smart-ambient-sunset-rgb-lamp/',
    imageUrl: 'https://nnstore.shop/wp-content/uploads/2026/10/sunset_lamp_product_1793319441224.jpg'
  });

  assert.strictEqual(result.success, true);
  assert.strictEqual(result.mock, true);
  assert.ok(result.message.includes('PRODUCT PUBLISHED LIVE ON NNSTORE.SHOP!'));
  assert.ok(result.message.includes('Smart Ambient Sunset RGB Lamp'));
  assert.ok(result.message.includes('Rs. 1,699'));
  assert.ok(result.message.includes('https://nnstore.shop/product/smart-ambient-sunset-rgb-lamp/'));
  assert.ok(result.message.includes('Flat Rs. 150 Cash on Delivery'));
  console.log('✅ notifyProductPublished test passed successfully!');
}

testNotifyPublished().catch(e => {
  console.error(e);
  process.exit(1);
});
