import request from '@/utils/request'

/**
 * 获取总览数据
 */
export function getOverviewStats() {
  return request({
    url: '/stats/overview',
    method: 'get'
  })
}

/**
 * 获取趋势数据
 */
export function getTrendStats() {
  return request({
    url: '/stats/trend',
    method: 'get'
  })
}

/**
 * 获取渠道数据
 */
export function getChannelStats() {
  return request({
    url: '/stats/channel',
    method: 'get'
  })
}
