/**
 * 记账 API
 * 记账 CRUD 操作
 */

import api from './index'

const recordApi = {
  /**
   * 获取记账列表
   * @param {Object} params - 筛选参数
   */
  async getList(params = {}) {
    return api.get('/records', { params })
  },

  /**
   * 获取记账详情
   * @param {number} id - 记账ID
   */
  async getById(id) {
    return api.get(`/records/${id}`)
  },

  /**
   * 创建记账
   * @param {Object} data - 记账数据
   */
  async create(data) {
    return api.post('/records', data)
  },

  /**
   * 更新记账
   * @param {number} id - 记账ID
   * @param {Object} data - 更新数据
   */
  async update(id, data) {
    return api.put(`/records/${id}`, data)
  },

  /**
   * 删除记账
   * @param {number} id - 记账ID
   */
  async delete(id) {
    return api.delete(`/records/${id}`)
  },

  /**
   * 获取统计摘要
   * @param {Object} params - 日期范围
   */
  async getStats(params = {}) {
    return api.get('/records/stats/summary', { params })
  }
}

export default recordApi
