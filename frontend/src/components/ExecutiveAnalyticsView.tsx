import React from 'react';
import { useShopRavenStore } from '../store/useShopRavenStore';

export function ExecutiveAnalyticsView() {
  const { grossRevenuePkr, netProfitPkr, rtoRatePct } = useShopRavenStore();

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800/60 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400">Total Sales Revenue</div>
          <div className="text-2xl font-bold text-white mt-1">Rs. {grossRevenuePkr.toLocaleString()}</div>
          <div className="text-xs text-emerald-400 mt-1">↑ +18.4% vs last period</div>
        </div>
        <div className="bg-slate-800/60 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400">Realized Net Profit</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">Rs. {netProfitPkr.toLocaleString()}</div>
          <div className="text-xs text-slate-400 mt-1">42.1% net margin</div>
        </div>
        <div className="bg-slate-800/60 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400">RTO Rate</div>
          <div className="text-2xl font-bold text-rose-400 mt-1">{rtoRatePct}%</div>
          <div className="text-xs text-slate-400 mt-1">Waiving Rs. 150 on prepaid</div>
        </div>
        <div className="bg-slate-800/60 border border-slate-700/60 p-4 rounded-xl">
          <div className="text-xs text-slate-400">Active SKUs</div>
          <div className="text-2xl font-bold text-blue-400 mt-1">54 Products</div>
          <div className="text-xs text-slate-400 mt-1">7 Official Categories</div>
        </div>
      </div>

      <div className="bg-slate-800/60 border border-slate-700/60 p-6 rounded-xl">
        <h3 className="font-semibold text-white mb-2">Pakistani City COD Distribution</h3>
        <p className="text-xs text-slate-400 mb-4">Lahore (118 orders), Karachi (94 orders), Islamabad/Rawalpindi (62 orders), Faisalabad (38 orders).</p>
        <div className="w-full bg-slate-700 h-3 rounded-full overflow-hidden flex">
          <div className="bg-blue-500 h-full w-[38%]" title="Lahore: 38%"></div>
          <div className="bg-indigo-500 h-full w-[30%]" title="Karachi: 30%"></div>
          <div className="bg-emerald-500 h-full w-[20%]" title="Islamabad: 20%"></div>
          <div className="bg-amber-500 h-full w-[12%]" title="Other: 12%"></div>
        </div>
      </div>
    </div>
  );
}

