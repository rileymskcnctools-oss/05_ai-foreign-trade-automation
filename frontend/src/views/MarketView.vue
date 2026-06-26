<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">🔍 市场研究</h2>
      <button @click="showGenerate = true" class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">+ 生成报告</button>
    </div>

    <!-- 报告列表 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
      <div v-for="report in reports" :key="report.id"
           class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow cursor-pointer"
           @click="openReport(report)">
        <div class="flex items-center justify-between mb-3">
          <span class="text-2xl">📊</span>
          <button @click.stop="deleteReport(report)" class="text-red-400 hover:text-red-600 text-sm">🗑</button>
        </div>
        <h3 class="font-semibold text-gray-800 mb-1 line-clamp-2">{{ report.report_title || report.title || 'Market Report' }}</h3>
        <p class="text-xs text-gray-400 mb-2">{{ report.country || report.target_market || '-' }} · {{ report.created_at?.split('T')[0] || '' }}</p>
        <p class="text-sm text-gray-500 line-clamp-3">{{ report.summary || report.executive_summary || '暂无摘要' }}</p>
        <div v-if="report.confidence" class="mt-3">
          <span class="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-700">置信度: {{ report.confidence }}/10</span>
        </div>
      </div>
      <div v-if="!reports.length" class="col-span-3 text-center py-12 text-gray-400">暂无市场报告，点击右上角生成</div>
    </div>

    <!-- 报告详情弹窗 -->
    <Modal :show="showDetail" @close="showDetail = false" :title="detailReport?.report_title || '报告详情'" size="xl">
      <div v-if="detailReport" class="prose max-w-none">
        <div class="whitespace-pre-wrap text-sm leading-relaxed">{{ detailReport.full_report || detailReport.summary || '暂无详细内容' }}</div>
      </div>
    </Modal>

    <!-- 生成报告弹窗 -->
    <Modal :show="showGenerate" @close="showGenerate = false" title="📊 生成市场研究报告">
      <div class="space-y-4">
        <div>
          <label class="block text-xs text-gray-500 mb-1">目标国家 *</label>
          <input v-model="genForm.country" class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="如: Ghana, Nigeria, Germany" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">额外需求</label>
          <textarea v-model="genForm.extra_context" rows="3" class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="如: 关注农业工具市场、竞争格局分析"></textarea>
        </div>
        <div class="flex gap-2">
          <button @click="generateReport" :disabled="generating"
                  class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm disabled:opacity-50">
            {{ generating ? '生成中...' : '🚀 开始生成' }}
          </button>
          <button @click="showGenerate = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">取消</button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marketApi } from '../api'
import Modal from '../components/Modal.vue'

const reports = ref([])
const showDetail = ref(false)
const detailReport = ref(null)
const showGenerate = ref(false)
const generating = ref(false)
const genForm = ref({ country: '', extra_context: '' })

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
  } catch (e) { window.showToast('删除失败', 'error') }
}

const generateReport = async () => {
  if (!genForm.value.country) { window.showToast('请填写目标国家', 'error'); return }
  generating.value = true
  try {
    const result = await marketApi.generateReport(genForm.value)
    window.showToast('✅ 报告已生成')
    showGenerate.value = false
    loadReports()
  } catch (e) { window.showToast('生成失败: ' + (e.response?.data?.error || e.message), 'error') }
  generating.value = false
}

const loadReports = async () => {
  try {
    const data = await marketApi.listReports()
    reports.value = data.reports || data
  } catch (e) {
    console.error('Load reports error:', e)
  }
}

onMounted(() => { loadReports() })
</script>
