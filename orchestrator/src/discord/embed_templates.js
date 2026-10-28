/**
 * Discord Rich Embed template builders for ShopRaven.
 */

function buildDraftCreatedEmbed(draftData) {
  const { id, title, salePrice, regularPrice, wholesaleCost, netProfit, marginPct, category, supplier } = draftData;

  return {
    title: `✨ New WooCommerce Draft Created: ${title}`,
    description: `ShopRaven has automated the complete sourcing, landed pricing, and SEO/AEO metadata for **nnstore.shop**.`,
    color: 0x22C55E, // Green
    fields: [
      { name: 'Category', value: category || 'General', inline: true },
      { name: 'Supplier', value: supplier || 'HHC / Oshi', inline: true },
      { name: 'Wholesale Cost', value: `PKR ${wholesaleCost}`, inline: true },
      { name: 'Sale Price (PKR)', value: `Rs. ${salePrice} (ends in *49/*99)`, inline: true },
      { name: 'Regular Price', value: `~~Rs. ${regularPrice}~~`, inline: true },
      { name: 'Net Take-Home Profit', value: `+PKR ${netProfit} (${marginPct}%)`, inline: true },
      { name: 'Doorstep Courier Math', value: `NN Store Landed: Rs. ${Number(salePrice) + 150} vs. Competitor Landed`, inline: false },
      { name: '1-Click Action', value: `Use \`/publish ${id}\` or edit directly in WordPress: [Edit Draft](https://nnstore.shop/wp-admin/post.php?post=${id}&action=edit)`, inline: false }
    ],
    footer: {
      text: 'ShopRaven AI Cofounder • nnstore.shop'
    },
    timestamp: new Date().toISOString()
  };
}

function buildMonthlyReportEmbed(pnlData) {
  return {
    title: `📊 Monthly Executive Digest — ${pnlData.month || 'October 2026'}`,
    description: `Realized Financial Performance & Delivery Accounting for **nnstore.shop**`,
    color: 0x8B5CF6, // Purple
    fields: [
      { name: 'Gross Revenue', value: `PKR ${pnlData.gross_revenue_pkr}`, inline: true },
      { name: 'Realized Net Profit', value: `PKR ${pnlData.true_net_take_home_pkr}`, inline: true },
      { name: 'Blended Margin', value: `${pnlData.blended_net_margin_pct}%`, inline: true },
      { name: 'Total Orders', value: String(pnlData.total_orders), inline: true },
      { name: 'Delivered', value: String(pnlData.delivered_orders), inline: true },
      { name: 'RTO Rate', value: `${pnlData.rto_rate_pct}%`, inline: true }
    ],
    footer: {
      text: 'ShopRaven Executive Reporting'
    },
    timestamp: new Date().toISOString()
  };
}

module.exports = {
  buildDraftCreatedEmbed,
  buildMonthlyReportEmbed
};

