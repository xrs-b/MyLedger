<template>
  <div class="page-container">
    <h1 class="page-title">记账列表</h1>
    
    <!-- 统计摘要 -->
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
    
    <!-- 记账列表 -->
    <div class="records-list" v-loading="loading">
      <div 
        v-for="record in records" 
        :key="record.id"
        class="record-item"
        @click="viewRecord(record)"
      >
        <div class="record-left">
          <van-icon :name="getCategoryIcon(record)" size="32" />
        </div>
        <div class="record-center">
          <div class="record-category">
            {{ record.category_name || '未知分类' }} - {{ record.category_item_name || '未知' }}
          </div>
          <div class="record-date">
            {{ formatDate(record.date) }}
          </div>
          <div class="record-remark" v-if="record.remark">
            {{ record.remark }}
          </div>
        </div>
        <div class="record-right">
          <span :class="['amount', record.type]">
            {{ record.type === 'income' ? '+' : '-' }}{{ formatAmount(record.amount) }}
          </span>
        </div>
      </div>
      
      <!-- 空状态 -->
      <van-empty v-if="!loading && records.length === 0" description="暂无记账记录" />
      
      <!-- 加载更多 -->
      <div class="load-more" v-if="hasMore" @click="loadMore">
        加载更多
      </div>
    </div>
    
    <!-- 记一笔按钮 -->
    <router-link to="/records/add" class="add-btn">
      <van-icon name="plus" size="24" />
      记一笔
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRecordStore } from '@/stores/record'
import { storeToRefs } from 'pinia'
import { Toast } from 'vant'
import { useRouter } from 'vue-router'

const router = useRouter()
const recordStore = useRecordStore()
const { records, stats, pagination, loading, hasMore } = storeToRefs(recordStore)

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 格式化日期
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 获取分类图标（简化）
const getCategoryIcon = (record) => {
  return record.type === 'income' ? 'arrow-up' : 'arrow-down'
}

// 查看详情
const viewRecord = (record) => {
  router.push(`/records/${record.id}`)
}

// 加载更多
const loadMore = () => {
  recordStore.loadMore()
}

// 初始化
onMounted(async () => {
  await recordStore.fetchRecords()
  await recordStore.fetchStats()
})
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

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-item.income {
  border-right: 1px solid rgba(255,255,255,0.3);
}

.stat-item .label {
  display: block;
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.stat-item .amount {
  font-size: 20px;
  font-weight: 600;
}

.records-list {
  min-height: 200px;
}

.record-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
}

.record-left {
  margin-right: 12px;
  color: #1989fa;
}

.record-center {
  flex: 1;
}

.record-category {
  font-size: 14px;
  color: #323233;
  margin-bottom: 4px;
}

.record-date {
  font-size: 12px;
  color: #969799;
}

.record-remark {
  font-size: 12px;
  color: #969799;
  margin-top: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.record-right {
  text-align: right;
}

.record-right .amount {
  font-size: 16px;
  font-weight: 600;
}

.record-right .amount.income {
  color: #07c160;
}

.record-right .amount.expense {
  color: #ee0a24;
}

.load-more {
  text-align: center;
  padding: 16px;
  color: #1989fa;
  cursor: pointer;
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  cursor: pointer;
}
</style>
