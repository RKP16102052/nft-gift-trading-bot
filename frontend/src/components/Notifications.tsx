import React, { useEffect } from 'react'
import { useStore } from '../store/useStore'
import { X, CheckCircle, AlertCircle, Info } from 'lucide-react'

export const Notifications: React.FC = () => {
  const { notifications, removeNotification } = useStore()

  return (
    <div className="fixed bottom-4 right-4 space-y-2 z-50">
      {notifications.map((notif) => (
        <NotificationItem
          key={notif.id}
          notification={notif}
          onClose={() => removeNotification(notif.id)}
        />
      ))}
    </div>
  )
}

interface NotificationItemProps {
  notification: { id: string; message: string; type: 'success' | 'error' | 'info' }
  onClose: () => void
}

const NotificationItem: React.FC<NotificationItemProps> = ({ notification, onClose }) => {
  useEffect(() => {
    const timer = setTimeout(onClose, 5000)
    return () => clearTimeout(timer)
  }, [onClose])

  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
  }[notification.type]

  const Icon = {
    success: CheckCircle,
    error: AlertCircle,
    info: Info,
  }[notification.type]

  return (
    <div className={`${bgColor} text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 animate-slide-in max-w-md`}>
      <Icon size={20} className="flex-shrink-0" />
      <span className="flex-1">{notification.message}</span>
      <button onClick={onClose} className="flex-shrink-0 hover:opacity-80">
        <X size={18} />
      </button>
    </div>
  )
}
