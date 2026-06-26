import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      // 只代理 API 路径，不拦截页面路径
      '/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/products/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/clients/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/market/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/outreach/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/quotation/api': { target: 'http://localhost:8020', changeOrigin: true },
      '/analytics/api': { target: 'http://localhost:8020', changeOrigin: true },
    },
  },
})
