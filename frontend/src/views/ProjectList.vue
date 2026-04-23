<template>
  <div class="project-list-container">
    <el-card>
      <div class="header">
        <h2>项目管理</h2>
        <el-button type="primary" @click="$router.push('/projects/create')">
          <el-icon><Plus /></el-icon>
          新建项目
        </el-button>
      </div>
      
      <!-- 筛选栏 -->
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="全部状态" clearable style="width: 150px">
            <el-option label="待启动" value="pending" />
            <el-option label="调研中" value="researching" />
            <el-option label="运行中" value="running" />
            <el-option label="已完成" value="finished" />
            <el-option label="已暂停" value="paused" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="loadProjects">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 项目列表 -->
      <el-table
        :data="projectList"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="项目名称" min-width="180" />
        <el-table-column prop="product" label="推广产品" min-width="150" />
        <el-table-column prop="target_market" label="目标市场" width="120" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度" width="150">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" />
          </template>
        </el-table-column>
        <el-table-column prop="total_task" label="任务" width="100">
          <template #default="{ row }">
            {{ row.finish_task }}/{{ row.total_task }}
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.create_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row.id)">
              详情
            </el-button>
            <el-button type="warning" link @click="editProject(row.id)">
              编辑
            </el-button>
            <el-button type="danger" link @click="deleteProject(row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadProjects"
          @current-change="loadProjects"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getProjectList, deleteProject } from '@/api/project'

const router = useRouter()

const loading = ref(false)
const projectList = ref<any[]>([])

const filterForm = reactive({
  status: ''
})

const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0
})

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    finished: 'success',
    running: 'warning',
    pending: 'info',
    researching: 'info',
    paused: 'info'
  }
  return types[status] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadProjects = async () => {
  loading.value = true
  try {
    const res = await getProjectList({
      page: pagination.page,
      page_size: pagination.page_size,
      status: filterForm.status || undefined
    })
    projectList.value = res.data
    pagination.total = res.total
  } catch (error) {
    console.error('加载项目列表失败:', error)
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.status = ''
  pagination.page = 1
  loadProjects()
}

const viewDetail = (id: number) => {
  router.push(`/projects/${id}`)
}

const editProject = (id: number) => {
  router.push(`/projects/${id}?action=edit`)
}

const deleteProjectItem = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个项目吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await deleteProject(id)
    ElMessage.success('项目已删除')
    loadProjects()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除项目失败:', error)
    }
  }
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.project-list-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
