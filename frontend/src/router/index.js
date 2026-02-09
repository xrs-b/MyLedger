/**
 * Vue Router 配置
 * 路由定义和守卫
 */

import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: '登录', guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { title: '注册', guest: true }
  },
  {
    path: '/records',
    name: 'Records',
    component: () => import('../views/Records.vue'),
    meta: { title: '记账列表', requiresAuth: true }
  },
  {
    path: '/records/add',
    name: 'AddRecord',
    component: () => import('../views/AddRecord.vue'),
    meta: { title: '记一笔', requiresAuth: true }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/Projects.vue'),
    meta: { title: '项目', requiresAuth: true }
  },
  {
    path: '/projects/add',
    name: 'AddProject',
    component: () => import('../views/AddProject.vue'),
    meta: { title: '新建项目', requiresAuth: true }
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: () => import('../views/ProjectDetail.vue'),
    meta: { title: '项目详情', requiresAuth: true }
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue'),
    meta: { title: '统计', requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { title: '我的', requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && (!user || !user.is_admin)) {
    next({ name: 'Home' })
    return
  }
  
  // 已登录用户访问登录/注册页，跳转到首页
  if ((to.meta.guest && token) && to.name !== 'Login') {
    next({ name: 'Home' })
    return
  }
  
  next()
})

// 全局后置守卫：设置页面标题
router.afterEach((to, from) => {
  document.title = to.meta.title || 'MyLedger'
})

export default router
