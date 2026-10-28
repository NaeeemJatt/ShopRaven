/**
 * Environment configuration for ShopRaven Node.js Orchestrator.
 */

const path = require('path');
const fs = require('fs');

try {
  const dotenv = require('dotenv');
  dotenv.config({ path: path.resolve(__dirname, '../../../.env') });
  dotenv.config(); // fallback to local
} catch (e) {
  // Built-in parser fallback when run outside container
  const envPath = path.resolve(__dirname, '../../../.env');
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, 'utf8');
    content.split(/\r?\n/).forEach(line => {
      const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
      if (match) {
        const key = match[1];
        let val = match[2] || '';
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
        if (val.startsWith("'") && val.endsWith("'")) val = val.slice(1, -1);
        if (!process.env[key]) process.env[key] = val;
      }
    });
  }
}

const NNSTORE_CATEGORIES = [
  'Beauty & Care',
  'Kitchen Accessories',
  'Home & Living',
  'Gym Accessories',
  'Electronic Accessories',
  'Auto & Tools',
  'Accessories'
];

const CONFIG = {
  PORT: process.env.ORCHESTRATOR_PORT || 4000,
  PYTHON_BACKEND_URL: process.env.PYTHON_BACKEND_URL || 'http://localhost:8000',
  WC_STORE_URL: process.env.WC_STORE_URL || 'https://nnstore.shop',
  WC_CONSUMER_KEY: process.env.WC_CONSUMER_KEY || '',
  WC_CONSUMER_SECRET: process.env.WC_CONSUMER_SECRET || '',
  DEFAULT_DELIVERY_FEE_PKR: Number(process.env.DEFAULT_DELIVERY_FEE_PKR) || 150,
  FREE_DELIVERY_THRESHOLD_PKR: Number(process.env.FREE_DELIVERY_THRESHOLD_PKR) || 2500,
  DISCORD_WEBHOOK_URL: process.env.DISCORD_WEBHOOK_URL || '',
  DISCORD_BOT_TOKEN: process.env.DISCORD_BOT_TOKEN || '',
  WHATSAPP_TOKEN: process.env.WHATSAPP_TOKEN || '',
  WHATSAPP_PHONE_NUMBER_ID: process.env.WHATSAPP_PHONE_NUMBER_ID || '',
  STORE_SUPPORT_WHATSAPP: process.env.STORE_SUPPORT_WHATSAPP || '+923114618934',
  WASENDER_API_URL: process.env.WASENDER_API_URL || 'https://wasenderapi.com/api/send-message',
  WASENDER_API_TOKEN: process.env.WASENDER_API_TOKEN || process.env.WHATSAPP_TOKEN || '',
  ADMIN_WHATSAPP_NUMBER: process.env.ADMIN_WHATSAPP_NUMBER || '+923114618934'
};

module.exports = {
  CONFIG,
  NNSTORE_CATEGORIES
};

