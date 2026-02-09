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
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.user?.is_admin || false,
    getToken: (state) => state.token
  },

  // ============ 动作 ============
  actions: {
    /**
     * 用户登录
     */
    async login(username, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authApi.login(username, password)
        const { access_token, user } = response.data
        
        this.token = access_token
        localStorage.setItem('token', access_token)
        this.user = user
        
        return { success: true, user }
      } catch (error) {
        this.error = error.data?.detail || '登录失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 用户注册
     */
    async register(username, password, inviteCode) {
      this.loading = true
      this.error = null
      
      try {
        await authApi.register(username, password, inviteCode)
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '注册失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载用户信息
     */
    async loadUser() {
      if (!this.token) return
      
      try {
        const response = await authApi.me()
        this.user = response.data
        return { success: true, user: this.user }
      } catch (error) {
        this.logout()
        return { success: false }
      }
    },

    /**
     * 用户退出
     */
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
