/**
 * 记账状态管理
 */

import { defineStore } from 'pinia'
import recordApi from '@/api/record'

export const useRecordStore = defineStore('record', {
  // ============ 状态 ============
  state: () => ({
    records: [],
    currentRecord: null,
    stats: null,
    pagination: {
      page: 1,
      pageSize: 20,
      total: 0,
      totalPages: 1
    },
    filters: {
      type: null,
      category_id: null,
      category_item_id: null,
      payment_method_id: null,
      project_id: null,
      start_date: null,
      end_date: null
    },
    loading: false,
    error: null
  }),

  // ============ Getter ============
  getters: {
    // 是否还有更多
    hasMore: (state) => state.pagination.page < state.pagination.totalPages,
    
    // 获取筛选条件
    getFilters: (state) => state.filters,
    
    // 收入总额
    incomeAmount: (state) => {
      const income = state.records.filter(r => r.type === 'income')
      return income.reduce((sum, r) => sum + Number(r.amount), 0)
    },
    
    // 支出总额
    expenseAmount: (state) => {
      const expense = state.records.filter(r => r.type === 'expense')
      return expense.reduce((sum, r) => sum + Number(r.amount), 0)
    }
  },

  // ============ 动作 ============
  actions: {
    /**
     * 获取记账列表
     * @param {boolean} append - 是否追加数据
     */
    async fetchRecords(append = false) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          ...this.filters,
          page: append ? this.pagination.page : 1,
          page_size: this.pagination.pageSize
        }
        
        // 移除空值
        Object.keys(params).forEach(key => {
          if (params[key] === null || params[key] === '') {
            delete params[key]
          }
        })
        
        const response = await recordApi.getList(params)
        const { records, total, page, page_size, total_pages } = response.data
        
        // 更新分页
        this.pagination = { page, pageSize: page_size, total, totalPages: total_pages }
        
        // 更新记录列表
        if (append) {
          this.records = [...this.records, ...records]
        } else {
          this.records = records
        }
        
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || '获取记账列表失败'
        console.error('获取记账列表错误:', error)
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 加载更多
     */
    async loadMore() {
      if (this.hasMore && !this.loading) {
        this.pagination.page++
        await this.fetchRecords(true)
      }
    },

    /**
     * 刷新列表
     */
    async refresh() {
      this.pagination.page = 1
      await this.fetchRecords(false)
    },

    /**
     * 获取记账详情
     * @param {number} id - 记账ID
     */
    async fetchRecord(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await recordApi.getById(id)
        this.currentRecord = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || '获取记账详情失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 创建记账
     * @param {Object} data - 记账数据
     */
    async create(data) {
      this.loading = true
      this.error = null
      
      try {
        await recordApi.create(data)
        await this.refresh()  // 刷新列表
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '创建失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 更新记账
     * @param {number} id - 记账ID
     * @param {Object} data - 更新数据
     */
    async update(id, data) {
      this.loading = true
      
      try {
        await recordApi.update(id, data)
        await this.refresh()
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '更新失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 删除记账
     * @param {number} id - 记账ID
     */
    async delete(id) {
      this.loading = true
      
      try {
        await recordApi.delete(id)
        await this.refresh()
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '删除失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取统计
     * @param {Object} params - 日期范围
     */
    async fetchStats(params = {}) {
      try {
        const response = await recordApi.getStats(params)
        this.stats = response.data
        return response.data
      } catch (error) {
        console.error('获取统计错误:', error)
        return null
      }
    },

    /**
     * 设置筛选条件
     * @param {Object} filters - 筛选条件
     */
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1
    },

    /**
     * 清空筛选条件
     */
    clearFilters() {
      this.filters = {
        type: null,
        category_id: null,
        category_item_id: null,
        payment_method_id: null,
        project_id: null,
        start_date: null,
        end_date: null
      }
      this.pagination.page = 1
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
