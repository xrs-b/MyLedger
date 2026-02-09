/**
 * 分类 API
 */

import api from './index'

const categoryApi = {
  /**
   * 获取所有分类
   */
  async getAll() {
    return api.get('/categories')
  },

  /**
   * 获取分类列表
   */
  async getList(type = null) {
    return api.get('/categories/list', { params: { type } })
  },

  /**
   * 获取所有二级分类
   */
  async getItems(categoryId = null) {
    return api.get('/categories/items', { params: { category_id: categoryId } })
  },

  /**
   * 获取支付方式
   */
  async getPaymentMethods() {
    return api.get('/categories/payment-methods')
  },

  /**
   * 创建分类
   */
  async create(data) {
    return api.post('/categories', data)
  },

  /**
   * 更新分类
   */
  async update(id, data) {
    return api.put(`/categories/${id}`, data)
  },

  /**
   * 删除分类
   */
  async delete(id) {
    return api.delete(`/categories/${id}`)
  }
}

export default categoryApi
