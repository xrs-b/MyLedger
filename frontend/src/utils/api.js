/**
 * API 工具函数
 */

// 显示 Toast 提示
export function showToast(message) {
  if (window.$toast) {
    window.$toast(message)
  } else {
    console.log('Toast:', message)
  }
}

// 显示成功提示
export function showSuccess(message) {
  showToast(message)
}

// 显示失败提示
export function showError(message) {
  showToast(message)
}

// 解析 API 错误信息
export function parseError(error) {
  if (!error) return '操作失败'
  
  // 从 error.data 中提取错误信息
  const data = error.data || error
  
  if (data.detail) {
    if (Array.isArray(data.detail)) {
      // FastAPI 验证错误
      const first = data.detail[0]
      if (first && first.msg) {
        return first.msg
      }
      if (first && first.type) {
        return formatErrorType(first.type)
      }
      return JSON.stringify(data.detail[0])
    }
    return data.detail
  }
  
  if (data.message) {
    return data.message
  }
  
  if (typeof data === 'string') {
    return data
  }
  
  return '操作失败'
}

// 格式化错误类型
function formatErrorType(type) {
  const errorMap = {
    'string_too_short': '内容太短',
    'string_too_long': '内容太长',
    'value_error': '数值错误',
    'missing': '缺少必填项',
    'invalid_email': '邮箱格式错误',
    'validation_error': '验证错误'
  }
  
  return errorMap[type] || type
}

// 检查是否已登录
export function isLoggedIn() {
  return !!localStorage.getItem('token')
}

// 获取当前用户
export function getCurrentUser() {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
  return null
}

// 退出登录
export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  window.location.href = '/login'
}
