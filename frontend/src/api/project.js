/**
 * 项目 API
 */

import api from './index'

const projectApi = {
  /**
   * 获取项目列表
   */
  async getList(status = null) {
    return api.get('/projects', { params: { status } })
  },

  /**
   * 获取项目详情
   */
  async getById(id) {
    return api.get(`/projects/${id}`)
  },

  /**
   * 创建项目
   */
  async create(data) {
    return api.post('/projects', data)
  },

  /**
   * 更新项目
   */
  async update(id, data) {
    return api.put(`/projects/${id}`, data)
  },

  /**
   * 删除项目
   */
  async delete(id) {
    return api.delete(`/projects/${id}`)
  }
}

export default projectApi
