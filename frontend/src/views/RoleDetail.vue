<template>
  <div class="role-detail-container">
    <el-card v-if="role">
      <template #header>
        <div class="card-header">
          <div class="role-header">
            <el-avatar :size="64" :src="role.avatar" icon="User" />
            <div class="role-info">
              <h2>{{ role.name }}</h2>
              <p>{{ role.role_code }}</p>
            </div>
          </div>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      
      <el-descriptions title="角色信息" :column="2" border>
        <el-descriptions-item label="角色名称">{{ role.name }}</el-descriptions-item>
        <el-descriptions-item label="角色编码">{{ role.role_code }}</el-descriptions-item>
        <el-descriptions-item label="状态" :span="2">
          <el-tag :type="getStatusType(role.status)">{{ role.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="核心职责" :span="2">{{ role.duty }}</el-descriptions-item>
        <el-descriptions-item label="任务统计">
          完成 {{ role.finish_task }} / 总计 {{ role.total_task }}
        </el-descriptions-item>
        <el-descriptions-item label="成功率">{{ role.success_rate }}%</el-descriptions-item>
      </el-descriptions>
      
      <h3 style="margin-top: 30px">默认 Prompt</h3>
      <el-input
        v-model="role.default_prompt"
        type="textarea"
        :rows="10"
        readonly
      />
      
      <h3 style="margin-top: 20px">当前任务</h3>
      <el-alert
        v-if="role.current_task"
        :title="role.current_task"
        type="info"
        show-icon
      />
      <el-empty v-else description="暂无执行中的任务" />
      
      <h3 style="margin-top: 20px">历史任务</h3>
      <el-table :data="historyTasks" style="width: 100%">
        <el-table-column prop="task_name" label="任务名称" />
        <el-table-column prop="project_name" label="所属项目" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="finish_time" label="完成时间" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import request from '@/utils/request'

const route = useRoute()
const role = ref<any>(null)
const historyTasks = ref<any[]>([])

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    idle: 'success',
    running: 'warning',
    error: 'danger'
  }
  return types[status] || 'info'
}

const loadRoleDetail = async () => {
  const id = Number(route.params.id)
  try {
    const [roleRes, historyRes] = await Promise.all([
      request({ url: `/roles/${id}`, method: 'get' }),
      request({ url: `/roles/${id}/history`, method: 'get', params: { page: 1, page_size: 10 } })
    ])
    role.value = roleRes.data
    historyTasks.value = historyRes.data || []
  } catch (error) {
    console.error('加载角色详情失败:', error)
  }
}

onMounted(() => {
  loadRoleDetail()
})
</script>

<style scoped>
.role-detail-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.role-header {
  display: flex;
  align-items: center;
  gap: 15px;
}

.role-info h2 {
  margin: 0 0 5px;
  font-size: 24px;
}

.role-info p {
  margin: 0;
  color: #909399;
}
</style>
