import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useStore } from '../store/useStore'
import { Gift, Home, ShoppingBag, Briefcase, Settings } from 'lucide-react'

export const Navbar: React.FC = () => {
  const { user } = useStore()
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="bg-white shadow-md border-b-2 border-pink-200 sticky top-0 z-40">
      <div className="container flex items-center justify-between py-4">
        <Link to="/" className="flex items-center gap-2">
          <Gift className="text-pink-500" size={28} />
          <span className="text-2xl font-bold text-pink-600">NFT Trading</span>
        </Link>

        <div className="flex items-center gap-6">
          <Link
            to="/"
            className={`flex items-center gap-1 px-3 py-2 rounded-lg transition ${
              isActive('/') ? 'bg-pink-100 text-pink-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Home size={20} />
            <span className="hidden sm:inline">Главная</span>
          </Link>

          <Link
            to="/marketplace"
            className={`flex items-center gap-1 px-3 py-2 rounded-lg transition ${
              isActive('/marketplace') ? 'bg-pink-100 text-pink-600' : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <ShoppingBag size={20} />
            <span className="hidden sm:inline">Маркетплейс</span>
          </Link>

          {user && (
            <Link
              to="/portfolio"
              className={`flex items-center gap-1 px-3 py-2 rounded-lg transition ${
                isActive('/portfolio') ? 'bg-pink-100 text-pink-600' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Briefcase size={20} />
              <span className="hidden sm:inline">Портфель</span>
            </Link>
          )}

          {user?.is_admin && (
            <Link
              to="/admin"
              className={`flex items-center gap-1 px-3 py-2 rounded-lg transition ${
                isActive('/admin') ? 'bg-pink-100 text-pink-600' : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Settings size={20} />
              <span className="hidden sm:inline">Админ</span>
            </Link>
          )}
        </div>

        {user && (
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-gray-600">{user.first_name}</p>
              <p className="font-bold text-pink-600">💎 {user.balance.toFixed(0)}</p>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
