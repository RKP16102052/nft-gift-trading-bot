import React, { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import apiClient from '../api/client'
import { PriceChart } from '../components/PriceChart'
import { Portfolio, PortfolioNFT, PriceHistory } from '../types'
import { TrendingUp, TrendingDown } from 'lucide-react'

const PortfolioPage: React.FC = () => {
  const { user, addNotification, setPortfolio } = useStore()
  const [portfolio, setLocalPortfolio] = useState<Portfolio | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedNFT, setSelectedNFT] = useState<PortfolioNFT | null>(null)
  const [priceHistory, setPriceHistory] = useState<PriceHistory[]>([])
  const [sellPrice, setSellPrice] = useState<string>('')
  const [sellQuantity, setSellQuantity] = useState<string>('1')
  const [selling, setSelling] = useState(false)

  useEffect(() => {
    loadPortfolio()
  }, [])

  const loadPortfolio = async () => {
    setLoading(true)
    try {
      const data = await apiClient.getPortfolio()
      setLocalPortfolio(data)
      setPortfolio(data)
    } catch (error) {
      console.error('Failed to load portfolio:', error)
      addNotification('Ошибка при загрузке портфеля', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleSelectNFT = async (nft: PortfolioNFT) => {
    setSelectedNFT(nft)
    try {
      const data = await apiClient.getPriceHistory(nft.nft_id, 30)
      setPriceHistory(data.history)
    } catch (error) {
      console.error('Failed to load price history:', error)
    }
  }

  const handleSellNFT = async () => {
    if (!selectedNFT || !sellPrice || !sellQuantity) {
      addNotification('Заполните все поля', 'error')
      return
    }

    setSelling(true)
    try {
      const price = parseFloat(sellPrice)
      const quantity = parseInt(sellQuantity)

      if (quantity > selectedNFT.quantity) {
        addNotification('Недостаточное количество NFT', 'error')
        setSelling(false)
        return
      }

      await apiClient.sellNFT(selectedNFT.nft_id, price, quantity)
      addNotification(`Вы выставили ${selectedNFT.name} на продажу! 🎉`, 'success')

      setSellPrice('')
      setSellQuantity('1')
      setSelectedNFT(null)
      await loadPortfolio()
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Ошибка при выставлении на продажу'
      addNotification(errorMsg, 'error')
    } finally {
      setSelling(false)
    }
  }

  if (loading) return <div className="text-center py-12">Загрузка портфеля...</div>
  if (!portfolio) return <div className="text-center py-12">Портфель не найден</div>

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Column - Stats */}
      <div className="lg:col-span-1 space-y-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📊 Мой портфель</h1>

        {/* Stats Cards */}
        <div className="card">
          <p className="text-sm text-gray-600">Баланс</p>
          <p className="text-3xl font-bold text-pink-600">💎 {portfolio.balance.toFixed(0)}</p>
        </div>

        <div className="card">
          <p className="text-sm text-gray-600">Стоимость портфеля</p>
          <p className="text-3xl font-bold text-blue-600">${portfolio.portfolio_value.toFixed(0)}</p>
        </div>

        <div className="card">
          <p className="text-sm text-gray-600">Общая стоимость</p>
          <p className="text-3xl font-bold text-green-600">${portfolio.total_value.toFixed(0)}</p>
        </div>

        <div className="card">
          <p className="text-sm text-gray-600">NFT в портфеле</p>
          <p className="text-3xl font-bold">{portfolio.total_nfts}</p>
        </div>

        {/* NFT List */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <h3 className="font-bold p-4 border-b-2 border-pink-200">Мои NFT</h3>
          <div className="max-h-96 overflow-y-auto">
            {portfolio.nfts.map((nft) => (
              <button
                key={nft.nft_id}
                onClick={() => handleSelectNFT(nft)}
                className={`w-full text-left p-3 border-b hover:bg-pink-50 transition ${
                  selectedNFT?.nft_id === nft.nft_id ? 'bg-pink-100' : ''
                }`}
              >
                <p className="font-semibold text-gray-800">{nft.name}</p>
                <p className="text-xs text-gray-600">Кол-во: {nft.quantity}</p>
                <p className="text-xs font-bold text-pink-600">💎 {nft.current_price}</p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Right Column - Chart & Sell Form */}
      <div className="lg:col-span-2 space-y-6">
        {selectedNFT && (
          <>
            {/* Chart */}
            {priceHistory.length > 0 && (
              <PriceChart history={priceHistory} nftName={selectedNFT.name} />
            )}

            {/* Sell Form */}
            <div className="card space-y-4">
              <h3 className="text-xl font-bold text-gray-800">🛍️ Выставить на продажу</h3>

              <div>
                <label className="label">Название</label>
                <input
                  type="text"
                  value={selectedNFT.name}
                  disabled
                  className="input bg-gray-100 cursor-not-allowed"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Текущая цена</label>
                  <input
                    type="number"
                    value={selectedNFT.current_price}
                    disabled
                    className="input bg-gray-100 cursor-not-allowed"
                  />
                </div>
                <div>
                  <label className="label">Ваша цена</label>
                  <input
                    type="number"
                    value={sellPrice}
                    onChange={(e) => setSellPrice(e.target.value)}
                    placeholder="Введите цену"
                    className="input"
                  />
                </div>
              </div>

              <div>
                <label className="label">Количество</label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    min="1"
                    max={selectedNFT.quantity}
                    value={sellQuantity}
                    onChange={(e) => setSellQuantity(e.target.value)}
                    className="input"
                  />
                  <span className="flex items-center px-4 bg-gray-100 rounded-lg text-gray-700">
                    макс: {selectedNFT.quantity}
                  </span>
                </div>
              </div>

              <div className="bg-pink-50 p-3 rounded-lg">
                <p className="text-sm text-gray-600">Вы получите</p>
                <p className="text-2xl font-bold text-pink-600">
                  💎 {(parseFloat(sellPrice || '0') * parseInt(sellQuantity || '1')).toFixed(0)}
                </p>
              </div>

              <button
                onClick={handleSellNFT}
                disabled={selling}
                className="btn-primary w-full disabled:opacity-50"
              >
                {selling ? 'Выставляю...' : '✅ Выставить на продажу'}
              </button>
            </div>

            {/* NFT Stats */}
            <div className="card space-y-3">
              <h3 className="font-bold text-gray-800">📈 Статистика</h3>
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Куплено по цене</span>
                  <span className="font-semibold">💎 {selectedNFT.acquired_price}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Текущая цена</span>
                  <span className="font-semibold text-blue-600">💎 {selectedNFT.current_price}</span>
                </div>
                <div className="flex justify-between items-center border-t-2 border-pink-200 pt-2">
                  <span className="text-gray-600">Прибыль за штуку</span>
                  <span className={`font-bold flex items-center gap-1 ${
                    selectedNFT.profit > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {selectedNFT.profit > 0 ? <TrendingUp size={20} /> : <TrendingDown size={20} />}
                    {selectedNFT.profit > 0 ? '+' : ''}{(selectedNFT.profit / selectedNFT.quantity).toFixed(0)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Общая прибыль</span>
                  <span className={`font-bold text-lg ${
                    selectedNFT.profit > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {selectedNFT.profit > 0 ? '+' : ''}{selectedNFT.profit.toFixed(0)}
                  </span>
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default PortfolioPage
