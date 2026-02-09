/**
 * Axios 实例配置
 */

const API_BASE_URL = '/api/v1'

// 封装的 fetch 函数，自动携带 token
async function fetchApi(url, options = {}) {
  const token = localStorage.getItem('token')
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers
  })
  
  const data = await response.json().catch(() => ({}))
  
  if (!response.ok) {
    // 401 未授权
    if (response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    
    throw { status: response.status, data }
  }
  
  return { data }
}

// API 方法
export const api = {
  get: (url, params) => {
    const query = params ? '?' + new URLSearchParams(params).toString() : ''
    return fetchApi(url + query, { method: 'GET' })
  },
  
  post: (url, data) => fetchApi(url, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  
  put: (url, data) => fetchApi(url, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  
  delete: (url) => fetchApi(url, { method: 'DELETE' })
}

export default api
