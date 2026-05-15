import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import apiClient from '../api/client'
import { NFTCard } from '../components/NFTCard'
import { NFT } from '../types'
import { ArrowRight, TrendingUp, Users, DollarSign } from 'lucide-react'

const HomePage: React.FC = () => {
  const [featuredNFTs, setFeaturedNFTs] = useState<NFT[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadFeatured = async () => {
      try {
        const data = await apiClient.getNFTList(1, 3)
        setFeaturedNFTs(data.items)
      } catch (error) {
        console.error('Failed to load featured NFTs:', error)
      } finally {
        setLoading(false)
      }
    }

    loadFeatured()
  }, [])

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-800 mb-4">
          Торгуйте <span className="text-pink-600">NFT-подарками</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Покупайте, продавайте и отслеживайте движение цен NFT как на настоящей бирже 📊
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link to="/marketplace" className="btn-primary flex items-center gap-2">
            🚀 Начать торговлю
            <ArrowRight size={20} />
          </Link>
          <button className="btn-secondary">📖 Узнать больше</button>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="text-4xl mb-2">🎁</div>
          <p className="text-3xl font-bold text-pink-600">10K+</p>
          <p className="text-gray-600">NFT в каталоге</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-2">👥</div>
          <p className="text-3xl font-bold text-pink-600">5K+</p>
          <p className="text-gray-600">Активных трейдеров</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-2">💰</div>
          <p className="text-3xl font-bold text-pink-600">$1M+</p>
          <p className="text-gray-600">Объём торгов</p>
        </div>
      </section>

      {/* Featured NFTs */}
      <section>
        <h2 className="text-3xl font-bold text-gray-800 mb-6">⭐ Рекомендуемые NFT</h2>
        {loading ? (
          <div className="text-center py-12">Загрузка...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
            {featuredNFTs.map((nft) => (
              <NFTCard key={nft.id} nft={nft} showBuyButton />
            ))}
          </div>
        )}
        <div className="text-center">
          <Link to="/marketplace" className="btn-secondary inline-flex items-center gap-2">
            Посмотреть все NFT
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white rounded-xl p-8 shadow-md">
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">🔄 Как это работает</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="text-5xl mb-4">1️⃣</div>
            <h3 className="font-bold text-lg mb-2">Регистрация</h3>
            <p className="text-gray-600 text-sm">Откройте WebApp в боте Telegram</p>
          </div>
          <div className="text-center">
            <div className="text-5xl mb-4">2️⃣</div>
            <h3 className="font-bold text-lg mb-2">Просмотр</h3>
            <p className="text-gray-600 text-sm">Найдите интересующие вас NFT</p>
          </div>
          <div className="text-center">
            <div className="text-5xl mb-4">3️⃣</div>
            <h3 className="font-bold text-lg mb-2">Торговля</h3>
            <p className="text-gray-600 text-sm">Покупайте и продавайте с прибылью</p>
          </div>
          <div className="text-center">
            <div className="text-5xl mb-4">4️⃣</div>
            <h3 className="font-bold text-lg mb-2">Анализ</h3>
            <p className="text-gray-600 text-sm">Смотрите графики и историю цен</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
