import React, { useMemo } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { PriceHistory } from '../types'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

interface PriceChartProps {
  history: PriceHistory[]
  nftName: string
}

export const PriceChart: React.FC<PriceChartProps> = ({ history, nftName }) => {
  const data = useMemo(() => {
    const labels = history.map((h) => new Date(h.timestamp).toLocaleDateString('ru-RU'))
    const prices = history.map((h) => h.price)

    return {
      labels,
      datasets: [
        {
          label: 'Цена',
          data: prices,
          borderColor: '#ec4899',
          backgroundColor: 'rgba(236, 72, 153, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 4,
          pointBackgroundColor: '#ec4899',
          pointHoverRadius: 6,
        },
      ],
    }
  }, [history])

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        labels: {
          font: { size: 12 },
          color: '#666',
        },
      },
      title: {
        display: true,
        text: `Цена ${nftName}`,
        font: { size: 14, weight: 'bold' as const },
        color: '#333',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: { color: 'rgba(0, 0, 0, 0.05)' },
        ticks: { color: '#666' },
      },
      x: {
        grid: { color: 'rgba(0, 0, 0, 0.05)' },
        ticks: { color: '#666' },
      },
    },
  }

  return (
    <div className="w-full h-96 bg-white p-4 rounded-lg shadow-md">
      <Line data={data} options={options} />
    </div>
  )
}
