import React, { useState } from 'react';
import { useShopRavenStore } from './store/useShopRavenStore';
import { ExecutiveAnalyticsView } from './components/ExecutiveAnalyticsView';
import { KeywordGapFinderView } from './components/KeywordGapFinderView';
import { SupplierPriceSimulatorView } from './components/SupplierPriceSimulatorView';
import { SEOAEOQueueView } from './components/SEOAEOQueueView';
import { DiscordLiveFeedView } from './components/DiscordLiveFeedView';

export default function App() {
  const [activeTab, setActiveTab] = useState<'analytics' | 'gap-finder' | 'price-sim' | 'drafts' | 'discord'>('analytics');

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      <header className="border-b border-slate-800 bg-slate-950/80 px-6 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">🦅</span>
          <div>
            <h1 className="font-bold text-lg text-white">ShopRaven Control Room</h1>
            <p className="text-xs text-blue-400">Autonomous AI Cofounder • nnstore.shop</p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('analytics')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${activeTab === 'analytics' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            Analytics
          </button>
          <button
            onClick={() => setActiveTab('gap-finder')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${activeTab === 'gap-finder' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            Market Gap
          </button>
          <button
            onClick={() => setActiveTab('price-sim')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${activeTab === 'price-sim' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            Pricing Simulator
          </button>
          <button
            onClick={() => setActiveTab('drafts')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${activeTab === 'drafts' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            Drafts Queue
          </button>
          <button
            onClick={() => setActiveTab('discord')}
            className={`px-3 py-1.5 rounded-md text-sm font-medium ${activeTab === 'discord' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            Discord Feed
          </button>
        </div>
      </header>

      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        {activeTab === 'analytics' && <ExecutiveAnalyticsView />}
        {activeTab === 'gap-finder' && <KeywordGapFinderView />}
        {activeTab === 'price-sim' && <SupplierPriceSimulatorView />}
        {activeTab === 'drafts' && <SEOAEOQueueView />}
        {activeTab === 'discord' && <DiscordLiveFeedView />}
      </main>
    </div>
  );
}

