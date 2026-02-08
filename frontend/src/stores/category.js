/**
 * 分类状态管理
 */

import { defineStore } from 'pinia'
import categoryApi from '@/api/category'

export const useCategoryStore = defineStore('category', {
  // ============ 状态 ============
  state: () => ({
    categories: {
      expense: [],  // 支出分类
      income: []    // 收入分类
    },
    paymentMethods: [],
    loading: false,
    error: null
  }),

  // ============ Getter ============
  getters: {
    // 获取支出分类
    expenseCategories: (state) => state.categories.expense,
    
    // 获取收入分类
    incomeCategories: (state) => state.categories.income,
    
    // 根据类型获取分类
    getByType: (state) => (type) => state.categories[type] || []
  },

  // ============ 动作 ============
  actions: {
    /**
     * 获取所有分类
     */
    async fetchCategories() {
      this.loading = true
      this.error = null
      
      try {
        const response = await categoryApi.getAll()
        this.categories = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '获取分类失败'
        console.error('获取分类错误:', error)
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取支付方式
     */
    async fetchPaymentMethods() {
      this.loading = true
      
      try {
        const response = await categoryApi.getPaymentMethods()
        this.paymentMethods = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || '获取支付方式失败'
        console.error('获取支付方式错误:', error)
      } finally {
        this.loading = false
      }
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
