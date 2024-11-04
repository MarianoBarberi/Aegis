'use client'
import { notFound } from 'next/navigation'
import Tickets from '@/app/dynamicComponents/tickets-resueltos'

const validLocations = ['sede%20central', 'sede%201', 'sede%202', 'sede%203']

export default function DynamicLocationPage({ params }: { params: { sedes: string } }) {
  if (!validLocations.includes(params.sedes)) {
    notFound()
  }

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Menú lateral */}
      <div className="w-full bg-white shadow-md">
        <Tickets sedes={params.sedes} />
      </div>
    </div>
  )
}