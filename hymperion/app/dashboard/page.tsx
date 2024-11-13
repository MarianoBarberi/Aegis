'use client'

import { useState } from 'react'
import { motion } from "framer-motion"
import { withPageAuthRequired } from '@auth0/nextjs-auth0/client'
import Menu from '@/app/components/side-menu' 
import Char from '@/app/components/char' 
import Alerts from '@/app/components/network-alerts'
import Image from 'next/image'

const variants = {
  open: { opacity: 1, x: 0 },
  closed: { opacity: 0, x: "-100%" },
}

function Dashboard() {
  const [isMenuVisible] = useState(true)

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Menú lateral  */}
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
            <div className="w-1/4 bg-black shadow-md rounded-lg flex items-center justify-center p-4">
              <Image src="/images/logo2.png" alt="Logo" className="max-w-full h-auto" width={180} height={180}/>
            </div>

            {/* Gráfica de pastel */}
            <div className="w-3/4 bg-white shadow-md rounded-lg">
              <Char />
            </div>
          </div>

          {/* Sección de tickets */}
          <div className="bg-white shadow-md rounded-lg">
            <Alerts />
          </div>
        </div>
      </div>
    </div>
  )
}

export default withPageAuthRequired(Dashboard, {
  returnTo: '/dashboard',
  onRedirecting: () => <div>Loading...</div>,
  onError: error => <div>Error: {error.message}</div>
})