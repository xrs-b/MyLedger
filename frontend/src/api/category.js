/**
 * 分类 API
 */

import api from './index'

const categoryApi = {
  async getAll() {
    return api.get('/categories')
  },

  async getList(type = null) {
    return api.get('/categories/list', { type })
  },

  async getItems(categoryId = null) {
    return api.get('/categories/items', { category_id: categoryId })
  },

  async getPaymentMethods() {
    return api.get('/categories/payment-methods')
  },

  async create(data) {
    return api.post('/categories', data)
  },

  async update(id, data) {
    return api.put(`/categories/${id}`, data)
  },

  async delete(id) {
    return api.delete(`/categories/${id}`)
  }
}

export default categoryApi
