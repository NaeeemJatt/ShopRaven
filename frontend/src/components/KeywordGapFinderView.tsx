import React from 'react';

export function KeywordGapFinderView() {
  const items = [
    { keyword: 'Ultrasonic Skin Scrubber', category: 'Beauty & Care', searches: '3,400', inStore: true },
    { keyword: 'Electric Vegetable Cutter 4 in 1', category: 'Kitchen Accessories', searches: '2,850', inStore: true },
    { keyword: 'Wireless Smart Sensor Car Charger', category: 'Auto & Tools', searches: '4,100', inStore: false },
    { keyword: 'Rechargeable Lint Remover Shaver', category: 'Home & Living', searches: '1,950', inStore: false },
  ];

  return (
    <div className="bg-slate-800/60 border border-slate-700/60 rounded-xl p-6">
      <h3 className="font-bold text-white mb-4">Trending Search Demand & Catalog Gaps</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-slate-700 text-slate-400 font-semibold text-xs">
            <tr>
              <th className="py-2">Keyword</th>
              <th className="py-2">Category</th>
              <th className="py-2">Monthly Searches</th>
              <th className="py-2">Status</th>
              <th className="py-2 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700 text-xs">
            {items.map((i, idx) => (
              <tr key={idx}>
                <td className="py-3 font-medium text-white">{i.keyword}</td>
                <td className="py-3 text-slate-300">{i.category}</td>
                <td className="py-3 text-slate-300">{i.searches}</td>
                <td className="py-3">
                  {i.inStore ? (
                    <span className="text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">In Store</span>
                  ) : (
                    <span className="text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">Missing Opportunity</span>
                  )}
                </td>
                <td className="py-3 text-right">
                  {!i.inStore ? (
                    <button className="px-2 py-1 bg-purple-600 text-white rounded font-medium hover:bg-purple-500">Auto-Import</button>
                  ) : (
                    <button className="text-blue-400 hover:underline">Refresh Tags</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

