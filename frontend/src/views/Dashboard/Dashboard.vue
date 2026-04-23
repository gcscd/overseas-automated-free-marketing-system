<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 总览数据卡片 -->
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-header">
            <span class="stat-label">项目总数</span>
            <el-icon class="stat-icon" color="#409EFF"><Folder /></el-icon>
          </div>
          <div class="stat-value">{{ stats.projects?.total || 0 }}</div>
          <div class="stat-detail">
            <span class="text-running">运行中：{{ stats.projects?.running || 0 }}</span>
            <span class="text-finished">已完成：{{ stats.projects?.finished || 0 }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-header">
            <span class="stat-label">任务总数</span>
            <el-icon class="stat-icon" color="#67C23A"><List /></el-icon>
          </div>
          <div class="stat-value">{{ stats.tasks?.total || 0 }}</div>
          <div class="stat-detail">
            <span class="text-running">进行中：{{ stats.tasks?.running || 0 }}</span>
            <span class="text-failed">失败：{{ stats.tasks?.failed || 0 }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-header">
            <span class="stat-label">AI 角色</span>
            <el-icon class="stat-icon" color="#E6A23C"><User /></el-icon>
          </div>
          <div class="stat-value">{{ stats.roles?.total || 0 }}</div>
          <div class="stat-detail">
            <span class="text-idle">空闲：{{ stats.roles?.idle || 0 }}</span>
            <span class="text-running">工作中：{{ stats.roles?.running || 0 }}</span>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-header">
            <span class="stat-label">累计收入</span>
            <el-icon class="stat-icon" color="#F56C6C"><Money /></el-icon>
          </div>
          <div class="stat-value">${{ stats.totals?.total_commission || '0.00' }}</div>
          <div class="stat-detail">
            <span>总曝光：{{ stats.totals?.total_view || 0 }}</span>
            <span>总点击：{{ stats.totals?.total_click || 0 }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card>
          <template #header>
            <span>数据趋势</span>
          </template>
          <div ref="trendChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>渠道分布</span>
          </template>
          <div ref="channelChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 最近项目 -->
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>最近项目</span>
          <el-button type="primary" text @click="$router.push('/projects')">
            查看更多
          </el-button>
        </div>
      </template>
      
      <el-table :data="recentProjects" style="width: 100%">
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="product" label="推广产品" />
        <el-table-column prop="target_market" label="目标市场" />
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
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewProject(row.id)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { onBeforeRouteLeave } from 'vue-router'
import { use, init } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { getOverviewStats, getTrendStats, getChannelStats } from '@/api/stats'
import { getProjectList } from '@/api/project'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent
])

const router = useRouter()

const stats = ref<any>({})
const recentProjects = ref<any[]>([])

const trendChartRef = ref<HTMLElement>()
const channelChartRef = ref<HTMLElement>()

let trendChart: any = null
let channelChart: any = null

const getStatusType = (status: string) => {
  const types: Record<string, 'success' | 'warning' | 'info' | 'danger'> = {
    finished: 'success',
    running: 'warning',
    pending: 'info',
    paused: 'info'
  }
  return types[status] || 'info'
}

const loadStats = async () => {
  try {
    const res = await getOverviewStats()
    stats.value = res.data
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentProjects = async () => {
  try {
    const res = await getProjectList({ page: 1, page_size: 5 })
    recentProjects.value = res.data
  } catch (error) {
    console.error('加载项目列表失败:', error)
  }
}

const initTrendChart = async () => {
  if (!trendChartRef.value) return
  
  try {
    const res = await getTrendStats()
    const { dates, views, clicks, conversions } = res.data
    
    trendChart = init(trendChartRef.value)
    trendChart.setOption({
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['曝光量', '点击量', '转化量']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '曝光量',
          type: 'line',
          data: views,
          smooth: true,
          itemStyle: { color: '#409EFF' }
        },
        {
          name: '点击量',
          type: 'line',
          data: clicks,
          smooth: true,
          itemStyle: { color: '#67C23A' }
        },
        {
          name: '转化量',
          type: 'line',
          data: conversions,
          smooth: true,
          itemStyle: { color: '#E6A23C' }
        }
      ]
    })
  } catch (error) {
    console.error('加载趋势图表失败:', error)
  }
}

const initChannelChart = async () => {
  if (!channelChartRef.value) return
  
  try {
    const res = await getChannelStats()
    const channels = res.data
    
    channelChart = init(channelChartRef.value)
    channelChart.setOption({
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '渠道',
          type: 'pie',
          radius: '50%',
          data: channels.map((c: any) => ({
            name: c.channel,
            value: c.views
          })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    })
  } catch (error) {
    console.error('加载渠道图表失败:', error)
  }
}

const viewProject = (id: number) => {
  router.push(`/projects/${id}`)
}

onMounted(async () => {
  await Promise.all([
    loadStats(),
    loadRecentProjects(),
    initTrendChart(),
    initChannelChart()
  ])
})

// 清理图表
onBeforeRouteLeave(() => {
  trendChart?.dispose()
  channelChart?.dispose()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.stat-card {
  text-align: center;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-icon {
  font-size: 24px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.stat-detail {
  display: flex;
  justify-content: space-around;
  font-size: 12px;
  color: #909399;
}

.text-running {
  color: #67C23A;
}

.text-finished {
  color: #409EFF;
}

.text-failed {
  color: #F56C6C;
}

.text-idle {
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
