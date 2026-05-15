import React, { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import apiClient from '../api/client'
import { Settings } from 'lucide-react'

const AdminPage: React.FC = () => {
  const { addNotification } = useStore()
  const [nftName, setNftName] = useState('')
  const [nftDescription, setNftDescription] = useState('')
  const [nftImageUrl, setNftImageUrl] = useState('')
  const [nftRarity, setNftRarity] = useState<'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'>('rare')
  const [nftPrice, setNftPrice] = useState<string>('100')
  const [loading, setLoading] = useState(false)

  const rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']

  const handleAddNFT = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!nftName || !nftDescription || !nftImageUrl || !nftPrice) {
      addNotification('Заполните все поля', 'error')
      return
    }

    setLoading(true)
    try {
      await apiClient.createNFT({
        name: nftName,
        description: nftDescription,
        image_url: nftImageUrl,
        rarity: nftRarity,
        current_price: parseFloat(nftPrice),
      })

      addNotification(`NFT "${nftName}" успешно добавлена! 🎉`, 'success')

      // Reset form
      setNftName('')
      setNftDescription('')
      setNftImageUrl('')
      setNftRarity('rare')
      setNftPrice('100')
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Ошибка при добавлении NFT'
      addNotification(errorMsg, 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <Settings size={32} />
          Админ-панель
        </h1>

        {/* Add NFT Form */}
        <div className="card space-y-6">
          <h2 className="text-2xl font-bold text-gray-800">➕ Добавить новый NFT</h2>

          <form onSubmit={handleAddNFT} className="space-y-4">
            <div>
              <label className="label">Название NFT</label>
              <input
                type="text"
                value={nftName}
                onChange={(e) => setNftName(e.target.value)}
                placeholder="например: Rare Dragon"
                className="input"
              />
            </div>

            <div>
              <label className="label">Описание</label>
              <textarea
                value={nftDescription}
                onChange={(e) => setNftDescription(e.target.value)}
                placeholder="Описание NFT"
                rows={3}
                className="input resize-none"
              />
            </div>

            <div>
              <label className="label">URL изображения</label>
              <input
                type="url"
                value={nftImageUrl}
                onChange={(e) => setNftImageUrl(e.target.value)}
                placeholder="https://example.com/image.jpg"
                className="input"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Рарность</label>
                <select
                  value={nftRarity}
                  onChange={(e) => setNftRarity(e.target.value as any)}
                  className="input"
                >
                  {rarities.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label">Цена (💎)</label>
                <input
                  type="number"
                  value={nftPrice}
                  onChange={(e) => setNftPrice(e.target.value)}
                  placeholder="100"
                  className="input"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full disabled:opacity-50"
            >
              {loading ? 'Добавляю...' : '✅ Добавить NFT'}
            </button>
          </form>
        </div>
      </div>

      {/* Preview */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-6">👁️ Предпросмотр</h2>

        {nftImageUrl ? (
          <div className="card space-y-4">
            <div className="bg-gradient-pink rounded-lg overflow-hidden h-64 flex items-center justify-center">
              <img
                src={nftImageUrl}
                alt="preview"
                className="w-full h-full object-cover"
                onError={(e) => {
                  ;(e.target as HTMLImageElement).src = 'https://via.placeholder.com/300?text=Invalid+Image'
                }}
              />
            </div>

            <div>
              <h3 className="text-xl font-bold text-gray-800">{nftName || 'NFT Name'}</h3>
              <p className="text-sm text-gray-600 mt-2">{nftDescription || 'NFT description'}</p>
            </div>

            <div className="flex justify-between items-center border-t-2 border-pink-200 pt-4">
              <div>
                <p className="text-xs text-gray-500">Рарность</p>
                <p className="font-bold text-pink-600">{nftRarity}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-500">Цена</p>
                <p className="text-2xl font-bold text-pink-600">💎 {nftPrice}</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="card h-96 flex items-center justify-center">
            <div className="text-center text-gray-400">
              <div className="text-6xl mb-4">🎨</div>
              <p>Введите URL изображения для предпросмотра</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminPage
