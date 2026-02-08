/**
 * 认证状态管理
 * 使用 Pinia 管理用户认证状态
 */

import { defineStore } from 'pinia'
import authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  // ============ 状态 ============
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    loading: false,
    error: null
  }),

  // ============ Getter ============
  getters: {
    // 是否已登录
    isLoggedIn: (state) => !!state.token,
    
    // 是否是管理员
    isAdmin: (state) => state.user?.is_admin || false,
    
    // 获取 Token
    getToken: (state) => state.token
  },

  // ============ 动作 ============
  actions: {
    /**
     * 用户登录
     * @param {string} username - 账号名
     * @param {string} password - 密码
     */
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.login({ username, password })
        const { access_token, user } = response.data
        
        // 保存 Token
        this.token = access_token
        localStorage.setItem('token', access_token)
        this.user = user
        
        return { success: true, user }
      } catch (error) {
        const message = error.response?.data?.detail || '登录失败'
        this.error = message
        return { success: false, message }
      } finally {
        this.loading = false
      }
    },

    /**
     * 用户注册
     * @param {string} username - 账号名
     * @param {string} password - 密码
     * @param {string} inviteCode - 邀请码
     */
    async register(username, password, inviteCode) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.register({
          username,
          password,
          invite_code: inviteCode
        })
        
        const { is_admin } = response.data
        return { success: true, is_admin }
      } catch (error) {
        const message = error.response?.data?.detail || '注册失败'
        this.error = message
        return { success: false, message }
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取当前用户信息
     */
    async fetchUser() {
      if (!this.token) return
      
      this.loading = true
      try {
        const response = await authApi.me()
        this.user = response.data
      } catch (error) {
        // Token 无效，清除状态
        this.logout()
      } finally {
        this.loading = false
      }
    },

    /**
     * 退出登录
     */
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
