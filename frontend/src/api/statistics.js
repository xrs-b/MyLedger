/**
 * 统计 API
 * 多维度统计接口
 */

import api from './index'

const statisticsApi = {
  /**
   * 获取统计摘要
   * @param {Object} params - 筛选参数
   */
  async getSummary(params = {}) {
    return api.get('/statistics/summary', { params })
  },

  /**
   * 按分类统计
   * @param {Object} params - 筛选参数
   */
  async getByCategory(params = {}) {
    return api.get('/statistics/by-category', { params })
  },

  /**
   * 按日统计
   * @param {Object} params - 筛选参数
   */
  async getByDay(params = {}) {
    return api.get('/statistics/by-day', { params })
  },

  /**
   * 按项目统计
   * @param {Object} params - 筛选参数
   */
  async getByProject(params = {}) {
    return api.get('/statistics/by-project', { params })
  },

  /**
   * 趋势分析
   * @param {string} period - 周期 (day/week/month)
   */
  async getTrend(period = 'month') {
    return api.get('/statistics/trend', { params: { period } })
  }
}

export default statisticsApi
