/**
 * 管理 API
 * 管理员专用 API
 */

import axios from 'axios'

const API_URL = '/api/v1/admin'

const adminApi = {
  // 用户管理
  async getUsers(params = {}) {
    return axios.get(`${API_URL}/users`, { params })
  },
  
  async getUserCount() {
    return axios.get(`${API_URL}/users/count`)
  },
  
  async updateUser(id, data) {
    return axios.put(`${API_URL}/users/${id}`, data)
  },
  
  async deleteUser(id) {
    return axios.delete(`${API_URL}/users/${id}`)
  },
  
  // 记录管理
  async getAllRecords(params = {}) {
    return axios.get(`${API_URL}/records`, { params })
  },
  
  async deleteRecord(id) {
    return axios.delete(`${API_URL}/records/${id}`)
  },
  
  // 分类管理
  async getAllCategories(type = null) {
    const params = type ? { type } : {}
    return axios.get(`${API_URL}/categories`, { params })
  },
  
  async createCategory(data) {
    return axios.post(`${API_URL}/categories`, data)
  },
  
  async updateCategory(id, data) {
    return axios.put(`${API_URL}/categories/${id}`, data)
  },
  
  async deleteCategory(id) {
    return axios.delete(`${API_URL}/categories/${id}`)
  },
  
  // 二级分类管理
  async getAllItems(categoryId = null) {
    const params = categoryId ? { category_id: categoryId } : {}
    return axios.get(`${API_URL}/category-items`, { params })
  },
  
  async createCategoryItem(data) {
    return axios.post(`${API_URL}/category-items`, data)
  },
  
  async deleteCategoryItem(id) {
    return axios.delete(`${API_URL}/category-items/${id}`)
  },
  
  // 支付方式管理
  async getAllPaymentMethods() {
    return axios.get(`${API_URL}/payment-methods`)
  },
  
  async createPaymentMethod(data) {
    return axios.post(`${API_URL}/payment-methods`, data)
  },
  
  async deletePaymentMethod(id) {
    return axios.delete(`${API_URL}/payment-methods/${id}`)
  },
  
  // 项目管理
  async getAllProjects(params = {}) {
    return axios.get(`${API_URL}/projects`, { params })
  },
  
  async deleteProject(id) {
    return axios.delete(`${API_URL}/projects/${id}`)
  },
  
  // 统计数据
  async getStats() {
    return axios.get(`${API_URL}/stats`)
  }
}

export default adminApi
