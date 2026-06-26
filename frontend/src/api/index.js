import axios from 'axios'

const api = axios.create({
  baseURL: '',
  timeout: 120000,
  headers: { 'Content-Type': 'application/json' },
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const msg = error.response?.data?.detail || error.response?.data?.error || error.message
    console.error('API Error:', msg)
    return Promise.reject(error)
  }
)

// ========== Dashboard API ==========
export const dashboardApi = {
  getStats: () => api.get('/api/dashboard/stats'),
  getHome: () => api.get('/api/dashboard/home'),
}

// ========== Products API ==========
export const productsApi = {
  list: (params) => api.get('/products/api/search', { params }),
  get: (code) => api.get(`/products/api/${code}`),
  create: (data) => api.post('/products/api/create', data),
  update: (code, data) => api.put(`/products/api/${code}`, data),
  delete: (code) => api.delete(`/products/api/${code}`),
  categories: () => api.get('/products/api/categories'),
  generate: (code, type) => api.get(`/products/api/${code}/generate/${type}`),
  exportCsv: () => api.get('/products/api/export/csv', { responseType: 'blob' }),
}

// ========== Clients API ==========
export const clientsApi = {
  list: (params) => api.get('/clients/api/list', { params }),
  get: (id) => api.get(`/clients/api/${id}`),
  create: (data) => api.post('/clients/api/create', data),
  update: (id, data) => api.put(`/clients/api/${id}`, data),
  delete: (id) => api.delete(`/clients/api/${id}`),
  activities: (id, params) => api.get(`/clients/api/${id}/activities`, { params }),
  logActivity: (id, data) => api.post(`/clients/api/${id}/activities`, data),
  analyze: (id) => api.post(`/clients/api/${id}/analyze`),
  analyses: (id) => api.get(`/clients/api/${id}/analyses`),
  reminders: () => api.get('/clients/api/reminders/summary'),
  generatePotential: (data) => api.post('/clients/api/generate-potential', data),
  searchReal: (data) => api.post('/clients/api/search-real-clients', data),
  batchInsert: (data) => api.post('/clients/api/batch-insert', data),
  exportCsv: () => api.get('/clients/api/export/csv', { responseType: 'blob' }),
}

// ========== Quotation API ==========
export const quotationApi = {
  list: (params) => api.get('/quotation/api/list', { params }),
  get: (no) => api.get(`/quotation/api/${no}`),
  create: (data) => api.post('/quotation/api/create', data),
  update: (no, data) => api.put(`/quotation/api/${no}`, data),
  delete: (no) => api.delete(`/quotation/api/${no}`),
  calculate: (data) => api.post('/quotation/api/calculate', data),
  aiOptimize: (data) => api.post('/quotation/api/ai-optimize', data),
  versions: (no) => api.get(`/quotation/api/${no}/versions`),
  stats: () => api.get('/quotation/api/stats'),
}

// ========== Market API ==========
export const marketApi = {
  listReports: () => api.get('/market/api/reports'),
  generateReport: (data) => api.post('/market/api/generate-report', data),
  getReport: (id) => api.get(`/market/api/reports/${id}`),
  deleteReport: (id) => api.delete(`/market/api/reports/${id}`),
}

// ========== Outreach API ==========
export const outreachApi = {
  generateEmail: (data) => api.post('/outreach/api/generate-email', data),
  generateWhatsapp: (data) => api.post('/outreach/api/generate-whatsapp', data),
  generateLinkedin: (data) => api.post('/outreach/api/generate-linkedin', data),
}

// ========== Analytics API ==========
export const analyticsApi = {
  products: () => api.get('/analytics/api/products'),
  clients: () => api.get('/analytics/api/clients'),
}

export default api
