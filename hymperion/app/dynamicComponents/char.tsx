'use client';

import { useState, useEffect, useCallback } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface RiskData {
  risk_description: string;
  risk_impact: string;
  risk_mitigation: string;
  risk_score: number;
  fecha: string;
  ubicacion: string;
  risk_level: string;
}

const RISK_LEVELS = [
  { name: 'Very Low', value: 1 },
  { name: 'Low', value: 2 },
  { name: 'Medium', value: 3 },
  { name: 'High', value: 4 },
  { name: 'Very High', value: 5 },
]

const COLORS = ['#00c176', '#88c100', '#fabe28', '#ff8a00', '#ff003c']
const UPDATE_INTERVAL = 60000; // 1 minuto

export default function NetworkAlerts({ sedes }: { sedes: string }) {
  const [riskData, setRiskData] = useState<RiskData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchRiskData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5000/tickets/pendientes/${sedes}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setRiskData(Array.isArray(data) ? data : [data]);
      setLastUpdated(new Date());
    } catch (err) {
      setError('An error occurred while fetching risk data. Please check your network connection and try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [sedes]);

  const processChartData = (data: RiskData[]) => {
    const riskCounts = RISK_LEVELS.map(level => ({
      name: level.name,
      value: data.filter(risk => risk.risk_score === level.value).length
    }));
    setChartData(riskCounts);
  };

  useEffect(() => {
    fetchRiskData();
    const intervalId = setInterval(fetchRiskData, UPDATE_INTERVAL);
    return () => clearInterval(intervalId);
  }, [fetchRiskData]);

  useEffect(() => {
    processChartData(riskData);
  }, [riskData]);

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
        )}
      </div>
  );
}
