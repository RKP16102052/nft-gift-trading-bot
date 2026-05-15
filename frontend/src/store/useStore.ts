import { create } from 'zustand'
import { User, NFT, Portfolio, Listing } from '../types'

interface Store {
  // User
  user: User | null
  setUser: (user: User | null) => void
  updateBalance: (balance: number) => void

  // Portfolio
  portfolio: Portfolio | null
  setPortfolio: (portfolio: Portfolio | null) => void

  // NFTs
  nfts: NFT[]
  setNFTs: (nfts: NFT[]) => void
  addNFT: (nft: NFT) => void

  // Listings
  listings: Listing[]
  setListings: (listings: Listing[]) => void

  // UI State
  loading: boolean
  setLoading: (loading: boolean) => void
  error: string | null
  setError: (error: string | null) => void

  // Notifications
  notifications: Array<{ id: string; message: string; type: 'success' | 'error' | 'info' }>
  addNotification: (message: string, type: 'success' | 'error' | 'info') => void
  removeNotification: (id: string) => void

  // Clear all
  reset: () => void
}

export const useStore = create<Store>((set) => ({
  // User
  user: null,
  setUser: (user) => set({ user }),
  updateBalance: (balance) => set((state) => ({
    user: state.user ? { ...state.user, balance } : null,
  })),

  // Portfolio
  portfolio: null,
  setPortfolio: (portfolio) => set({ portfolio }),

  // NFTs
  nfts: [],
  setNFTs: (nfts) => set({ nfts }),
  addNFT: (nft) => set((state) => ({ nfts: [...state.nfts, nft] })),

  // Listings
  listings: [],
  setListings: (listings) => set({ listings }),

  // UI
  loading: false,
  setLoading: (loading) => set({ loading }),
  error: null,
  setError: (error) => set({ error }),

  // Notifications
  notifications: [],
  addNotification: (message, type) => set((state) => ({
    notifications: [
      ...state.notifications,
      { id: Date.now().toString(), message, type },
    ],
  })),
  removeNotification: (id) => set((state) => ({
    notifications: state.notifications.filter((n) => n.id !== id),
  })),

  // Reset
  reset: () => set({
    user: null,
    portfolio: null,
    nfts: [],
    listings: [],
    loading: false,
    error: null,
    notifications: [],
  }),
}))
