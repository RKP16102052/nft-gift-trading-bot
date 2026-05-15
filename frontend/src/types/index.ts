export interface User {
  id: number
  telegram_id: string
  username?: string
  first_name?: string
  last_name?: string
  balance: number
  created_at: string
  is_admin: boolean
}

export interface NFT {
  id: number
  name: string
  description: string
  image_url: string
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'
  current_price: number
  created_at: string
}

export interface UserNFT {
  id: number
  user_id: number
  nft_id: number
  quantity: number
  acquired_price: number
  acquired_at: string
}

export interface Listing {
  id: number
  nft_id: number
  nft_name: string
  nft_rarity: string
  seller_id: number
  price: number
  quantity: number
  created_at: string
  is_active: boolean
}

export interface Transaction {
  id: number
  user_id: number
  nft_id: number
  transaction_type: 'buy' | 'sell' | 'transfer' | 'reward'
  amount: number
  quantity: number
  price_per_unit: number
  created_at: string
}

export interface PriceHistory {
  id: number
  nft_id: number
  price: number
  timestamp: string
}

export interface Portfolio {
  user_id: number
  balance: number
  total_nfts: number
  portfolio_value: number
  total_value: number
  nfts: PortfolioNFT[]
}

export interface PortfolioNFT {
  nft_id: number
  name: string
  quantity: number
  acquired_price: number
  current_price: number
  value: number
  profit: number
}
