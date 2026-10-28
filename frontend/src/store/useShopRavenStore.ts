/**
 * Zustand Global State Store for ShopRaven Control Room Dashboard.
 */

import { create } from 'zustand';

interface ShopRavenState {
  timeframe: string;
  grossRevenuePkr: number;
  netProfitPkr: number;
  rtoRatePct: number;
  activeDrafts: any[];
  discordLogs: any[];
  setTimeframe: (tf: string) => void;
  triggerResearchCycle: () => Promise<void>;
  publishDraft: (id: number) => Promise<void>;
}

export const useShopRavenStore = create<ShopRavenState>((set) => ({
  timeframe: '30d',
  grossRevenuePkr: 450200,
  netProfitPkr: 189450,
  rtoRatePct: 7.7,
  activeDrafts: [
    {
      id: 1042,
      title: 'Ultrasonic Skin Scrubber Pore Cleaner',
      salePrice: 1399,
      regularPrice: 2049,
      wholesaleCost: 850,
      category: 'Beauty & Care',
      supplier: 'HHC Dropshipping',
      status: 'draft'
    },
    {
      id: 1043,
      title: 'Wireless Smart Sensor Car Charger Mount',
      salePrice: 1899,
      regularPrice: 2749,
      wholesaleCost: 1200,
      category: 'Auto & Tools',
      supplier: 'Oshi Dropshipping',
      status: 'draft'
    }
  ],
  discordLogs: [],
  setTimeframe: (tf) => set({ timeframe: tf }),
  triggerResearchCycle: async () => {
    // API call to Python backend
  },
  publishDraft: async (id) => {
    // API call to Orchestrator /api/publish-draft/:id
    set((state) => ({
      activeDrafts: state.activeDrafts.filter((d) => d.id !== id)
    }));
  }
}));

