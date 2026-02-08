/**
 * 项目 API
 * 项目 CRUD 操作
 */

import axios from 'axios'

const API_URL = '/api/v1/projects'

const projectApi = {
  /**
   * 获取项目列表
   * @param {Object} params - 筛选参数
   */
  async getList(params = {}) {
    return axios.get(API_URL, { params })
  },

  /**
   * 获取项目详情
   * @param {number} id - 项目ID
   */
  async getById(id) {
    return axios.get(`${API_URL}/${id}`)
  },

  /**
   * 创建项目
   * @param {Object} data - 项目数据
   */
  async create(data) {
    return axios.post(API_URL, data)
  },

  /**
   * 更新项目
   * @param {number} id - 项目ID
   * @param {Object} data - 更新数据
   */
  async update(id, data) {
    return axios.put(`${API_URL}/${id}`, data)
  },

  /**
   * 删除项目
   * @param {number} id - 项目ID
   */
  async delete(id) {
    return axios.delete(`${API_URL}/${id}`)
  },

  /**
   * 完成项目
   * @param {number} id - 项目ID
   */
  async complete(id) {
    return axios.post(`${API_URL}/${id}/complete`)
  },

  /**
   * 重新打开项目
   * @param {number} id - 项目ID
   */
  async reopen(id) {
    return axios.post(`${API_URL}/${id}/reopen`)
  }
}

export default projectApi
