/**
 * 认证 API
 * 处理用户注册、登录等认证请求
 */

import api from './index'

const authApi = {
  /**
   * 用户注册
   */
  async register(username, password, invite_code) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    formData.append('invite_code', invite_code)
    
    return api.post('/auth/register', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  /**
   * 用户登录
   */
  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },

  /**
   * 获取当前用户信息
   */
  async me() {
    return api.get('/auth/me')
  },

  /**
   * 退出登录
   */
  async logout() {
    return api.post('/auth/logout')
  },

  /**
   * 刷新 Token
   */
  async refresh() {
    return api.post('/auth/refresh')
  }
}

export default authApi
