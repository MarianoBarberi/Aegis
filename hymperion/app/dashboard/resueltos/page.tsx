'use client'
//import NetworkAlerts from '@/app/components/network-alerts'
import Tickets from '@/app/components/tickets-resuelto' 



export default function Page() {
  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Menú lateral */}
      <div className="w-full bg-white shadow-md">
        <Tickets />
      </div>
    </div>
  )
}