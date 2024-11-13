'use client'
import { notFound } from 'next/navigation'
import Alert from '@/app/dynamicComponents/network-alerts'
import Char from '@/app/dynamicComponents/char'
import Menu  from '@/app/components/side-menu'
import { motion } from "framer-motion";
import { useState } from 'react'
import { withPageAuthRequired } from '@auth0/nextjs-auth0/client'

const validLocations = ['sede%20central', 'sede%201', 'sede%202', 'sede%203']

const variants = {
  open: { opacity: 1, x: 0 },
  closed: { opacity: 0, x: "-100%" },
}


function DynamicLocationPage({ params }: { params: { sedes: string } }) {
  if (!validLocations.includes(params.sedes)) {
    notFound()
  }
  const [isMenuVisible] = useState(true)


  return ( 
        <div className="flex h-screen bg-gray-100 overflow-hidden">
          {/* Menú lateral */}
          <motion.div 
            className="bg-white shadow-md"
            animate={isMenuVisible ? "open" : "closed"}
            variants={variants}
            initial="closed"
            transition={{ duration: 0.3 }}
          >
            <Menu />
          </motion.div>
    
          {/* Contenido principal con scroll */}
          <div className="flex-1 overflow-y-auto">
            <div className="min-h-full p-4 space-y-4">
              <div className="flex space-x-4">
                {/* Imagen principal */}
                <div className="w-1/4 bg-white shadow-md rounded-lg flex items-center justify-center p-4">
                  <img src="/placeholder.svg?height=150&width=150" alt="Placeholder" className="max-w-full h-auto" />
                </div>
    
                {/* Gráfica de pastel */}
                <div className="w-3/4 bg-white shadow-md rounded-lg">
                  <Char sedes={params.sedes} />
                </div>
              </div>
    
              {/* Sección de tickets */}
              <div className="bg-white shadow-md rounded-lg">
                <Alert sedes={params.sedes} />
              </div>
            </div>
          </div>
        </div>
  )
}

export default withPageAuthRequired(DynamicLocationPage, {
  returnTo: '/dashboard',
  onRedirecting: () => <div>Loading...</div>,
  onError: error => <div>Error: {error.message}</div>
})