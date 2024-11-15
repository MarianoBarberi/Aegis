'use client'

import { useState, useEffect, useCallback, useMemo } from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

interface RiskData {
  risk_description: string
  risk_impact: string
  risk_mitigation: string
  risk_score: number
}

const RISK_LEVELS = [
  { name: 'Very Low', value: 1 },
  { name: 'Low', value: 2 },
  { name: 'Medium', value: 3 },
  { name: 'High', value: 4 },
  { name: 'Very High', value: 5 },
]

const COLORS = ['#00c176', '#88c100', '#fabe28', '#ff8a00', '#ff003c']
const UPDATE_INTERVAL = 60000 // 1 minute

export default function RiskDistributionChart() {
  const [riskData, setRiskData] = useState<RiskData[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdateTime, setLastUpdateTime] = useState<Date | null>(null)
  const [isUpdating, setIsUpdating] = useState(false)

  // Fetch Risk Data
  const fetchRiskData = useCallback(async () => {
    setIsUpdating(true)
    try {
      const response = await fetch('http://localhost:5000/tickets/pendientes')
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data: RiskData[] = await response.json()
      setRiskData(data)
      setLastUpdateTime(new Date())
      setError(null)
    } catch (err) {
      setError('An error occurred while fetching risk data.')
      console.error(err)
    } finally {
      setIsLoading(false)
      setIsUpdating(false)
    }
  }, [])

  // Process data for chart
  const chartData = useMemo(() => {
    return RISK_LEVELS.map(level => ({
      name: level.name,
      value: riskData.filter(risk => risk.risk_score === level.value).length
    }))
  }, [riskData])

  useEffect(() => {
    fetchRiskData()
    const intervalId = setInterval(fetchRiskData, UPDATE_INTERVAL)
    return () => clearInterval(intervalId)
  }, [fetchRiskData])

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-t-4 border-blue-500"></div>
      </div>
    )
  }

  return (
      <div className="p-6">
        {error ? (
          <div className="text-center text-red-500 mb-4">{error}</div>
        ) : (
          <div className="h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
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
                      const data = payload[0].payload
                      return (
                        <div className="bg-white border border-gray-200 p-2 shadow-md rounded">
                          <p className="font-bold">{data.name}</p>
                          <p>Count: {data.value}</p>
                        </div>
                      )
                    }
                    return null
                  }}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
  )
}
