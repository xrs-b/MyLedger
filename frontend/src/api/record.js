/**
 * 记账 API
 */

import api from './index'

const recordApi = {
  async getList(params = {}) {
    return api.get('/records', params)
  },

  async getById(id) {
    return api.get(`/records/${id}`)
  },

  async create(data) {
    return api.post('/records', data)
  },

  async update(id, data) {
    return api.put(`/records/${id}`, data)
  },

  async delete(id) {
    return api.delete(`/records/${id}`)
  },

  async getStats(params = {}) {
    return api.get('/records/stats/summary', params)
  }
}

export default recordApi
