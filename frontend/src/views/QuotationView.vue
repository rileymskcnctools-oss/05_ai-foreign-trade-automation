<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ====== TOP BAR ====== -->
    <div class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-[1600px] mx-auto px-4 sm:px-6 py-4">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <h1 class="text-xl font-bold text-gray-800 flex items-center gap-2">
            <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Quotations
          </h1>
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 w-full sm:w-auto">
            <!-- Search -->
            <div class="relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by quote no or customer..."
                class="pl-9 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 w-full sm:w-64"
                @input="debouncedFetch"
              />
            </div>
            <!-- Status Filter -->
            <select
              v-model="statusFilter"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              @change="fetchQuotations"
            >
              <option value="">All Status</option>
              <option value="draft">Draft</option>
              <option value="sent">Sent</option>
              <option value="negotiating">Negotiating</option>
              <option value="won">Won</option>
              <option value="lost">Lost</option>
            </select>
            <!-- New Quotation Button -->
            <button
              @click="openEditor()"
              class="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors shadow-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              New Quotation
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ====== STATS CARDS ====== -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 py-4">
      <div class="grid grid-cols-2 lg:grid-cols-5 gap-3">
        <div v-for="stat in statsCards" :key="stat.label"
          class="bg-white rounded-xl border border-gray-200 p-4 shadow-sm">
          <div class="text-xs font-medium text-gray-500 uppercase tracking-wide">{{ stat.label }}</div>
          <div class="mt-1 text-xl font-bold" :class="stat.color">{{ stat.value }}</div>
        </div>
      </div>
    </div>

    <!-- ====== QUOTATION TABLE ====== -->
    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 pb-8">
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Quote No</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Customer</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Country</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Items</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Total Amount</th>
                <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">Margin</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Status</th>
                <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Created</th>
                <th class="px-4 py-3 text-center text-xs font-semibold text-gray-600 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-100">
              <tr v-if="loading">
                <td colspan="9" class="px-4 py-12 text-center text-gray-400">
                  <svg class="animate-spin h-6 w-6 mx-auto mb-2 text-indigo-500" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Loading...
                </td>
              </tr>
              <tr v-else-if="quotations.length === 0">
                <td colspan="9" class="px-4 py-12 text-center text-gray-400">
                  No quotations found.
                </td>
              </tr>
              <tr
                v-for="q in quotations"
                :key="q.quotation_no"
                class="hover:bg-indigo-50/40 transition-colors cursor-pointer"
                @click="viewQuotation(q)"
              >
                <td class="px-4 py-3">
                  <span class="text-sm font-mono font-semibold text-indigo-700">{{ q.quotation_no }}</span>
                </td>
                <td class="px-4 py-3">
                  <div class="text-sm font-medium text-gray-900">{{ q.customer_name }}</div>
                  <div class="text-xs text-gray-500">{{ q.contact_person }}</div>
                </td>
                <td class="px-4 py-3 text-sm text-gray-700">{{ q.client_country || q.country || '-' }}</td>
                <td class="px-4 py-3 text-center text-sm text-gray-700">{{ q.items_count }}</td>
                <td class="px-4 py-3 text-right text-sm font-semibold text-gray-900">
                  {{ formatCurrency(q.total_amount, q.currency) }}
                </td>
                <td class="px-4 py-3 text-right">
                  <span class="text-sm font-semibold" :class="marginColor(q.profit_margin)">
                    {{ q.profit_margin != null ? q.profit_margin.toFixed(1) + '%' : '—' }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold"
                    :class="statusBadge(q.status)">
                    {{ capitalizeFirst(q.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(q.created_at) }}</td>
                <td class="px-4 py-3 text-center" @click.stop>
                  <div class="inline-flex items-center gap-1">
                    <button @click="viewQuotation(q)" class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-indigo-600" title="View">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button @click="openEditor(q)" class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-amber-600" title="Edit">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button @click="confirmDelete(q)" class="p-1.5 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-red-600" title="Delete">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-between px-4 py-3 border-t border-gray-200 bg-gray-50">
          <div class="text-sm text-gray-500">
            Showing {{ (page - 1) * perPage + 1 }}–{{ Math.min(page * perPage, totalCount) }} of {{ totalCount }}
          </div>
          <div class="flex items-center gap-1">
            <button
              @click="page = Math.max(1, page - 1); fetchQuotations()
  fetchAllProducts()"
              :disabled="page <= 1"
              class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >Previous</button>
            <button
              v-for="p in paginationRange"
              :key="p"
              @click="page = p; fetchQuotations()
  fetchAllProducts()"
              class="px-3 py-1.5 text-sm rounded-lg border"
              :class="p === page ? 'bg-indigo-600 text-white border-indigo-600' : 'border-gray-300 bg-white hover:bg-gray-50'"
            >{{ p }}</button>
            <button
              @click="page = Math.min(totalPages, page + 1); fetchQuotations()
  fetchAllProducts()"
              :disabled="page >= totalPages"
              class="px-3 py-1.5 text-sm rounded-lg border border-gray-300 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >Next</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ====== FULL-SCREEN EDITOR MODAL ====== -->
    <Teleport to="body">
      <div v-if="editorOpen" class="fixed inset-0 z-50 flex flex-col bg-white">
        <!-- Editor Header -->
        <div class="flex items-center justify-between px-6 py-3 bg-indigo-700 text-white shrink-0 shadow-lg">
          <div class="flex items-center gap-3">
            <button @click="closeEditor" class="p-1.5 rounded-lg hover:bg-white/20 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            <h2 class="text-lg font-bold">
              {{ editingId ? `Edit Quotation ${form.quotation_no}` : 'New Quotation' }}
            </h2>
          </div>
          <div class="flex items-center gap-4 text-sm">
            <span>Grand Total: <b>{{ formatCurrency(grandTotal, form.currency) }}</b></span>
            <span>
              Margin: <b :class="marginColor(profitMargin)">{{ profitMargin.toFixed(1) }}%</b>
            </span>
          </div>
        </div>

        <!-- Editor Body (scrollable) -->
        <div class="flex-1 overflow-y-auto px-6 py-6 space-y-6">
          <!-- ===== Section A: Header ===== -->
          <section class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span class="w-1 h-5 bg-indigo-500 rounded-full"></span>
              Header Information
            </h3>
            <!-- Row 1 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Quote No</label>
                <input v-model="form.quotation_no" type="text" disabled
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-gray-50 text-gray-500" placeholder="Auto-generated" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Customer *</label>
                <select v-model="form.customer_id" @change="onCustomerChange"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                  <option value="">Select customer...</option>
                  <option v-for="c in customers" :key="c.id" :value="c.id">{{ c.company_name || c.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Contact Person</label>
                <input v-model="form.contact_person" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Country</label>
                <input v-model="form.country" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
            </div>
            <!-- Row 2 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Currency</label>
                <select v-model="form.currency"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500">
                  <option value="USD">USD ($)</option>
                  <option value="EUR">EUR (€)</option>
                  <option value="CNY">CNY (¥)</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Trade Term</label>
                <select v-model="form.trade_term"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500">
                  <option value="EXW">EXW</option>
                  <option value="FOB">FOB</option>
                  <option value="CIF">CIF</option>
                  <option value="CFR">CFR</option>
                  <option value="DDP">DDP</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Loading Port</label>
                <input v-model="form.loading_port" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Destination Port</label>
                <input v-model="form.destination_port" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
            </div>
            <!-- Row 3 -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Valid Until</label>
                <input v-model="form.valid_until" type="date"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Sales Person</label>
                <input v-model="form.sales_person" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Status</label>
                <select v-model="form.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500">
                  <option value="draft">Draft</option>
                  <option value="sent">Sent</option>
                  <option value="negotiating">Negotiating</option>
                  <option value="won">Won</option>
                  <option value="lost">Lost</option>
                </select>
              </div>
            </div>
          </section>

          <!-- ===== Section B: Product Lines ===== -->
          <section class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
                <span class="w-1 h-5 bg-indigo-500 rounded-full"></span>
                Product Lines
              </h3>
              <button @click="addProductLine"
                class="inline-flex items-center gap-1 px-3 py-1.5 text-xs font-medium bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Row
              </button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full text-sm">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="px-2 py-2 text-left text-xs font-semibold text-gray-600 w-8">#</th>
                    <th class="px-2 py-2 text-left text-xs font-semibold text-gray-600 min-w-[200px]">Product</th>
                    <th class="px-2 py-2 text-left text-xs font-semibold text-gray-600">SKU</th>
                    <th class="px-2 py-2 text-right text-xs font-semibold text-gray-600 w-20">Qty</th>
                    <th class="px-2 py-2 text-left text-xs font-semibold text-gray-600 w-16">Unit</th>
                    <th class="px-2 py-2 text-right text-xs font-semibold text-gray-600 w-28">Unit Price</th>
                    <th class="px-2 py-2 text-right text-xs font-semibold text-gray-600 w-20">Disc %</th>
                    <th class="px-2 py-2 text-right text-xs font-semibold text-gray-600 w-28">Amount</th>
                    <th class="px-2 py-2 w-10"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(line, idx) in form.lines" :key="idx" class="border-b border-gray-100">
                    <td class="px-2 py-2 text-gray-400 text-xs">{{ idx + 1 }}</td>
                    <td class="px-2 py-2">
                      <select
                        v-model="line.product_code"
                        @change="onProductSelect(idx, $event)"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm bg-white focus:ring-1 focus:ring-indigo-500"
                      >
                        <option value="">Select product...</option>
                        <option v-for="p in allProducts" :key="p.product_code" :value="p.product_code">
                          {{ p.product_code }} - {{ p.product_name_en }}
                        </option>
                      </select>
                    </td>
                    <td class="px-2 py-2">
                      <input v-model="line.sku" type="text" readonly
                        class="w-full px-2 py-1.5 border border-gray-200 rounded text-sm bg-gray-50 text-gray-500" />
                    </td>
                    <td class="px-2 py-2">
                      <input v-model.number="line.qty" type="number" min="1"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500"
                        @input="calcLineAmount(idx)" />
                    </td>
                    <td class="px-2 py-2">
                      <input v-model="line.unit" type="text"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm focus:ring-1 focus:ring-indigo-500" />
                    </td>
                    <td class="px-2 py-2">
                      <input v-model.number="line.unit_price" type="number" min="0" step="0.01"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500"
                        @input="calcLineAmount(idx)" />
                    </td>
                    <td class="px-2 py-2">
                      <input v-model.number="line.discount" type="number" min="0" max="100" step="0.1"
                        class="w-full px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500"
                        @input="calcLineAmount(idx)" />
                    </td>
                    <td class="px-2 py-2 text-right font-medium text-gray-800">
                      {{ formatCurrency(line.amount || 0, form.currency) }}
                    </td>
                    <td class="px-2 py-2">
                      <button @click="removeProductLine(idx)"
                        class="p-1 rounded hover:bg-red-50 text-gray-400 hover:text-red-500 transition-colors"
                        :disabled="form.lines.length <= 1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- ===== Section C + D: Cost & Profit (side by side on large screens) ===== -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Section C: Cost Breakdown -->
            <section class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
                <span class="w-1 h-5 bg-indigo-500 rounded-full"></span>
                Cost Breakdown
              </h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <label class="text-sm text-gray-600">Product Total</label>
                  <span class="text-sm font-semibold">{{ formatCurrency(productTotal, form.currency) }}</span>
                </div>
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Discount %</label>
                  <input v-model.number="form.overall_discount" type="number" min="0" max="100" step="0.1"
                    class="w-28 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Shipping Cost</label>
                  <input v-model.number="form.shipping_cost" type="number" min="0" step="0.01"
                    class="w-36 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Insurance</label>
                  <input v-model.number="form.insurance" type="number" min="0" step="0.01"
                    class="w-36 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Packing Cost</label>
                  <input v-model.number="form.packing_cost" type="number" min="0" step="0.01"
                    class="w-36 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Other Charges</label>
                  <input v-model.number="form.other_charges" type="number" min="0" step="0.01"
                    class="w-36 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between pt-3 border-t border-gray-200">
                  <label class="text-sm font-bold text-gray-800">Grand Total</label>
                  <span class="text-lg font-bold text-indigo-700">{{ formatCurrency(grandTotal, form.currency) }}</span>
                </div>
              </div>
            </section>

            <!-- Section D: Profit Analysis -->
            <section class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
                <span class="w-1 h-5 bg-green-500 rounded-full"></span>
                Profit Analysis
              </h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between gap-3">
                  <label class="text-sm text-gray-600">Total Cost</label>
                  <input v-model.number="form.total_cost" type="number" min="0" step="0.01"
                    class="w-36 px-2 py-1.5 border border-gray-300 rounded text-sm text-right focus:ring-1 focus:ring-indigo-500" />
                </div>
                <div class="flex items-center justify-between">
                  <label class="text-sm text-gray-600">Selling Price</label>
                  <span class="text-sm font-semibold">{{ formatCurrency(grandTotal, form.currency) }}</span>
                </div>
                <div class="flex items-center justify-between">
                  <label class="text-sm text-gray-600">Gross Profit</label>
                  <span class="text-sm font-bold" :class="grossProfit >= 0 ? 'text-green-600' : 'text-red-600'">
                    {{ formatCurrency(grossProfit, form.currency) }}
                  </span>
                </div>
                <div class="flex items-center justify-between pt-3 border-t border-gray-200">
                  <label class="text-sm font-bold text-gray-800">Profit Margin</label>
                  <div class="flex items-center gap-2">
                    <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div class="h-full rounded-full transition-all duration-300"
                        :class="profitMarginColorBg"
                        :style="{ width: Math.max(0, Math.min(100, profitMargin)) + '%' }"></div>
                    </div>
                    <span class="text-lg font-bold" :class="marginColor(profitMargin)">
                      {{ profitMargin.toFixed(1) }}%
                    </span>
                  </div>
                </div>
                <!-- Visual indicator -->
                <div class="mt-2 p-3 rounded-lg" :class="profitIndicatorBg">
                  <div class="flex items-center gap-2">
                    <svg v-if="profitMargin >= 15" class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <svg v-else-if="profitMargin >= 5" class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                    <svg v-else class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span class="text-sm font-medium" :class="profitMargin >= 15 ? 'text-green-700' : profitMargin >= 5 ? 'text-amber-700' : 'text-red-700'">
                      {{ profitMargin >= 15 ? 'Healthy margin' : profitMargin >= 5 ? 'Low margin – consider adjusting' : 'Critical – below target margin' }}
                    </span>
                  </div>
                </div>
              </div>
            </section>
          </div>

          <!-- ===== Section E: Trade Terms ===== -->
          <section class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span class="w-1 h-5 bg-indigo-500 rounded-full"></span>
              Trade Terms & Details
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Payment Terms</label>
                <select v-model="form.payment_terms"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500">
                  <option value="">Select...</option>
                  <option value="TT">T/T (Telegraphic Transfer)</option>
                  <option value="LC">L/C (Letter of Credit)</option>
                  <option value="OA">O/A (Open Account)</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Lead Time (days)</label>
                <input v-model.number="form.lead_time" type="number" min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Warranty</label>
                <input v-model="form.warranty" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
                  placeholder="e.g., 12 months" />
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Sample Policy</label>
                <input v-model="form.sample_policy" type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500"
                  placeholder="e.g., Free sample, buyer pays shipping" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">OEM/ODM</label>
                <textarea v-model="form.oem_odm" rows="2"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 resize-none"
                  placeholder="OEM/ODM capabilities..."></textarea>
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Packing Details</label>
                <textarea v-model="form.packing_details" rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 resize-none"
                  placeholder="Standard export packing..."></textarea>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Remarks</label>
                <textarea v-model="form.remarks" rows="3"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 resize-none"
                  placeholder="Additional notes..."></textarea>
              </div>
            </div>
          </section>

          <!-- ===== Section F: AI Assistant ===== -->
          <section class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border border-indigo-200 shadow-sm p-5">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                AI Assistant
              </h3>
              <button
                @click="runAiOptimize"
                :disabled="aiLoading"
                class="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <svg v-if="aiLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                AI Optimize
              </button>
            </div>
            <div v-if="aiLoading" class="flex items-center justify-center py-8 text-gray-500">
              <svg class="animate-spin h-5 w-5 mr-2 text-indigo-500" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Analyzing quotation data...
            </div>
            <div v-else-if="aiSuggestions" class="bg-white rounded-lg border border-indigo-200 p-4">
              <h4 class="text-sm font-bold text-indigo-800 mb-3">💡 AI Recommendations</h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div v-if="aiSuggestions.recommended_price" class="flex items-start gap-2 p-2 rounded-lg bg-gray-50">
                  <span class="text-xs font-semibold text-gray-500 mt-0.5 w-28 shrink-0">Price</span>
                  <span class="text-sm text-gray-800">{{ aiSuggestions.recommended_price }}</span>
                </div>
                <div v-if="aiSuggestions.recommended_moq" class="flex items-start gap-2 p-2 rounded-lg bg-gray-50">
                  <span class="text-xs font-semibold text-gray-500 mt-0.5 w-28 shrink-0">MOQ</span>
                  <span class="text-sm text-gray-800">{{ aiSuggestions.recommended_moq }}</span>
                </div>
                <div v-if="aiSuggestions.trade_term" class="flex items-start gap-2 p-2 rounded-lg bg-gray-50">
                  <span class="text-xs font-semibold text-gray-500 mt-0.5 w-28 shrink-0">Trade Term</span>
                  <span class="text-sm text-gray-800">{{ aiSuggestions.trade_term }}</span>
                </div>
                <div v-if="aiSuggestions.payment_terms" class="flex items-start gap-2 p-2 rounded-lg bg-gray-50">
                  <span class="text-xs font-semibold text-gray-500 mt-0.5 w-28 shrink-0">Payment</span>
                  <span class="text-sm text-gray-800">{{ aiSuggestions.payment_terms }}</span>
                </div>
              </div>
              <div v-if="aiSuggestions.risk_notes" class="mt-3 p-3 rounded-lg bg-amber-50 border border-amber-200">
                <div class="flex items-start gap-2">
                  <svg class="w-4 h-4 text-amber-600 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <div>
                    <div class="text-xs font-bold text-amber-800 mb-0.5">Risk Notes</div>
                    <div class="text-sm text-amber-700">{{ aiSuggestions.risk_notes }}</div>
                  </div>
                </div>
              </div>
              <div v-if="aiSuggestions.general_advice" class="mt-3 text-sm text-gray-600">
                {{ aiSuggestions.general_advice }}
              </div>
            </div>
            <div v-else class="text-center py-6 text-sm text-gray-400">
              Click "AI Optimize" to get intelligent pricing and trade term recommendations.
            </div>
          </section>

          <!-- ===== Version History (shown when viewing/editing existing) ===== -->
          <section v-if="editingId && versions.length > 0"
            class="bg-white rounded-xl border border-gray-200 shadow-sm p-5">
            <h3 class="text-sm font-bold text-gray-700 uppercase tracking-wider mb-4 flex items-center gap-2">
              <span class="w-1 h-5 bg-gray-400 rounded-full"></span>
              Version History
            </h3>
            <div class="space-y-2">
              <div v-for="ver in versions" :key="ver.version"
                class="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                <div class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center text-xs font-bold shrink-0">
                  v{{ ver.version }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-gray-800">Version {{ ver.version }}</span>
                    <span class="text-xs text-gray-400">{{ formatDate(ver.date) }}</span>
                  </div>
                  <p class="text-xs text-gray-500 mt-0.5">{{ ver.change_summary }}</p>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Editor Footer (fixed) -->
        <div class="shrink-0 border-t border-gray-200 bg-white px-6 py-3 flex items-center justify-between shadow-[0_-4px_12px_rgba(0,0,0,0.05)]">
          <div class="flex items-center gap-6">
            <div>
              <span class="text-xs text-gray-500">Grand Total</span>
              <div class="text-xl font-bold text-indigo-700">{{ formatCurrency(grandTotal, form.currency) }}</div>
            </div>
            <div>
              <span class="text-xs text-gray-500">Profit Margin</span>
              <div class="text-xl font-bold" :class="marginColor(profitMargin)">{{ profitMargin.toFixed(1) }}%</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button @click="closeEditor"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              Cancel
            </button>
            <button @click="saveQuotation('draft')"
              :disabled="saving"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors">
              Save Draft
            </button>
            <button @click="saveQuotation('sent')"
              :disabled="saving"
              class="inline-flex items-center gap-1.5 px-5 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors shadow-sm"
            >
              <svg v-if="saving" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Save &amp; Send
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ====== VIEW DETAIL MODAL ====== -->
    <Teleport to="body">
      <div v-if="viewOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        @click.self="viewOpen = false">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-gray-50">
            <h3 class="text-lg font-bold text-gray-800">Quotation {{ viewData.quotation_no }}</h3>
            <div class="flex items-center gap-2">
              <button @click="openEditor(viewData)" class="px-3 py-1.5 text-sm bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Edit</button>
              <button @click="viewOpen = false" class="p-1.5 rounded-lg hover:bg-gray-200 text-gray-500">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto p-6 space-y-4" v-if="viewData">
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div><span class="text-xs text-gray-500">Customer</span><div class="text-sm font-medium">{{ viewData.customer_name }}</div></div>
              <div><span class="text-xs text-gray-500">Country</span><div class="text-sm font-medium">{{ viewData.country }}</div></div>
              <div><span class="text-xs text-gray-500">Status</span><div><span class="inline-flex px-2 py-0.5 text-xs font-semibold rounded-full" :class="statusBadge(viewData.status)">{{ capitalizeFirst(viewData.status) }}</span></div></div>
              <div><span class="text-xs text-gray-500">Created</span><div class="text-sm font-medium">{{ formatDate(viewData.created_at) }}</div></div>
            </div>
            <div v-if="viewData.lines && viewData.lines.length" class="border rounded-lg overflow-hidden">
              <table class="min-w-full text-sm">
                <thead class="bg-gray-50"><tr>
                  <th class="px-3 py-2 text-left text-xs font-semibold text-gray-600">Product</th>
                  <th class="px-3 py-2 text-right text-xs font-semibold text-gray-600">Qty</th>
                  <th class="px-3 py-2 text-right text-xs font-semibold text-gray-600">Unit Price</th>
                  <th class="px-3 py-2 text-right text-xs font-semibold text-gray-600">Amount</th>
                </tr></thead>
                <tbody class="divide-y divide-gray-100">
                  <tr v-for="(line, i) in viewData.lines" :key="i">
                    <td class="px-3 py-2">{{ line.product_name }}</td>
                    <td class="px-3 py-2 text-right">{{ line.qty }} {{ line.unit }}</td>
                    <td class="px-3 py-2 text-right">{{ formatCurrency(line.unit_price, viewData.currency) }}</td>
                    <td class="px-3 py-2 text-right font-medium">{{ formatCurrency(line.amount, viewData.currency) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="flex items-center justify-end gap-6 pt-4 border-t">
              <div class="text-right">
                <span class="text-xs text-gray-500">Total</span>
                <div class="text-lg font-bold text-indigo-700">{{ formatCurrency(viewData.total_amount, viewData.currency) }}</div>
              </div>
              <div class="text-right">
                <span class="text-xs text-gray-500">Margin</span>
                <div class="text-lg font-bold" :class="marginColor(viewData.profit_margin)">{{ viewData.profit_margin != null ? viewData.profit_margin.toFixed(1) + '%' : '—' }}</div>
              </div>
            </div>
            <!-- Version History in View -->
            <div v-if="versions.length > 0" class="pt-4 border-t">
              <h4 class="text-xs font-bold text-gray-600 uppercase tracking-wider mb-3">Version History</h4>
              <div class="space-y-2">
                <div v-for="ver in versions" :key="ver.version" class="flex items-center gap-3 text-sm">
                  <span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold">v{{ ver.version }}</span>
                  <span class="text-gray-500 text-xs">{{ formatDate(ver.date) }}</span>
                  <span class="text-gray-700 text-xs">{{ ver.change_summary }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ====== DELETE CONFIRMATION ====== -->
    <Teleport to="body">
      <div v-if="deleteTarget" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
        @click.self="deleteTarget = null">
        <div class="bg-white rounded-xl shadow-2xl p-6 max-w-sm w-full">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div>
              <h4 class="text-sm font-bold text-gray-800">Delete Quotation</h4>
              <p class="text-xs text-gray-500">This action cannot be undone.</p>
            </div>
          </div>
          <p class="text-sm text-gray-600 mb-5">
            Are you sure you want to delete quotation <strong>{{ deleteTarget.quotation_no }}</strong>?
          </p>
          <div class="flex items-center justify-end gap-2">
            <button @click="deleteTarget = null"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancel</button>
            <button @click="executeDelete"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700">Delete</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { quotationApi, productsApi, clientsApi } from '../api'

// ==================== STATE ====================
const quotations = ref([])
const customers = ref([])
const allProducts = ref([])
const stats = ref({})
const loading = ref(false)
const saving = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const page = ref(1)
const perPage = ref(20)
const totalCount = ref(0)
const totalPages = ref(1)

// Editor
const editorOpen = ref(false)
const editingId = ref(null)

// View detail
const viewOpen = ref(false)
const viewData = ref(null)

// Delete
const deleteTarget = ref(null)

// Version history
const versions = ref([])

// AI
const aiLoading = ref(false)
const aiSuggestions = ref(null)

// Product search removed

// ==================== FORM ====================
const defaultForm = () => ({
  quotation_no: '',
  customer_id: '',
  customer_name: '',
  contact_person: '',
  country: '',
  currency: 'USD',
  trade_term: 'FOB',
  loading_port: '',
  destination_port: '',
  valid_until: '',
  sales_person: '',
  status: 'draft',
  lines: [createEmptyLine()],
  overall_discount: 0,
  shipping_cost: 0,
  insurance: 0,
  packing_cost: 0,
  other_charges: 0,
  total_cost: 0,
  payment_terms: '',
  lead_time: '',
  warranty: '',
  sample_policy: '',
  oem_odm: '',
  packing_details: '',
  remarks: '',
})

function createEmptyLine() {
  return {
    product_id: '',
    product_name: '',
    product_search: '',
    sku: '',
    material: '',
    moq: '',
    qty: 1,
    unit: 'pcs',
    unit_price: 0,
    discount: 0,
    amount: 0,

  }
}

const form = reactive(defaultForm())

// ==================== COMPUTED ====================
const productTotal = computed(() => {
  return (form.lines || []).reduce((sum, line) => sum + (line.amount || 0), 0)
})

const grandTotal = computed(() => {
  const subtotal = productTotal.value
  const afterDiscount = subtotal * (1 - (form.overall_discount || 0) / 100)
  const extras = (form.shipping_cost || 0) + (form.insurance || 0) + (form.packing_cost || 0) + (form.other_charges || 0)
  return afterDiscount + extras
})

const grossProfit = computed(() => {
  return grandTotal.value - (form.total_cost || 0)
})

const profitMargin = computed(() => {
  if (!grandTotal.value || grandTotal.value === 0) return 0
  return (grossProfit.value / grandTotal.value) * 100
})

const profitMarginColorBg = computed(() => {
  if (profitMargin.value >= 15) return 'bg-green-500'
  if (profitMargin.value >= 5) return 'bg-amber-500'
  return 'bg-red-500'
})

const profitIndicatorBg = computed(() => {
  if (profitMargin.value >= 15) return 'bg-green-50 border border-green-200'
  if (profitMargin.value >= 5) return 'bg-amber-50 border border-amber-200'
  return 'bg-red-50 border border-red-200'
})

const statsCards = computed(() => {
  const s = stats.value || {}
  return [
    { label: 'Total', value: s.total ?? '—', color: 'text-gray-800' },
    { label: 'Draft', value: s.draft ?? '—', color: 'text-gray-500' },
    { label: 'Sent', value: s.sent ?? '—', color: 'text-blue-600' },
    { label: 'Won', value: s.won ?? '—', color: 'text-green-600' },
    { label: 'Revenue', value: s.revenue != null ? formatCompactCurrency(s.revenue) : '—', color: 'text-indigo-700' },
  ]
})

const paginationRange = computed(() => {
  const total = totalPages.value
  const current = page.value
  const range = []
  const delta = 2
  for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
    range.push(i)
  }
  return range
})

// ==================== HELPERS ====================
function formatCurrency(amount, currency = 'USD') {
  if (amount == null) return '—'
  const symbols = { USD: '$', EUR: '€', CNY: '¥' }
  const sym = symbols[currency] || currency + ' '
  return sym + Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatCompactCurrency(amount) {
  if (amount == null) return '—'
  if (amount >= 1000000) return '$' + (amount / 1000000).toFixed(1) + 'M'
  if (amount >= 1000) return '$' + (amount / 1000).toFixed(1) + 'K'
  return '$' + amount.toFixed(0)
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  const d = new Date(dateStr)
  if (isNaN(d.getTime())) return dateStr
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function capitalizeFirst(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}

function marginColor(margin) {
  if (margin == null) return 'text-gray-400'
  if (margin >= 15) return 'text-green-600'
  if (margin >= 5) return 'text-amber-600'
  return 'text-red-600'
}

function statusBadge(status) {
  const map = {
    draft: 'bg-gray-100 text-gray-700',
    sent: 'bg-blue-100 text-blue-700',
    negotiating: 'bg-amber-100 text-amber-700',
    won: 'bg-green-100 text-green-700',
    lost: 'bg-red-100 text-red-700',
  }
  return map[status] || 'bg-gray-100 text-gray-700'
}

// Debounce helper
let fetchTimer = null
function debouncedFetch() {
  clearTimeout(fetchTimer)
  fetchTimer = setTimeout(() => {
    page.value = 1
    fetchQuotations()
  }, 300)
}

// ==================== API CALLS ====================
async function fetchQuotations() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      per_page: perPage.value,
    }
    if (searchQuery.value) params.search = searchQuery.value
    if (statusFilter.value) params.status = statusFilter.value

    const res = await quotationApi.list(params)
    const items = res.quotations || res.items || res.data || res || []
    quotations.value = items.map(q => ({
      ...q,
      customer_name: q.customer_name || q.client_name || '-',
      client_country: q.client_country || q.country || '-',
      items_count: q.items_count || q.items?.length || 0,
    }))
    totalCount.value = res.total || quotations.value.length
    totalPages.value = res.total_pages || Math.ceil(totalCount.value / perPage.value) || 1
  } catch (e) {
    console.error('Failed to fetch quotations:', e)
    window.showToast?.('Failed to load quotations', 'error')
  } finally {
    loading.value = false
  }
}

async function fetchStats() {
  try {
    const res = await quotationApi.stats()
    // Map API response to expected format
    const byStatus = {}
    if (res.by_status) {
      res.by_status.forEach(s => { byStatus[s.status] = s.cnt })
    }
    stats.value = {
      total: res.total_quotations || 0,
      draft: byStatus.draft || 0,
      sent: byStatus.sent || 0,
      won: byStatus.won || 0,
      revenue: res.total_revenue || 0,
    }
  } catch (e) {
    console.error('Failed to fetch stats:', e)
  }
}

async function fetchAllProducts() {
  try {
    const res = await productsApi.list({ limit: 200 })
    allProducts.value = res.results || res.items || res.data || []
  } catch (e) { console.error(e) }
}

async function fetchCustomers() {
  try {
    const res = await clientsApi.list({ per_page: 1000 })
    customers.value = res.clients || res.items || res.data || res || []
  } catch (e) {
    console.error('Failed to fetch customers:', e)
  }
}

async function fetchVersions(quotationNo) {
  try {
    const res = await quotationApi.versions(quotationNo)
    versions.value = res.items || res.data || res || []
  } catch (e) {
    versions.value = []
  }
}

// ==================== EDITOR ====================
function openEditor(quotation = null) {
  aiSuggestions.value = null
  versions.value = []

  if (quotation && quotation.quotation_no) {
    editingId.value = quotation.quotation_no
    // Load full data
    loadQuotationForEdit(quotation.quotation_no)
  } else {
    editingId.value = null
    Object.assign(form, defaultForm())
  }

  editorOpen.value = true
}

async function loadQuotationForEdit(no) {
  try {
    const res = await quotationApi.get(no)
    const q = res.data || res
    Object.assign(form, {
      quotation_no: q.quotation_no || '',
      customer_id: q.customer_id || '',
      customer_name: q.customer_name || '',
      contact_person: q.contact_person || '',
      country: q.country || '',
      currency: q.currency || 'USD',
      trade_term: q.trade_term || 'FOB',
      loading_port: q.loading_port || '',
      destination_port: q.destination_port || '',
      valid_until: q.valid_until || '',
      sales_person: q.sales_person || '',
      status: q.status || 'draft',
      lines: (q.lines || []).map(l => ({
        ...createEmptyLine(),
        ...l,
        product_search: l.product_name || '',
        showDropdown: false,
        searchResults: [],
      })),
      overall_discount: q.overall_discount || 0,
      shipping_cost: q.shipping_cost || 0,
      insurance: q.insurance || 0,
      packing_cost: q.packing_cost || 0,
      other_charges: q.other_charges || 0,
      total_cost: q.total_cost || 0,
      payment_terms: q.payment_terms || '',
      lead_time: q.lead_time || '',
      warranty: q.warranty || '',
      sample_policy: q.sample_policy || '',
      oem_odm: q.oem_odm || '',
      packing_details: q.packing_details || '',
      remarks: q.remarks || '',
    })
    if (form.lines.length === 0) {
      form.lines = [createEmptyLine()]
    }
    fetchVersions(no)
  } catch (e) {
    window.showToast?.('Failed to load quotation details', 'error')
  }
}

function closeEditor() {
  editorOpen.value = false
  editingId.value = null
}

// ==================== PRODUCT LINES ====================
function addProductLine() {
  form.lines.push(createEmptyLine())
}

function removeProductLine(idx) {
  if (form.lines.length <= 1) return
  form.lines.splice(idx, 1)
}

function calcLineAmount(idx) {
  const line = form.lines[idx]
  if (!line) return
  const qty = Number(line.qty) || 0
  const price = Number(line.unit_price) || 0
  const disc = Number(line.discount) || 0
  line.amount = qty * price * (1 - disc / 100)
}

// Product search removed - using simple select dropdown instead

function onProductSelect(idx, event) {
  const code = event.target.value
  const line = form.lines[idx]
  if (!code) {
    line.product_name = ''
    line.sku = ''
    line.material = ''
    line.moq = ''
    return
  }
  const product = allProducts.value.find(p => p.product_code === code)
  if (product) {
    line.product_id = product.id
    line.product_code = product.product_code
    line.product_name = product.product_name_en || ''
    line.sku = product.product_code || ''
    line.material = product.material || ''
    line.moq = product.moq || ''
    line.unit = 'pcs'
  }
  calcLineAmount(idx)
}

// hideProductDropdown removed

// ==================== CUSTOMER ====================
function onCustomerChange() {
  const c = customers.value.find(c => String(c.id) === String(form.customer_id))
  if (c) {
    form.customer_name = c.company_name || c.name || ''
    form.contact_person = c.contact_person || c.contact || ''
    form.country = c.country || ''
  }
}

// ==================== SAVE ====================
async function saveQuotation(statusOverride) {
  if (statusOverride) form.status = statusOverride

  // Validate required fields
  if (!form.customer_id) {
    window.showToast?.('Please select a customer', 'warning')
    return
  }
  if (!form.lines.some(l => l.product_id || l.product_name)) {
    window.showToast?.('Please add at least one product line', 'warning')
    return
  }

  saving.value = true
  try {
    const payload = {
      ...form,
      lines: form.lines.filter(l => l.product_id || l.product_name).map(l => ({
        product_id: l.product_id,
        product_name: l.product_name,
        sku: l.sku,
        qty: l.qty,
        unit: l.unit,
        unit_price: l.unit_price,
        discount: l.discount,
        amount: l.amount,
      })),
      total_amount: grandTotal.value,
      profit_margin: profitMargin.value,
    }

    if (editingId.value) {
      await quotationApi.update(editingId.value, payload)
      window.showToast?.('Quotation updated successfully', 'success')
    } else {
      await quotationApi.create(payload)
      window.showToast?.('Quotation created successfully', 'success')
    }

    closeEditor()
    fetchQuotations()
    fetchStats()
  } catch (e) {
    console.error('Save failed:', e)
    window.showToast?.('Failed to save quotation', 'error')
  } finally {
    saving.value = false
  }
}

// ==================== VIEW ====================
async function viewQuotation(q) {
  viewData.value = q
  viewOpen.value = true
  await fetchVersions(q.quotation_no)
}

// ==================== DELETE ====================
function confirmDelete(q) {
  deleteTarget.value = q
}

async function executeDelete() {
  if (!deleteTarget.value) return
  try {
    await quotationApi.delete(deleteTarget.value.quotation_no)
    window.showToast?.('Quotation deleted', 'success')
    deleteTarget.value = null
    fetchQuotations()
    fetchStats()
  } catch (e) {
    window.showToast?.('Failed to delete quotation', 'error')
  }
}

// ==================== AI OPTIMIZE ====================
async function runAiOptimize() {
  aiLoading.value = true
  aiSuggestions.value = null
  try {
    const payload = {
      currency: form.currency,
      trade_term: form.trade_term,
      customer_name: form.customer_name,
      country: form.country,
      lines: form.lines.filter(l => l.product_name).map(l => ({
        product_name: l.product_name,
        qty: l.qty,
        unit_price: l.unit_price,
        amount: l.amount,
      })),
      total_amount: grandTotal.value,
      total_cost: form.total_cost,
      profit_margin: profitMargin.value,
    }
    const res = await quotationApi.aiOptimize(payload)
    aiSuggestions.value = res.data || res.suggestions || res || {}
  } catch (e) {
    console.error('AI optimize failed:', e)
    window.showToast?.('AI optimization failed. Please try again.', 'error')
  } finally {
    aiLoading.value = false
  }
}

// ==================== LIFECYCLE ====================
onMounted(() => {
  fetchQuotations()
  fetchStats()
  fetchCustomers()
  fetchAllProducts()
})
</script>
