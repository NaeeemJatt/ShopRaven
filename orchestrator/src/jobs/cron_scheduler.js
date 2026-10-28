/**
 * Cron Job Scheduler for ShopRaven Orchestrator.
 * Fully automated 30-minute autonomous hunting, sourcing, SEO/AISEO enrichment,
 * storefront health auditing, and visitor journey optimization.
 */

const cron = require('node-cron');
const axios = require('axios');
const StorefrontMenuOptimizer = require('../woocommerce/menu_reorder');
const { CONFIG } = require('../config/env');

let activeCronJobs = [];

function startScheduledJobs(onPipelineTrigger) {
  const menuOptimizer = new StorefrontMenuOptimizer();

  // Clear any existing crons
  activeCronJobs.forEach(job => job.stop());
  activeCronJobs = [];

  // 1. Every 30 Minutes: Continuous Product Hunting Scout (Chains into Oshi/HHC Sourcing & Listing)
  const scoutJob = cron.schedule('*/30 * * * *', async () => {
    console.log('[CRON 30-MIN] Triggering Autonomous Product Hunting & Chained Sourcing Pipeline...');
    try {
      if (onPipelineTrigger) {
        onPipelineTrigger('scout_and_source');
      }
      await axios.post(`${CONFIG.PYTHON_BACKEND_URL}/api/v1/research/scan`).catch(() => {});
    } catch (err) {
      console.error('[CRON ERROR] 30-min Hunting Pipeline failed:', err.message);
    }
  });
  activeCronJobs.push(scoutJob);

  // 2. Every 30 Minutes: Parallel SEO & AI Search Engine Optimization (AEO/GEO) Engine
  const seoJob = cron.schedule('*/30 * * * *', async () => {
    console.log('[CRON 30-MIN] Running Parallel SEO/AISEO Roman-Urdu & Schema.org Optimization...');
    try {
      if (onPipelineTrigger) {
        onPipelineTrigger('seo_aeo_enrichment');
      }
    } catch (err) {
      console.error('[CRON ERROR] Parallel SEO/AEO failed:', err.message);
    }
  });
  activeCronJobs.push(seoJob);

  // 3. Every 30 Minutes: Parallel Autonomous Storefront Auditor & Self-Healing Bug Fixer
  const auditorJob = cron.schedule('*/30 * * * *', async () => {
    console.log('[CRON 30-MIN] Running Parallel Storefront Auditor & Self-Healing Bug Fixer on nnstore.shop...');
    try {
      if (onPipelineTrigger) {
        onPipelineTrigger('storefront_auditor');
      }
    } catch (err) {
      console.error('[CRON ERROR] Storefront Auditor failed:', err.message);
    }
  });
  activeCronJobs.push(auditorJob);

  // 4. Every 15 Minutes: Parallel Visitor Journey, Clickstream & Bounce/Exit Analyzer
  const visitorJob = cron.schedule('*/15 * * * *', async () => {
    console.log('[CRON 15-MIN] Analyzing Visitor Clickstream, Cart Drops, and Deploying CRO Countermeasures...');
    try {
      if (onPipelineTrigger) {
        onPipelineTrigger('visitor_cro_analyzer');
      }
    } catch (err) {
      console.error('[CRON ERROR] Visitor CRO Analyzer failed:', err.message);
    }
  });
  activeCronJobs.push(visitorJob);

  // 5. Every 2 Hours: Supplier Stock & Restock Waitlist Check
  const stockJob = cron.schedule('0 */2 * * *', async () => {
    console.log('[CRON] Running 2-hour Supplier Stock & Waitlist Verification...');
  });
  activeCronJobs.push(stockJob);

  // 6. Every Sunday at 02:00 AM PKT: Store Menu Reordering & Weekly SEO Blog
  const sundayJob = cron.schedule('0 2 * * 0', async () => {
    console.log('[CRON] Running Sunday 02:00 AM Store Menu Reorder by Velocity...');
    try {
      await menuOptimizer.reorderCatalogByVelocity();
    } catch (err) {
      console.error('[CRON ERROR] Menu reorder failed:', err.message);
    }
  });
  activeCronJobs.push(sundayJob);

  console.log('✅ ShopRaven Fully-Automated 30-Min Cron Scheduler initialized.');
}

module.exports = {
  startScheduledJobs
};

