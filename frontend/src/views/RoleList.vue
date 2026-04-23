<template>
  <div class="role-list-container">
    <el-card>
      <h2>AI 角色管理</h2>
      
      <el-table :data="roleList" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" width="150">
          <template #default="{ row }">
            <div class="role-name">
              <el-avatar :size="32" :src="row.avatar" icon="User" />
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role_code" label="角色编码" width="200" />
        <el-table-column prop="duty" label="核心职责" min-width="250" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="任务统计" width="150">
          <template #default="{ row }">
            {{ row.finish_task }}/{{ row.total_task }}
          </template>
        </el-table-column>
        <el-table-column label="成功率" width="100">
          <template #default="{ row }">
            {{ row.success_rate }}%
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row.id)">
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/utils/request'

const loading = ref(false)
const roleList = ref<any[]>([])

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    idle: 'success',
    running: 'warning',
    error: 'danger'
  }
  return types[status] || 'info'
}

const loadRoles = async () => {
  loading.value = true
  try {
    const res = await request({
      url: '/roles',
      method: 'get'
    })
    roleList.value = res.data
  } catch (error) {
    console.error('加载角色列表失败:', error)
  } finally {
    loading.value = false
  }
}

const viewDetail = (id: number) => {
  // TODO: 实现角色详情
  console.log('查看角色详情:', id)
}

onMounted(() => {
  loadRoles()
})
</script>

<style scoped>
.role-list-container {
  padding: 20px;
}

.role-name {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>
