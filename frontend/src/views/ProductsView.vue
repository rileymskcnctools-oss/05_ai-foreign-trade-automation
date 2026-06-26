<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-gray-800">📦 产品管理</h2>
      <div class="flex gap-2">
        <button @click="showCreate = true"
                class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">
          + 新增产品
        </button>
        <button @click="exportCsv"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">
          📥 导出CSV
        </button>
      </div>
    </div>

    <!-- 搜索 & 筛选 -->
    <div class="flex gap-3 mb-4">
      <input v-model="query" @keyup.enter="loadProducts"
             class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
             placeholder="搜索产品名称、编码、关键词..." />
      <select v-model="selectedCategory" @change="loadProducts"
              class="px-4 py-2 border border-gray-300 rounded-lg text-sm bg-white">
        <option value="">全部分类</option>
        <option v-for="cat in categories" :key="cat.category" :value="cat.category">
          {{ cat.category }} ({{ cat.product_count }})
        </option>
      </select>
      <button @click="loadProducts"
              class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">
        搜索
      </button>
    </div>

    <!-- 产品表格 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-600">
            <tr>
              <th class="px-4 py-3 text-left font-medium">编码</th>
              <th class="px-4 py-3 text-left font-medium">产品名称</th>
              <th class="px-4 py-3 text-left font-medium">分类</th>
              <th class="px-4 py-3 text-left font-medium">材质</th>
              <th class="px-4 py-3 text-left font-medium">重量(kg)</th>
              <th class="px-4 py-3 text-left font-medium">使用场景</th>
              <th class="px-4 py-3 text-left font-medium">MOQ</th>
              <th class="px-4 py-3 text-left font-medium">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.product_code"
                class="border-t border-gray-100 hover:bg-gray-50 cursor-pointer"
                @click="openDetail(p.product_code)">
              <td class="px-4 py-3 font-mono text-primary-600">{{ p.product_code }}</td>
              <td class="px-4 py-3">{{ p.product_name_en }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-xs bg-blue-50 text-blue-700">{{ p.category }}</span>
              </td>
              <td class="px-4 py-3 text-gray-500">{{ p.material || '-' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ p.weight_kg || '-' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ p.use_scenario || '-' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ p.moq || '-' }}</td>
              <td class="px-4 py-3" @click.stop>
                <div class="flex gap-1">
                  <button @click="openDetail(p.product_code)" class="text-blue-500 hover:text-blue-700 px-1">👁</button>
                  <button @click="editProduct(p)" class="text-amber-500 hover:text-amber-700 px-1">✏️</button>
                  <button @click="deleteProduct(p)" class="text-red-500 hover:text-red-700 px-1">🗑</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="!products.length" class="px-6 py-12 text-center text-gray-400">暂无产品数据</div>
    </div>

    <!-- 产品详情弹窗 -->
    <Modal :show="showDetail" @close="showDetail = false" :title="detailTitle" size="lg">
      <div v-if="detailLoading" class="text-center py-8 text-gray-400">加载中...</div>
      <div v-else-if="detail">
        <!-- 查看模式 -->
        <div v-if="!editMode">
          <!-- 基本信息 -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <span class="text-xs text-gray-400">产品编码</span>
              <p class="text-sm font-mono font-semibold text-primary-600">{{ detail.product_code }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">状态</span>
              <p class="text-sm">
                <span class="px-2 py-0.5 rounded-full text-xs"
                      :class="detail.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'">
                  {{ detail.status || 'active' }}
                </span>
              </p>
            </div>
            <div>
              <span class="text-xs text-gray-400">英文名</span>
              <p class="text-sm">{{ detail.product_name_en || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">中文名</span>
              <p class="text-sm">{{ detail.product_name_cn || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">分类</span>
              <p class="text-sm">{{ detail.category || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">材质</span>
              <p class="text-sm">{{ detail.material || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">使用场景</span>
              <p class="text-sm">{{ detail.use_scenario || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">重量</span>
              <p class="text-sm">{{ detail.weight_kg || '-' }} kg</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">MOQ</span>
              <p class="text-sm">{{ detail.moq || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">交期(天)</span>
              <p class="text-sm">{{ detail.lead_time_days || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">包装方式</span>
              <p class="text-sm">{{ detail.packaging_type || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">每箱数量</span>
              <p class="text-sm">{{ detail.qty_per_carton || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">箱规(cm)</span>
              <p class="text-sm">{{ detail.carton_size_cm || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">表面处理</span>
              <p class="text-sm">{{ detail.surface_treatment || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">HS编码</span>
              <p class="text-sm font-mono">{{ detail.hs_code || '-' }}</p>
            </div>
            <div>
              <span class="text-xs text-gray-400">认证</span>
              <p class="text-sm">{{ detail.certification || '-' }}</p>
            </div>
          </div>

          <!-- 目标关键词 -->
          <div v-if="detail.target_keywords" class="mb-4">
            <span class="text-xs text-gray-400">🎯 目标关键词</span>
            <p class="mt-1 text-sm bg-gray-50 rounded-lg p-3">{{ detail.target_keywords }}</p>
          </div>

          <!-- 产品规格 -->
          <div v-if="detail.specifications" class="mb-4">
            <span class="text-xs text-gray-400">📐 产品规格</span>
            <pre class="mt-1 text-sm bg-gray-50 rounded-lg p-3 whitespace-pre-wrap">{{ detail.specifications }}</pre>
          </div>

          <!-- 尺寸图 -->
          <div v-if="detail.dimensions_image" class="mb-4">
            <span class="text-xs text-gray-400">🖼️ 尺寸图</span>
            <p class="mt-1 text-sm bg-gray-50 rounded-lg p-3">{{ detail.dimensions_image }}</p>
          </div>

          <!-- 卖点 (格式化显示) -->
          <div v-if="detail.selling_points" class="mb-4">
            <div class="flex items-center justify-between mb-1">
              <span class="text-xs text-gray-400">✨ 卖点</span>
              <button @click="spExpanded = true" class="text-xs text-primary-600 hover:text-primary-800">🔍 全屏查看</button>
            </div>
            <div class="mt-1 text-sm bg-gray-50 rounded-lg p-3 max-h-48 overflow-y-auto"
                 v-html="formatSellingPoints(detail.selling_points)">
            </div>
          </div>
          <!-- AI 生成区域 -->
          <div class="mt-6 border-t border-gray-200 pt-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-3">🤖 AI 内容生成</h4>
            <div class="flex flex-wrap gap-2 mb-4">
              <button @click="generateContent('seo')" :disabled="generating"
                      class="px-3 py-1.5 bg-blue-500 text-white rounded-lg text-xs hover:bg-blue-600 disabled:opacity-50 flex items-center gap-1">
                <span v-if="generating === 'seo'" class="animate-spin">⏳</span>
                <span v-else>🔤</span>
                {{ generating === 'seo' ? '生成中...' : 'SEO标题' }}
              </button>
              <button @click="generateContent('selling_points')" :disabled="generating"
                      class="px-3 py-1.5 bg-green-500 text-white rounded-lg text-xs hover:bg-green-600 disabled:opacity-50 flex items-center gap-1">
                <span v-if="generating === 'selling_points'" class="animate-spin">⏳</span>
                <span v-else>✨</span>
                {{ generating === 'selling_points' ? '生成中...' : '卖点提炼' }}
              </button>
              <button @click="generateContent('whatsapp')" :disabled="generating"
                      class="px-3 py-1.5 bg-emerald-500 text-white rounded-lg text-xs hover:bg-emerald-600 disabled:opacity-50 flex items-center gap-1">
                <span v-if="generating === 'whatsapp'" class="animate-spin">⏳</span>
                <span v-else>💬</span>
                {{ generating === 'whatsapp' ? '生成中...' : 'WhatsApp话术' }}
              </button>
              <button @click="generateContent('alibaba')" :disabled="generating"
                      class="px-3 py-1.5 bg-orange-500 text-white rounded-lg text-xs hover:bg-orange-600 disabled:opacity-50 flex items-center gap-1">
                <span v-if="generating === 'alibaba'" class="animate-spin">⏳</span>
                <span v-else>🏪</span>
                {{ generating === 'alibaba' ? '生成中...' : '阿里巴巴详情' }}
              </button>
            </div>

            <!-- AI 生成结果区域 -->
            <div v-if="genResult" class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200 p-4">
              <div class="flex items-center justify-between mb-2">
                <h5 class="text-sm font-semibold text-gray-700">
                  {{ genResultTitle }}
                </h5>
                <button @click="copyGenResult"
                        class="px-3 py-1 bg-white border border-gray-300 rounded-lg text-xs text-gray-600 hover:bg-gray-50 hover:border-gray-400 flex items-center gap-1 transition-colors">
                  <span v-if="copied">✅</span>
                  <span v-else>📋</span>
                  {{ copied ? '已复制' : '复制' }}
                </button>
              </div>
              <pre class="text-sm text-gray-700 whitespace-pre-wrap font-sans bg-white rounded-lg p-3 border border-gray-200 max-h-80 overflow-y-auto">{{ genResult }}</pre>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-2 mt-4">
            <button @click="switchToEdit" class="px-4 py-2 bg-amber-500 text-white rounded-lg text-sm hover:bg-amber-600">✏️ 编辑</button>
          </div>
        </div>

        <!-- 编辑模式 -->
        <div v-else>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="field in EDITABLE_FIELDS" :key="field.field">
              <label class="block text-xs text-gray-500 mb-1">{{ field.label }}</label>
              <input v-model="editForm[field.field]"
                     :type="field.type || 'text'"
                     :step="field.type === 'number' ? '0.01' : undefined"
                     class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
          </div>
          <!-- 规格 (多行) -->
          <div class="mt-4">
            <label class="block text-xs text-gray-500 mb-1">📐 产品规格 (多行)</label>
            <textarea v-model="editForm.specifications" rows="5"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none font-mono"></textarea>
          </div>
          <!-- 卖点 (多行) -->
          <div class="mt-4">
            <label class="block text-xs text-gray-500 mb-1">✨ 卖点 (多行)</label>
            <textarea v-model="editForm.selling_points" rows="5"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
          </div>
          <div class="flex gap-2 mt-4">
            <button @click="saveEdit" class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">💾 保存</button>
            <button @click="editMode = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm hover:bg-gray-300">取消</button>
          </div>
        </div>
      </div>
    </Modal>

    <!-- 新增产品弹窗 -->
    <Modal :show="showCreate" @close="showCreate = false" title="➕ 新增产品">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-xs text-gray-500 mb-1">产品编码 *</label>
          <input v-model="createForm.product_code" class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="GF-001" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">英文名 *</label>
          <input v-model="createForm.product_name_en" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">中文名</label>
          <input v-model="createForm.product_name_cn" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">分类 *</label>
          <select v-model="createForm.category" class="w-full px-3 py-2 border rounded-lg text-sm bg-white">
            <option value="">选择分类</option>
            <option v-for="cat in categories" :key="cat.category" :value="cat.category">{{ cat.category }}</option>
          </select>
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">材质</label>
          <input v-model="createForm.material" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">使用场景</label>
          <input v-model="createForm.use_scenario" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">重量(kg)</label>
          <input v-model="createForm.weight_kg" type="number" step="0.01" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">MOQ</label>
          <input v-model="createForm.moq" type="number" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div>
          <label class="block text-xs text-gray-500 mb-1">包装方式</label>
          <input v-model="createForm.packaging_type" class="w-full px-3 py-2 border rounded-lg text-sm" />
        </div>
        <div class="col-span-2">
          <label class="block text-xs text-gray-500 mb-1">产品规格</label>
          <textarea v-model="createForm.specifications" rows="3"
                    class="w-full px-3 py-2 border rounded-lg text-sm" placeholder="填写产品规格信息..."></textarea>
        </div>
      </div>
      <div class="flex gap-2 mt-4">
        <button @click="submitCreate" class="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700">创建</button>
        <button @click="showCreate = false" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">取消</button>
      </div>
    </Modal>
  </div>

    <!-- 卖点全屏弹窗 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="spExpanded" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/60">
          <div class="bg-white w-full max-w-4xl max-h-[90vh] rounded-xl shadow-2xl overflow-hidden flex flex-col">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800">✨ 产品卖点</h3>
              <div class="flex gap-2">
                <button @click="copySellingPoints" class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700">📋 复制</button>
                <button @click="spExpanded = false" class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700">✕ 关闭</button>
              </div>
            </div>
            <div class="flex-1 overflow-y-auto px-6 py-5 text-sm leading-relaxed space-y-3 selling-points"
                 v-html="formatSellingPoints(detail?.selling_points)">
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { productsApi } from '../api'
import Modal from '../components/Modal.vue'

// ── 可编辑字段定义（完整 29 项，与旧 HTMX 模板一致） ──
const EDITABLE_FIELDS = [
  { label: '英文名', field: 'product_name_en', type: 'text' },
  { label: '中文名', field: 'product_name_cn', type: 'text' },
  { label: '分类', field: 'category', type: 'text' },
  { label: '子分类', field: 'sub_category', type: 'text' },
  { label: '材质', field: 'material', type: 'text' },
  { label: '手柄材质', field: 'handle_material', type: 'text' },
  { label: '重量(kg)', field: 'weight_kg', type: 'number' },
  { label: '齿数', field: 'tine_count', type: 'number' },
  { label: '硬度', field: 'hardness', type: 'text' },
  { label: '表面处理', field: 'surface_treatment', type: 'text' },
  { label: 'MOQ', field: 'moq', type: 'number' },
  { label: '包装方式', field: 'packaging_type', type: 'text' },
  { label: '每箱数量', field: 'qty_per_carton', type: 'number' },
  { label: '箱规(cm)', field: 'carton_size_cm', type: 'text' },
  { label: '箱毛重(kg)', field: 'gw_per_carton_kg', type: 'number' },
  { label: '交期(天)', field: 'lead_time_days', type: 'number' },
  { label: '认证', field: 'certification', type: 'text' },
  { label: '关键词', field: 'target_keywords', type: 'text' },
  { label: '使用场景', field: 'use_scenario', type: 'text' },
  { label: '目标市场', field: 'target_markets', type: 'text' },
  { label: '卖点角度', field: 'selling_angle', type: 'text' },
  { label: '竞品参考', field: 'competitor_ref', type: 'text' },
  { label: 'HS编码', field: 'hs_code', type: 'text' },
  { label: '20ft装柜量', field: 'loading_qty_20ft', type: 'number' },
  { label: '40ft装柜量', field: 'loading_qty_40ft', type: 'number' },
  { label: '40HQ装柜量', field: 'loading_qty_40hq', type: 'number' },
  { label: '尺寸图路径', field: 'dimensions_image', type: 'text' },
]

// 生成类型的中文标题映射
const GEN_TITLES = {
  seo: '🔤 SEO 标题生成结果',
  selling_points: '✨ 卖点提炼结果',
  whatsapp: '💬 WhatsApp 话术结果',
  alibaba: '🏪 阿里巴巴详情结果',
}

// ── 卖点格式化函数 ──
function formatSellingPoints(text) {
  if (!text) return ''
  return text
    // **bold** → styled span
    .replace(/\*\*(.+?)\*\*/g, '<span class="font-semibold text-gray-900 block text-base mb-1">$1</span>')
    // Handle AX-001 style: section headers separated by " | "
    .split(/\s*\|\s*/)
    .map(section => {
      return section
        .split(/\n\s*\n/)
        .map(para => {
          const lines = para.trim().split(/\n/)
          const firstLine = lines[0].trim()
          const html = para.trim().replace(/\n/g, '<br>')
          // Feature/Benefit blocks → left color bar
          if (firstLine.startsWith('Feature:') || firstLine.startsWith('Benefit:')) {
            const color = firstLine.startsWith('Feature:') ? 'border-blue-400' : 'border-green-400'
            return `<div class="pl-3 ${color} border-l-2">${html}</div>`
          }
          // Plain text section header (short line, not starting with number, followed by Feature/Benefit)
          const isHeader = lines.length >= 2 &&
            firstLine.length < 60 &&
            !firstLine.startsWith('Feature') &&
            !firstLine.startsWith('Benefit') &&
            !firstLine.match(/^\d+\./) &&
            (para.includes('Feature:') || para.includes('Benefit:'))
          if (isHeader) {
            const rest = lines.slice(1).join('\n').trim()
            return `<div class="mb-2"><span class="font-semibold text-gray-900 block text-base mb-1">${firstLine}</span>${rest ? '<div class="mt-1">' + rest.replace(/\n/g, '<br>') + '</div>' : ''}</div>`
          }
          return `<div>${html}</div>`
        })
        .join('')
    })
    .join('<div class="border-t border-gray-200 my-3"></div>')
}

// ── 产品列表 ──
const products = ref([])
const categories = ref([])
const query = ref('')
const selectedCategory = ref('')

// ── 详情弹窗 ──
const showDetail = ref(false)
const detailCode = ref('')
const detail = ref(null)
const detailLoading = ref(false)
const editMode = ref(false)
const spExpanded = ref(false)
const editForm = ref({})
const generating = ref(null)

// ── AI 生成结果 ──
const genResult = ref('')
const genResultType = ref('')
const copied = ref(false)

const genResultTitle = computed(() => GEN_TITLES[genResultType.value] || '生成结果')
const detailTitle = computed(() => {
  if (!detail.value) return ''
  return `📦 ${detail.value.product_code} - ${detail.value.product_name_en || ''}`
})

// ── 新增弹窗 ──
const showCreate = ref(false)
const createForm = ref({
  product_code: '',
  product_name_en: '',
  product_name_cn: '',
  category: '',
  material: '',
  use_scenario: '',
  weight_kg: '',
  moq: '',
  packaging_type: '',
  specifications: '',
})

// ── 加载产品列表 ──
const loadProducts = async () => {
  try {
    const params = {}
    if (query.value) params.q = query.value
    if (selectedCategory.value) params.category = selectedCategory.value
    const data = await productsApi.list(params)
    products.value = data.results || data
  } catch (e) {
    console.error(e)
  }
}

// ── 加载分类 ──
const loadCategories = async () => {
  try {
    categories.value = await productsApi.categories()
  } catch (e) {
    console.error(e)
  }
}

// ── 打开产品详情 ──
const openDetail = async (code) => {
  detailCode.value = code
  showDetail.value = true
  detailLoading.value = true
  editMode.value = false
  genResult.value = ''
  genResultType.value = ''
  try {
    detail.value = await productsApi.get(code)
  } catch (e) {
    window.showToast('加载产品详情失败', 'error')
  }
  detailLoading.value = false
}

// ── 编辑产品 ──
const editProduct = async (p) => {
  // 先打开详情，再切换到编辑模式
  await openDetail(p.product_code)
  switchToEdit()
}

const switchToEdit = () => {
  editForm.value = { ...detail.value }
  editMode.value = true
}

const saveEdit = async () => {
  try {
    const data = { ...editForm.value }
    delete data.product_code
    delete data.id
    delete data.created_at
    delete data.updated_at
    // 清理空值
    Object.keys(data).forEach(k => {
      if (data[k] === '' || data[k] === null) delete data[k]
    })
    // 数字字段转换
    const numberFields = EDITABLE_FIELDS.filter(f => f.type === 'number').map(f => f.field)
    numberFields.forEach(f => {
      if (data[f] !== undefined && data[f] !== null && data[f] !== '') {
        data[f] = parseFloat(data[f])
      }
    })
    await productsApi.update(detailCode.value, data)
    window.showToast('✅ 产品已更新')
    editMode.value = false
    openDetail(detailCode.value)
    loadProducts()
  } catch (e) {
    window.showToast('更新失败: ' + (e.response?.data?.error || e.message), 'error')
  }
}

// ── 删除产品 ──
const deleteProduct = async (p) => {
  if (!confirm(`确定要删除 ${p.product_code} ${p.product_name_en} 吗？`)) return
  try {
    await productsApi.delete(p.product_code)
    window.showToast('✅ 已删除')
    loadProducts()
  } catch (e) {
    window.showToast('删除失败', 'error')
  }
}

// ── 新增产品 ──
const submitCreate = async () => {
  if (!createForm.value.product_code || !createForm.value.product_name_en || !createForm.value.category) {
    window.showToast('请填写必填字段（产品编码、英文名、分类）', 'error')
    return
  }
  try {
    const data = { ...createForm.value }
    if (data.weight_kg) data.weight_kg = parseFloat(data.weight_kg)
    if (data.moq) data.moq = parseInt(data.moq)
    // 清理空值
    Object.keys(data).forEach(k => {
      if (data[k] === '' || data[k] === null) delete data[k]
    })
    await productsApi.create(data)
    window.showToast('✅ 产品已创建')
    showCreate.value = false
    createForm.value = {
      product_code: '',
      product_name_en: '',
      product_name_cn: '',
      category: '',
      material: '',
      use_scenario: '',
      weight_kg: '',
      moq: '',
      packaging_type: '',
      specifications: '',
    }
    loadProducts()
  } catch (e) {
    window.showToast('创建失败: ' + (e.response?.data?.error || e.message), 'error')
  }
}

// ── AI 内容生成 ──
const copySellingPoints = () => {
  const text = detail.value?.selling_points || ""
  navigator.clipboard.writeText(text).then(() => window.showToast("✅ 已复制到剪贴板")).catch(() => window.showToast("复制失败", "error"))
}

const generateContent = async (type) => {
  generating.value = type
  genResult.value = ''
  genResultType.value = ''
  copied.value = false
  try {
    const result = await productsApi.generate(detailCode.value, type)
    // 显示生成结果（而不是仅 toast）
    genResult.value = result.content || result.text || result.result || JSON.stringify(result, null, 2)
    genResultType.value = type
    // 刷新详情数据（但保留 genResult）
    try {
      const freshDetail = await productsApi.get(detailCode.value)
      detail.value = freshDetail
    } catch (_) { /* ignore refresh error */ }
  } catch (e) {
    window.showToast('生成失败: ' + (e.response?.data?.error || e.message), 'error')
  }
  generating.value = null
}

// ── 复制生成结果 ──
const copyGenResult = async () => {
  try {
    await navigator.clipboard.writeText(genResult.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch (e) {
    // fallback
    const textarea = document.createElement('textarea')
    textarea.value = genResult.value
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  }
}

// ── 导出 CSV ──
const exportCsv = async () => {
  try {
    const blob = await productsApi.exportCsv()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'products_export.csv'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    window.showToast('导出失败', 'error')
  }
}

// ── 初始化 ──
onMounted(() => {
  loadProducts()
  loadCategories()
})
</script>
