import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout.vue'

const routes = [
  { 
    path: '/', 
    name: 'Login', 
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: Layout,
    meta: { title: '数据看板', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/Dashboard.vue') }
    ]
  },
  { 
    path: '/projects', 
    name: 'Projects', 
    component: Layout,
    meta: { title: '项目管理', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/ProjectList.vue') },
      { path: 'create', component: () => import('@/views/ProjectCreate.vue') },
      { path: ':id', component: () => import('@/views/ProjectDetail.vue') }
    ]
  },
  { 
    path: '/roles', 
    name: 'Roles', 
    component: Layout,
    meta: { title: 'AI 角色', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/RoleList.vue') },
      { path: ':id', component: () => import('@/views/RoleDetail.vue') }
    ]
  },
  { 
    path: '/tasks', 
    name: 'Tasks', 
    component: Layout,
    meta: { title: '任务监控', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/TaskList.vue') }
    ]
  },
  { 
    path: '/channels', 
    name: 'Channels', 
    component: Layout,
    meta: { title: '渠道管理', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/ChannelList.vue') }
    ]
  },
  { 
    path: '/proxies', 
    name: 'Proxies', 
    component: Layout,
    meta: { title: '代理管理', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/ProxyList.vue') }
    ]
  },
  { 
    path: '/settings', 
    name: 'Settings', 
    component: Layout,
    meta: { title: '系统设置', requiresAuth: true },
    children: [
      { path: '', component: () => import('@/views/Settings.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - Hermes 营销系统` : 'Hermes 营销系统'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('access_token')
    if (!token && to.name !== 'Login') {
      next({ name: 'Login' })
      return
    }
  }
  
  // 如果已登录，访问登录页则跳转到首页
  if (to.name === 'Login') {
    const token = localStorage.getItem('access_token')
    if (token) {
      next({ name: 'Dashboard' })
      return
    }
  }
  
  next()
})

export default router
