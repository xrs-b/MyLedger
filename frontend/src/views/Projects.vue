<template>
  <div class="page-container">
    <h1 class="page-title">项目</h1>
    
    <!-- 项目列表 -->
    <div class="projects-list" v-loading="loading">
      <div 
        v-for="project in projects" 
        :key="project.id"
        class="project-card"
        @click="viewProject(project)"
      >
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
        
        <!-- 进度条 -->
        <div class="progress-bar">
          <div 
            class="progress-fill"
            :style="{ width: getExpenseRate(project) + '%' }"
            :class="getExpenseRate(project) > 100 ? 'over' : ''"
          ></div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <van-empty v-if="!loading && projects.length === 0" description="暂无项目" />
    </div>
    
    <!-- 新建按钮 -->
    <router-link to="/projects/add" class="add-btn">
      <van-icon name="plus" size="24" />
      新建
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProjectStore } from '@/stores/project'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const projectStore = useProjectStore()
const { projects, loading } = storeToRefs(projectStore)

const formatAmount = (amount) => {
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const getAvgExpense = (project) => {
  if (project.member_count <= 0) return 0
  return project.total_expense / project.member_count
}

const getExpenseRate = (project) => {
  if (project.budget <= 0) return 0
  return Math.min(100, (Number(project.total_expense) / Number(project.budget)) * 100)
}

const viewProject = (project) => {
  router.push(`/projects/${project.id}`)
}

// 初始化
onMounted(() => {
  projectStore.fetchProjects()
})
</script>

<style scoped>
.projects-list {
  padding-bottom: 60px;
}

.project-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  cursor: pointer;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.project-title {
  font-size: 16px;
  font-weight: 600;
  color: #323233;
}

.project-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  font-size: 12px;
  color: #969799;
  margin-bottom: 2px;
}

.info-item .value {
  font-size: 14px;
  color: #323233;
}

.info-item .value.expense {
  color: #ee0a24;
}

.progress-bar {
  height: 6px;
  background: #ebedf0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1989fa, #07c160);
  border-radius: 3px;
  transition: width 0.3s;
}

.progress-fill.over {
  background: #ee0a24;
}

.add-btn {
  position: fixed;
  right: 16px;
  bottom: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #07c160 0%, #1989fa 100%);
  border-radius: 50%;
  color: #fff;
  box-shadow: 0 4px 12px rgba(7, 193, 96, 0.4);
  cursor: pointer;
}
</style>
