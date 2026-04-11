import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import { fileURLToPath, URL } from 'node:url'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      // Esto ayuda a que el SW detecte cambios automáticamente
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'Turismo WJL E.I.R.L.', // Nombre legal completo
        short_name: 'Turismo WJL',      // Más descriptivo que solo "Turismo"
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        theme_color: '#E31E24',         // El rojo de tu logo para la barra superior
        description: 'Transporte de pasajeros y carga - Uniendo Familias',
        icons: [
          {
            src: 'icons/icon-192.png',  // Quitamos el / inicial para evitar problemas de ruta en build
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'icons/icon-512.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'icons/icon-512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'         // Importante para que Android no corte mal el icono
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
})