/**
 * 统计 API
 * 多维度统计接口
 */

import axios from 'axios'

const API_URL = '/api/v1/statistics'

const statisticsApi = {
  /**
   * 获取统计摘要
   * @param {Object} params - 筛选参数
   */
  async getSummary(params = {}) {
    return axios.get(`${API_URL}/summary`, { params })
  },

  /**
   * 按分类统计
   * @param {Object} params - 筛选参数
   */
  async getByCategory(params = {}) {
    return axios.get(`${API_URL}/by-category`, { params })
  },

  /**
   * 按日统计
   * @param {Object} params - 筛选参数
   */
  async getByDay(params = {}) {
    return axios.get(`${API_URL}/by-day`, { params })
  },

  /**
   * 按项目统计
   * @param {Object} params - 筛选参数
   */
  async getByProject(params = {}) {
    return axios.get(`${API_URL}/by-project`, { params })
  },

  /**
   * 趋势分析
   * @param {string} period - 周期 (day/week/month)
   */
  async getTrend(period = 'month') {
    return axios.get(`${API_URL}/trend`, { params: { period } })
  }
}

export default statisticsApi
