import React from 'react';
import { useShopRavenStore } from '../store/useShopRavenStore';

export function SEOAEOQueueView() {
  const { activeDrafts, publishDraft } = useShopRavenStore();

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-white text-base">WooCommerce Drafts Queue (nnstore.shop)</h3>
        <span className="text-xs text-slate-400">{activeDrafts.length} drafts pending review</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {activeDrafts.map((d) => (
          <div key={d.id} className="bg-slate-800/60 border border-slate-700/60 p-4 rounded-xl space-y-3 text-xs">
            <div className="flex justify-between">
              <span className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-bold">DRAFT #{d.id}</span>
              <span className="text-slate-400">{d.supplier}</span>
            </div>
            <h4 className="font-bold text-white text-sm">{d.title}</h4>
            <div className="flex justify-between">
              <span>Sale: <strong className="text-emerald-400">Rs. {d.salePrice}</strong></span>
              <span>Regular: <span className="line-through text-slate-400">Rs. {d.regularPrice}</span></span>
              <span>Cost: <span className="text-slate-300">Rs. {d.wholesaleCost}</span></span>
            </div>
            <div className="pt-2 border-t border-slate-700 flex space-x-2">
              <button
                onClick={() => publishDraft(d.id)}
                className="flex-1 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded font-semibold text-center"
              >
                1-Click Publish Live
              </button>
              <a
                href={`https://nnstore.shop/wp-admin/post.php?post=${d.id}&action=edit`}
                target="_blank"
                rel="noreferrer"
                className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded font-medium text-center"
              >
                Edit Draft
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

