import React, { useState } from 'react';

export function AdPlannerAndCreativeView() {
  const [budget, setBudget] = useState(2500);
  const [targetOrders, setTargetOrders] = useState(15);
  const [selectedTheme, setSelectedTheme] = useState('ramzan');
  const [adPlan, setAdPlan] = useState<any>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [creativeOutput, setCreativeOutput] = useState<any>(null);

  const calculateBreakevenROAS = (sale: number, cost: number, rto: number = 0.15) => {
    const net = sale - cost - (rto * 250);
    return net > 0 ? (sale / net).toFixed(2) : '99.00';
  };

  const handleGenerateAdPlan = () => {
    setIsGenerating(true);
    setTimeout(() => {
      const beRoas = calculateBreakevenROAS(1399, 780);
      setAdPlan({
        campaign: 'ShopRaven_AdvantagePlus_SkinScrubber',
        budget: budget,
        targetOrders: targetOrders,
        beRoas: beRoas,
        scaleRoas: (parseFloat(beRoas) * 1.35).toFixed(2),
        maxCpp: Math.round((1399 - 780 - 37.5) * 0.70),
        cities: ['Karachi', 'Lahore', 'Islamabad/Rawalpindi', 'Faisalabad', 'Multan', 'Peshawar'],
        hooks: [
          '⚡ "Abhi Mangwaein Aur Parcel Khol Kar Tasalli Karein!" — 100% Cash-on-Delivery',
          '🇵🇰 Salon jesa glow ab ghar bethe! Flat Rs. 150 shipping across Pakistan',
          '🔥 Pakistan ki No.1 Trending Deal! Limited Stock available at Rs. 1,399'
        ],
        rules: [
          'Day 1-2: Broad CBO Testing with 3 Creatives',
          'Day 3: KILL ad sets with CPP > Max Acceptable CPP after 48h',
          'Day 6: SCALE budget +20% on ad sets with ROAS > Target'
        ]
      });
      setIsGenerating(false);
    }, 600);
  };

  const handleGenerateCreatives = () => {
    setCreativeOutput({
      theme: selectedTheme,
      carouselSlides: 5,
      bannerUrl: 'temp_studio_output/banners/skin_scrubber_banner.jpg',
      format: '1080x1080 Square + 9:16 Vertical Reel',
      status: 'Ready to Publish to Meta Ads'
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">📢 7-Day Meta Ad Planner & Creative Studio</h2>
          <p className="text-sm text-slate-400">Alippo Features #14 & #15: Automated Pakistani ROAS math, Ad Hooks, Festival Banners & Heatmaps.</p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
          Growth Suite Active
        </span>
      </div>

      {/* Grid: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Left Column: 7-Day Meta Ad Campaign Planner */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-bold text-white flex items-center space-x-2">
            <span>🎯</span>
            <span>Meta Ad Budget & Target Planner</span>
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 block mb-1">Daily Budget (PKR)</label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 outline-none"
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 block mb-1">Target Daily Orders</label>
              <input
                type="number"
                value={targetOrders}
                onChange={(e) => setTargetOrders(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 outline-none"
              />
            </div>
          </div>

          <button
            onClick={handleGenerateAdPlan}
            disabled={isGenerating}
            className="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-lg transition shadow-md shadow-blue-600/30 flex items-center justify-center space-x-2"
          >
            <span>⚡</span>
            <span>{isGenerating ? 'Computing Mathematical Model...' : 'Generate 7-Day Meta Strategy'}</span>
          </button>

          {adPlan && (
            <div className="bg-slate-950 border border-slate-800/80 rounded-lg p-4 space-y-3 text-xs">
              <div className="grid grid-cols-3 gap-2 text-center">
                <div className="bg-slate-900 p-2 rounded border border-slate-800">
                  <span className="text-slate-400 block">Break-Even ROAS</span>
                  <strong className="text-amber-400 text-sm">{adPlan.beRoas}x</strong>
                </div>
                <div className="bg-slate-900 p-2 rounded border border-slate-800">
                  <span className="text-slate-400 block">Target Scale ROAS</span>
                  <strong className="text-emerald-400 text-sm">{adPlan.scaleRoas}x</strong>
                </div>
                <div className="bg-slate-900 p-2 rounded border border-slate-800">
                  <span className="text-slate-400 block">Max Cost/Purchase</span>
                  <strong className="text-blue-400 text-sm">Rs. {adPlan.maxCpp}</strong>
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-bold block mb-1">Top Pakistani City Cluster:</span>
                <div className="flex flex-wrap gap-1.5">
                  {adPlan.cities.map((c: string) => (
                    <span key={c} className="px-2 py-0.5 bg-slate-800 text-slate-300 rounded text-[11px] border border-slate-700">
                      {c}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-slate-400 font-bold block mb-1">High-Conversion Urdu Hooks:</span>
                <ul className="space-y-1 text-slate-300">
                  {adPlan.hooks.map((h: string, idx: number) => (
                    <li key={idx} className="flex items-start space-x-1.5">
                      <span className="text-emerald-400">✓</span>
                      <span>{h}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Festival Creative & Banner Maker */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-bold text-white flex items-center space-x-2">
            <span>🎨</span>
            <span>Festival Sale Banner & Carousel Studio</span>
          </h3>

          <div>
            <label className="text-xs text-slate-400 block mb-1">Campaign Festival Theme</label>
            <select
              value={selectedTheme}
              onChange={(e) => setSelectedTheme(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 outline-none"
            >
              <option value="ramzan">🌙 Ramzan Mubarak Mega Sale</option>
              <option value="eid">✨ Eid-ul-Fitr Special Deals</option>
              <option value="azadi">🇵🇰 14 August Azadi Mubarak</option>
              <option value="11_11">⚡ 11.11 Mega Shopping Festival</option>
              <option value="blessed_friday">🕌 Blessed Friday Mega Savings</option>
            </select>
          </div>

          <button
            onClick={handleGenerateCreatives}
            className="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg transition shadow-md shadow-emerald-600/30 flex items-center justify-center space-x-2"
          >
            <span>🖼️</span>
            <span>Render 5-Slide Carousel & Festival Banner</span>
          </button>

          {creativeOutput && (
            <div className="bg-slate-950 border border-slate-800/80 rounded-lg p-4 space-y-2 text-xs">
              <div className="flex justify-between items-center text-emerald-400 font-bold">
                <span>✓ Creatives Generated Successfully</span>
                <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">1080x1080 Standard</span>
              </div>
              <p className="text-slate-300">
                Generated 5-slide Hook-to-Offer carousel for Meta feed + high-contrast festival promotional creative with strikethrough pricing.
              </p>
              <div className="bg-slate-900 p-2.5 rounded border border-slate-800 font-mono text-[11px] text-slate-400">
                Output: 5 JPEG Slides + Strikethrough Festival Hero Graphic
              </div>
            </div>
          )}

          {/* Heatmap & Speed Optimizer Widget Preview */}
          <div className="border-t border-slate-800 pt-4 space-y-2">
            <span className="text-xs font-bold text-slate-400 flex items-center space-x-1.5">
              <span>🔥</span>
              <span>Storefront Behavior Heatmap & Speed (Alippo #21)</span>
            </span>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="bg-slate-800/60 p-2.5 rounded border border-slate-700/50">
                <span className="text-slate-400 block text-[11px]">Average Scroll Depth</span>
                <strong className="text-white text-sm">74.2% (Passed 50% fold)</strong>
              </div>
              <div className="bg-slate-800/60 p-2.5 rounded border border-slate-700/50">
                <span className="text-slate-400 block text-[11px]">Primary CTA Clicks</span>
                <strong className="text-emerald-400 text-sm">82% COD / 18% WhatsApp</strong>
              </div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

