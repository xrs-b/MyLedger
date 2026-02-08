/**
 * 记账 API
 * 记账 CRUD 操作
 */

import axios from 'axios'

const API_URL = '/api/v1/records'

const recordApi = {
  /**
   * 获取记账列表
   * @param {Object} params - 筛选参数
   */
  async getList(params = {}) {
    return axios.get(API_URL, { params })
  },

  /**
   * 获取记账详情
   * @param {number} id - 记账ID
   */
  async getById(id) {
    return axios.get(`${API_URL}/${id}`)
  },

  /**
   * 创建记账
   * @param {Object} data - 记账数据
   */
  async create(data) {
    return axios.post(API_URL, data)
  },

  /**
   * 更新记账
   * @param {number} id - 记账ID
   * @param {Object} data - 更新数据
   */
  async update(id, data) {
    return axios.put(`${API_URL}/${id}`, data)
  },

  /**
   * 删除记账
   * @param {number} id - 记账ID
   */
  async delete(id) {
    return axios.delete(`${API_URL}/${id}`)
  },

  /**
   * 获取统计摘要
   * @param {Object} params - 日期范围
   */
  async getStats(params = {}) {
    return axios.get(`${API_URL}/stats/summary`, { params })
  }
}

export default recordApi
