<template>
  <div class="p-6 max-w-7xl mx-auto">
    <h1 class="text-2xl font-bold text-gray-800 mb-6">客户触达</h1>

    <!-- Tab Switching -->
    <div class="flex gap-1 mb-6 border-b border-gray-200">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="[
          'px-5 py-2.5 text-sm font-medium rounded-t-lg transition-colors',
          activeTab === tab.key
            ? 'bg-white text-blue-600 border border-b-white border-gray-200 -mb-px'
            : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
        ]"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- Main Layout: Left settings + Right result -->
    <div class="flex gap-6">
      <!-- Left: Settings Panel -->
      <div class="w-80 flex-shrink-0 space-y-4">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h2 class="text-base font-semibold text-gray-700 mb-4">设置</h2>

          <!-- Client Selector -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-600 mb-1.5">选择客户</label>
            <select
              v-model="selectedClientId"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              <option :value="null" disabled>请选择客户...</option>
              <option v-for="client in clients" :key="client.id" :value="client.id">
                {{ client.company_name || client.name }}
              </option>
            </select>
          </div>

          <!-- Message Type (Email only) -->
          <div v-if="activeTab === 'email'" class="mb-4">
            <label class="block text-sm font-medium text-gray-600 mb-1.5">消息类型</label>
            <select
              v-model="messageType"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              <option value="cold_intro">初次联系</option>
              <option value="follow_up">跟进</option>
              <option value="product_intro">产品介绍</option>
            </select>
          </div>

          <!-- WhatsApp also has message type -->
          <div v-if="activeTab === 'whatsapp'" class="mb-4">
            <label class="block text-sm font-medium text-gray-600 mb-1.5">消息类型</label>
            <select
              v-model="messageType"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            >
              <option value="cold_intro">初次联系</option>
              <option value="follow_up">跟进</option>
              <option value="product_intro">产品介绍</option>
            </select>
          </div>

          <!-- Generate Button -->
          <button
            @click="generateContent"
            :disabled="!selectedClientId || generating"
            :class="[
              'w-full py-2.5 rounded-lg text-sm font-medium transition-all',
              !selectedClientId || generating
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700 active:scale-[0.98]'
            ]"
          >
            <span v-if="generating" class="flex items-center justify-center gap-2">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              生成中...
            </span>
            <span v-else>✨ 生成内容</span>
          </button>
        </div>

        <!-- History List -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h2 class="text-base font-semibold text-gray-700 mb-3">历史记录</h2>
          <div v-if="filteredHistory.length === 0" class="text-sm text-gray-400 text-center py-4">
            暂无记录
          </div>
          <div v-else class="space-y-2 max-h-80 overflow-y-auto">
            <button
              v-for="(item, idx) in filteredHistory"
              :key="idx"
              @click="loadHistory(item)"
              class="w-full text-left px-3 py-2.5 rounded-lg border border-gray-100 hover:bg-blue-50 hover:border-blue-200 transition-colors"
            >
              <div class="flex items-center justify-between">
                <span class="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                  {{ tabLabel(item.type) }}
                </span>
                <span class="text-xs text-gray-400">{{ item.time }}</span>
              </div>
              <p class="text-sm text-gray-600 mt-1 truncate">
                {{ item.subject || item.message?.substring(0, 40) || '...' }}...
              </p>
            </button>
          </div>
        </div>
      </div>

      <!-- Right: Result Display -->
      <div class="flex-1 min-w-0">
        <div v-if="!result" class="bg-white rounded-xl shadow-sm border border-gray-200 min-h-[400px] flex items-center justify-center">
          <div class="text-center text-gray-400">
            <svg class="w-16 h-16 mx-auto mb-3 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            <p class="text-sm">选择客户并点击「生成内容」开始</p>
          </div>
        </div>

        <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 min-h-[400px]">
          <!-- Action Bar -->
          <div class="flex items-center justify-between px-5 py-3 border-b border-gray-100">
            <h3 class="text-sm font-semibold text-gray-700">
              {{ activeTab === 'email' ? '📧 邮件内容' : activeTab === 'whatsapp' ? '💬 WhatsApp 消息' : '🔗 LinkedIn 消息' }}
            </h3>
            <div class="flex gap-2">
              <template v-if="!editing">
                <button @click="copyContent" class="px-3 py-1.5 text-xs rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 transition-colors">📋 复制</button>
                <button @click="startEdit" class="px-3 py-1.5 text-xs rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 transition-colors">✏️ 编辑</button>
                <button @click="clearResult" class="px-3 py-1.5 text-xs rounded-lg bg-red-50 hover:bg-red-100 text-red-500 transition-colors">🗑 删除</button>
              </template>
              <template v-else>
                <button @click="saveEdit" class="px-3 py-1.5 text-xs rounded-lg bg-green-500 hover:bg-green-600 text-white transition-colors">💾 保存</button>
                <button @click="cancelEdit" class="px-3 py-1.5 text-xs rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 transition-colors">❌ 取消</button>
              </template>
            </div>
          </div>

          <!-- Email Content -->
          <div v-if="activeTab === 'email'" class="p-5">
            <div v-if="!editing">
              <div class="bg-amber-50 border border-amber-200 rounded-lg px-4 py-3 mb-4">
                <span class="text-xs font-medium text-amber-600">主题</span>
                <p class="text-sm font-medium text-gray-800 mt-0.5 whitespace-pre-wrap">{{ result.subject }}</p>
              </div>
              <div class="bg-gray-50 rounded-lg px-5 py-4 min-h-[300px]">
                <pre class="whitespace-pre-wrap text-sm text-gray-700 font-sans leading-relaxed">{{ result.body }}</pre>
              </div>
            </div>
            <div v-else class="space-y-3">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">主题</label>
                <input v-model="editData.subject" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">正文</label>
                <textarea v-model="editData.body" rows="16" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-y"></textarea>
              </div>
            </div>
          </div>

          <!-- WhatsApp Content (chat bubble) -->
          <div v-else-if="activeTab === 'whatsapp'" class="p-5">
            <div v-if="!editing">
              <div class="max-w-lg">
                <div class="bg-green-100 border border-green-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
                  <pre class="whitespace-pre-wrap text-sm text-gray-800 font-sans leading-relaxed">{{ result.message }}</pre>
                </div>
                <p class="text-xs text-gray-400 mt-1 ml-2">{{ formatTime(new Date()) }}</p>
              </div>
            </div>
            <div v-else>
              <label class="block text-xs font-medium text-gray-500 mb-1">消息内容</label>
              <textarea v-model="editData.message" rows="16" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-y"></textarea>
            </div>
          </div>

          <!-- LinkedIn Content (professional card) -->
          <div v-else-if="activeTab === 'linkedin'" class="p-5">
            <div v-if="!editing">
              <div class="border border-gray-200 rounded-lg overflow-hidden">
                <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-4 py-2">
                  <span class="text-white text-xs font-medium">LinkedIn InMail</span>
                </div>
                <div class="px-5 py-4 bg-white min-h-[300px]">
                  <pre class="whitespace-pre-wrap text-sm text-gray-700 font-sans leading-relaxed">{{ result.message }}</pre>
                </div>
              </div>
            </div>
            <div v-else>
              <label class="block text-xs font-medium text-gray-500 mb-1">消息内容</label>
              <textarea v-model="editData.message" rows="16" class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-y"></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { outreachApi, clientsApi } from '../api'

