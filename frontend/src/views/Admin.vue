<template>
  <div class="page-container" v-loading="loading">
    <h1 class="page-title">管理后台</h1>
    
    <!-- 统计数据 -->
    <div class="stats-grid" v-if="stats">
      <div class="stat-card">
        <div class="stat-value">{{ stats.user_count }}</div>
        <div class="stat-label">用户</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.record_count }}</div>
        <div class="stat-label">记录</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.project_count }}</div>
        <div class="stat-label">项目</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.category_count }}</div>
        <div class="stat-label">分类</div>
      </div>
    </div>
    
    <!-- 功能菜单 -->
    <div class="menu-grid">
      <div class="menu-item" @click="activeTab = 'users'">
        <van-icon name="user-o" size="32" />
        <span>用户管理</span>
      </div>
      <div class="menu-item" @click="activeTab = 'records'">
        <van-icon name="orders-o" size="32" />
        <span>记录管理</span>
      </div>
      <div class="menu-item" @click="activeTab = 'categories'">
        <van-icon name="label-o" size="32" />
        <span>分类管理</span>
      </div>
      <div class="menu-item" @click="activeTab = 'projects'">
        <van-icon name="cluster-o" size="32" />
        <span>项目管理</span>
      </div>
    </div>
    
    <!-- 用户管理 -->
    <div v-if="activeTab === 'users'" class="tab-content">
      <h3 class="section-title">用户列表</h3>
      <div class="list">
        <div v-for="user in users" :key="user.id" class="list-item">
          <div class="item-info">
            <span class="item-name">{{ user.username }}</span>
            <van-tag :type="user.is_admin ? 'danger' : 'default'" size="small">
              {{ user.is_admin ? '管理员' : '用户' }}
            </van-tag>
            <span class="item-date">{{ formatDate(user.created_at) }}</span>
          </div>
          <van-button 
            v-if="user.id !== currentUser?.id"
            type="danger" 
            size="small" 
            plain
            @click="deleteUser(user.id)"
          >
            删除
          </van-button>
        </div>
      </div>
    </div>
    
    <!-- 记录管理 -->
    <div v-if="activeTab === 'records'" class="tab-content">
      <h3 class="section-title">记录列表</h3>
      <div class="list">
        <div v-for="record in records" :key="record.id" class="list-item">
          <div class="item-info">
            <span :class="['amount', record.type]">
              {{ record.type === 'income' ? '+' : '-' }}¥{{ record.amount }}
            </span>
            <span class="item-date">{{ formatDate(record.date) }}</span>
          </div>
          <van-button type="danger" size="small" plain @click="deleteRecord(record.id)">
            删除
          </van-button>
        </div>
      </div>
    </div>
    
    <!-- 分类管理 -->
    <div v-if="activeTab === 'categories'" class="tab-content">
      <h3 class="section-title">分类列表</h3>
      <div class="list">
        <div v-for="category in categories" :key="category.id" class="list-item">
          <div class="item-info">
            <span class="item-name">{{ category.name }}</span>
            <van-tag :type="category.type === 'expense' ? 'warning' : 'success'" size="small">
              {{ category.type === 'expense' ? '支出' : '收入' }}
            </van-tag>
          </div>
          <van-button type="danger" size="small" plain @click="deleteCategory(category.id)">
            删除
          </van-button>
        </div>
      </div>
    </div>
    
    <!-- 项目管理 -->
    <div v-if="activeTab === 'projects'" class="tab-content">
      <h3 class="section-title">项目列表</h3>
      <div class="list">
        <div v-for="project in projects" :key="project.id" class="list-item">
          <div class="item-info">
            <span class="item-name">{{ project.title }}</span>
            <van-tag :type="project.status === 'ongoing' ? 'primary' : 'success'" size="small">
              {{ project.status === 'ongoing' ? '进行中' : '已完成' }}
            </van-tag>
            <span class="item-amount">¥{{ project.total_expense }}</span>
          </div>
          <van-button type="danger" size="small" plain @click="deleteProject(project.id)">
            删除
          </van-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import adminApi from '@/api/admin'
import { Toast, Dialog } from 'vant'

const authStore = useAuthStore()

const loading = ref(false)
const activeTab = ref('users')
const stats = ref(null)
const users = ref([])
const records = ref([])
const categories = ref([])
const projects = ref([])

const currentUser = authStore.user

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const loadData = async () => {
  loading.value = true
  try {
    const [statsRes, usersRes, recordsRes, categoriesRes, projectsRes] = await Promise.all([
      adminApi.getStats(),
      adminApi.getUsers(),
      adminApi.getRecords(1, 100),
      adminApi.getCategories(),
      adminApi.getProjects(null, 1, 100)
    ])
    
    stats.value = statsRes.data
    users.value = usersRes.data
    records.value = recordsRes.data.records || recordsRes.data
    categories.value = categoriesRes.data
    projects.value = projectsRes.data.projects || projectsRes.data
  } catch (error) {
    Toast.fail('加载数据失败')
    console.error('加载数据错误:', error)
  } finally {
    loading.value = false
  }
}

const deleteUser = async (id) => {
  Dialog.confirm({
    title: '确认删除',
    message: '确定要删除这个用户吗？',
  }).then(async () => {
    try {
      await adminApi.deleteUser(id)
      Toast.success('删除成功')
      loadData()
    } catch (error) {
      Toast.fail(error.response?.data?.detail || '删除失败')
    }
  })
}

const deleteRecord = async (id) => {
  Dialog.confirm({
    title: '确认删除',
    message: '确定要删除这条记录吗？',
  }).then(async () => {
    try {
      await adminApi.deleteRecord(id)
      Toast.success('删除成功')
      loadData()
    } catch (error) {
      Toast.fail(error.response?.data?.detail || '删除失败')
    }
  })
}

const deleteCategory = async (id) => {
  Dialog.confirm({
    title: '确认删除',
    message: '确定要删除这个分类吗？二级分类也会被删除。',
  }).then(async () => {
    try {
      await adminApi.deleteCategory(id)
      Toast.success('删除成功')
      loadData()
    } catch (error) {
      Toast.fail(error.response?.data?.detail || '删除失败')
    }
  })
}

const deleteProject = async (id) => {
  Dialog.confirm({
    title: '确认删除',
    message: '确定要删除这个项目吗？关联的记录也会被删除。',
  }).then(async () => {
    try {
      await adminApi.deleteProject(id)
      Toast.success('删除成功')
      loadData()
    } catch (error) {
      Toast.fail(error.response?.data?.detail || '删除失败')
    }
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  color: #fff;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
}

.stat-label {
  font-size: 12px;
  opacity: 0.8;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 8px;
  background: #fff;
  border-radius: 8px;
  cursor: pointer;
}

.menu-item span {
  font-size: 12px;
  margin-top: 8px;
}

.tab-content {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f7f8fa;
  border-radius: 8px;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-size: 14px;
  font-weight: 500;
}

.item-date {
  font-size: 12px;
  color: #969799;
}

.item-amount {
  font-size: 14px;
  color: #ee0a24;
}

.amount.income {
  color: #07c160;
}

.amount.expense {
  color: #ee0a24;
}
</style>
