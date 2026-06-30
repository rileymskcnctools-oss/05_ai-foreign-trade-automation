<template>
  <div>
    <!-- 标题栏 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">🔍 市场研究工作台</h2>
        <p class="text-sm text-gray-500 mt-1">报告 {{ stats.report_count }} 篇 · 知识点 {{ stats.knowledge_count }} 条 · 覆盖 {{ stats.country_count }} 个市场</p>
      </div>
      <button @click="showGenerate = true" class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700 flex items-center gap-1">
        <span>+</span> 生成报告
      </button>
    </div>

    <!-- Tab 导航 -->
    <div class="flex gap-1 mb-6 border-b border-gray-200">
      <button v-for="tab in tabs" :key="tab.key"
        @click="activeTab = tab.key"
        :class="['px-4 py-2 text-sm font-medium rounded-t-lg transition-colors',
          activeTab === tab.key ? 'bg-white border border-b-white text-primary-700 -mb-px' : 'text-gray-500 hover:text-gray-700']">
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- ==================== Tab 1: 报告列表 ==================== -->
    <div v-if="activeTab === 'reports'">
      <!-- 搜索栏 -->
      <div class="flex gap-3 mb-4">
        <input v-model="reportFilter.keyword" @input="debounceLoadReports"
          class="flex-1 px-3 py-2 border rounded-lg text-sm" placeholder="🔍 搜索报告（国家、关键词）" />
        <select v-model="reportFilter.country" @change="loadReports" class="px-3 py-2 border rounded-lg text-sm">
          <option value="">全部国家</option>
          <option v-for="c in availableCountries" :key="c.country" :value="c.country">
            {{ c.country }} ({{ c.reports }})
          </option>
        </select>
      </div>

      <!-- 报告卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="report in reports" :key="report.id"
          class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow cursor-pointer group"
          @click="openReport(report)">
          <div class="flex items-center justify-between mb-3">
            <span class="text-2xl">📊</span>
            <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button @click.stop="exportReport(report)" class="text-blue-400 hover:text-blue-600 text-sm" title="导出">📥</button>
              <button @click.stop="deleteReport(report)" class="text-red-400 hover:text-red-600 text-sm" title="删除">🗑</button>
            </div>
          </div>
          <h3 class="font-semibold text-gray-800 mb-1 line-clamp-2">{{ report.report_title || 'Market Report' }}</h3>
          <p class="text-xs text-gray-400 mb-2">
            <span class="inline-block px-1.5 py-0.5 bg-gray-100 rounded text-gray-600 mr-1">{{ report.country }}</span>
            {{ report.created_at?.split('T')[0] || '' }}
          </p>
          <p class="text-sm text-gray-500 line-clamp-3">{{ report.summary || '暂无摘要' }}</p>
          <div v-if="report.confidence" class="mt-3 flex items-center gap-2">
            <span :class="['text-xs px-2 py-0.5 rounded-full',
              report.confidence === 'high' ? 'bg-green-50 text-green-700' :
              report.confidence === 'medium' ? 'bg-yellow-50 text-yellow-700' : 'bg-red-50 text-red-700']">
              置信度: {{ report.confidence }}
            </span>
          </div>
        </div>
        <div v-if="!reports.length" class="col-span-3 text-center py-12 text-gray-400">
          暂无市场报告，点击右上角"生成报告"开始
        </div>
      </div>
    </div>

    <!-- ==================== Tab 2: 知识库 ==================== -->
    <div v-if="activeTab === 'knowledge'">
      <!-- 筛选栏 -->
      <div class="flex gap-3 mb-4">
        <input v-model="kbFilter.keyword" @input="debounceLoadKnowledge"
          class="flex-1 px-3 py-2 border rounded-lg text-sm" placeholder="🔍 搜索知识点" />
        <select v-model="kbFilter.country" @change="loadKnowledge" class="px-3 py-2 border rounded-lg text-sm">
          <option value="">全部国家</option>
          <option v-for="c in kbStats.by_country || []" :key="c.country" :value="c.country">
            {{ c.country }} ({{ c.count }})
          </option>
        </select>
        <select v-model="kbFilter.category" @change="loadKnowledge" class="px-3 py-2 border rounded-lg text-sm">
          <option value="">全部类别</option>
          <option v-for="c in kbStats.by_category || []" :key="c.category" :value="c.category">
            {{ categoryLabel(c.category) }} ({{ c.count }})
          </option>
        </select>
      </div>

      <!-- 类别标签 -->
      <div class="flex flex-wrap gap-2 mb-4">
        <button @click="kbFilter.category = ''; loadKnowledge()"
          :class="['px-3 py-1 rounded-full text-xs transition-colors',
            !kbFilter.category ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200']">
          全部
        </button>
        <button v-for="c in kbStats.by_category || []" :key="c.category"
          @click="kbFilter.category = c.category; loadKnowledge()"
          :class="['px-3 py-1 rounded-full text-xs transition-colors',
            kbFilter.category === c.category ? 'bg-primary-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200']">
          {{ categoryLabel(c.category) }} {{ c.count }}
        </button>
      </div>

      <!-- 知识卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div v-for="item in knowledge" :key="item.id"
          class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-lg">{{ categoryIcon(item.category) }}</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">{{ categoryLabel(item.category) }}</span>
            <span class="text-xs text-gray-400">{{ item.country }}</span>
            <span v-if="item.verified" class="text-xs text-green-600">✓ 已验证</span>
          </div>
          <p class="text-sm text-gray-700 leading-relaxed">{{ item.knowledge }}</p>
          <p class="text-xs text-gray-400 mt-2">{{ item.created_at?.split('T')[0] || '' }} · {{ item.source }}</p>
        </div>
        <div v-if="!knowledge.length" class="col-span-2 text-center py-12 text-gray-400">
          暂无知识点，生成报告时会自动提取
        </div>
      </div>
    </div>

    <!-- ==================== Tab 3: 市场对比 ==================== -->
    <div v-if="activeTab === 'compare'">
      <!-- 国家选择 -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 mb-6">
        <h3 class="font-semibold text-gray-800 mb-3">选择对比市场（至少选2个）</h3>
        <div class="flex flex-wrap gap-2 mb-3">
          <button v-for="c in availableCountries" :key="c.country"
            @click="toggleCompareCountry(c.country)"
            :class="['px-3 py-1.5 rounded-lg text-sm border transition-colors',
              compareCountries.includes(c.country) ? 'bg-primary-600 text-white border-primary-600' : 'bg-white text-gray-600 border-gray-200 hover:border-primary-300']">
            {{ c.country }}
            <span class="text-xs opacity-70">({{ c.reports }}报告/{{ c.knowledge }}知识点)</span>
          </button>
        </div>
        <button @click="runCompare" :disabled="compareCountries.length < 2 || comparing"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm disabled:opacity-50">
          {{ comparing ? '对比中...' : '🔍 开始对比' }}
        </button>
      </div>

      <!-- 对比结果 -->
      <div v-if="compareResult" class="space-y-6">
        <!-- 概览表格 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-5 py-3 bg-gray-50 border-b">
            <h3 class="font-semibold text-gray-800">📊 市场概览对比</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-gray-50">
                  <th class="px-4 py-2 text-left font-medium text-gray-600">维度</th>
                  <th v-for="c in compareResult.countries" :key="c.country"
                    class="px-4 py-2 text-left font-medium text-gray-600">{{ c.country }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr>
                  <td class="px-4 py-2 text-gray-500">报告状态</td>
                  <td v-for="c in compareResult.countries" :key="c.country" class="px-4 py-2">
                    <span :class="c.has_report ? 'text-green-600' : 'text-gray-400'">
                      {{ c.has_report ? '✅ 已有报告' : '❌ 暂无' }}
                    </span>
                  </td>
                </tr>
                <tr>
                  <td class="px-4 py-2 text-gray-500">置信度</td>
                  <td v-for="c in compareResult.countries" :key="c.country" class="px-4 py-2">
                    <span :class="['px-2 py-0.5 rounded-full text-xs',
                      c.confidence === 'high' ? 'bg-green-50 text-green-700' :
                      c.confidence === 'medium' ? 'bg-yellow-50 text-yellow-700' : 'bg-gray-50 text-gray-500']">
                      {{ c.confidence || '-' }}
                    </span>
                  </td>
                </tr>
                <tr>
                  <td class="px-4 py-2 text-gray-500">知识点数</td>
                  <td v-for="c in compareResult.countries" :key="c.country" class="px-4 py-2 font-medium">
                    {{ c.knowledge_count }}
                  </td>
                </tr>
                <tr>
                  <td class="px-4 py-2 text-gray-500">已有客户</td>
                  <td v-for="c in compareResult.countries" :key="c.country" class="px-4 py-2 font-medium">
                    {{ c.client_count }}
                  </td>
                </tr>
                <tr>
                  <td class="px-4 py-2 text-gray-500">报告摘要</td>
                  <td v-for="c in compareResult.countries" :key="c.country" class="px-4 py-2 text-xs text-gray-600 max-w-xs">
                    {{ c.summary || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 知识点对比 -->
        <div v-for="cat in compareKnowledgeCategories" :key="cat"
          class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-5 py-3 bg-gray-50 border-b">
            <h3 class="font-semibold text-gray-800">{{ categoryIcon(cat) }} {{ categoryLabel(cat) }}</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 divide-x divide-gray-100">
            <div v-for="c in compareResult.countries" :key="c.country" class="p-4">
              <h4 class="font-medium text-gray-700 mb-2 text-sm">{{ c.country }}</h4>
              <ul v-if="c.knowledge[cat]?.length" class="space-y-1">
                <li v-for="(k, i) in c.knowledge[cat]" :key="i" class="text-xs text-gray-600 pl-3 relative before:content-['•'] before:absolute before:left-0 before:text-primary-500">
                  {{ k }}
                </li>
              </ul>
              <p v-else class="text-xs text-gray-400">暂无数据</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==================== 报告详情弹窗 ==================== -->
    <Modal :show="showDetail" @close="showDetail = false" :title="detailReport?.report_title || '报告详情'" size="xl">
      <div v-if="detailReport">
        <!-- 报告头部信息 -->
        <div class="flex items-center justify-between mb-4 pb-4 border-b">
          <div class="flex items-center gap-3">
            <span class="text-3xl">📊</span>
            <div>
              <h3 class="font-bold text-lg">{{ detailReport.report_title }}</h3>
              <p class="text-sm text-gray-500">
                {{ detailReport.country }} · {{ detailReport.product_category }} · {{ detailReport.created_at?.split('T')[0] }}
                <span :class="['ml-2 px-2 py-0.5 rounded-full text-xs',
                  detailReport.confidence === 'high' ? 'bg-green-50 text-green-700' :
                  detailReport.confidence === 'medium' ? 'bg-yellow-50 text-yellow-700' : 'bg-red-50 text-red-700']">
                  置信度: {{ detailReport.confidence }}
                </span>
              </p>
            </div>
          </div>
          <!-- 放大按钮 -->
          <button @click="fullscreenReport = detailReport"
            class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors" title="放大阅读">
            🔍
          </button>
        </div>

        <!-- 摘要 -->
        <div v-if="detailReport.summary" class="mb-4 p-3 bg-blue-50 rounded-lg">
          <h4 class="text-sm font-semibold text-blue-800 mb-1">📝 摘要</h4>
          <p class="text-sm text-blue-900">{{ detailReport.summary }}</p>
        </div>

        <!-- 完整报告（markdown渲染） -->
        <div class="prose max-w-none mb-6 report-content"
          v-html="renderMarkdown(detailReport.full_report || '暂无详细内容')">
        </div>

        <!-- 关联知识点 -->
        <div v-if="detailReport.knowledge_entries?.length" class="mt-4 pt-4 border-t">
          <h4 class="font-semibold text-gray-800 mb-3">🧠 关联知识点 ({{ detailReport.knowledge_entries.length }}条)</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div v-for="k in detailReport.knowledge_entries" :key="k.id"
              class="bg-gray-50 rounded-lg p-3 text-sm">
              <span class="text-xs px-1.5 py-0.5 rounded bg-blue-100 text-blue-700 mr-2">{{ categoryLabel(k.category) }}</span>
              <span class="text-gray-700">{{ k.knowledge }}</span>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex gap-2 mt-4 pt-4 border-t">
          <button @click="exportReport(detailReport, 'md')" class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">📥 导出 MD</button>
          <button @click="exportReport(detailReport, 'pdf')" class="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700">📄 导出 PDF</button>
          <button @click="fullscreenReport = detailReport" class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">🔍 全屏阅读</button>
          <button @click="showDetail = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">关闭</button>
        </div>
      </div>
    </Modal>

    <!-- ==================== 全屏阅读模式 ==================== -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="fullscreenReport" class="fixed inset-0 z-50 bg-white overflow-y-auto">
          <!-- 顶部工具栏 -->
          <div class="sticky top-0 z-10 bg-white border-b shadow-sm">
            <div class="max-w-5xl mx-auto px-6 py-3 flex items-center justify-between">
              <div>
                <h2 class="font-bold text-xl text-gray-800">{{ fullscreenReport.report_title }}</h2>
                <p class="text-sm text-gray-500">
                  {{ fullscreenReport.country }} · {{ fullscreenReport.product_category }} · {{ fullscreenReport.created_at?.split('T')[0] }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <button @click="exportReport(fullscreenReport, 'md')" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">📥 MD</button>
                <button @click="exportReport(fullscreenReport, 'pdf')" class="px-3 py-1.5 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700">📄 PDF</button>
                <button @click="fullscreenReport = null" class="px-3 py-1.5 bg-gray-100 text-gray-600 rounded-lg text-sm hover:bg-gray-200">✕ 退出全屏</button>
              </div>
            </div>
          </div>
          <!-- 报告内容 -->
          <div class="max-w-5xl mx-auto px-6 py-8">
            <div v-if="fullscreenReport.summary" class="mb-6 p-4 bg-blue-50 rounded-xl border border-blue-100">
              <h4 class="text-sm font-semibold text-blue-800 mb-2">📝 摘要</h4>
              <p class="text-base text-blue-900 leading-relaxed">{{ fullscreenReport.summary }}</p>
            </div>
            <div class="report-content-fullscreen" v-html="renderMarkdown(fullscreenReport.full_report || '暂无详细内容')">
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- ==================== 生成报告弹窗 ==================== -->
    <Modal :show="showGenerate" @close="showGenerate = false" title="📊 生成市场研究报告">
      <div class="space-y-4">
        <div>
          <label class="block text-xs text-gray-500 mb-1">目标国家 *</label>
          <input v-model="genForm.country" class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="如: Ghana, Nigeria, Germany" />
          <!-- 常用市场快捷选择 -->
          <div class="flex flex-wrap gap-1 mt-2">
            <button v-for="c in quickCountries" :key="c"
              @click="genForm.country = c"
              :class="['px-2 py-0.5 rounded text-xs border',
                genForm.country === c ? 'bg-primary-600 text-white border-primary-600' : 'bg-white text-gray-500 border-gray-200 hover:border-primary-300']">
              {{ c }}
            </button>
          </div>
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">产品类别</label>
          <select v-model="genForm.product_category" class="w-full px-3 py-2 border rounded-lg text-sm">
            <option>Manual Farm Tools</option>
            <option>Garden Tools</option>
            <option>Agricultural Equipment</option>
            <option>Hardware Tools</option>
            <option>Construction Tools</option>
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">额外需求</label>
          <textarea v-model="genForm.extra_context" rows="3" class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="如: 关注农业工具市场、竞争格局分析、重点分析西非市场"></textarea>
        </div>
        <div class="flex gap-2">
          <button @click="generateReport" :disabled="generating"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm disabled:opacity-50">
            {{ generating ? '⏳ 生成中（约30秒）...' : '🚀 开始生成' }}
          </button>
          <button @click="showGenerate = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">取消</button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { marketApi } from '../api'
import Modal from '../components/Modal.vue'

// ========== 状态 ==========
const activeTab = ref('reports')
const tabs = [
  { key: 'reports', icon: '📊', label: '市场报告' },
  { key: 'knowledge', icon: '🧠', label: '知识库' },
  { key: 'compare', icon: '⚖️', label: '市场对比' },
]

// 报告
const reports = ref([])
const reportFilter = reactive({ keyword: '', country: '' })
const showDetail = ref(false)
const detailReport = ref(null)
const fullscreenReport = ref(null)
const showGenerate = ref(false)
const generating = ref(false)
const genForm = ref({ country: '', product_category: 'Manual Farm Tools', extra_context: '' })
const stats = ref({ report_count: 0, knowledge_count: 0, country_count: 0 })
const availableCountries = ref([])
const quickCountries = ['Ghana', 'Nigeria', 'Kenya', 'Tanzania', 'South Africa', 'Germany', 'India', 'Myanmar', 'Philippines', 'Brazil']

// 知识库
const knowledge = ref([])
const kbFilter = reactive({ keyword: '', country: '', category: '' })
const kbStats = ref({ total: 0, by_country: [], by_category: [] })

// 市场对比
const compareCountries = ref([])
const compareResult = ref(null)
const comparing = ref(false)

// ========== Markdown 渲染 ==========
const renderMarkdown = (text) => {
  if (!text) return ''
  let html = text
    // 转义HTML
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    // 代码块
    .replace(/```[\s\S]*?```/g, (m) => `<pre class="bg-gray-900 text-gray-100 rounded-lg p-4 my-3 text-sm overflow-x-auto">${m.slice(3, -3).replace(/^\w+\n/, '')}</pre>`)
    // 行内代码
    .replace(/`([^`]+)`/g, '<code class="bg-gray-100 text-pink-600 px-1.5 py-0.5 rounded text-sm">$1</code>')
    // 标题
    .replace(/^#### (.+)$/gm, '<h4 class="text-base font-bold text-gray-800 mt-5 mb-2 pb-1 border-b border-gray-100">$1</h4>')
    .replace(/^### (.+)$/gm, '<h3 class="text-lg font-bold text-gray-800 mt-6 mb-3 pb-1 border-b border-gray-200">$1</h3>')
    .replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold text-gray-800 mt-8 mb-4 pb-2 border-b-2 border-primary-200">$1</h2>')
    .replace(/^# (.+)$/gm, '<h1 class="text-2xl font-bold text-gray-900 mt-8 mb-4 pb-2 border-b-2 border-primary-300">$1</h1>')
    // 粗体 + 斜体
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-gray-900">$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // 列表项
    .replace(/^[\s]*[-*] (.+)$/gm, '<li class="ml-4 pl-2 relative before:content-[\'▸\'] before:absolute before:-left-1 before:text-primary-500 before:text-xs mb-1">$1</li>')
    .replace(/^[\s]*\d+\. (.+)$/gm, '<li class="ml-4 pl-2 mb-1">$1</li>')
    // 换行
    .replace(/\n\n/g, '</p><p class="mb-3 leading-relaxed">')
    .replace(/\n/g, '<br>')

  // 包裹列表项
  html = html.replace(/(<li[^>]*>.*?<\/li>(\s*<br>)?)+/gs, (match) => {
    return '<ul class="space-y-1 my-3">' + match.replace(/<br>/g, '') + '</ul>'
  })

  return `<div class="mb-3 leading-relaxed">${html}</div>`
}

// ========== 工具函数 ==========
const categoryLabel = (cat) => {
  const map = { agriculture: '农业', import: '进口', competitor: '竞品', pricing: '定价', distribution: '分销', general: '综合' }
  return map[cat] || cat || '综合'
}
const categoryIcon = (cat) => {
  const map = { agriculture: '🌾', import: '🚢', competitor: '🏢', pricing: '💰', distribution: '📦', general: '📋' }
  return map[cat] || '📋'
}

let debounceTimer = null
const debounceLoadReports = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(loadReports, 300)
}

// ========== 报告操作 ==========
const loadReports = async () => {
  try {
    const params = {}
    if (reportFilter.keyword) params.keyword = reportFilter.keyword
    if (reportFilter.country) params.country = reportFilter.country
    const data = await marketApi.listReports(params)
    reports.value = data.reports || data
  } catch (e) { console.error('Load reports error:', e) }
}

const loadStats = async () => {
  try {
    const data = await fetch('/market/api/stats').then(r => r.json())
    stats.value = data
  } catch (e) { console.error('Load stats error:', e) }
}

const loadCountries = async () => {
  try {
    const data = await fetch('/market/api/compare/available-countries').then(r => r.json())
    availableCountries.value = data.countries || []
  } catch (e) { console.error('Load countries error:', e) }
}

const openReport = async (r) => {
  try {
    detailReport.value = await marketApi.getReport(r.id)
  } catch (e) {
    detailReport.value = r
  }
  showDetail.value = true
}

const deleteReport = async (r) => {
  if (!confirm('确定要删除此报告吗？')) return
  try {
    await marketApi.deleteReport(r.id)
    window.showToast('✅ 已删除')
    reports.value = reports.value.filter(x => x.id !== r.id)
    loadStats()
  } catch (e) { window.showToast('删除失败', 'error') }
}

const exportReport = async (r, format = 'md') => {
  try {
    const resp = await fetch(`/market/api/reports/${r.id}/export?format=${format}`)
    const blob = await resp.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `market_report_${r.country || 'unknown'}.${format}`
    a.click()
    URL.revokeObjectURL(url)
    window.showToast(`✅ ${format.toUpperCase()} 已导出`)
  } catch (e) { window.showToast('导出失败', 'error') }
}

const generateReport = async () => {
  if (!genForm.value.country) { window.showToast('请填写目标国家', 'error'); return }
  generating.value = true
  try {
    await marketApi.generateReport(genForm.value)
    window.showToast('✅ 报告已生成')
    showGenerate.value = false
    genForm.value = { country: '', product_category: 'Manual Farm Tools', extra_context: '' }
    loadReports()
    loadStats()
    loadCountries()
  } catch (e) { window.showToast('生成失败: ' + (e.response?.data?.error || e.message), 'error') }
  generating.value = false
}

// ========== 知识库操作 ==========
const loadKnowledge = async () => {
  try {
    const params = {}
    if (kbFilter.keyword) params.keyword = kbFilter.keyword
    if (kbFilter.country) params.country = kbFilter.country
    if (kbFilter.category) params.category = kbFilter.category
    const data = await marketApi.listKnowledge(params)
    knowledge.value = data.items || []
  } catch (e) { console.error('Load knowledge error:', e) }
}

const loadKbStats = async () => {
  try {
    const data = await marketApi.knowledgeStats()
    kbStats.value = data
  } catch (e) { console.error('Load kb stats error:', e) }
}

const debounceLoadKnowledge = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(loadKnowledge, 300)
}

// ========== 市场对比操作 ==========
const toggleCompareCountry = (country) => {
  const idx = compareCountries.value.indexOf(country)
  if (idx >= 0) compareCountries.value.splice(idx, 1)
  else compareCountries.value.push(country)
}

const compareKnowledgeCategories = computed(() => {
  if (!compareResult.value) return []
  const cats = new Set()
  for (const c of compareResult.value.countries) {
    for (const cat of Object.keys(c.knowledge || {})) {
      cats.add(cat)
    }
  }
  return [...cats]
})

const runCompare = async () => {
  if (compareCountries.value.length < 2) return
  comparing.value = true
  try {
    const data = await marketApi.compare(compareCountries.value.join(','))
    compareResult.value = data
  } catch (e) { window.showToast('对比失败', 'error') }
  comparing.value = false
}

// ========== 初始化 ==========
onMounted(() => {
  loadReports()
  loadStats()
  loadCountries()
  loadKnowledge()
  loadKbStats()
})
</script>

<style scoped>
/* 报告内容格式化 */
.report-content :deep(h1),
.report-content :deep(h2),
.report-content-fullscreen :deep(h1),
.report-content-fullscreen :deep(h2) {
  font-weight: 700;
  color: #1a202c;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e2e8f0;
}
.report-content :deep(h1) { font-size: 1.5rem; }
.report-content :deep(h2) { font-size: 1.25rem; }
.report-content-fullscreen :deep(h1) { font-size: 1.875rem; }
.report-content-fullscreen :deep(h2) { font-size: 1.5rem; }

.report-content :deep(h3),
.report-content-fullscreen :deep(h3) {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
  margin-top: 1.25rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid #e2e8f0;
}

.report-content :deep(h4),
.report-content-fullscreen :deep(h4) {
  font-size: 1rem;
  font-weight: 700;
  color: #2d3748;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

.report-content :deep(p),
.report-content-fullscreen :deep(p) {
  margin-bottom: 0.75rem;
  line-height: 1.75;
  color: #4a5568;
}

.report-content :deep(ul),
.report-content-fullscreen :deep(ul) {
  margin: 0.75rem 0;
  padding-left: 1rem;
}

.report-content :deep(li),
.report-content-fullscreen :deep(li) {
  line-height: 1.75;
  color: #4a5568;
  margin-bottom: 0.25rem;
}

.report-content :deep(strong),
.report-content-fullscreen :deep(strong) {
  color: #1a202c;
  font-weight: 600;
}

.report-content :deep(pre),
.report-content-fullscreen :deep(pre) {
  background: #1a202c;
  color: #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  font-size: 0.875rem;
  overflow-x: auto;
}

.report-content :deep(code),
.report-content-fullscreen :deep(code) {
  background: #f7fafc;
  color: #e53e3e;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
}

/* 全屏模式字号更大 */
.report-content-fullscreen :deep(p),
.report-content-fullscreen :deep(li) {
  font-size: 1rem;
  line-height: 1.8;
}

.report-content-fullscreen :deep(h3) {
  font-size: 1.25rem;
  margin-top: 2rem;
}
</style>
