'use client'

import { useState, useEffect, useCallback } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface RiskData {
  risk_description: string
  risk_impact: string
  risk_mitigation: string
  risk_score: number
}

const COLORS = ['#10B981', '#FBBF24', '#F59E0B', '#EF4444', '#8B5CF6']

const RISK_LEVELS = [
  { name: 'Very Low', value: 1 },
  { name: 'Low', value: 2 },
  { name: 'Medium', value: 3 },
  { name: 'High', value: 4 },
  { name: 'Very High', value: 5 },
]

const UPDATE_INTERVAL = 60000 // 1 minute

function RiskDistributionChart({ sedes }: { sedes: string }) {
  const [chartData, setChartData] = useState<{ name: string; value: number }[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdateTime, setLastUpdateTime] = useState<Date | null>(null)
  const [isUpdating, setIsUpdating] = useState(false)

  const fetchRiskData = useCallback(async () => {
    setIsUpdating(true)
    try {
      const response = await fetch(`http://localhost:5000/tickets/${sedes}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: RiskData[] = await response.json()
      processChartData(data)
      setLastUpdateTime(new Date())
      setError(null)
    } catch (err) {
      setError('An error occurred while fetching risk data.')
      console.error(err)
    } finally {
      setIsLoading(false)
      setIsUpdating(false)
    }
  }, [location])

  const processChartData = (data: RiskData[]) => {
    const riskCounts = RISK_LEVELS.map(level => ({
      name: level.name,
      value: data.filter(risk => risk.risk_score === level.value).length
    }))
    setChartData(riskCounts)
  }

  useEffect(() => {
    fetchRiskData()
    const intervalId = setInterval(fetchRiskData, UPDATE_INTERVAL)
    return () => clearInterval(intervalId)
  }, [fetchRiskData])

  if (isLoading) {
    return <div className="flex items-center justify-center h-full">Loading...</div>
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>
  }

  return (
    <div className="h-full flex flex-col">
      <div className="text-sm font-semibold mb-2">Risk Distribution - {sedes}</div>
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius="80%"
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const data = payload[0].payload;
                  return (
                    <div className="bg-white border border-gray-200 p-2 shadow-md rounded">
                      <p className="font-bold">{data.name}</p>
                      <p>Count: {data.value}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="text-xs text-gray-500 mt-2 flex justify-between items-center">
        {lastUpdateTime && (
          <span>Last updated: {lastUpdateTime.toLocaleTimeString()}</span>
        )}
        {isUpdating && (
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-900 mr-2"></div>
            <span>Updating...</span>
          </div>
        )}
      </div>
    </div>
  )
}

function TicketsList({ sedes }: { sedes: string }) {
  const [tickets, setTickets] = useState<RiskData[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await fetch(`http://localhost:5000/tickets/${sedes}`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data: RiskData[] = await response.json()
        setTickets(data)
      } catch (err) {
        setError('An error occurred while fetching tickets.')
        console.error(err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchTickets()
  }, [location])

  if (isLoading) {
    return <div className="flex items-center justify-center h-full">Loading events...</div>
  }

  if (error) {
    return <div className="text-center text-red-500">{error}</div>
  }

  return (
    <div className="h-full overflow-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Risk Score</th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {tickets.map((ticket, index) => (
            <tr key={index}>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.risk_description}</td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.risk_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function LocationPage({ sedes }: { sedes: string }) {
  return (
    <>
      <div className=" w-full h flex-1 flex p-4 space-x-4">
        {/* Gráfica de pastel */}
          <RiskDistributionChart sedes={sedes} />
      </div>
    </>
  )
}