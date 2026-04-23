import { createRouter, createWebHistory } from 'vue-router'

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
    component: () => import('@/views/Dashboard.vue'),
    meta: { title: '数据看板', requiresAuth: true }
  },
  { 
    path: '/projects', 
    name: 'Projects', 
    component: () => import('@/views/ProjectList.vue'),
    meta: { title: '项目管理', requiresAuth: true }
  },
  { 
    path: '/projects/create', 
    name: 'CreateProject', 
    component: () => import('@/views/ProjectCreate.vue'),
    meta: { title: '创建项目', requiresAuth: true }
  },
  { 
    path: '/projects/:id', 
    name: 'ProjectDetail', 
    component: () => import('@/views/ProjectDetail.vue'),
    meta: { title: '项目详情', requiresAuth: true }
  },
  { 
    path: '/roles', 
    name: 'Roles', 
    component: () => import('@/views/RoleList.vue'),
    meta: { title: 'AI 角色', requiresAuth: true }
  },
  { 
    path: '/tasks', 
    name: 'Tasks', 
    component: () => import('@/views/TaskList.vue'),
    meta: { title: '任务监控', requiresAuth: true }
  },
  { 
    path: '/channels', 
    name: 'Channels', 
    component: () => import('@/views/ChannelList.vue'),
    meta: { title: '渠道管理', requiresAuth: true }
  },
  { 
    path: '/settings', 
    name: 'Settings', 
    component: () => import('@/views/Settings.vue'),
    meta: { title: '系统设置', requiresAuth: true }
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
