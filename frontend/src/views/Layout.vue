<template>
  <div class="layout-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="appStore.sidebarCollapsed ? '64px' : '220px'">
        <div class="logo">
          <el-icon v-if="!appStore.sidebarCollapsed" :size="32" color="#409EFF"><Histogram /></el-icon>
          <span v-if="!appStore.sidebarCollapsed">Hermes</span>
        </div>
        
        <el-menu
          :default-active="activeMenu"
          :collapse="appStore.sidebarCollapsed"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          router
          unique-opened
        >
          <el-menu-item index="/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <template #title>数据看板</template>
          </el-menu-item>
          
          <el-menu-item index="/projects">
            <el-icon><Folder /></el-icon>
            <template #title>项目管理</template>
          </el-menu-item>
          
          <el-menu-item index="/roles">
            <el-icon><User /></el-icon>
            <template #title>AI 角色</template>
          </el-menu-item>
          
          <el-menu-item index="/tasks">
            <el-icon><List /></el-icon>
            <template #title>任务监控</template>
          </el-menu-item>
          
          <el-menu-item index="/channels">
            <el-icon><Connection /></el-icon>
            <template #title>渠道管理</template>
          </el-menu-item>
          
          <el-menu-item index="/proxies">
            <el-icon><Position /></el-icon>
            <template #title>代理管理</template>
          </el-menu-item>
          
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <template #title>系统设置</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header>
          <div class="header-left">
            <el-icon class="collapse-btn" @click="toggleSidebar">
              <component :is="appStore.sidebarCollapsed ? 'Expand' : 'Fold'" />
            </el-icon>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="breadCrumbName">{{ breadCrumbName }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-dropdown>
              <span class="user-info">
                <el-avatar :size="32" icon="User" />
                <span class="username">{{ userStore.userInfo?.username || 'Admin' }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()

const appStore = useAppStore()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const breadCrumbName = computed(() => {
  return route.meta.title as string || ''
})

onMounted(async () => {
  // 获取用户信息
  await userStore.getUserInfo()
})

const toggleSidebar = () => {
  appStore.toggleSidebar()
}

const handleLogout = async () => {
  await userStore.userLogout()
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  transition: width 0.3s;
  overflow-x: hidden;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 60px;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}

.el-menu {
  border-right: none;
}

.el-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  transition: color 0.3s;
}

.collapse-btn:hover {
  color: #409EFF;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #606266;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
