/**
 * Axios 实例配置
 */

import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      // 401 未授权 - 清除token并跳转登录
      if (status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        
        // 如果不是在登录页，跳转登录
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
      }
      
      // 返回错误信息
      return Promise.reject({
        status,
        data: data.detail ? { detail: data.detail } : data
      })
    }
    
    return Promise.reject(error)
  }
)

export default api
