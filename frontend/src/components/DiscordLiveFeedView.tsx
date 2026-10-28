import React from 'react';

export function DiscordLiveFeedView() {
  const events = [
    { type: 'MARKET_RESEARCH', text: 'Discovered 4 new high-growth keywords across Beauty & Care and Auto & Tools.', color: 'border-purple-500 text-purple-400' },
    { type: 'CATALOG_GAP_CHECK', text: 'Identified "Wireless Smart Sensor Car Charger Mount" missing on nnstore.shop.', color: 'border-blue-500 text-blue-400' },
    { type: 'SUPPLIER_CHECK', text: 'HHC (Rs. 850) vs Oshi (Rs. 820) -> Selected winner: Oshi Dropshipping.', color: 'border-amber-500 text-amber-400' },
    { type: 'PRICE_RESEARCH', text: 'Calculated Landed COD Price: Rs. 1,899 (+58% profit, beats competitor landed).', color: 'border-emerald-500 text-emerald-400' },
    { type: 'WOOCOMMERCE_DRAFT', text: 'Created Draft #1043 on nnstore.shop. Use /publish 1043 on Discord to publish!', color: 'border-green-500 text-green-400' }
  ];

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-white text-base">Live Discord Webhook Stream (#shopraven-alerts)</h3>
        <span className="text-xs text-slate-500 font-mono">Channel ID: 1234567890</span>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {events.map((e, idx) => (
          <div key={idx} className={`p-3 rounded bg-slate-900 border-l-4 ${e.color}`}>
            <span className="font-bold">[{e.type}]</span> {e.text}
          </div>
        ))}
      </div>
    </div>
  );
}

