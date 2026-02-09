/**
 * 分类状态管理
 */

import { defineStore } from 'pinia'
import categoryApi from '@/api/category'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: {
      expense: [],
      income: []
    },
    paymentMethods: [],
    loading: false,
    error: null
  }),

  getters: {
    expenseCategories: (state) => state.categories.expense || [],
    incomeCategories: (state) => state.categories.income || []
  },

  actions: {
    async fetchCategories() {
      this.loading = true
      this.error = null
      
      try {
        const response = await categoryApi.getAll()
        this.categories = response.data || { expense: [], income: [] }
      } catch (error) {
        this.error = error.data?.detail || '获取分类失败'
        console.error('获取分类错误:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchPaymentMethods() {
      this.loading = true
      
      try {
        const response = await categoryApi.getPaymentMethods()
        this.paymentMethods = response.data || []
      } catch (error) {
        this.error = error.data?.detail || '获取支付方式失败'
        console.error('获取支付方式错误:', error)
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
