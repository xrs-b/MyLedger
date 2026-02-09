/**
 * 认证 API
 */

import api from './index'

const authApi = {
  async register(username, password, invite_code) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    formData.append('invite_code', invite_code)
    
    return api.post('/auth/register', formData)
  },

  async login(username, password) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    return api.post('/auth/login', formData)
  },

  async me() {
    return api.get('/auth/me')
  },

  async logout() {
    return api.post('/auth/logout')
  },

  async refresh() {
    return api.post('/auth/refresh')
  }
}

export default authApi
