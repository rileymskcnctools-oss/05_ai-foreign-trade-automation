<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-6">📈 数据分析</h2>

    <!-- Tab 切换 -->
    <div class="flex gap-2 mb-6">
      <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
              class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              :class="activeTab === tab.key ? 'bg-primary-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50 border'">
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- 产品分析 -->
    <div v-if="activeTab === 'products'">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">产品总数</p>
          <p class="text-2xl font-bold text-blue-600">{{ productData.overview?.total || '-' }}</p>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">分类数</p>
          <p class="text-2xl font-bold text-green-600">{{ productData.categories?.length || '-' }}</p>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">SEO覆盖率</p>
          <p class="text-2xl font-bold text-purple-600">{{ productData.seo?.coverage || '-' }}%</p>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <h3 class="text-base font-semibold text-gray-700 mb-4">分类分布</h3>
          <canvas ref="productCatChart" height="250"></canvas>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <h3 class="text-base font-semibold text-gray-700 mb-4">材质分布</h3>
          <canvas ref="productMatChart" height="250"></canvas>
        </div>
      </div>
    </div>

    <!-- 客户分析 -->
    <div v-if="activeTab === 'clients'">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">客户总数</p>
          <p class="text-2xl font-bold text-blue-600">{{ clientData.overview?.total || '-' }}</p>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">国家数</p>
          <p class="text-2xl font-bold text-green-600">{{ clientData.countries?.length || '-' }}</p>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <p class="text-sm text-gray-500">A级客户</p>
          <p class="text-2xl font-bold text-amber-600">{{ aClients }}</p>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <h3 class="text-base font-semibold text-gray-700 mb-4">客户国家分布</h3>
          <canvas ref="clientCountryChart" height="250"></canvas>
        </div>
        <div class="bg-white rounded-xl p-5 shadow-sm border">
          <h3 class="text-base font-semibold text-gray-700 mb-4">评级分布</h3>
          <canvas ref="clientGradeChart" height="250"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { Chart, DoughnutController, BarController, ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip } from 'chart.js'
import { analyticsApi } from '../api'

Chart.register(DoughnutController, BarController, ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip)

const tabs = [
  { key: 'products', label: '产品分析', icon: '📦' },
  { key: 'clients', label: '客户分析', icon: '👥' },
]
const activeTab = ref('products')
const productData = ref({})
const clientData = ref({})

const productCatChart = ref(null)
const productMatChart = ref(null)
const clientCountryChart = ref(null)
const clientGradeChart = ref(null)

const aClients = computed(() => {
  const scores = clientData.value.scores || []
  const a = scores.find(s => s.grade === 'A' || s.score_range?.startsWith('A'))
  return a?.count || 0
})

const renderProductCharts = async () => {
  await nextTick()
  if (productCatChart.value && productData.value.categories?.length) {
    new Chart(productCatChart.value, {
      type: 'doughnut',
      data: {
        labels: productData.value.categories.map(c => c.category),
        datasets: [{ data: productData.value.categories.map(c => c.count), backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'] }],
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } },
    })
  }
  if (productMatChart.value && productData.value.materials?.length) {
    new Chart(productMatChart.value, {
      type: 'bar',
      data: {
        labels: productData.value.materials.map(m => m.material),
        datasets: [{ label: '产品数', data: productData.value.materials.map(m => m.count), backgroundColor: '#3b82f6', borderRadius: 6 }],
      },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
    })
  }
}

const renderClientCharts = async () => {
  await nextTick()
  if (clientCountryChart.value && clientData.value.countries?.length) {
    new Chart(clientCountryChart.value, {
      type: 'doughnut',
      data: {
        labels: clientData.value.countries.map(c => c.country),
        datasets: [{ data: clientData.value.countries.map(c => c.count), backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'] }],
      },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } },
    })
  }
  if (clientGradeChart.value && clientData.value.scores?.length) {
    new Chart(clientGradeChart.value, {
      type: 'bar',
      data: {
        labels: clientData.value.scores.map(s => s.grade || s.score_range),
        datasets: [{ label: '客户数', data: clientData.value.scores.map(s => s.count), backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'], borderRadius: 6 }],
      },
      options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
    })
  }
}

watch(activeTab, async (tab) => {
  if (tab === 'products' && productData.value.overview) renderProductCharts()
  if (tab === 'clients' && clientData.value.overview) renderClientCharts()
})

onMounted(async () => {
  try {
    const [p, c] = await Promise.all([analyticsApi.products(), analyticsApi.clients()])
    productData.value = p
    clientData.value = c
    await renderProductCharts()
  } catch (e) { console.error('Analytics load error:', e) }
})
</script>
