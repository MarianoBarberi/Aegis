// middleware.js

import { withAuth } from '@auth0/nextjs-auth0/edge';

export default withAuth({
  pages: {
    signIn: '/api/auth/login', // Cambia esto según tu ruta de inicio de sesión
  },
});

export const config = {
  matcher: ['/protected-page/:path*'], // Rutas protegidas
};

