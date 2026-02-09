/**
 * 管理状态管理
 */

import { defineStore } from 'pinia'
import adminApi from '@/api/admin'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    stats: null,
    users: [],
    records: [],
    categories: [],
    paymentMethods: [],
    projects: [],
    pagination: {
      page: 1,
      pageSize: 20,
      total: 0
    },
    loading: false,
    error: null
  }),

  actions: {
    async fetchStats() {
      this.loading = true
      
      try {
        const response = await adminApi.getStats()
        this.stats = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取统计失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchUsers(page = 1, pageSize = 20) {
      this.loading = true
      
      try {
        const response = await adminApi.getUsers(page, pageSize)
        this.users = response.data || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取用户列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchRecords(page = 1, pageSize = 20) {
      this.loading = true
      
      try {
        const response = await adminApi.getRecords(page, pageSize)
        this.records = response.data?.records || []
        this.pagination.total = response.data?.total || 0
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取记录列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchCategories(type = null) {
      this.loading = true
      
      try {
        const response = await adminApi.getCategories(type)
        this.categories = response.data || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取分类列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchPaymentMethods() {
      this.loading = true
      
      try {
        const response = await adminApi.getPaymentMethods()
        this.paymentMethods = response.data || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取支付方式列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchProjects(status = null, page = 1, pageSize = 20) {
      this.loading = true
      
      try {
        const response = await adminApi.getProjects(status, page, pageSize)
        this.projects = response.data || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取项目列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteUser(id) {
      try {
        await adminApi.deleteUser(id)
        await this.fetchUsers()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '删除失败'
        return { success: false, message: this.error }
      }
    },

    async deleteRecord(id) {
      try {
        await adminApi.deleteRecord(id)
        await this.fetchRecords()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '删除失败'
        return { success: false, message: this.error }
      }
    },

    async deleteCategory(id) {
      try {
        await adminApi.deleteCategory(id)
        await this.fetchCategories()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '删除失败'
        return { success: false, message: this.error }
      }
    },

    clearError() {
      this.error = null
    }
  }
})
