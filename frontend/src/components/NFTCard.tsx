import React from 'react'
import { NFT } from '../types'
import { ShoppingBag, TrendingUp } from 'lucide-react'

interface NFTCardProps {
  nft: NFT
  onBuy?: () => void
  onSell?: () => void
  showBuyButton?: boolean
  showSellButton?: boolean
}

const rarityConfig = {
  common: { emoji: '🟢', color: 'text-green-600', bg: 'bg-green-100' },
  uncommon: { emoji: '🔵', color: 'text-blue-600', bg: 'bg-blue-100' },
  rare: { emoji: '🟣', color: 'text-purple-600', bg: 'bg-purple-100' },
  epic: { emoji: '🟡', color: 'text-yellow-600', bg: 'bg-yellow-100' },
  legendary: { emoji: '🔴', color: 'text-red-600', bg: 'bg-red-100' },
}

export const NFTCard: React.FC<NFTCardProps> = ({
  nft,
  onBuy,
  onSell,
  showBuyButton = false,
  showSellButton = false,
}) => {
  const rarity = rarityConfig[nft.rarity as keyof typeof rarityConfig]

  return (
    <div className="card-interactive group">
      {/* Image */}
      <div className="relative mb-4 overflow-hidden rounded-lg bg-gradient-pink h-48">
        <img
          src={nft.image_url}
          alt={nft.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform"
        />
        <div className={`absolute top-2 right-2 ${rarity.bg} ${rarity.color} badge`}>
          {rarity.emoji} {nft.rarity}
        </div>
      </div>

      {/* Content */}
      <h3 className="text-lg font-bold text-gray-800 mb-2">{nft.name}</h3>
      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{nft.description}</p>

      {/* Price */}
      <div className="mb-4">
        <p className="text-xs text-gray-500">Текущая цена</p>
        <p className="text-2xl font-bold text-pink-600">💎 {nft.current_price}</p>
      </div>

      {/* Buttons */}
      <div className="flex gap-2">
        {showBuyButton && (
          <button
            onClick={onBuy}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            <ShoppingBag size={18} />
            Купить
          </button>
        )}
        {showSellButton && (
          <button
            onClick={onSell}
            className="btn-secondary flex-1 flex items-center justify-center gap-2"
          >
            <TrendingUp size={18} />
            Продать
          </button>
        )}
      </div>
    </div>
  )
}
