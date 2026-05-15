import axios, { AxiosInstance } from 'axios'
import { User, NFT, Portfolio, Listing, Transaction, PriceHistory } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 10000,
    })

    // Add WebApp init data to headers
    this.client.interceptors.request.use((config) => {
      const initData = (window as any).Telegram?.WebApp?.initData
      if (initData) {
        config.headers['X-Init-Data'] = initData
      }
      return config
    })
  }

  // NFT endpoints
  async getNFTList(page = 1, perPage = 10, rarity?: string) {
    const response = await this.client.get('/nft/list', {
      params: { page, per_page: perPage, rarity },
    })
    return response.data
  }

  async getNFT(id: number) {
    const response = await this.client.get(`/nft/${id}`)
    return response.data as NFT
  }

  async getPriceHistory(nftId: number, days = 7) {
    const response = await this.client.get(`/nft/${nftId}/price-history`, {
      params: { days },
    })
    return response.data as { nft_id: number; nft_name: string; current_price: number; days: number; history: PriceHistory[] }
  }

  async createNFT(nftData: { name: string; description: string; image_url: string; rarity: string; current_price: number }) {
    const response = await this.client.post('/nft/create', nftData)
    return response.data as NFT
  }

  // User endpoints
  async getCurrentUser() {
    const response = await this.client.get('/user/me')
    return response.data as User
  }

  async getPortfolio() {
    const response = await this.client.get('/user/portfolio')
    return response.data as Portfolio
  }

  async addBalance(amount: number) {
    const response = await this.client.post('/user/add-balance', { amount })
    return response.data as User
  }

  // Market endpoints
  async getListings(page = 1, perPage = 10) {
    const response = await this.client.get('/market/listings', {
      params: { page, per_page: perPage },
    })
    return response.data as { total: number; page: number; per_page: number; total_pages: number; items: Listing[] }
  }

  async sellNFT(nftId: number, price: number, quantity = 1) {
    const response = await this.client.post('/market/sell', { nft_id: nftId, price, quantity })
    return response.data as Listing
  }

  async cancelListing(listingId: number) {
    const response = await this.client.post('/market/cancel', { listing_id: listingId })
    return response.data as { message: string; listing_id: number }
  }

  async buyNFT(listingId: number, quantity = 1) {
    const response = await this.client.post('/market/buy', { listing_id: listingId, quantity })
    return response.data as Transaction
  }

  async getUserOrders(page = 1, perPage = 10) {
    const response = await this.client.get('/market/orders', {
      params: { page, per_page: perPage },
    })
    return response.data as { total: number; page: number; per_page: number; total_pages: number; items: Transaction[] }
  }
}

export default new APIClient()
