<script setup lang="ts">
import { ref, onMounted } from 'vue'
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
.dashboard-wrapper {
  height: 100%;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 20px;
}

.el-main {
  background-color: #f0f2f5;
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
