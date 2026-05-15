import React, { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import apiClient from '../api/client'
import { NFTCard } from '../components/NFTCard'
import { Listing } from '../types'
import { ShoppingBag } from 'lucide-react'

const MarketplacePage: React.FC = () => {
  const { user, addNotification } = useStore()
  const [listings, setListings] = useState<Listing[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [selectedRarity, setSelectedRarity] = useState<string | null>(null)

  const rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']
  const rarityEmojis = {
    common: '🟢',
    uncommon: '🔵',
    rare: '🟣',
    epic: '🟡',
    legendary: '🔴',
  }

  useEffect(() => {
    loadListings()
  }, [page, selectedRarity])

  const loadListings = async () => {
    setLoading(true)
    try {
      const data = await apiClient.getListings(page, 12)
      let items = data.items

      if (selectedRarity) {
        items = items.filter((l) => l.nft_rarity === selectedRarity)
      }

      setListings(items)
      setTotalPages(data.total_pages)
    } catch (error) {
      console.error('Failed to load listings:', error)
      addNotification('Ошибка при загрузке маркетплейса', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleBuy = async (listing: Listing) => {
    if (!user) {
      addNotification('Пожалуйста, авторизуйтесь', 'error')
      return
    }

    try {
      await apiClient.buyNFT(listing.id, 1)
      addNotification(`Вы купили ${listing.nft_name}! 🎉`, 'success')
      loadListings()
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Ошибка при покупке'
      addNotification(errorMsg, 'error')
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">🏪 Маркетплейс NFT</h1>
        <p className="text-gray-600">Найдите лучшие NFT для вашего портфеля</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => {
            setSelectedRarity(null)
            setPage(1)
          }}
          className={`btn ${
            selectedRarity === null ? 'btn-primary' : 'btn-secondary'
          }`}
        >
          Все
        </button>
        {rarities.map((rarity) => (
          <button
            key={rarity}
            onClick={() => {
              setSelectedRarity(rarity)
              setPage(1)
            }}
            className={`btn ${
              selectedRarity === rarity ? 'btn-primary' : 'btn-secondary'
            }`}
          >
            {rarityEmojis[rarity as keyof typeof rarityEmojis]} {rarity}
          </button>
        ))}
      </div>

      {/* Listings Grid */}
      {loading ? (
        <div className="text-center py-12">Загрузка...</div>
      ) : listings.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {listings.map((listing) => (
              <div
                key={listing.id}
                className="card-interactive group"
              >
                <div className="relative mb-4 overflow-hidden rounded-lg bg-gradient-pink h-48">
                  <div className="w-full h-full flex items-center justify-center text-6xl">
                    🎁
                  </div>
                </div>

                <h3 className="text-lg font-bold text-gray-800 mb-2">{listing.nft_name}</h3>
                <p className="text-sm text-gray-600 mb-3">Кол-во: {listing.quantity}</p>

                <div className="mb-4">
                  <p className="text-xs text-gray-500">Цена</p>
                  <p className="text-2xl font-bold text-pink-600">💎 {listing.price}</p>
                </div>

                <button
                  onClick={() => handleBuy(listing)}
                  className="btn-primary w-full flex items-center justify-center gap-2"
                >
                  <ShoppingBag size={18} />
                  Купить
                </button>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="flex justify-center gap-2 mt-8">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="btn-secondary disabled:opacity-50"
            >
              ← Назад
            </button>
            <span className="flex items-center px-4 py-2 text-gray-600">
              Страница {page} из {totalPages}
            </span>
            <button
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page === totalPages}
              className="btn-secondary disabled:opacity-50"
            >
              Далее →
            </button>
          </div>
        </>
      ) : (
        <div className="text-center py-12">
          <p className="text-xl text-gray-600">Маркетплейс пуст</p>
        </div>
      )}
    </div>
  )
}

export default MarketplacePage
