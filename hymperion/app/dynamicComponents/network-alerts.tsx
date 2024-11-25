'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect, useCallback } from 'react'
import { AlertCircle, CheckCircle, ShieldAlert, X, RefreshCw, Filter, Calendar, MapPin, RotateCcw, Lock } from "lucide-react"
import { motion } from "framer-motion"

interface RiskData {
  id: number
  risk_description: string
  risk_impact: string
  risk_mitigation: string
  risk_score: number
  fecha: string
  ubicacion: string
  estado: string 
  evento: string
}

type RiskLevel = 'All' | '1' | '2' | '3' | '4' | '5'

export default function NetworkAlerts({ sedes }: { sedes: string }) {
  const router = useRouter()
  const [riskData, setRiskData] = useState<RiskData[]>([])
  const [filteredRiskData, setFilteredRiskData] = useState<RiskData[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [riskLevel, setRiskLevel] = useState<RiskLevel>('All')
  const [selectedRisk, setSelectedRisk] = useState<RiskData | null>(null)
  const [startDate, setStartDate] = useState<string>('')
  const [endDate, setEndDate] = useState<string>('')
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  const decodedSede = decodeURIComponent(sedes)
  let decodedSedeText = decodedSede
  switch (decodedSedeText.toLowerCase()) {
    case 'sede central':
      decodedSedeText = 'Central Office'
      break
    case 'sede 1':
      decodedSedeText = 'Laboratory 1'
      break
    case 'sede 2':
      decodedSedeText = 'Laboratory 2'
      break
    case 'sede 3':
      decodedSedeText = 'Laboratory 3'
      break
    default:
      break
  }

  const fetchRiskData = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch(`http://localhost:5000/tickets/pendientes/${sedes}`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setRiskData(Array.isArray(data) ? data : [data])
      setLastUpdated(new Date())
    } catch (err) {
      setError('An error occurred while fetching risk data. Please check your network connection and try again.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }, [sedes])

  useEffect(() => {
    fetchRiskData()
    const intervalId = setInterval(fetchRiskData, 60000) // 60000 ms = 1 minute
    return () => clearInterval(intervalId)
  }, [fetchRiskData])

  useEffect(() => {
    filterRiskData()
  }, [riskLevel, startDate, endDate, riskData])

  const filterRiskData = useCallback(() => {
    let filtered = riskData.filter(risk => 
      (risk.ubicacion || '').toLowerCase() === decodedSede.toLowerCase()
    )
    if (riskLevel !== 'All') {
      filtered = filtered.filter((risk) => risk.risk_score === parseInt(riskLevel))
    }
    if (startDate && endDate) {
      filtered = filtered.filter((risk) => {
        const riskDate = new Date(risk.fecha)
        return riskDate >= new Date(startDate) && riskDate <= new Date(endDate)
      })
    }
    setFilteredRiskData(filtered)
  }, [riskData, riskLevel, startDate, endDate, decodedSede])

  const resetFilters = () => {
    setRiskLevel('All')
    setStartDate('')
    setEndDate('')
  }

  const getRiskColor = (score: number) => {
    switch (score) {
      case 1: return '#00c176'
      case 2: return '#88c100'
      case 3: return '#fabe28'
      case 4: return '#ff8a00'
      case 5: return '#ff003c'
      default: return '#8f8f8f'
    }
  }
  
  const getRiskLevelText = (score: number) => {
    switch (score) {
      case 1: return 'Very Low'
      case 2: return 'Low'
      case 3: return 'Medium'
      case 4: return 'High'
      case 5: return 'Very High'
      default: return 'Unknown'
    }
  }

  const updateTicketStatus = async (id: number, newStatus: string) => {
    try {
      const response = await fetch(`http://localhost:5000/tickets/${id}/resuelto`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: newStatus }),
      })
      if (response.ok) {
        fetchRiskData()
        setSelectedRisk(null)
      } else {
        console.error('Failed to update ticket status')
      }
    } catch (error) {
      console.error('Error updating ticket status:', error)
    }
  }

  const handleRedirect = () => {
    const currentPath = window.location.pathname
    if (currentPath === '/dashboard/sede%20central') {
      router.push('/dashboard/sede%20central/resueltos')
    } else if (currentPath === '/dashboard/sede%201') {
      router.push('/dashboard/sede%201/resueltos')
    } else if (currentPath === '/dashboard/sede%202') {
      router.push('/dashboard/sede%202/resueltos')
    } else if (currentPath === '/dashboard/sede%203') {
      router.push('/dashboard/sede%203/resueltos')
    } else {
      console.warn('Ruta no reconocida.')
    }
  }

  if (isLoading && !riskData.length) {
    return (
      <div className="flex justify-center items-center h-full p-4">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  if (error && !riskData.length) {
    return (
      <div className="text-center py-10">
        <AlertCircle className="h-16 w-16 text-red-500 mx-auto mb-4" />
        <p className="text-red-500 mb-4">{error}</p>
        <button 
          onClick={fetchRiskData}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors flex items-center mx-auto"
        >
          <RefreshCw className="h-5 w-5 mr-2" />
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="w-full h-full max-h-full bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
      <div className="p-4 bg-gray-50 border-b border-gray-200">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Events of {decodedSedeText}</h2>
          {lastUpdated && (
            <p className="text-sm text-gray-600">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </p>
          )}
        </div>
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center">
            <Filter className="h-5 w-5 mr-2 text-gray-500" />
            <select
              value={riskLevel}
              onChange={(e) => setRiskLevel(e.target.value as RiskLevel)}
              className="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="All">All Risks</option>
              <option value="1">Very Low Risk</option>
              <option value="2">Low Risk</option>
              <option value="3">Medium Risk</option>
              <option value="4">High Risk</option>
              <option value="5">Very High Risk</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <Calendar className="h-5 w-5 text-gray-500" />
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <span>to</span>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={resetFilters}
            className="flex items-center px-3 py-1 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset Filters
          </button>
          <button
            onClick={handleRedirect}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Resolved
          </button>
        </div>
      </div>
      <div className="p-2 flex-grow overflow-hidden">
        <div className="overflow-y-auto h-full pr-2 space-y-2">
          {filteredRiskData.length === 0 ? (
            <p className="text-center text-gray-500">No pending tickets available for the selected filters.</p>
          ) : (
            filteredRiskData.map((risk, index) => (
              <div 
                key={index} 
                className="bg-white border border-gray-200 rounded-lg shadow-sm p-3 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => setSelectedRisk(risk)}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-1" style={{ color: getRiskColor(risk.risk_score) }}>
                    <ShieldAlert className="h-4 w-4" />
                    <span className="font-bold text-sm">
                      Risk Level: {getRiskLevelText(risk.risk_score)}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <Calendar className="h-4 w-4" />
                    <span>{risk.fecha ? new Date(risk.fecha).toLocaleString() : 'Date unknown'}</span>
                  </div>
                </div>
                <p className="text-sm text-gray-700 mb-2">{risk.evento}</p>
                <div className="flex items-center space-x-1 text-sm text-gray-500">
                  <MapPin className="h-4 w-4" />
                  <span>{risk.ubicacion || 'Location unknown'}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
      {selectedRisk && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-gray-800">Detailed Risk Assessment</h3>
              <button onClick={() => setSelectedRisk(null)} className="text-gray-500 hover:text-gray-700">
                <X className="h-6 w-6" />
              </button>
            </div>
            <div className="space-y-4">
            <div className="flex items-center space-x-2" style={{ color: getRiskColor(selectedRisk.risk_score) }}>
                <ShieldAlert className="h-5 w-5 mr-2" />
                Risk Level {selectedRisk.risk_score}: {getRiskLevelText(selectedRisk.risk_score)}
              </div>
              <div>
                <h4 className="font-semibold">Description:</h4>
                <p>{selectedRisk.risk_description}</p>
              </div>
              <div>
                <h4 className="font-semibold">Impact:</h4>
                <p>{selectedRisk.risk_impact}</p>
              </div>
              <div>
                <h4 className="font-semibold">Mitigation:</h4>
                <p>{selectedRisk.risk_mitigation}</p>
              </div>
              <div className="flex justify-between text-sm text-gray-500">
                <div className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>{selectedRisk.fecha}</span>
                </div>
                <div className="flex items-center space-x-1">
                  <MapPin className="h-4 w-4" />
                  <span>{selectedRisk.ubicacion || 'Sede no especificada'}</span>
                </div>
                <div className="flex items-center space-x-4 mt-4">
                  <button
                      onClick={() => updateTicketStatus(selectedRisk.id, 'resuelto')}
                      className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
                    >
                      <CheckCircle className="h-5 w-5 inline-block mr-2" />
                      Mark as Resolved
                    </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}