/**
 * 管理 API
 */

import api from './index'

const adminApi = {
  // 用户管理
  async getUsers(page = 1, pageSize = 20) {
    return api.get('/admin/users', { params: { page, page_size: pageSize } })
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

  // 记录管理
  async getRecords(page = 1, pageSize = 20) {
    return api.get('/admin/records', { params: { page, page_size: pageSize } })
  },

  async deleteRecord(id) {
    return api.delete(`/admin/records/${id}`)
  },

  // 分类管理
  async getCategories(type = null) {
    return api.get('/admin/categories', { params: { type } })
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

  // 二级分类管理
  async getCategoryItems(categoryId = null) {
    return api.get('/admin/category-items', { params: { category_id: categoryId } })
  },

  async createCategoryItem(data) {
    return api.post('/admin/category-items', data)
  },

  async deleteCategoryItem(id) {
    return api.delete(`/admin/category-items/${id}`)
  },

  // 支付方式管理
  async getPaymentMethods() {
    return api.get('/admin/payment-methods')
  },

  async createPaymentMethod(data) {
    return api.post('/admin/payment-methods', data)
  },

  async deletePaymentMethod(id) {
    return api.delete(`/admin/payment-methods/${id}`)
  },

  // 项目管理
  async getProjects(status = null, page = 1, pageSize = 20) {
    return api.get('/admin/projects', { params: { status, page, page_size: pageSize } })
  },

  async deleteProject(id) {
    return api.delete(`/admin/projects/${id}`)
  },

  // 统计数据
  async getStats() {
    return api.get('/admin/stats')
  }
}

export default adminApi
