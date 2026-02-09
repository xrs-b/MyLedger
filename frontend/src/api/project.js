/**
 * 项目 API
 */

import api from './index'

const projectApi = {
  async getList(status = null) {
    return api.get('/projects', { status })
  },

  async getById(id) {
    return api.get(`/projects/${id}`)
  },

  async create(data) {
    return api.post('/projects', data)
  },

  async update(id, data) {
    return api.put(`/projects/${id}`, data)
  },

  async delete(id) {
    return api.delete(`/projects/${id}`)
  }
}

export default projectApi
