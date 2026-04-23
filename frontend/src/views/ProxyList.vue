<template>
  <div class="proxy-list-container">
    <el-card>
      <div class="header">
        <h2>代理管理</h2>
        <div>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加代理
          </el-button>
          <el-button @click="batchCheck">批量检测</el-button>
        </div>
      </div>
      
      <!-- 代理列表 -->
      <el-table :data="proxyList" v-loading="loading">
        <el-table-column prop="proxy_name" label="代理名称" width="150" />
        <el-table-column prop="ip_address" label="IP 地址" width="150">
          <template #default="{ row }">
            {{ row.ip_address }}:{{ row.port }}
          </template>
        </el-table-column>
        <el-table-column prop="proxy_type" label="类型" width="100" />
        <el-table-column prop="country" label="国家" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="health_status" label="健康状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getHealthType(row.health_status)">{{ row.health_status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_check" label="最后检查" width="180">
          <template #default="{ row }">
            {{ row.last_check ? formatDate(row.last_check) : '未检查' }}
          </template>
        </el-table-column>
        <el-table-column prop="response_time" label="响应时间" width="100">
          <template #default="{ row }">
            {{ row.response_time ? row.response_time + 'ms' : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="checkHealth(row.id)">检测</el-button>
            <el-button type="danger" link @click="deleteProxy(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 添加代理对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="添加代理"
      width="500px"
    >
      <el-form :model="proxyForm" label-width="100px">
        <el-form-item label="代理名称" required>
          <el-input v-model="proxyForm.proxy_name" placeholder="给代理起个名字" />
        </el-form-item>
        <el-form-item label="IP 地址" required>
          <el-input v-model="proxyForm.ip_address" placeholder="123.123.123.123" />
        </el-form-item>
        <el-form-item label="端口" required>
          <el-input-number v-model="proxyForm.port" :min="1" :max="65535" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="proxyForm.proxy_type" style="width: 100%">
            <el-option label="HTTP" value="http" />
            <el-option label="HTTPS" value="https" />
            <el-option label="SOCKS5" value="socks5" />
          </el-select>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="proxyForm.username" placeholder="选填" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="proxyForm.password" type="password" placeholder="选填" />
        </el-form-item>
        <el-form-item label="国家">
          <el-input v-model="proxyForm.country" placeholder="如：US" />
        </el-form-item>
        <el-form-item label="城市">
          <el-input v-model="proxyForm.city" placeholder="如：New York" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="closeDialog">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const proxyList = ref<any[]>([])

const proxyForm = reactive({
  proxy_name: '',
  ip_address: '',
  port: 8080,
  proxy_type: 'http',
  username: '',
  password: '',
  country: '',
  city: ''
})

const getHealthType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'danger' | 'info'> = {
    healthy: 'success',
    unhealthy: 'warning',
    error: 'danger'
  }
  return types[status] || 'info'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadProxies = async () => {
  loading.value = true
  try {
    const res = await request({
      url: '/proxies',
      method: 'get'
    })
    proxyList.value = res.data
  } catch (error) {
    console.error('加载代理列表失败:', error)
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  Object.assign(proxyForm, {
    proxy_name: '',
    ip_address: '',
    port: 8080,
    proxy_type: 'http',
    username: '',
    password: '',
    country: '',
    city: ''
  })
  dialogVisible.value = true
}

const closeDialog = () => {
  dialogVisible.value = false
}

const submitForm = async () => {
  if (!proxyForm.proxy_name || !proxyForm.ip_address) {
    ElMessage.warning('请填写代理名称和 IP 地址')
    return
  }
  
  submitting.value = true
  try {
    await request({
      url: '/proxies',
      method: 'post',
      data: proxyForm
    })
    ElMessage.success('代理添加成功')
    closeDialog()
    loadProxies()
  } catch (error) {
    console.error('添加代理失败:', error)
  } finally {
    submitting.value = false
  }
}

const checkHealth = async (id: number) => {
  try {
    const res = await request({
      url: `/proxies/${id}/health-check`,
      method: 'post'
    })
    ElMessage.success(res.msg)
    loadProxies()
  } catch (error) {
    console.error('检查代理失败:', error)
  }
}

const batchCheck = async () => {
  try {
    const res = await request({
      url: '/proxies/batch-check',
      method: 'post'
    })
    ElMessage.success(`检查完成：健康 ${res.data.healthy} / 总计 ${res.data.total}`)
    loadProxies()
  } catch (error) {
    console.error('批量检查失败:', error)
  }
}

const deleteProxy = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个代理吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await request({
      url: `/proxies/${id}`,
      method: 'delete'
    })
    ElMessage.success('代理已删除')
    loadProxies()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除代理失败:', error)
    }
  }
}

onMounted(() => {
  loadProxies()
})
</script>

<style scoped>
.proxy-list-container {
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
</style>
