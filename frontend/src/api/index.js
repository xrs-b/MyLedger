/**
 * API 配置
 */

const API_BASE_URL = '/api/v1'

// 获取 token
const getToken = () => localStorage.getItem('token')

// API 请求函数
async function request(method, url, data = null, params = null) {
  const token = getToken()
  
  // 构建 URL
  let fullUrl = `${API_BASE_URL}${url}`
  if (params) {
    const searchParams = new URLSearchParams()
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        searchParams.append(key, params[key])
      }
    })
    const queryString = searchParams.toString()
    if (queryString) {
      fullUrl += `?${queryString}`
    }
  }
  
  // 构建请求配置
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  }
  
  // 添加认证头
  if (token) {
    options.headers['Authorization'] = `Bearer ${token}`
  }
  
  // 添加请求体
  if (data && (method === 'POST' || method === 'PUT')) {
    options.body = JSON.stringify(data)
  }
  
  try {
    const response = await fetch(fullUrl, options)
    const result = await response.json().catch(() => ({}))
    
    if (!response.ok) {
      // 401 未授权
      if (response.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login'
        }
      }
      throw { status: response.status, data: result }
    }
    
    return { data: result }
  } catch (error) {
    console.error(`API Error [${method} ${url}]:`, error)
    throw error
  }
}

// API 方法
export const api = {
  get: (url, params) => request('GET', url, null, params),
  post: (url, data) => request('POST', url, data),
  put: (url, data) => request('PUT', url, data),
  delete: (url) => request('DELETE', url)
}

export default api
