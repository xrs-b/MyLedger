<template>
  <div class="page-container" v-loading="loading">
    <template v-if="project">
      <!-- 返回按钮 -->
      <div class="back-bar" @click="goBack">
        <van-icon name="arrow-left" />
        <span>返回项目</span>
      </div>
      
      <!-- 项目信息 -->
      <div class="project-header-card">
        <h1 class="project-title">{{ project.title }}</h1>
        
        <van-tag :type="project.status === 'ongoing' ? 'primary' : 'success'" class="status-tag">
          {{ project.status === 'ongoing' ? '进行中' : '已完成' }}
        </van-tag>
        
        <div class="project-dates">
          {{ formatDate(project.start_date) }} - {{ formatDate(project.end_date) }}
        </div>
        
        <div class="project-stats">
          <div class="stat-item">
            <span class="stat-value">¥{{ formatAmount(project.budget) }}</span>
            <span class="stat-label">预算</span>
          </div>
          <div class="stat-item">
            <span class="stat-value expense">¥{{ formatAmount(project.total_expense) }}</span>
            <span class="stat-label">已消费</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">¥{{ formatAmount(project.avg_expense) }}</span>
            <span class="stat-label">人均</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ project.member_count }}人</span>
            <span class="stat-label">人数</span>
          </div>
        </div>
        
        <!-- 进度条 -->
        <div class="progress-section">
          <div class="progress-info">
            <span>消费率 {{ project.expense_rate.toFixed(1) }}%</span>
            <span>剩余 ¥{{ formatAmount(project.budget - project.total_expense) }}</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: Math.min(100, project.expense_rate) + '%' }"
              :class="project.expense_rate > 100 ? 'over' : ''"
            ></div>
          </div>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <van-button 
            v-if="project.status === 'ongoing'"
            type="success" 
            size="small"
            @click="completeProject"
          >
            完成项目
          </van-button>
          <van-button 
            v-else
            type="primary" 
            size="small"
            @click="reopenProject"
          >
            重新打开
          </van-button>
          <van-button 
            type="danger" 
            size="small"
            plain
            @click="deleteProject"
          >
            删除项目
          </van-button>
        </div>
      </div>
      
      <!-- 记一笔按钮 -->
      <router-link 
        :to="`/records/add?project_id=${project.id}`" 
        class="add-record-btn"
      >
        <van-icon name="plus" />
        记一笔
      </router-link>
      
      <!-- 消费记录列表 -->
      <div class="records-section">
        <h3 class="section-title">消费记录 ({{ project.records.length }})</h3>
        
        <div class="records-list">
          <div 
            v-for="record in project.records" 
            :key="record.id"
            class="record-item"
          >
            <div class="record-icon">
              <span :class="['type-icon', record.type]">{{ record.type === 'income' ? '+' : '-' }}</span>
            </div>
            <div class="record-info">
              <div class="record-amount" :class="record.type">
                {{ record.type === 'income' ? '+' : '-' }}¥{{ formatAmount(record.amount) }}
              </div>
              <div class="record-date">{{ formatDateTime(record.date) }}</div>
              <div class="record-remark" v-if="record.remark">{{ record.remark }}</div>
            </div>
          </div>
          
          <van-empty v-if="project.records.length === 0" description="暂无消费记录" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { Toast, MessageBox } from 'vant'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const project = ref(null)

const formatAmount = (amount) => {
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const formatDateTime = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const goBack = () => {
  router.push('/projects')
}

const completeProject = async () => {
  try {
    await MessageBox.confirm('确定要完成这个项目吗？', '完成项目')
    
    const result = await projectStore.complete(project.value.id)
    if (result.success) {
      Toast.success('项目已完成')
      project.value = projectStore.currentProject
    } else {
      Toast.fail(result.message)
    }
  } catch (error) {
    // 用户取消，不做任何处理
  }
}

const reopenProject = async () => {
  const result = await projectStore.reopen(project.value.id)
  if (result.success) {
    Toast.success('项目已重新打开')
    project.value = projectStore.currentProject
  } else {
    Toast.fail(result.message)
  }
}

const deleteProject = async () => {
  try {
    await MessageBox.confirm('确定要删除这个项目吗？关联的消费记录也会被删除。', '删除项目')
    
    loading.value = true
    const result = await projectStore.delete(project.value.id)
    
    if (result.success) {
      Toast.success('删除成功')
      router.push('/projects')
    } else {
      Toast.fail(result.message)
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除项目错误:', error)
    }
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(async () => {
  loading.value = true
  const result = await projectStore.fetchProject(route.params.id)
  if (result.success) {
    project.value = result.data
  } else {
    Toast.fail(result.message)
    router.push('/projects')
  }
  loading.value = false
})
</script>

<style scoped>
.back-bar {
  display: flex;
  align-items: center;
  padding: 12px 0;
  color: #1989fa;
  cursor: pointer;
}

.project-header-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: #fff;
  margin-bottom: 16px;
}

.project-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px 0;
}

.status-tag {
  margin-bottom: 12px;
}

.project-dates {
  font-size: 14px;
  opacity: 0.8;
  margin-bottom: 16px;
}

.project-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 16px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
}

.stat-value.expense {
  color: #ff6b6b;
}

.stat-label {
  display: block;
  font-size: 12px;
  opacity: 0.8;
}

.progress-section {
  margin-bottom: 16px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-bottom: 6px;
}

.progress-bar {
  height: 8px;
  background: rgba(255,255,255,0.3);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #07c160;
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-fill.over {
  background: #ff6b6b;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.add-record-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: linear-gradient(135deg, #07c160 0%, #1989fa 100%);
  border-radius: 24px;
  color: #fff;
  font-weight: 600;
  margin-bottom: 16px;
  cursor: pointer;
}

.records-section {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f7f8fa;
  border-radius: 8px;
}

.record-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.type-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
}

.type-icon.income {
  background: #07c160;
  color: #fff;
}

.type-icon.expense {
  background: #ee0a24;
  color: #fff;
}

.record-info {
  flex: 1;
}

.record-amount {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.record-amount.income {
  color: #07c160;
}

.record-amount.expense {
  color: #ee0a24;
}

.record-date {
  font-size: 12px;
  color: #969799;
}

.record-remark {
  font-size: 12px;
  color: #969799;
  margin-top: 4px;
}
</style>
