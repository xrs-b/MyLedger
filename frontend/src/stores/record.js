/**
 * 记账状态管理
 */

import api from '@/api/record'

export const useRecordStore = defineStore('record', {
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

  getters: {
    hasMore: (state) => state.pagination.page < state.pagination.totalPages,
    getFilters: (state) => state.filters,
    incomeAmount: (state) => {
      const income = state.records.filter(r => r.type === 'income')
      return income.reduce((sum, r) => sum + Number(r.amount), 0)
    },
    expenseAmount: (state) => {
      const expense = state.records.filter(r => r.type === 'expense')
      return expense.reduce((sum, r) => sum + Number(r.amount), 0)
    }
  },

  actions: {
    async fetchRecords(append = false) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          ...this.filters,
          page: append ? this.pagination.page : 1,
          page_size: this.pagination.pageSize
        }
        
        Object.keys(params).forEach(key => {
          if (params[key] === null || params[key] === '') {
            delete params[key]
          }
        })
        
        const response = await api.getList(params)
        const { records, total, page, page_size, total_pages } = response.data
        
        this.pagination = { page, pageSize: page_size, total, totalPages: total_pages }
        
        if (append) {
          this.records = [...this.records, ...(records || [])]
        } else {
          this.records = records || []
        }
        
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取记账列表失败'
        console.error('获取记账列表错误:', error)
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async loadMore() {
      if (this.hasMore && !this.loading) {
        this.pagination.page++
        await this.fetchRecords(true)
      }
    },

    async refresh() {
      this.pagination.page = 1
      await this.fetchRecords(false)
    },

    async fetchRecord(id) {
      this.loading = true
      
      try {
        const response = await api.getById(id)
        this.currentRecord = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取记账详情失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async create(data) {
      this.loading = true
      
      try {
        await api.create(data)
        await this.refresh()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '创建失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async update(id, data) {
      this.loading = true
      
      try {
        await api.update(id, data)
        await this.refresh()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '更新失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async delete(id) {
      this.loading = true
      
      try {
        await api.delete(id)
        await this.refresh()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '删除失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchStats(params = {}) {
      try {
        const response = await api.getStats(params)
        this.stats = response.data
        return response.data
      } catch (error) {
        console.error('获取统计错误:', error)
        return null
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.pagination.page = 1
    },

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

    clearError() {
      this.error = null
    }
  }
})
