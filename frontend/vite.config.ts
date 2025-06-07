import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Redireciona qualquer requisição que comece com /api
      '/api': {
        // O alvo é o seu backend rodando no Docker na porta 8000
        target: 'http://localhost:8000',
        // Necessário para o proxy funcionar corretamente
        changeOrigin: true,
      },
    },
  },
})