<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">👥 客户 CRM</h2>
        <p class="text-sm text-gray-500 mt-1">管理 {{ clientsList.length }} 个客户</p>
      </div>
      <div class="flex gap-3">
        <button @click="exportCsv"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium">
          ⬇️ 导出 CSV
        </button>
        <button @click="showCreate = true"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium">
          + 新建客户
        </button>
      </div>
    </div>

    <!-- Pipeline 概览 -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div v-for="(count, status) in pipeline" :key="status"
        class="bg-white rounded-xl border border-gray-200 p-4 card-hover">
        <p class="text-xs text-gray-500 uppercase">{{ status }}</p>
        <p class="text-xl font-bold text-gray-900">{{ count }}</p>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="bg-white rounded-xl border border-gray-200 p-4 mb-6">
      <div class="flex gap-3">
        <select v-model="filters.status" @change="loadClients"
          class="px-4 py-2 border border-gray-300 rounded-lg bg-white">
          <option value="">全部状态</option>
          <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
        </select>
        <select v-model="filters.grade" @change="loadClients"
          class="px-4 py-2 border border-gray-300 rounded-lg bg-white">
          <option value="">全部评级</option>
          <option v-for="g in ['A', 'B', 'C', 'D']" :key="g" :value="g">{{ g }}</option>
        </select>
      </div>
    </div>

    <!-- AI客户开发按钮 -->
    <button @click="showAIModal = true"
      class="mb-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm font-medium">
      🤖 AI客户开发
    </button>

    <!-- 客户列表 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-600">
            <tr>
              <th class="px-4 py-3 text-left font-medium">公司名</th>
              <th class="px-4 py-3 text-left font-medium">国家</th>
              <th class="px-4 py-3 text-left font-medium">联系人</th>
              <th class="px-4 py-3 text-left font-medium">邮箱</th>
              <th class="px-4 py-3 text-left font-medium">状态</th>
              <th class="px-4 py-3 text-left font-medium">评级</th>
              <th class="px-4 py-3 text-left font-medium">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in clientsList" :key="c.id" class="border-t border-gray-100 hover:bg-gray-50">
              <td class="px-4 py-3 font-medium">{{ c.company_name }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.country || '-' }}</td>
              <td class="px-4 py-3 text-gray-500">{{ c.contact_person || '-' }}</td>
              <td class="px-4 py-3 text-gray-500 text-xs">{{ c.email || '-' }}</td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-xs" :class="statusBadge(c.status)">{{ c.status }}</span>
              </td>
              <td class="px-4 py-3">
                <span class="px-2 py-0.5 rounded-full text-xs font-bold" :class="gradeBadge(c.grade)">{{ c.grade || '-' }}</span>
              </td>
              <td class="px-4 py-3" @click.stop>
                <div class="flex gap-1">
                  <button @click="openDetail(c)" class="text-blue-500 hover:text-blue-700 px-1" title="查看详情">👁</button>
                  <button @click="editClient(c)" class="text-amber-500 hover:text-amber-700 px-1" title="编辑">✏️</button>
                  <button @click="deleteClient(c)" class="text-red-500 hover:text-red-700 px-1" title="删除">🗑</button>
                  <button @click="analyzeClient(c)" :disabled="analyzing === c.id"
                    class="text-purple-500 hover:text-purple-700 px-1 disabled:opacity-50" title="AI分析">🤖</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="!clientsList.length" class="px-6 py-12 text-center text-gray-400">暂无客户数据</div>
    </div>

    <!-- ======================== SLIDE-OUT PANEL (客户详情) ======================== -->
    <Teleport to="body">
      <div v-if="showDetail" class="fixed inset-0 z-50">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black bg-opacity-30 transition-opacity"
          :class="detailVisible ? 'opacity-100' : 'opacity-0'"
          @click="closeDetail"></div>
        <!-- Slide panel -->
        <div ref="detailSlide"
          class="absolute top-0 right-0 h-full w-full max-w-2xl bg-white shadow-2xl overflow-y-auto transform transition-transform duration-300"
          :class="detailVisible ? 'translate-x-0' : 'translate-x-full'">
          <!-- Header -->
          <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between z-10">
            <div class="flex items-center gap-3">
              <h2 class="text-lg font-semibold text-gray-900">{{ detailClient?.company_name || '客户详情' }}</h2>
              <span v-if="detailClient?.grade"
                class="px-2 py-0.5 text-xs font-bold rounded-full"
                :class="GRADE_COLORS[detailClient.grade] || 'bg-gray-100 text-gray-700'">
                {{ detailClient.grade }}
              </span>
            </div>
            <button @click="closeDetail" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
          </div>
          <!-- Body -->
          <div v-if="detailClient" class="p-6 space-y-6">
            <!-- 联系信息卡片 -->
            <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 border border-blue-100">
              <h3 class="text-sm font-semibold text-gray-700 mb-3">📇 联系信息</h3>
              <div class="grid grid-cols-2 gap-3">
                <template v-for="f in contactFields" :key="f.label">
                  <div v-if="f.val" class="flex items-center gap-2 text-sm">
                    <span>{{ f.icon }}</span>
                    <span class="text-gray-500">{{ f.label }}:</span>
                    <a v-if="f.link" :href="f.link" target="_blank" class="text-primary-600 hover:underline truncate">{{ f.val }}</a>
                    <span v-else>{{ f.val }}</span>
                  </div>
                </template>
                <p v-if="!contactFields.some(f => f.val)" class="text-gray-400 text-sm col-span-2">暂无联系方式</p>
              </div>
            </div>
            <!-- 业务信息 -->
            <div class="bg-white rounded-xl border border-gray-200 p-5">
              <h3 class="text-sm font-semibold text-gray-700 mb-3">🏢 业务信息</h3>
              <div class="grid grid-cols-2 gap-3">
                <div v-for="f in bizFields" :key="f.label" class="text-sm">
                  <span class="text-gray-500">{{ f.label }}:</span>
                  <span class="font-medium ml-1">{{ f.val || '-' }}</span>
                </div>
                <div v-if="detailClient.notes" class="text-sm col-span-2">
                  <span class="text-gray-500">备注:</span>
                  <span class="ml-1">{{ detailClient.notes }}</span>
                </div>
              </div>
            </div>
            <!-- 跟进记录 -->
            <div class="bg-white rounded-xl border border-gray-200 p-5">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-semibold text-gray-700">📋 跟进记录</h3>
                <button @click="showAddActivity = true" class="text-xs text-primary-600 hover:text-primary-800 font-medium">+ 新增记录</button>
              </div>
              <div class="space-y-3">
                <div v-if="!activities.length" class="text-gray-400 text-sm">暂无跟进记录</div>
                <div v-for="a in activities" :key="a.id" class="flex gap-3 p-3 bg-gray-50 rounded-lg">
                  <span class="text-lg">{{ ACTIVITY_ICONS[a.activity_type] || '📋' }}</span>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2">
                      <span class="font-medium text-sm">{{ a.subject || a.activity_type }}</span>
                      <span class="text-xs text-gray-400">{{ a.direction === 'inbound' ? '←' : '→' }}</span>
                      <span class="text-xs text-gray-400 ml-auto">{{ a.created_at ? a.created_at.substring(0, 16) : '' }}</span>
                    </div>
                    <p v-if="a.content" class="text-xs text-gray-600 mt-1 truncate">{{ a.content }}</p>
                    <span v-if="a.follow_up_date" class="text-xs text-orange-500 mt-1 inline-block">⏰ 跟进: {{ a.follow_up_date }}</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- AI 背调 -->
            <div class="bg-white rounded-xl border border-gray-200 p-5">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-sm font-semibold text-gray-700">🤖 AI 客户分析</h3>
                <button @click="runAnalysis" :disabled="analyzingDetail"
                  class="px-3 py-1.5 bg-purple-600 text-white text-xs rounded-lg hover:bg-purple-700 font-medium disabled:opacity-50">
                  {{ analyzingDetail ? '⏳ 分析中...' : '🔍 运行背调' }}
                </button>
              </div>
              <div v-if="latestAnalysis">
                <div v-if="latestAnalysis.summary" class="bg-purple-50 rounded-lg p-4 mb-3">
                  <p class="text-sm text-purple-900 whitespace-pre-wrap">{{ latestAnalysis.summary }}</p>
                </div>
                <div v-if="latestAnalysis.recommendations" class="bg-green-50 rounded-lg p-4 mb-3">
                  <h4 class="text-xs font-semibold text-green-700 mb-1">💡 建议</h4>
                  <p class="text-sm text-green-900 whitespace-pre-wrap">{{ latestAnalysis.recommendations }}</p>
                </div>
                <div v-if="latestAnalysis.grade_suggested" class="text-xs text-gray-500">
                  建议评级: <span class="font-bold">{{ latestAnalysis.grade_suggested }}</span>
                  · 分析时间: {{ latestAnalysis.created_at || '-' }}
                </div>
              </div>
              <p v-else class="text-sm text-gray-500">点击"运行背调"开始 AI 分析</p>
            </div>
            <!-- 快捷操作 -->
            <div class="flex gap-3">
              <button @click="openEditFromDetail"
                class="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm font-medium">
                ✏️ 编辑客户
              </button>
              <button @click="closeDetail"
                class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm">
                关闭
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ======================== 新增客户弹窗 ======================== -->
    <Teleport to="body">
      <Modal :show="showCreate" @close="showCreate = false" title="新建客户">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">公司名 *</label>
            <input v-model="createForm.company_name" required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">国家 *</label>
            <input v-model="createForm.country" required
              class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">联系人</label>
            <input v-model="createForm.contact_person"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
            <input v-model="createForm.email" type="email"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">WhatsApp</label>
            <input v-model="createForm.whatsapp"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">来源</label>
            <select v-model="createForm.source"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white">
              <option value="alibaba">阿里巴巴</option>
              <option value="exhibition">展会</option>
              <option value="referral">转介绍</option>
              <option value="cold_outreach">主动开发</option>
              <option value="other">其他</option>
            </select>
          </div>
        </div>
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">备注</label>
          <textarea v-model="createForm.notes" rows="2"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary-500"></textarea>
        </div>
        <div class="flex justify-end gap-3 mt-4">
          <button @click="showCreate = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
          <button @click="submitCreate"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">保存客户</button>
        </div>
      </Modal>
    </Teleport>

    <!-- ======================== 编辑客户弹窗 ======================== -->
    <Teleport to="body">
      <Modal :show="showEdit" @close="showEdit = false" title="编辑客户" size="lg">
        <div class="grid grid-cols-2 gap-4">
          <div v-for="field in editableFields" :key="field.field">
            <label class="block text-xs text-gray-500 mb-1">{{ field.label }}{{ field.required ? ' *' : '' }}</label>
            <select v-if="field.type === 'select'" v-model="editForm[field.field]"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white">
              <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
            <textarea v-else-if="field.type === 'textarea'" v-model="editForm[field.field]" rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"></textarea>
            <input v-else v-model="editForm[field.field]" :required="field.required"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm outline-none focus:ring-2 focus:ring-primary-500" />
          </div>
        </div>
        <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-gray-200">
          <button @click="showEdit = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
          <button @click="saveEdit"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">💾 保存修改</button>
        </div>
      </Modal>
    </Teleport>

    <!-- ======================== 新增跟进记录弹窗 ======================== -->
    <Teleport to="body">
      <Modal :show="showAddActivity" @close="showAddActivity = false" title="📝 新增跟进记录">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">类型</label>
            <select v-model="activityForm.activity_type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white text-sm">
              <option value="email">📧 邮件</option>
              <option value="whatsapp">📱 WhatsApp</option>
              <option value="call">📞 电话</option>
              <option value="meeting">🤝 会面</option>
              <option value="note">📝 备注</option>
              <option value="quotation">💰 报价</option>
              <option value="sample">📦 寄样</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">方向</label>
            <select v-model="activityForm.direction"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white text-sm">
              <option value="outbound">→ 发出</option>
              <option value="inbound">← 收到</option>
            </select>
          </div>
        </div>
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">主题</label>
          <input v-model="activityForm.subject"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="如: 报价跟进" />
        </div>
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">内容</label>
          <textarea v-model="activityForm.content" rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" placeholder="记录详情..."></textarea>
        </div>
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">下次跟进日期</label>
          <input v-model="activityForm.follow_up_date" type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm" />
        </div>
        <div class="flex justify-end gap-3 mt-4">
          <button @click="showAddActivity = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 text-sm">取消</button>
          <button @click="submitActivity"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">保存</button>
        </div>
      </Modal>
    </Teleport>

    <!-- ======================== 删除确认弹窗 ======================== -->
    <Teleport to="body">
      <Modal :show="showDeleteConfirm" @close="showDeleteConfirm = false" title="确认删除">
        <p class="text-gray-700 mb-2">
          确定要删除客户 "<strong>{{ deleteTarget?.company_name }}</strong>" 吗？
        </p>
        <p class="text-sm text-red-600 mb-4">
          ⚠️ 此操作不可撤销，关联的跟进记录也会一并删除（级联删除）。
        </p>
        <div class="flex justify-end gap-3">
          <button @click="showDeleteConfirm = false"
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">取消</button>
          <button @click="confirmDelete"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">确认删除</button>
        </div>
      </Modal>
    </Teleport>

    <!-- ======================== AI客户开发弹窗 ======================== -->
    <Teleport to="body">
      <Modal :show="showAIModal" @close="showAIModal = false" title="🔍 AI客户开发" size="lg">
        <!-- Tab 切换 -->
        <div class="flex gap-1 mb-5 bg-gray-100 rounded-lg p-1">
          <button @click="aiTab = 'real'"
            class="flex-1 px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="aiTab === 'real' ? 'bg-white text-purple-700 shadow-sm' : 'text-gray-600 hover:text-gray-800'">
            🌐 真实搜索
          </button>
          <button @click="aiTab = 'fiction'"
            class="flex-1 px-4 py-2 rounded-md text-sm font-medium transition-colors"
            :class="aiTab === 'fiction' ? 'bg-white text-purple-700 shadow-sm' : 'text-gray-600 hover:text-gray-800'">
            🤖 AI虚构（练习用）
          </button>
        </div>

        <!-- 真实搜索面板 -->
        <div v-show="aiTab === 'real'">
          <div class="flex gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">搜索关键词 *</label>
              <input v-model="realSearch.query" type="text"
                placeholder="如: agricultural tools importer Nigeria"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div class="w-40">
              <label class="block text-sm font-medium text-gray-700 mb-1">目标国家</label>
              <input v-model="realSearch.country" type="text"
                placeholder="如: Nigeria"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div class="w-32">
              <label class="block text-sm font-medium text-gray-700 mb-1">搜索数量</label>
              <select v-model="realSearch.count"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-white">
                <option :value="5">5个</option>
                <option :value="8">8个</option>
                <option :value="12">12个</option>
              </select>
            </div>
            <div class="flex items-end">
              <button @click="searchRealClients" :disabled="aiSearching"
                class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium whitespace-nowrap disabled:opacity-50">
                {{ aiSearching ? '⏳ 搜索中...' : '🔍 搜索真实客户' }}
              </button>
            </div>
          </div>
          <div class="text-xs text-gray-500 mb-4">
            通过 Google 搜索目标市场的真实公司，抓取网站提取联系方式，AI 自动分析评级。
            搜索结果来自真实网页，联系方式可直接使用。
          </div>
          <div class="bg-gray-50 rounded-lg p-4 min-h-[100px]">
            <!-- 搜索结果 -->
            <div v-if="realResults.length">
              <div class="flex justify-between items-center mb-3">
                <p class="text-sm font-medium text-green-700">✅ 找到 {{ realResults.length }} 个真实公司</p>
                <button @click="batchInsert('real')"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium">
                  📥 一键录入CRM
                </button>
              </div>
              <div class="space-y-3">
                <div v-for="(c, i) in realResults" :key="i"
                  class="bg-white border border-gray-200 rounded-lg p-4">
                  <div class="flex justify-between items-start">
                    <div>
                      <p class="font-medium text-gray-900">
                        {{ c.company_name || 'Unknown' }}
                        <span v-if="c.email || c.phone || c.whatsapp || c.linkedin"
                          class="px-2 py-0.5 text-xs rounded-full bg-green-100 text-green-700 ml-1">有联系方式</span>
                        <span v-else
                          class="px-2 py-0.5 text-xs rounded-full bg-yellow-100 text-yellow-700 ml-1">需手动查找</span>
                        <span v-if="c.confidence === 'high'"
                          class="px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-700 ml-1">高可信</span>
                        <span v-else-if="c.confidence === 'medium'"
                          class="px-2 py-0.5 text-xs rounded-full bg-gray-100 text-gray-600 ml-1">中可信</span>
                      </p>
                      <p class="text-xs text-gray-500">{{ c.country || '' }} · {{ c.business_type || '' }}</p>
                    </div>
                    <span class="px-2 py-1 text-xs font-bold rounded-full"
                      :class="GRADE_COLORS[c.grade] || 'bg-yellow-100 text-yellow-700'">
                      {{ c.grade || 'C' }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mt-2">{{ c.analysis_notes || c.target_note || '' }}</p>
                  <div class="flex flex-wrap gap-3 mt-2 text-xs text-gray-500">
                    <span v-if="c.website">🌐 <a :href="c.website" target="_blank" class="text-blue-600 hover:underline">{{ c.website.length > 40 ? c.website.substring(0, 40) + '...' : c.website }}</a></span>
                    <span v-if="c.source" class="text-purple-600 font-medium">📌 {{ c.source }}</span>
                  </div>
                  <div v-if="c.contact_person || c.email || c.phone || c.whatsapp || c.linkedin"
                    class="flex flex-wrap gap-3 mt-1.5 text-xs text-gray-400">
                    <span v-if="c.contact_person">👤 {{ c.contact_person }}</span>
                    <span v-if="c.email">✉️ {{ c.email }}</span>
                    <span v-if="c.phone">📞 {{ c.phone }}</span>
                    <span v-if="c.whatsapp">📱 {{ c.whatsapp }}</span>
                    <span v-if="c.linkedin">💼 <a :href="c.linkedin" target="_blank" class="text-blue-500">LinkedIn</a></span>
                  </div>
                </div>
              </div>
            </div>
            <p v-else-if="!aiSearching" class="text-gray-400 text-sm">输入关键词点击搜索开始</p>
          </div>
        </div>

        <!-- AI虚构面板 -->
        <div v-show="aiTab === 'fiction'">
          <div class="flex gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">目标市场</label>
              <select v-model="fictionSearch.market"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-white">
                <option value="Africa">非洲</option>
                <option value="Europe">欧洲</option>
                <option value="Southeast Asia">东南亚</option>
                <option value="South America">南美</option>
                <option value="Middle East">中东</option>
                <option value="Global">全球</option>
              </select>
            </div>
            <div class="w-32">
              <label class="block text-sm font-medium text-gray-700 mb-1">生成数量</label>
              <select v-model="fictionSearch.count"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-white">
                <option :value="3">3个</option>
                <option :value="5">5个</option>
                <option :value="8">8个</option>
                <option :value="10">10个</option>
              </select>
            </div>
            <div class="flex items-end">
              <button @click="generateFictionClients" :disabled="aiGenerating"
                class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 font-medium disabled:opacity-50">
                {{ aiGenerating ? '⏳ AI生成中...' : '🤖 生成虚构客户' }}
              </button>
            </div>
          </div>
          <div class="bg-amber-50 border border-amber-200 rounded-lg p-3 mb-4">
            <p class="text-xs text-amber-700">⚠️ <strong>注意：</strong>此模式生成的是虚构数据，联系方式为AI编造，不可用于真实联系。仅适合 CRM 练习和流程测试。</p>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 min-h-[100px]">
            <!-- 虚构结果 -->
            <div v-if="fictionResults.length">
              <div class="flex justify-between items-center mb-3">
                <p class="text-sm font-medium text-green-700">✅ 生成了 {{ fictionResults.length }} 个虚构客户</p>
                <button @click="batchInsert('fiction')"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-medium">
                  📥 一键录入CRM
                </button>
              </div>
              <div class="space-y-3">
                <div v-for="(c, i) in fictionResults" :key="i"
                  class="bg-white border border-gray-200 rounded-lg p-4">
                  <div class="flex justify-between items-start">
                    <div>
                      <p class="font-medium text-gray-900">
                        {{ c.company_name }}
                        <span v-if="c.email || c.whatsapp || c.linkedin"
                          class="px-2 py-0.5 text-xs rounded-full bg-green-100 text-green-700 ml-1">有联系方式</span>
                        <span v-else
                          class="px-2 py-0.5 text-xs rounded-full bg-red-100 text-red-700 ml-1">无联系方式</span>
                      </p>
                      <p class="text-xs text-gray-500">{{ c.country || '' }} · {{ c.business_type || '' }}</p>
                    </div>
                    <span class="px-2 py-1 text-xs font-bold rounded-full"
                      :class="GRADE_COLORS[c.grade] || 'bg-yellow-100 text-yellow-700'">
                      {{ c.grade || 'C' }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-600 mt-2">{{ c.target_note || '' }}</p>
                  <div class="flex flex-wrap gap-3 mt-2 text-xs text-gray-500">
                    <span v-if="c.estimated_container_volume || c.estimated_annual_import_volume">📦 {{ c.estimated_container_volume || c.estimated_annual_import_volume }}</span>
                    <span v-if="c.main_products">🛒 {{ c.main_products }}</span>
                    <span v-if="c.source" class="text-purple-600 font-medium">📌 {{ c.source }}</span>
                    <span v-if="c.source_channel" class="text-indigo-500">🔗 {{ c.source_channel }}</span>
                  </div>
                  <div v-if="c.contact_person || c.email || c.whatsapp || c.linkedin"
                    class="flex flex-wrap gap-3 mt-1.5 text-xs text-gray-400">
                    <span v-if="c.contact_person">👤 {{ c.contact_person }}</span>
                    <span v-if="c.email">✉️ {{ c.email }}</span>
                    <span v-if="c.whatsapp">📱 {{ c.whatsapp }}</span>
                    <span v-if="c.linkedin">💼 {{ c.linkedin }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p v-else-if="!aiGenerating" class="text-gray-400 text-sm">点击"生成虚构客户"开始</p>
          </div>
        </div>
      </Modal>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { clientsApi } from '../api'
import Modal from '../components/Modal.vue'

// ==================== Constants ====================
const ACTIVITY_ICONS = {
  'email': '📧', 'whatsapp': '📱', 'call': '📞', 'meeting': '🤝',
  'note': '📝', 'quotation': '💰', 'sample': '📦',
}

const GRADE_COLORS = {
  'A': 'bg-green-100 text-green-700',
  'B': 'bg-blue-100 text-blue-700',
  'C': 'bg-yellow-100 text-yellow-700',
  'D': 'bg-red-100 text-red-700',
}

const statusOptions = ['lead', 'prospect', 'contacted', 'interested', 'quoted', 'negotiating', 'customer', 'lost']

// ==================== State ====================
const clientsList = ref([])
const filters = ref({ status: '', grade: '' })

// Detail slide-out panel
const showDetail = ref(false)
const detailVisible = ref(false)
const detailClient = ref(null)
const activities = ref([])
const latestAnalysis = ref(null)
const analyzingDetail = ref(false)

// Create
const showCreate = ref(false)
const createForm = ref({
  company_name: '', country: '', contact_person: '', email: '',
  whatsapp: '', source: 'alibaba', notes: ''
})

// Edit
const showEdit = ref(false)
const editForm = ref({})
const editingId = ref(null)
const editableFields = [
  { label: '公司名', field: 'company_name', required: true },
  { label: '国家', field: 'country', required: true },
  { label: '联系人', field: 'contact_person' },
  { label: '邮箱', field: 'email' },
  { label: 'WhatsApp', field: 'whatsapp' },
  { label: 'LinkedIn', field: 'linkedin' },
  { label: '网站', field: 'website' },
  { label: '业务类型', field: 'business_type' },
  { label: '主营产品', field: 'main_products' },
  { label: '目标市场', field: 'market_regions' },
  { label: '备注', field: 'notes', type: 'textarea' },
  { label: '状态', field: 'status', type: 'select', options: statusOptions },
  { label: '评级', field: 'grade', type: 'select', options: ['', 'A', 'B', 'C', 'D'] },
]

// Activity
const showAddActivity = ref(false)
const activityForm = ref({
  activity_type: 'email', direction: 'outbound',
  subject: '', content: '', follow_up_date: ''
})

// Delete
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)

// AI modal
const showAIModal = ref(false)
const aiTab = ref('real')
const aiSearching = ref(false)
const aiGenerating = ref(false)

const realSearch = ref({ query: '', country: '', count: 8 })
const realResults = ref([])
const fictionSearch = ref({ market: 'Africa', count: 5 })
const fictionResults = ref([])

// Analyzing (table row)
const analyzing = ref(null)

// ==================== Computed ====================
const pipeline = computed(() => {
  const counts = {}
  clientsList.value.forEach(c => {
    if (c.status) {
      counts[c.status] = (counts[c.status] || 0) + 1
    }
  })
  return counts
})

const contactFields = computed(() => {
  if (!detailClient.value) return []
  const c = detailClient.value
  return [
    { icon: '👤', label: '联系人', val: c.contact_person },
    { icon: '✉️', label: '邮箱', val: c.email, link: c.email ? `mailto:${c.email}` : '' },
    { icon: '📱', label: 'WhatsApp', val: c.whatsapp, link: c.whatsapp ? `https://wa.me/${c.whatsapp.replace(/[^0-9]/g, '')}` : '' },
    { icon: '📞', label: '电话', val: c.phone, link: c.phone ? `tel:${c.phone}` : '' },
    { icon: '💼', label: 'LinkedIn', val: c.linkedin, link: c.linkedin },
    { icon: '🌐', label: '网站', val: c.website, link: c.website },
  ]
})

const bizFields = computed(() => {
  if (!detailClient.value) return []
  const c = detailClient.value
  return [
    { label: '业务类型', val: c.business_type },
    { label: '主营产品', val: c.main_products },
    { label: '目标市场', val: c.market_regions },
    { label: '预估体量', val: c.estimated_volume },
    { label: '来源', val: c.source },
    { label: '状态', val: c.status },
  ]
})

// ==================== Badge helpers ====================
const statusBadge = (s) => ({
  'bg-green-50 text-green-700': s === 'customer',
  'bg-blue-50 text-blue-700': s === 'contacted' || s === 'negotiating' || s === 'quoted',
  'bg-gray-50 text-gray-700': s === 'lead' || s === 'prospect',
  'bg-yellow-50 text-yellow-700': s === 'interested',
  'bg-red-50 text-red-700': s === 'lost',
})

const gradeBadge = (g) => GRADE_COLORS[g] ? { [GRADE_COLORS[g]]: true } : {}

// ==================== Load data ====================
const loadClients = async () => {
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.grade) params.grade = filters.value.grade
    const data = await clientsApi.list(params)
    clientsList.value = data.clients || data || []
  } catch (e) {
    console.error('Failed to load clients:', e)
  }
}

