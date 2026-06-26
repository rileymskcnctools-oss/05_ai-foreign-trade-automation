<template>
  <div class="flex h-screen bg-gray-50">
    <Sidebar />
    <main class="flex-1 overflow-y-auto">
      <div class="px-6 py-6">
        <router-view />
      </div>
    </main>
    <Toast />
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
import Toast from './components/Toast.vue'
</script>
