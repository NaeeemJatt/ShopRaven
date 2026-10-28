import React, { useState } from 'react';

export function SupplierPriceSimulatorView() {
  const [wholesale, setWholesale] = useState(850);
  const [competitor, setCompetitor] = useState(1650);

  const floor = wholesale * 1.40;
  const target = wholesale * 1.50;
  const compLanded = competitor + 220; // Rs. 220 competitor courier
  const idealSale = compLanded - 150;
  const rawSale = Math.max(floor, Math.min(idealSale, target));
  const roundedSale = Math.ceil(rawSale / 100) * 100 - 1;
  const regular = Math.ceil((roundedSale + 550) / 100) * 100 - 1;
  const netProfit = roundedSale - wholesale;

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-6 max-w-xl mx-auto space-y-4">
      <h3 className="font-bold text-white text-base">HHC vs. Oshi +40%-50% Landed Price Calculator</h3>
      <div className="space-y-3 text-xs">
        <div>
          <label className="block text-slate-300 mb-1">Wholesale PKR Cost (HHC or Oshi):</label>
          <input
            type="number"
            value={wholesale}
            onChange={(e) => setWholesale(Number(e.target.value) || 0)}
            className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white font-bold"
          />
        </div>
        <div>
          <label className="block text-slate-300 mb-1">Competitor Market Average (PKR):</label>
          <input
            type="number"
            value={competitor}
            onChange={(e) => setCompetitor(Number(e.target.value) || 0)}
            className="w-full bg-slate-900 border border-slate-700 rounded p-2 text-white font-bold"
          />
        </div>
      </div>

      <div className="pt-4 border-t border-slate-700 text-xs space-y-2">
        <div className="flex justify-between">
          <span className="text-slate-400">+40% Minimum Margin Floor:</span>
          <span className="font-semibold text-slate-200">Rs. {Math.round(floor).toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-slate-400">Competitor Doorstep Total (Avg + Rs. 220):</span>
          <span className="font-semibold text-rose-400">Rs. {Math.round(compLanded).toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-sm font-bold pt-2 border-t border-slate-700">
          <span className="text-emerald-400">Recommended Sale Price (*49/*99):</span>
          <span className="text-emerald-400 font-extrabold text-base">Rs. {roundedSale.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-slate-400">
          <span>Strikethrough Regular Price:</span>
          <span className="line-through">Rs. {regular.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-emerald-300 font-semibold">
          <span>Realized Net Profit per Order:</span>
          <span>+Rs. {netProfit.toLocaleString()} (+{((netProfit / wholesale) * 100).toFixed(1)}%)</span>
        </div>
      </div>
    </div>
  );
}

