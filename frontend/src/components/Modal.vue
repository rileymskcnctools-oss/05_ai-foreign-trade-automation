<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="fixed inset-0 z-40 flex items-center justify-center">
        <div class="fixed inset-0 bg-black/50" @click="$emit('close')"></div>
        <div class="relative bg-white rounded-xl shadow-2xl max-h-[85vh] overflow-y-auto"
             :class="size === 'lg' ? 'w-full max-w-4xl' : size === 'xl' ? 'w-full max-w-6xl' : 'w-full max-w-2xl'">
          <div class="sticky top-0 bg-white px-6 py-4 border-b border-gray-200 flex items-center justify-between z-10">
            <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
            <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 text-xl">&times;</button>
          </div>
          <div class="px-6 py-4">
            <slot />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: { type: String, default: '' },
  size: { type: String, default: 'md' },
})
defineEmits(['close'])
</script>

<style scoped>
.modal-enter-active { transition: all 0.2s ease; }
.modal-leave-active { transition: all 0.2s ease; }
.modal-enter-from { opacity: 0; }
.modal-leave-to { opacity: 0; }
</style>