// ==================== Detail panel ====================
const openDetail = async (c) => {
  detailClient.value = c
  showDetail.value = true
  activities.value = []
  latestAnalysis.value = null
  // Trigger slide-in animation
  await nextTick()
  detailVisible.value = true
  // Load full client data
  try {
    const full = await clientsApi.get(c.id)
    detailClient.value = full
  } catch (e) { /* keep original data */ }
  // Load activities
  try {
    const aData = await clientsApi.activities(c.id)
    activities.value = aData.activities || []
  } catch (e) { /* ignore */ }
  // Load analyses
  try {
    const anData = await clientsApi.analyses(c.id)
    const analyses = anData.analyses || []
    if (analyses.length) latestAnalysis.value = analyses[0]
  } catch (e) { /* ignore */ }
}

const closeDetail = () => {
  detailVisible.value = false
  setTimeout(() => {
    showDetail.value = false
    detailClient.value = null
  }, 300)
}

const openEditFromDetail = () => {
  const c = detailClient.value
  closeDetail()
  setTimeout(() => editClient(c), 350)
}

// ==================== Analysis ====================
const runAnalysis = async () => {
  if (!detailClient.value) return
  analyzingDetail.value = true
  try {
    const result = await clientsApi.analyze(detailClient.value.id)
    if (result.success) {
      latestAnalysis.value = result.analysis
      window.showToast('✅ 客户分析完成')
    } else {
      window.showToast('分析失败: ' + (result.error || ''), 'error')
    }
  } catch (e) {
    window.showToast('分析失败', 'error')
  }
  analyzingDetail.value = false
}

