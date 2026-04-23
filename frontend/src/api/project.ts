import request from '@/utils/request'

export interface Project {
  id: number
  name: string
  product: string
  target_market: string
  core_selling_point: string
  target_keyword: string
  target_channel: string
  target_domain: string | null
  affiliate_link: string | null
  status: string
  progress: number
  total_task: number
  finish_task: number
  total_view: number
  total_click: number
  total_conversion: number
  total_commission: string
  create_time: string
  deadline?: string
  research_report?: string
  remark?: string
}

export interface ProjectCreate {
  name: string
  product: string
  target_market: string
  core_selling_point: string
  target_keyword: string
  target_channel: string
  target_domain?: string
  affiliate_link?: string
  deadline?: string
  remark?: string
}

/**
 * 获取项目列表
 */
export function getProjectList(params: { page: number; page_size: number; status?: string }) {
  return request({
    url: '/projects',
    method: 'get',
    params
  })
}

/**
 * 获取项目详情
 */
export function getProjectDetail(id: number) {
  return request({
    url: `/projects/${id}`,
    method: 'get'
  })
}

/**
 * 创建项目
 */
export function createProject(data: ProjectCreate) {
  return request({
    url: '/projects',
    method: 'post',
    data
  })
}

/**
 * 更新项目
 */
export function updateProject(id: number, data: Partial<ProjectCreate>) {
  return request({
    url: `/projects/${id}`,
    method: 'put',
    data
  })
}

/**
 * 更新项目状态
 */
export function updateProjectStatus(id: number, status: string) {
  return request({
    url: `/projects/${id}/status`,
    method: 'patch',
    params: { status }
  })
}

/**
 * 删除项目
 */
export function deleteProject(id: number) {
  return request({
    url: `/projects/${id}`,
    method: 'delete'
  })
}

/**
 * 获取项目任务列表
 */
export function getProjectTasks(id: number) {
  return request({
    url: `/projects/${id}/tasks`,
    method: 'get'
  })
}

/**
 * 获取项目统计数据
 */
export function getProjectStats(id: number) {
  return request({
    url: `/projects/${id}/stats`,
    method: 'get'
  })
}
