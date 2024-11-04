'use client'

import Image from 'next/image';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { useUser } from '@auth0/nextjs-auth0/client';
import { useState } from 'react';

export default function Home() {
  const { user, isLoading } = useUser();  // Obtener el estado de autenticación
  const text = "Diagnoticando la salud de tu red".split(" ");

  if (isLoading) return <div>Cargando...</div>;  // Mostrar un mensaje de carga mientras se verifica la autenticación

  return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-600">
        <div className="text-center">
          <motion.div initial="hidden" animate="visible" variants={{
            hidden: {
              scale: .8,
              opacity: 0
            },
            visible: {
              scale: 1,
              opacity: 1,
              transition: {
                delay: .4
              }
            },
          }}>
            <h1 className="text-4xl font-bold mb-4">Bienvenido a Aegis</h1> 
          </motion.div>
          <div className="text-xl mb-8">
            {text.map((el, i) => (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{
                  duration: 0.25,
                  delay: i / 10
                }}
                key={i}
              >
                {el}{" "}
              </motion.span>
            ))}
          </div>
          <motion.button
            whileHover={{ scale: 1.2 }}
            onHoverStart={e => {}}
            onHoverEnd={e => {}}
            whileTap={{ scale: 0.9 }}
            className={`text-white font-bold py-2 px-4 rounded ${
              user ? 'bg-green-500 hover:bg-green-700' : 'bg-blue-500 hover:bg-blue-700'
            }`}
          >
            {user ? (
              <Link href="/dashboard">
                Ir al Dashboard
              </Link>
            ) : (
              <Link href="/api/auth/login">
                Iniciar sesión con Auth0
              </Link>
            )}
          </motion.button>
        </div>
      </div>
  );
}
