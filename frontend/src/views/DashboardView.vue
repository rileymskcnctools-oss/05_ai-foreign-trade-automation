<template>
  <div>
    <h2 class="text-2xl font-bold text-gray-800 mb-6">📊 数据概览</h2>

    <!-- KPI 卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div v-for="kpi in kpis" :key="kpi.label"
           class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-400 uppercase tracking-wide">{{ kpi.label }}</p>
            <p class="text-2xl font-bold mt-1" :class="kpi.color">{{ kpi.value }}</p>
          </div>
          <span class="text-2xl opacity-60">{{ kpi.icon }}</span>
        </div>
      </div>
    </div>

    <!-- 图表区: 3个图并排 -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <!-- 产品分类 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-600 mb-3">📦 产品分类</h3>
        <div class="flex justify-center"><canvas ref="categoryChart" height="180"></canvas></div>
      </div>
      <!-- 客户国家分布 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-600 mb-3">🌍 客户国家分布</h3>
        <canvas ref="countryChart" height="180"></canvas>
      </div>
      <!-- Pipeline 阶段 -->
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <h3 class="text-sm font-semibold text-gray-600 mb-3">📈 客户 Pipeline</h3>
        <div class="flex justify-center"><canvas ref="pipelineChart" height="180"></canvas></div>
      </div>
    </div>

    <!-- 最近报价 + 待跟进 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <h3 class="text-base font-semibold text-gray-700 mb-4">💰 最近报价</h3>
        <div v-if="home.recent_quotations?.length" class="space-y-3">
          <div v-for="q in home.recent_quotations" :key="q.quotation_no"
               class="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
            <div>
              <p class="text-sm font-medium text-gray-800">{{ q.quotation_no }}</p>
              <p class="text-xs text-gray-400">{{ q.company_name }} · {{ q.country }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-semibold text-gray-700">${{ q.total_amount?.toLocaleString() }}</p>
              <span class="text-xs px-2 py-0.5 rounded-full"
                    :class="statusClass(q.status)">{{ q.status }}</span>
            </div>
          </div>
        </div>
        <p v-else class="text-sm text-gray-400">暂无报价记录</p>
      </div>

      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <h3 class="text-base font-semibold text-gray-700 mb-4">🔔 待跟进客户</h3>
        <div v-if="reminders.length" class="space-y-3">
          <div v-for="r in reminders.slice(0, 8)" :key="r.id || r.company_name"
               class="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
            <div>
              <p class="text-sm font-medium text-gray-800">{{ r.company_name || 'Unknown' }}</p>
              <p class="text-xs text-gray-400">{{ r.country }} · {{ r.reason || r.status }}</p>
            </div>
            <span class="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700">待跟进</span>
          </div>
        </div>
        <p v-else class="text-sm text-gray-400">暂无待跟进客户</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { Chart, DoughnutController, BarController, ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip } from 'chart.js'
import { dashboardApi, clientsApi, analyticsApi } from '../api'

Chart.register(DoughnutController, BarController, ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip)

const stats = ref({})
const home = ref({})
const reminders = ref([])
const countries = ref([])
const subCategories = ref([])
const categoryChart = ref(null)
const countryChart = ref(null)
const pipelineChart = ref(null)

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16']

const kpis = computed(() => [
  { label: '产品总数', value: stats.value.active_products ?? '-', icon: '📦', color: 'text-blue-600' },
  { label: '客户总数', value: stats.value.total_clients ?? '-', icon: '👥', color: 'text-green-600' },
  { label: '报价单数', value: stats.value.total_quotations ?? '-', icon: '💰', color: 'text-amber-600' },
  { label: '市场报告', value: stats.value.market_reports ?? '-', icon: '📊', color: 'text-purple-600' },
])

const statusClass = (status) => ({
  'bg-green-50 text-green-700': status === 'accepted',
  'bg-amber-50 text-amber-700': status === 'draft' || status === 'sent',
  'bg-red-50 text-red-700': status === 'rejected',
  'bg-gray-50 text-gray-700': !['accepted', 'draft', 'sent', 'rejected'].includes(status),
})

const renderCharts = () => {
  // 产品分类饼图
  if (categoryChart.value && subCategories.value.length) {
    const cats = subCategories.value
    new Chart(categoryChart.value, {
      type: 'doughnut',
      data: {
        labels: cats.map(c => c.name),
        datasets: [{
          data: cats.map(c => c.count),
          backgroundColor: COLORS,
          borderWidth: 2, borderColor: '#fff',
        }],
      },
      options: {
        responsive: true, cutout: '55%',
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } },
      },
    })
  }

  // 客户国家分布 (横向柱状图)
  if (countryChart.value && countries.value.length) {
    const sorted = [...countries.value].sort((a, b) => b.client_count - a.client_count)
    new Chart(countryChart.value, {
      type: 'bar',
      data: {
        labels: sorted.map(c => c.country),
        datasets: [{
          label: '客户数',
          data: sorted.map(c => c.client_count),
          backgroundColor: sorted.map((c, i) => COLORS[i % COLORS.length]),
          borderRadius: 4,
          barThickness: 16,
        }],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, ticks: { stepSize: 1, font: { size: 10 } } },
          y: { ticks: { font: { size: 10 } } },
        },
      },
    })
  }

  // Pipeline 阶段饼图
  if (pipelineChart.value && home.value.clients?.by_status?.length) {
    const statuses = home.value.clients.by_status
    new Chart(pipelineChart.value, {
      type: 'doughnut',
      data: {
        labels: statuses.map(s => s.status),
        datasets: [{
          data: statuses.map(s => s.count),
          backgroundColor: COLORS,
          borderWidth: 2, borderColor: '#fff',
        }],
      },
      options: {
        responsive: true, cutout: '55%',
        plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, padding: 8, font: { size: 11 } } } },
      },
    })
  }
}

onMounted(async () => {
  try {
    const [s, h, clientData] = await Promise.all([
      dashboardApi.getStats(),
      dashboardApi.getHome(),
      analyticsApi.clients(),
    ])
    stats.value = s
    home.value = h
    countries.value = clientData.countries || []
    const subCatResp = await fetch("/api/dashboard/sub-categories")
    const subCatData = await subCatResp.json()
    subCategories.value = subCatData.sub_categories || []
  } catch (e) {
    console.error('Dashboard load error:', e)
    window.showToast('加载仪表盘数据失败', 'error')
  }

  try {
    const r = await clientsApi.reminders()
    if (Array.isArray(r)) {
      reminders.value = r
    } else if (r && typeof r === 'object') {
      reminders.value = [
        ...(r.overdue_clients || []),
        ...(r.stale_clients || []),
        ...(r.upcoming_3_days || []),
      ]
    }
  } catch (e) { console.warn('Reminders load error:', e) }

  await nextTick()
  renderCharts()
})
</script>
