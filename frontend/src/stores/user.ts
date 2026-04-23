import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, logout, getCurrentUser } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>(localStorage.getItem('access_token') || '')
  const userInfo = ref<any>(null)

  /**
   * 登录
   */
  async function userLogin(username: string, password: string) {
    const res = await login({ username, password })
    token.value = res.data.access_token
    localStorage.setItem('access_token', token.value)
    await getUserInfo()
    return res
  }

  /**
   * 获取用户信息
   */
  async function getUserInfo() {
    try {
      const res = await getCurrentUser()
      userInfo.value = res.data
      return res
    } catch (error) {
      console.error('获取用户信息失败:', error)
      return null
    }
  }

  /**
   * 登出
   */
  async function userLogout() {
    await logout()
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('access_token')
  }

  return {
    token,
    userInfo,
    userLogin,
    getUserInfo,
    userLogout
  }
})
