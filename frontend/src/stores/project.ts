import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getProjectList, getProjectDetail, createProject, updateProject, deleteProject } from '@/api/project'
import type { Project, ProjectCreate } from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projectList = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const total = ref(0)

  /**
   * 获取项目列表
   */
  async function fetchProjectList(params: { page: number; page_size: number; status?: string }) {
    const res = await getProjectList(params)
    projectList.value = res.data
    total.value = res.total
    return res
  }

  /**
   * 获取项目详情
   */
  async function fetchProjectDetail(id: number) {
    const res = await getProjectDetail(id)
    currentProject.value = res.data
    return res
  }

  /**
   * 创建项目
   */
  async function createNewProject(data: ProjectCreate) {
    const res = await createProject(data)
    await fetchProjectList({ page: 1, page_size: 10 })
    return res
  }

  /**
   * 更新项目
   */
  async function updateProjectData(id: number, data: Partial<ProjectCreate>) {
    const res = await updateProject(id, data)
    if (currentProject.value?.id === id) {
      currentProject.value = res.data
    }
    await fetchProjectList({ page: 1, page_size: 10 })
    return res
  }

  /**
   * 删除项目
   */
  async function deleteProjectData(id: number) {
    const res = await deleteProject(id)
    await fetchProjectList({ page: 1, page_size: 10 })
    return res
  }

  return {
    projectList,
    currentProject,
    total,
    fetchProjectList,
    fetchProjectDetail,
    createNewProject,
    updateProjectData,
    deleteProjectData
  }
})