const tabs = [
  { key: 'email', label: 'Email', icon: '📧' },
  { key: 'whatsapp', label: 'WhatsApp', icon: '💬' },
  { key: 'linkedin', label: 'LinkedIn', icon: '🔗' }
]

const activeTab = ref('email')
const clients = ref([])
const selectedClientId = ref(null)
const messageType = ref('cold_intro')
const generating = ref(false)
const result = ref(null)
const editing = ref(false)
const editData = ref({})
const history = ref([])

const filteredHistory = computed(() => {
  return history.value
    .filter(item => item.clientId === selectedClientId.value && item.type === activeTab.value)
    .reverse()
})

function tabLabel(key) {
  const tab = tabs.find(t => t.key === key)
  return tab ? `${tab.icon} ${tab.label}` : key
}

function formatTime(d) {
  return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function addToHistory(data) {
  history.value.push({
    ...data,
    clientId: selectedClientId.value,
    type: activeTab.value,
    time: formatTime(new Date())
  })
}

function loadHistory(item) {
  if (item.type === 'email') {
    result.value = { subject: item.subject, body: item.body }
  } else {
    result.value = { message: item.message }
  }
  editing.value = false
}

async function generateContent() {
  if (!selectedClientId.value) return
  generating.value = true
  result.value = null
  editing.value = false

  try {
    if (activeTab.value === 'email') {
      const res = await outreachApi.generateEmail({ client_id: selectedClientId.value, message_type: messageType.value })
      result.value = res.data || res
      addToHistory({ subject: result.value.subject, body: result.value.body })
    } else if (activeTab.value === 'whatsapp') {
      const res = await outreachApi.generateWhatsapp({ client_id: selectedClientId.value, message_type: messageType.value })
      result.value = res.data || res
      addToHistory({ message: result.value.message })
    } else {
      const res = await outreachApi.generateLinkedin({ client_id: selectedClientId.value })
      result.value = res.data || res
      addToHistory({ message: result.value.message })
    }
    window.showToast?.('内容生成成功', 'success')
  } catch (err) {
    console.error(err)
    window.showToast?.('生成失败: ' + (err.response?.data?.detail || err.message), 'error')
  } finally {
    generating.value = false
  }
}

function getCopyText() {
  if (!result.value) return ''
  if (activeTab.value === 'email') {
    return `主题: ${result.value.subject}\n\n${result.value.body}`
  }
  return result.value.message
}

async function copyContent() {
  try {
    await window.navigator.clipboard.writeText(getCopyText())
    window.showToast?.('已复制到剪贴板', 'success')
  } catch {
    window.showToast?.('复制失败', 'error')
  }
}

function startEdit() {
  editing.value = true
  editData.value = { ...result.value }
}

function saveEdit() {
  result.value = { ...editData.value }
  editing.value = false
  window.showToast?.('已保存', 'success')
}

function cancelEdit() {
  editing.value = false
  editData.value = {}
}

function clearResult() {
  result.value = null
  editing.value = false
  editData.value = {}
}

onMounted(async () => {
  try {
    const res = await clientsApi.list({})
    clients.value = res.clients || res
  } catch (err) {
    console.error('Failed to load clients:', err)
  }
})
</script>
