<template>
  <div class="project-create-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑项目' : '创建新项目' }}</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>
      
      <el-form
        ref="projectFormRef"
        :model="projectForm"
        :rules="projectRules"
        label-width="140px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="projectForm.name" placeholder="请输入项目名称" />
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="推广产品/服务" prop="product">
              <el-input v-model="projectForm.product" placeholder="请输入推广的产品或服务" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="目标市场" prop="target_market">
              <el-select v-model="projectForm.target_market" placeholder="请选择目标市场" style="width: 100%">
                <el-option label="美国" value="US" />
                <el-option label="英国" value="UK" />
                <el-option label="加拿大" value="CA" />
                <el-option label="澳大利亚" value="AU" />
                <el-option label="新加坡" value="SG" />
                <el-option label="日本" value="JP" />
                <el-option label="德国" value="DE" />
                <el-option label="法国" value="FR" />
              </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="12">
            <el-form-item label="目标域名">
              <el-input v-model="projectForm.target_domain" placeholder="选填，如 example.com" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="核心卖点" prop="core_selling_point">
          <el-input
            v-model="projectForm.core_selling_point"
            type="textarea"
            :rows="3"
            placeholder="请描述产品/服务的核心卖点和独特优势"
          />
        </el-form-item>
        
        <el-form-item label="目标关键词" prop="target_keyword">
          <el-input
            v-model="projectForm.target_keyword"
            type="textarea"
            :rows="2"
            placeholder="请输入目标关键词，多个关键词用逗号分隔"
          />
        </el-form-item>
        
        <el-form-item label="推广渠道" prop="target_channel">
          <el-checkbox-group v-model="projectForm.target_channel">
            <el-checkbox label="Facebook" />
            <el-checkbox label="Instagram" />
            <el-checkbox label="TikTok" />
            <el-checkbox label="Twitter" />
            <el-checkbox label="YouTube" />
            <el-checkbox label="Pinterest" />
            <el-checkbox label="LinkedIn" />
            <el-checkbox label="Reddit" />
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="联盟链接">
          <el-input v-model="projectForm.affiliate_link" placeholder="选填，如 Amazon Affiliate 链接" />
        </el-form-item>
        
        <el-form-item label="截止时间">
          <el-date-picker
            v-model="projectForm.deadline"
            type="datetime"
            placeholder="选择截止时间"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="projectForm.remark"
            type="textarea"
            :rows="2"
            placeholder="选填，其他说明或要求"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ isEdit ? '保存修改' : '创建项目' }}
          </el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { createProject, getProjectDetail, updateProject } from '@/api/project'

const route = useRoute()
const router = useRouter()

const projectFormRef = ref<FormInstance>()
const submitting = ref(false)
const isEdit = ref(false)
const projectId = ref<number | null>(null)

const projectForm = reactive({
  name: '',
  product: '',
  target_market: '',
  core_selling_point: '',
  target_keyword: '',
  target_channel: [] as string[],
  target_domain: '',
  affiliate_link: '',
  deadline: '' as string | Date | null,
  remark: ''
})

const projectRules: FormRules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  product: [
    { required: true, message: '请输入推广产品/服务', trigger: 'blur' }
  ],
  target_market: [
    { required: true, message: '请选择目标市场', trigger: 'change' }
  ],
  core_selling_point: [
    { required: true, message: '请输入核心卖点', trigger: 'blur' }
  ],
  target_keyword: [
    { required: true, message: '请输入目标关键词', trigger: 'blur' }
  ],
  target_channel: [
    { type: 'array', required: true, message: '请选择推广渠道', trigger: 'change' }
  ]
}

// 检查是否是编辑模式
onMounted(() => {
  const { id, action } = route.query
  if (id && action === 'edit') {
    isEdit.value = true
    projectId.value = Number(id)
    loadProjectDetail(projectId.value)
  }
})

const loadProjectDetail = async (id: number) => {
  try {
    const res = await getProjectDetail(id)
    const data = res.data
    Object.assign(projectForm, {
      name: data.name,
      product: data.product,
      target_market: data.target_market,
      target_domain: data.target_domain || '',
      core_selling_point: data.core_selling_point,
      target_keyword: data.target_keyword,
      target_channel: JSON.parse(data.target_channel || '[]'),
      affiliate_link: data.affiliate_link || '',
      deadline: data.deadline || null,
      remark: data.remark || ''
    })
  } catch (error) {
    console.error('加载项目详情失败:', error)
    ElMessage.error('加载项目失败')
  }
}

const handleSubmit = async () => {
  if (!projectFormRef.value) return
  
  await projectFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        const submitData = {
          ...projectForm,
          target_channel: JSON.stringify(projectForm.target_channel)
        }
        
        if (isEdit.value && projectId.value) {
          await updateProject(projectId.value, submitData)
          ElMessage.success('项目已更新')
        } else {
          await createProject(submitData)
          ElMessage.success('项目创建成功')
        }
        
        router.push('/projects')
      } catch (error) {
        console.error('提交项目失败:', error)
      } finally {
        submitting.value = false
      }
    }
  })
}
</script>

<style scoped>
.project-create-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
