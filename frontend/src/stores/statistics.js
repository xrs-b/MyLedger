/**
 * 统计状态管理
 */

import { defineStore } from 'pinia'
import statisticsApi from '@/api/statistics'

export const useStatisticsStore = defineStore('statistics', {
  // ============ 状态 ============
  state: () => ({
    summary: null,
    categoryData: [],
    dailyData: [],
    projectData: [],
    trendData: [],
    filters: {
      start_date: null,
      end_date: null,
      type: null,
      category_id: null
    },
    loading: false,
    error: null
  }),

  // ============ Getter ============
  getters: {
    // 净收入
    netAmount: (state) => {
      if (!state.summary) return 0
      return state.summary.income_amount - state.summary.expense_amount
    },
    
    // 消费率
    expenseRate: (state) => {
      if (!state.summary || state.summary.income_amount <= 0) return 0
      return (state.summary.expense_amount / state.summary.income_amount * 100).toFixed(1)
    }
  },

  // ============ 动作 ============
  actions: {
    /**
     * 获取统计摘要
     */
    async fetchSummary() {
      this.loading = true
      this.error = null
      
      try {
        const params = this.buildParams()
        const response = await statisticsApi.getSummary(params)
        this.summary = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || '获取统计失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取分类统计
     */
    async fetchCategoryData() {
      this.loading = true
      
      try {
        const params = this.buildParams()
        const response = await statisticsApi.getByCategory(params)
        this.categoryData = response.data.categories
        return response.data
      } catch (error) {
        console.error('获取分类统计错误:', error)
        return null
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取按日统计
     */
    async fetchDailyData() {
      try {
        const params = this.buildParams()
        const response = await statisticsApi.getByDay(params)
        this.dailyData = response.data.data
        return response.data
      } catch (error) {
        console.error('获取按日统计错误:', error)
        return null
      }
    },

    /**
     * 获取项目统计
     */
    async fetchProjectData() {
      try {
        const params = this.buildParams()
        const response = await statisticsApi.getByProject(params)
        this.projectData = response.data.projects
        return response.data
      } catch (error) {
        console.error('获取项目统计错误:', error)
        return null
      }
    },

    /**
     * 获取趋势数据
     * @param {string} period - 周期
     */
    async fetchTrendData(period = 'month') {
      try {
        const response = await statisticsApi.getTrend(period)
        this.trendData = response.data.data
        return response.data
      } catch (error) {
        console.error('获取趋势数据错误:', error)
        return null
      }
    },

    /**
     * 加载全部统计
     */
    async loadAll() {
      this.loading = true
      await Promise.all([
        this.fetchSummary(),
        this.fetchCategoryData(),
        this.fetchDailyData(),
        this.fetchProjectData()
      ])
      this.loading = false
    },

    /**
     * 设置筛选条件
     * @param {Object} filters - 筛选条件
     */
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    /**
     * 清空筛选条件
     */
    clearFilters() {
      this.filters = {
        start_date: null,
        end_date: null,
        type: null,
        category_id: null
      }
    },

    /**
     * 构建查询参数
     */
    buildParams() {
      const params = {}
      if (this.filters.start_date) params.start_date = this.filters.start_date
      if (this.filters.end_date) params.end_date = this.filters.end_date
      if (this.filters.type) params.type = this.filters.type
      if (this.filters.category_id) params.category_id = this.filters.category_id
      return params
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
