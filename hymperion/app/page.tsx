'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Shield, Lock, Eye, Zap } from 'lucide-react'
import { useUser } from '@auth0/nextjs-auth0/client';
import Link from 'next/link'

export default function AegisLandingPage() {
  const { user, isLoading } = useUser();  // Obtener el estado de autenticación
  const [isVisible, setIsVisible] = useState(false)
  
  useEffect(() => {
    setIsVisible(true)
  }, [])
  
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.1,
        delayChildren: 0.3
      }
    }
  }
  
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { 
        type: "spring",
        stiffness: 100
      }
    }
  }
  
  if (isLoading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-32 w-32 border-t-4 border-blue-500"></div>
    </div>
  );
  
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* Hero Section */}
      <motion.section 
        className="relative overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-100 to-purple-100 opacity-50"></div>
        <div className="container mx-auto px-4 py-24 relative z-10">
          <motion.div 
            className="max-w-3xl mx-auto text-center"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <motion.h1 variants={itemVariants} className="text-5xl md:text-6xl font-extrabold mb-6 text-blue-800">
              AEGIS
            </motion.h1>
            <motion.p variants={itemVariants} className="text-xl mb-8 text-gray-600">
              Advanced cybersecurity solutions for businesses of all sizes
            </motion.p>
            <motion.div variants={itemVariants}>
              <button className={`text-white font-bold py-2 px-4 rounded ${
              user ? 'bg-blue-500 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-700'
            }`}
          >
            {user ? (
              <Link href="/dashboard">
                Go to Dashboard
              </Link>
            ) : (
              <Link href="/api/auth/login">
                Login
              </Link>
            )}
          </button>
            </motion.div>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <motion.h2 
            className="text-3xl font-bold text-center mb-12 text-blue-800"
            initial={{ opacity: 0, y: -20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            viewport={{ once: true }}
          >
            What's Aegis?
          </motion.h2>
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
          >
            {[
              { icon: Shield, title: "Impenetrable Defense", description: "Our multi-layered security approach keeps your data safe from all threats" },
              { icon: Lock, title: "End-to-End Encryption", description: "Your information is encrypted at every step, ensuring complete privacy" },
              { icon: Eye, title: "24/7 Monitoring", description: "Our AI-powered systems vigilantly watch for any suspicious activity" },
              { icon: Zap, title: "Lightning-Fast Response", description: "Instant threat detection and neutralization to minimize damage" }
            ].map((feature, index) => (
              <motion.div 
                key={index} 
                className="bg-gray-100 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300"
                variants={itemVariants}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <feature.icon className="w-12 h-12 mb-4 text-blue-600" />
                <h3 className="text-xl font-semibold mb-2 text-blue-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-200 py-8">
        <div className="container mx-auto px-4 text-center text-gray-600">
          <p>&copy; 2024 Aegis Cybersecurity. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}