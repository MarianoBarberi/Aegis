'use client'
import { notFound } from 'next/navigation'
import Tickets from '@/app/dynamicComponents/tickets-resueltos'
import { withPageAuthRequired } from '@auth0/nextjs-auth0/client'

const validLocations = ['sede%20central', 'sede%201', 'sede%202', 'sede%203']

function DynamicLocationPage({ params }: { params: { sedes: string } }) {
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

export default withPageAuthRequired(DynamicLocationPage, {
  returnTo: '/dashboard',
  onRedirecting: () => <div>Loading...</div>,
  onError: error => <div>Error: {error.message}</div>
})