<template>
  <div class="page-container">
    <h1 class="page-title">项目</h1>
    
    <div class="projects-list" v-if="!loading">
      <div v-for="project in projects" :key="project.id" class="project-card" @click="viewProject(project)">
        <div class="project-header">
          <span class="project-title">{{ project.title }}</span>
          <van-tag :type="project.status === 'ongoing' ? 'primary' : 'success'">
            {{ project.status === 'ongoing' ? '进行中' : '已完成' }}
          </van-tag>
        </div>
        <div class="project-info">
          <div class="info-item">
            <span class="label">时间</span>
            <span class="value">{{ formatDate(project.start_date) }} - {{ formatDate(project.end_date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">预算</span>
            <span class="value">¥{{ formatAmount(project.budget) }}</span>
          </div>
          <div class="info-item">
            <span class="label">已消费</span>
            <span class="value expense">¥{{ formatAmount(project.total_expense) }}</span>
          </div>
          <div class="info-item">
            <span class="label">人均</span>
            <span class="value">¥{{ formatAmount(getAvgExpense(project)) }}</span>
          </div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: getExpenseRate(project) + '%' }" :class="{ over: getExpenseRate(project) > 100 }"></div>
        </div>
      </div>
      <van-empty v-if="projects.length === 0" description="暂无项目" />
    </div>
    <div v-else class="loading">加载中...</div>
    
    <router-link to="/projects/add" class="add-btn">
      <van-icon name="plus" size="24" />
      新建
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const projects = ref([])
const loading = ref(false)

const formatAmount = (amount) => Number(amount || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}
const getAvgExpense = (p) => p.member_count > 0 ? p.total_expense / p.member_count : 0
const getExpenseRate = (p) => p.budget > 0 ? Math.min(100, (Number(p.total_expense) / Number(p.budget)) * 100) : 0

const viewProject = (project) => router.push(\`/projects/\${project.id}\`)
const loadProjects = async () => {
  loading.value = true
  try {
    const res = await api.get('/projects', {})
    projects.value = res.data.projects || []
  } catch (error) {
    console.error('获取项目列表失败:', error)
  } finally {
    loading.value = false
  }
}
onMounted(loadProjects)
</script>

<style scoped>
.projects-list { padding-bottom: 60px; }
.project-card { background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 12px; cursor: pointer; }
.project-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.project-title { font-size: 16px; font-weight: 600; color: #323233; }
.project-info { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 12px; }
.info-item { display: flex; flex-direction: column; }
.info-item .label { font-size: 12px; color: #969799; margin-bottom: 2px; }
.info-item .value { font-size: 14px; color: #323233; }
.info-item .value.expense { color: #ee0a24; }
.progress-bar { height: 6px; background: #ebedf0; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #1989fa, #07c160); border-radius: 3px; transition: width 0.3s; }
.progress-fill.over { background: #ee0a24; }
.loading { text-align: center; padding: 40px; color: #969799; }

.add-btn {
  position: fixed;
  right: 16px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #07c160 0%, #1989fa 100%);
  border-radius: 50%;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(7, 193, 96, 0.4);
  cursor: pointer;
}
</style>