const analyzeClient = async (c) => {
  analyzing.value = c.id
  try {
    const result = await clientsApi.analyze(c.id)
    if (result.success) window.showToast('✅ AI分析完成')
    else window.showToast('分析失败: ' + (result.error || ''), 'error')
  } catch (e) {
    window.showToast('分析失败', 'error')
  }
  analyzing.value = null
}

// ==================== Create ====================
const submitCreate = async () => {
  if (!createForm.value.company_name || !createForm.value.country) {
    window.showToast('请填写公司名和国家', 'error')
    return
  }
  try {
    await clientsApi.create(createForm.value)
    window.showToast('✅ 客户已创建')
    showCreate.value = false
    createForm.value = { company_name: '', country: '', contact_person: '', email: '', whatsapp: '', source: 'alibaba', notes: '' }
    loadClients()
  } catch (e) {
    window.showToast('创建失败', 'error')
  }
}

// ==================== Edit ====================
const editClient = (c) => {
  editingId.value = c.id
  editForm.value = { ...c }
  showEdit.value = true
}

const saveEdit = async () => {
  try {
    const data = { ...editForm.value }
    delete data.id
    delete data.created_at
    delete data.updated_at
    await clientsApi.update(editingId.value, data)
    window.showToast('✅ 客户信息已更新')
    showEdit.value = false
    loadClients()
  } catch (e) {
    window.showToast('更新失败', 'error')
  }
}

