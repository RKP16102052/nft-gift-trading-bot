import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useStore } from './store/useStore'
import apiClient from './api/client'
import { Navbar } from './components/Navbar'
import { Notifications } from './components/Notifications'
import HomePage from './pages/HomePage'
import MarketplacePage from './pages/MarketplacePage'
import PortfolioPage from './pages/PortfolioPage'
import AdminPage from './pages/AdminPage'
import './styles/index.css'

function App() {
  const { user, setUser, loading, setLoading } = useStore()

  useEffect(() => {
    const initUser = async () => {
      setLoading(true)
      try {
        const userData = await apiClient.getCurrentUser()
        setUser(userData)
      } catch (error) {
        console.error('Failed to load user:', error)
      } finally {
        setLoading(false)
      }
    }

    initUser()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-pink">
        <div className="text-center">
          <div className="animate-spin text-4xl mb-4">🎁</div>
          <p className="text-xl text-pink-600 font-semibold">Загрузка...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-pink">
        <Navbar />
        <main className="container py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/marketplace" element={<MarketplacePage />} />
            <Route path="/portfolio" element={user ? <PortfolioPage /> : <Navigate to="/" />} />
            <Route path="/admin" element={user?.is_admin ? <AdminPage /> : <Navigate to="/" />} />
          </Routes>
        </main>
        <Notifications />
      </div>
    </Router>
  )
}

export default App
