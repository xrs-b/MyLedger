<template>
  <div class="page-container">
    <h1 class="page-title">我的</h1>
    
    <!-- 用户信息 -->
    <div class="user-card">
      <div class="avatar">
        {{ user?.username?.charAt(0)?.toUpperCase() || 'U' }}
      </div>
      <div class="user-info">
        <div class="username">{{ user?.username || '未登录' }}</div>
        <div class="role" v-if="user?.is_admin">管理员</div>
      </div>
    </div>
    
    <!-- 菜单列表 -->
    <div class="menu-list">
      <div class="menu-item" @click="goTo('/records')">
        <span class="icon">📝</span>
        <span class="label">记账列表</span>
        <span class="arrow">›</span>
      </div>
      <div class="menu-item" @click="goTo('/projects')">
        <span class="icon">📁</span>
        <span class="label">项目管理</span>
        <span class="arrow">›</span>
      </div>
      <div class="menu-item" @click="goTo('/statistics')">
        <span class="icon">📊</span>
        <span class="label">统计报表</span>
        <span class="arrow">›</span>
      </div>
      <div class="menu-item" v-if="isAdmin" @click="goTo('/admin')">
        <span class="icon">⚙️</span>
        <span class="label">管理后台</span>
        <span class="arrow">›</span>
      </div>
    </div>
    
    <!-- 退出登录 -->
    <div class="logout-btn" @click="logout">
      退出登录
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)
const loading = ref(false)

const isAdmin = () => user.value?.is_admin || false

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      user.value = JSON.parse(userStr)
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
})

const goTo = (path) => {
  router.push(path)
}

const logout = () => {
  if (loading.value) return
  
  loading.value = true
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.user-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  margin-bottom: 20px;
  color: #fff;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin-right: 16px;
}

.user-info .username {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.user-info .role {
  font-size: 12px;
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  display: inline-block;
}

.menu-list {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:active {
  background: #f5f5f5;
}

.menu-item .icon {
  font-size: 20px;
  margin-right: 12px;
}

.menu-item .label {
  flex: 1;
  font-size: 16px;
  color: #333;
}

.menu-item .arrow {
  color: #999;
  font-size: 20px;
}

.logout-btn {
  text-align: center;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  color: #ee0a24;
  font-size: 16px;
  cursor: pointer;
}

.logout-btn:active {
  background: #f5f5f5;
}
</style>