// ==================== Delete ====================
const deleteClient = (c) => {
  deleteTarget.value = c
  showDeleteConfirm.value = true
}

const confirmDelete = async () => {
  if (!deleteTarget.value) return
  try {
    await clientsApi.delete(deleteTarget.value.id)
    window.showToast(`✅ 已删除 ${deleteTarget.value.company_name}`)
    showDeleteConfirm.value = false
    deleteTarget.value = null
    loadClients()
  } catch (e) {
    window.showToast('删除失败', 'error')
  }
}

// ==================== Activity ====================
const submitActivity = async () => {
  if (!detailClient.value) return
  try {
    const data = { ...activityForm.value }
    // Remove empty fields
    Object.keys(data).forEach(k => { if (!data[k]) delete data[k] })
    const result = await clientsApi.logActivity(detailClient.value.id, data)
    if (result.success) {
      window.showToast('✅ 跟进记录已添加')
      showAddActivity.value = false
      activityForm.value = { activity_type: 'email', direction: 'outbound', subject: '', content: '', follow_up_date: '' }
      // Reload activities
      const aData = await clientsApi.activities(detailClient.value.id)
      activities.value = aData.activities || []
    } else {
      window.showToast('保存失败', 'error')
    }
  } catch (e) {
    window.showToast('保存失败', 'error')
  }
}

