'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Home, Menu, X, ChevronLeft, ChevronRight, Hospital, Building, LogOut } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const menuItems = [
  { name: 'Home', icon: Home, href: '/dashboard' },
  { name: 'Central', icon: Building, href: '/dashboard/sede%20central' },
  { name: 'Lab 1', icon: Hospital, href: '/dashboard/sede%201' },
  { name: 'Lab 2', icon: Hospital, href: '/dashboard/sede%202' },
  { name: 'Lab 3', icon: Hospital, href: '/dashboard/sede%203' },
  { name: 'Logout', icon: LogOut, href: '/api/auth/logout' },
]

const menuItemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 },
}

const sidebarVariants = {
  expanded: { width: '185px' },
  collapsed: { width: '64px' },
}

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <motion.div 
      className="bg-white shadow-md h-full relative"
      initial="expanded"
      animate={isExpanded ? "expanded" : "collapsed"}
      variants={sidebarVariants}
    >
      <div className="flex items-center justify-between p-4 md:hidden">
        <span className="font-bold text-xl">Menu</span>
        <motion.button
          onClick={() => setIsOpen(!isOpen)}
          className="p-2"
          whileTap={{ scale: 0.95 }}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </motion.button>
      </div>
      <AnimatePresence>
        {(isOpen || window.innerWidth >= 768) && (
          <motion.nav
            initial="hidden"
            animate="visible"
            exit="hidden"
            className={`md:block overflow-hidden`}
          >
            <ul className="space-y-2 p-4">
              {menuItems.map((item, index) => (
                <motion.li
                  key={item.name}
                  variants={menuItemVariants}
                  initial="hidden"
                  animate="visible"
                  exit="hidden"
                  transition={{ delay: index * 0.1 }}
                >
                  <Link href={item.href} className="flex items-center space-x-3 text-gray-700 p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200">
                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.95 }} className="relative">
                      {item.icon && <item.icon size={20} />}
                      {item.icon === Hospital && (
                      <span className="absolute bottom-0 right-0 translate-x-1 translate-y-1 text-xs bg-black text-white rounded-full w-3.5 h-3.5 flex items-center justify-center">
                        {index - 1}
                      </span>
                      )}
                    </motion.div>
                    {isExpanded && <span>{item.name}</span>}
                  </Link>
                </motion.li>
              ))}
            </ul>
          </motion.nav>
        )}
      </AnimatePresence>
      <motion.button
        className="absolute top-1/2 -right-3 bg-white rounded-full p-1 shadow-md"
        onClick={() => setIsExpanded(!isExpanded)}
        whileTap={{ scale: 0.95 }}
      >
        {isExpanded ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </motion.button>
    </motion.div>
  )
}