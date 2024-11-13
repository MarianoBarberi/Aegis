'use client'
//import NetworkAlerts from '@/app/components/network-alerts'
import Tickets from '@/app/components/tickets-resuelto' 
import { withPageAuthRequired } from '@auth0/nextjs-auth0/client'



function Page() {
  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Menú lateral */}
      <div className="w-full bg-white shadow-md">
        <Tickets />
      </div>
    </div>
  )
}

export default withPageAuthRequired(Page, {
  returnTo: '/dashboard/resueltos',
  onRedirecting: () => <div>Loading...</div>,
  onError: error => <div>Error: {error.message}</div>
})