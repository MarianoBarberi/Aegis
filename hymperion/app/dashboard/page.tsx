'use client'

import { useState } from 'react'
import { motion } from "framer-motion"
import Menu from '@/app/components/side-menu' 
import Char from '@/app/components/char' 
import Alerts from '@/app/components/network-alerts'

const variants = {
  open: { opacity: 1, x: 0 },
  closed: { opacity: 0, x: "-100%" },
}

export default function Page() {
  const [isMenuVisible] = useState(true)

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Menú lateral  */}
      <motion.div 
        className=" bg-white shadow-md"
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