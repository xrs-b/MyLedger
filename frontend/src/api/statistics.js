/**
 * 统计 API
 */

import api from './index'

const statisticsApi = {
  async getSummary(params = {}) {
    return api.get('/statistics/summary', params)
  },

  async getByCategory(params = {}) {
    return api.get('/statistics/by-category', params)
  },

  async getByDay(params = {}) {
    return api.get('/statistics/by-day', params)
  },

  async getByProject(params = {}) {
    return api.get('/statistics/by-project', params)
  },

  async getTrend(period = 'month') {
    return api.get('/statistics/trend', { period })
  }
}

export default statisticsApi
