<template>
  <div class="settings-container">
    <el-card>
      <h2>系统设置</h2>
      
      <el-tabs>
        <el-tab-pane label="AI 配置">
          <el-form label-width="150px">
            <el-form-item label="默认 AI 模型">
              <el-select v-model="aiConfig.model" style="width: 300px">
                <el-option label="Claude 3.5 Sonnet" value="claude-3-5-sonnet" />
                <el-option label="GPT-4 Turbo" value="gpt-4-turbo" />
                <el-option label="GPT-3.5 Turbo" value="gpt-3.5-turbo" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="API Key">
              <el-input v-model="aiConfig.apiKey" type="password" show-password style="width: 400px" />
            </el-form-item>
            
            <el-form-item label="温度参数">
              <el-slider v-model="aiConfig.temperature" :min="0" :max="1" :step="0.1" style="width: 300px" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveAiConfig">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="代理配置">
          <el-alert title="代理配置功能开发中" type="info" show-icon />
        </el-tab-pane>
        
        <el-tab-pane label="系统配置">
          <el-form label-width="150px">
            <el-form-item label="最大并发任务数">
              <el-input-number v-model="systemConfig.maxConcurrent" :min="1" :max="20" />
            </el-form-item>
            
            <el-form-item label="默认最大重试次数">
              <el-input-number v-model="systemConfig.maxRetry" :min="0" :max="5" />
            </el-form-item>
            
            <el-form-item label="日志级别">
              <el-select v-model="systemConfig.logLevel" style="width: 200px">
                <el-option label="DEBUG" value="DEBUG" />
                <el-option label="INFO" value="INFO" />
                <el-option label="WARNING" value="WARNING" />
                <el-option label="ERROR" value="ERROR" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveSystemConfig">保存配置</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const aiConfig = reactive({
  model: 'claude-3-5-sonnet',
  apiKey: '',
  temperature: 0.7
})

const systemConfig = reactive({
  maxConcurrent: 10,
  maxRetry: 2,
  logLevel: 'INFO'
})

const saveAiConfig = () => {
  ElMessage.success('AI 配置已保存')
}

const saveSystemConfig = () => {
  ElMessage.success('系统配置已保存')
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}
</style>