// ==================== Export ====================
const exportCsv = async () => {
  try {
    const blob = await clientsApi.exportCsv()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'clients.csv'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    window.showToast('✅ CSV已导出')
  } catch (e) {
    window.showToast('导出失败', 'error')
  }
}

// ==================== AI Client Development ====================
const searchRealClients = async () => {
  if (!realSearch.value.query && !realSearch.value.country) {
    window.showToast('⚠️ 请输入搜索关键词或目标国家', 'error')
    return
  }
  aiSearching.value = true
  realResults.value = []
  try {
    const result = await clientsApi.searchReal({
      query: realSearch.value.query,
      country: realSearch.value.country,
      max_results: realSearch.value.count
    })
    if (result.success) {
      realResults.value = result.clients || []
      if (!realResults.value.length && result.raw && result.raw.length) {
        window.showToast('⚠️ AI分析未返回结构化数据，请查看原始结果', 'error')
      }
    } else {
      window.showToast('搜索失败: ' + (result.error || ''), 'error')
    }
  } catch (e) {
    window.showToast('搜索失败', 'error')
  }
  aiSearching.value = false
}

const generateFictionClients = async () => {
  aiGenerating.value = true
  fictionResults.value = []
  try {
    const result = await clientsApi.generatePotential({
      target_market: fictionSearch.value.market,
      count: fictionSearch.value.count
    })
    if (result.success) {
      fictionResults.value = result.clients || []
    } else {
      window.showToast('生成失败: ' + (result.error || ''), 'error')
    }
  } catch (e) {
    window.showToast('生成失败', 'error')
  }
  aiGenerating.value = false
}

const batchInsert = async (mode) => {
  const clients = mode === 'real' ? realResults.value : fictionResults.value
  if (!clients.length) return
  try {
    const result = await clientsApi.batchInsert({ clients })
    if (result.success) {
      let msg = `✅ 成功录入 ${result.inserted} 个客户`
      if (result.skipped > 0) {
        msg += `，跳过 ${result.skipped} 个重复客户`
      }
      window.showToast(msg)
      if (mode === 'real') realResults.value = []
      else fictionResults.value = []
      showAIModal.value = false
      loadClients()
    } else {
      window.showToast('录入失败', 'error')
    }
  } catch (e) {
    window.showToast('录入失败', 'error')
  }
}

// ==================== Init ====================
onMounted(() => {
  loadClients()
})
</script>
