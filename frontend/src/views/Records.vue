<template>
  <div class="page-container">
    <h1 class="page-title">记账列表</h1>
    
    <div class="stats-card" v-if="stats">
      <div class="stat-item income">
        <span class="label">收入</span>
        <span class="amount">+{{ formatAmount(stats.income_amount) }}</span>
      </div>
      <div class="stat-item expense">
        <span class="label">支出</span>
        <span class="amount">-{{ formatAmount(stats.expense_amount) }}</span>
      </div>
    </div>
    
    <div class="records-list" v-if="!loading">
      <div v-for="record in records" :key="record.id" class="record-item" @click="viewRecord(record)">
        <div class="record-left">
          <van-icon :name="record.type === 'income' ? 'arrow-up' : 'arrow-down'" size="32" />
        </div>
        <div class="record-center">
          <div class="record-category">{{ record.category_name || '未知分类' }}</div>
          <div class="record-date">{{ formatDate(record.date) }}</div>
          <div class="record-project" v-if="record.project_title">
            <van-icon name="cluster-o" size="12" />
            {{ record.project_title }}
          </div>
        </div>
        <div class="record-right">
          <span :class="['amount', record.type]">
            {{ record.type === 'income' ? '+' : '-' }}{{ formatAmount(record.amount) }}
          </span>
        </div>
      </div>
      <van-empty v-if="records.length === 0" description="暂无记账记录" />
    </div>
    
    <div v-else class="loading">加载中...</div>
    
    <router-link to="/records/add" class="add-btn">
      <van-icon name="plus" size="24" />
      记一笔
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()
const records = ref([])
const stats = ref(null)
const loading = ref(false)

const formatAmount = (amount) => {
  return Number(amount || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const viewRecord = (record) => {
  router.push(\`/records/\${record.id}\`)
}

const loadData = async () => {
  loading.value = true
  try {
    const recordsRes = await api.get('/records', { page: 1, page_size: 50 })
    records.value = recordsRes.data.records || []
    stats.value = await api.get('/records/stats/summary', {})
  } catch (error) {
    console.error('获取数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.stats-card {
  display: flex;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  color: #fff;
}

.stat-item { flex: 1; text-align: center; }
.stat-item.income { border-right: 1px solid rgba(255,255,255,0.3); }
.stat-item .label { display: block; font-size: 12px; opacity: 0.8; margin-bottom: 4px; }
.stat-item .amount { font-size: 20px; font-weight: 600; }

.records-list { min-height: 200px; }

.record-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
}

.record-left { margin-right: 12px; color: #1989fa; }
.record-center { flex: 1; }
.record-category { font-size: 14px; color: #323233; margin-bottom: 4px; }
.record-date { font-size: 12px; color: #969799; }
.record-project { display: flex; align-items: center; gap: 4px; font-size: 12px; color: #1989fa; margin-top: 4px; }
.record-right { text-align: right; }
.record-right .amount { font-size: 16px; font-weight: 600; }
.record-right .amount.income { color: #07c160; }
.record-right .amount.expense { color: #ee0a24; }

.loading { text-align: center; padding: 40px; color: #969799; }

.add-btn {
  position: fixed;
  right: 16px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  cursor: pointer;
}
</style>
