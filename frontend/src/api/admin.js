/**
 * 管理 API
 */

import api from './index'

const adminApi = {
  async getUsers(page = 1, pageSize = 20) {
    return api.get('/admin/users', { page, page_size: pageSize })
  },

  async getUserCount() {
    return api.get('/admin/users/count')
  },

  async updateUser(id, data) {
    return api.put(`/admin/users/${id}`, data)
  },

  async deleteUser(id) {
    return api.delete(`/admin/users/${id}`)
  },

  async getRecords(page = 1, pageSize = 20) {
    return api.get('/admin/records', { page, page_size: pageSize })
  },

  async deleteRecord(id) {
    return api.delete(`/admin/records/${id}`)
  },

  async getCategories(type = null) {
    return api.get('/admin/categories', { type })
  },

  async createCategory(data) {
    return api.post('/admin/categories', data)
  },

  async updateCategory(id, data) {
    return api.put(`/admin/categories/${id}`, data)
  },

  async deleteCategory(id) {
    return api.delete(`/admin/categories/${id}`)
  },

  async getCategoryItems(categoryId = null) {
    return api.get('/admin/category-items', { category_id: categoryId })
  },

  async createCategoryItem(data) {
    return api.post('/admin/category-items', data)
  },

  async deleteCategoryItem(id) {
    return api.delete(`/admin/category-items/${id}`)
  },

  async getPaymentMethods() {
    return api.get('/admin/payment-methods')
  },

  async createPaymentMethod(data) {
    return api.post('/admin/payment-methods', data)
  },

  async deletePaymentMethod(id) {
    return api.delete(`/admin/payment-methods/${id}`)
  },

  async getProjects(status = null, page = 1, pageSize = 20) {
    return api.get('/admin/projects', { status, page, page_size: pageSize })
  },

  async deleteProject(id) {
    return api.delete(`/admin/projects/${id}`)
  },

  async getStats() {
    return api.get('/admin/stats')
  }
}

export default adminApi
