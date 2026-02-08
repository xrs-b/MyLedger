/**
 * 认证 API
 * 处理用户注册、登录等认证请求
 */

import axios from 'axios'

const API_URL = '/api/v1/auth'

const authApi = {
  /**
   * 用户注册
   * @param {Object} data - 注册数据
   * @param {string} data.username - 账号名
   * @param {string} data.password - 密码
   * @param {string} data.invite_code - 邀请码
   */
  async register(data) {
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)
    formData.append('invite_code', data.invite_code)
    
    return axios.post(`${API_URL}/register`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  /**
   * 用户登录
   * @param {Object} data - 登录数据
   * @param {string} data.username - 账号名
   * @param {string} data.password - 密码
   */
  async login(data) {
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)
    
    return axios.post(`${API_URL}/login`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  /**
   * 获取当前用户信息
   */
  async me() {
    return axios.get(`${API_URL}/me`)
  },

  /**
   * 退出登录
   */
  async logout() {
    return axios.post(`${API_URL}/logout`)
  },

  /**
   * 刷新 Token
   */
  async refresh() {
    return axios.post(`${API_URL}/refresh`)
  }
}

export default authApi
