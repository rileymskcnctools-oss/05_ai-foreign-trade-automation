<template>
  <aside class="w-64 bg-white border-r border-gray-200 flex flex-col flex-shrink-0">
    <div class="px-6 py-5 border-b border-gray-100">
      <h1 class="text-xl font-bold text-gray-800">🔨 FT Workspace</h1>
      <p class="text-xs text-gray-400 mt-1">Foreign Trade AI v4.0</p>
    </div>
    <nav class="flex-1 px-3 py-4 space-y-1">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="isActive(item.path)
          ? 'bg-primary-50 text-primary-700 border-l-4 border-primary-500'
          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
      >
        <span class="mr-3 text-lg">{{ item.icon }}</span>
        {{ item.label }}
      </router-link>
    </nav>
    <div class="px-4 py-3 border-t border-gray-100 text-xs text-gray-400">
      Vue 3 + FastAPI
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const menuItems = [
  { path: '/dashboard', label: '数据概览', icon: '📊' },
  { path: '/products', label: '产品管理', icon: '📦' },
  { path: '/clients', label: '客户CRM', icon: '👥' },
  { path: '/quotation', label: '报价助手', icon: '💰' },
  { path: '/market', label: '市场研究', icon: '🔍' },
  { path: '/outreach', label: '开发信', icon: '📧' },
  { path: '/analytics', label: '数据分析', icon: '📈' },
]

const isActive = (path) => route.path === path || route.path.startsWith(path + '/')
</script>
