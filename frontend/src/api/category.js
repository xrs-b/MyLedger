/**
 * 分类 API
 * 获取分类和支付方式
 */

import axios from 'axios'

const API_URL = '/api/v1/categories'

const categoryApi = {
  /**
   * 获取所有分类（包含二级分类）
   */
  async getAll() {
    return axios.get(API_URL)
  },

  /**
   * 获取分类列表
   * @param {string} type - 分类类型 (expense/income)
   */
  async getList(type = null) {
    const params = type ? { type } : {}
    return axios.get(`${API_URL}/list`, { params })
  },

  /**
   * 获取单个分类详情
   * @param {number} id - 分类ID
   */
  async getById(id) {
    return axios.get(`${API_URL}/${id}`)
  },

  /**
   * 创建分类
   * @param {Object} data - 分类数据
   */
  async create(data) {
    return axios.post(API_URL, data)
  },

  /**
   * 更新分类
   * @param {number} id - 分类ID
   * @param {Object} data - 更新数据
   */
  async update(id, data) {
    return axios.put(`${API_URL}/${id}`, data)
  },

  /**
   * 删除分类
   * @param {number} id - 分类ID
   */
  async delete(id) {
    return axios.delete(`${API_URL}/${id}`)
  },

  /**
   * 获取所有二级分类
   * @param {number} categoryId - 一级分类ID（可选）
   */
  async getItems(categoryId = null) {
    const params = categoryId ? { category_id: categoryId } : {}
    return axios.get(`${API_URL}/items`, { params })
  },

  /**
   * 获取支付方式列表
   */
  async getPaymentMethods() {
    return axios.get(`${API_URL}/payment-methods`)
  },

  /**
   * 创建支付方式
   * @param {Object} data - 支付方式数据
   */
  async createPaymentMethod(data) {
    return axios.post(`${API_URL}/payment-methods`, data)
  }
}

export default categoryApi
