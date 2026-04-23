<template>
  <div class="channel-list-container">
    <el-card>
      <h2>渠道管理</h2>
      
      <el-table :data="channelList" style="width: 100%">
        <el-table-column prop="channel" label="渠道名称" width="150" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="account_count" label="绑定账号数" width="120" />
        <el-table-column prop="today_posts" label="今日发布" width="100" />
        <el-table-column prop="total_views" label="总曝光量" width="120" />
        <el-table-column prop="total_clicks" label="总点击量" width="120" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link>配置</el-button>
            <el-button type="primary" link>查看账号</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const channelList = ref([
  { channel: 'Facebook', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'Instagram', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'TikTok', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'Twitter', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'YouTube', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'Pinterest', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'LinkedIn', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 },
  { channel: 'Reddit', status: 'active', account_count: 0, today_posts: 0, total_views: 0, total_clicks: 0 }
])
</script>

<style scoped>
.channel-list-container {
  padding: 20px;
}
</style>
