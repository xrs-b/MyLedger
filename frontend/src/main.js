/**
 * Vue 应用入口
 * MyLedger 前端
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Vant, { Toast } from 'vant'
import 'vant/lib/index.css'
import 'vant/toast/style'
import App from './App.vue'
import router from './router'
import './style.css'

// 创建 Vue 应用
const app = createApp(App)

// 注册插件
app.use(createPinia())  // 状态管理
app.use(router)          // 路由
app.use(Vant)            // Vant UI 组件库

// 将 Toast 设置为全局方法
app.config.globalProperties.$toast = Toast

// 挂载应用
app.mount('#app')

console.log('MyLedger Frontend Started')
