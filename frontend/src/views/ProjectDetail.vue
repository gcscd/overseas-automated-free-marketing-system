<template>
  <div class="project-detail-container">
    <el-card v-if="project">
      <template #header>
        <div class="card-header">
          <h2>{{ project.name }}</h2>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      
      <!-- 项目基本信息 -->
      <el-descriptions title="基本信息" :column="2" border>
        <el-descriptions-item label="项目名称">{{ project.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(project.status)">{{ project.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="推广产品">{{ project.product }}</el-descriptions-item>
        <el-descriptions-item label="目标市场">{{ project.target_market }}</el-descriptions-item>
        <el-descriptions-item label="进度">
          <el-progress :percentage="project.progress" />
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDate(project.create_time) }}</el-descriptions-item>
      </el-descriptions>
      
      <!-- 统计数据 -->
      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="6">
          <el-statistic title="任务总数" :value="stats?.tasks?.total || 0" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="已完成" :value="stats?.tasks?.finished || 0" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="总曝光" :value="project.total_view || 0" />
        </el-col>
        <el-col :span="6">
          <el-statistic title="总点击" :value="project.total_click || 0" />
        </el-col>
      </el-row>
      
      <!-- 任务列表 -->
      <h3 style="margin-top: 30px">任务列表</h3>
      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="task_name" label="任务名称" />
        <el-table-column prop="role_name" label="负责角色" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProjectDetail, getProjectTasks, getProjectStats } from '@/api/project'

const route = useRoute()
const project = ref<any>(null)
const tasks = ref<any[]>([])
const stats = ref<any>(null)

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    finished: 'success',
    running: 'warning',
    pending: 'info',
    failed: 'danger'
  }
  return types[status] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadProject = async () => {
  const id = Number(route.params.id)
  const [projectRes, tasksRes, statsRes] = await Promise.all([
    getProjectDetail(id),
    getProjectTasks(id),
    getProjectStats(id)
  ])
  
  project.value = projectRes.data
  tasks.value = tasksRes.data
  stats.value = statsRes.data
}

onMounted(() => {
  loadProject()
})
</script>

<style scoped>
.project-detail-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}
</style>
