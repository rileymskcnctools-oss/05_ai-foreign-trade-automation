import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', name: 'Dashboard', component: () => import('../views/DashboardView.vue'), meta: { title: '数据概览' } },
  { path: '/products', name: 'Products', component: () => import('../views/ProductsView.vue'), meta: { title: '产品管理' } },
  { path: '/clients', name: 'Clients', component: () => import('../views/ClientsView.vue'), meta: { title: '客户CRM' } },
  { path: '/quotation', name: 'Quotation', component: () => import('../views/QuotationView.vue'), meta: { title: '报价助手' } },
  { path: '/market', name: 'Market', component: () => import('../views/MarketView.vue'), meta: { title: '市场研究' } },
  { path: '/outreach', name: 'Outreach', component: () => import('../views/OutreachView.vue'), meta: { title: '开发信' } },
  { path: '/analytics', name: 'Analytics', component: () => import('../views/AnalyticsView.vue'), meta: { title: '数据分析' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = `${to.meta.title || 'FT Workspace'} - FT Workspace`
})

export default router
