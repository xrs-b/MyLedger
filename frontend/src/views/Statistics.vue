<template>
  <div class="page-container" v-loading="loading">
    <h1 class="page-title">统计</h1>
    
    <!-- 日期筛选 -->
    <div class="date-filter">
      <van-button 
        v-for="range in dateRanges" 
        :key="range.value"
        :type="dateRange === range.value ? 'primary' : 'default'"
        size="small"
        @click="setDateRange(range.value)"
      >
        {{ range.label }}
      </van-button>
      <van-button 
        type="default" 
        size="small"
        @click="showCustomDate = true"
      >
        自定义
      </van-button>
    </div>
    
    <!-- 统计摘要 -->
    <div class="summary-card" v-if="summary">
      <div class="summary-row main">
        <div class="summary-item">
          <span class="label">收入</span>
          <span class="value income">+{{ formatAmount(summary.income_amount) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">支出</span>
          <span class="value expense">-{{ formatAmount(summary.expense_amount) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">结余</span>
          <span class="value" :class="netAmount >= 0 ? 'income' : 'expense'">
            {{ netAmount >= 0 ? '+' : '' }}{{ formatAmount(netAmount) }}
          </span>
        </div>
      </div>
    </div>
    
    <!-- 分类占比饼图 -->
    <div class="chart-card">
      <h3 class="chart-title">分类支出占比</h3>
      <div ref="pieChartRef" class="chart-container"></div>
    </div>
    
    <!-- 收支趋势图 -->
    <div class="chart-card">
      <h3 class="chart-title">收支趋势</h3>
      <div ref="lineChartRef" class="chart-container"></div>
    </div>
    
    <!-- 项目消费 -->
    <div class="chart-card" v-if="projectData.length > 0">
      <h3 class="chart-title">项目消费</h3>
      <div class="project-list">
        <div 
          v-for="project in projectData" 
          :key="project.project_id"
          class="project-item"
        >
          <span class="project-name">{{ project.project_title }}</span>
          <span class="project-amount">¥{{ formatAmount(project.total) }}</span>
        </div>
      </div>
    </div>
    
    <!-- 自定义日期选择 -->
    <van-popup v-model:show="showCustomDate" position="bottom">
      <van-date-picker
        v-model="customDateRange"
        type="range"
        title="选择日期范围"
        @confirm="onCustomDateConfirm"
        @cancel="showCustomDate = false"
      />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { storeToRefs } from 'pinia'
import * as echarts from 'echarts'

const statisticsStore = useStatisticsStore()
const { summary, categoryData, dailyData, projectData, loading } = storeToRefs(statisticsStore)

const pieChartRef = ref(null)
const lineChartRef = ref(null)
let pieChart = null
let lineChart = null

const dateRange = ref('month')
const showCustomDate = ref(false)
const customDateRange = ref([])

const dateRanges = [
  { value: 'week', label: '本周' },
  { value: 'month', label: '本月' },
  { value: 'quarter', label: '季度' },
  { value: 'year', label: '全年' }
]

// 计算属性
const netAmount = computed(() => {
  if (!summary.value) return 0
  return summary.value.income_amount - summary.value.expense_amount
})

// 格式化金额
const formatAmount = (amount) => {
  return Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

// 设置日期范围
const setDateRange = (value) => {
  dateRange.value = value
  const now = new Date()
  let start = new Date()
  
  switch (value) {
    case 'week':
      start.setDate(now.getDate() - 7)
      break
    case 'month':
      start.setMonth(now.getMonth() - 1)
      break
    case 'quarter':
      start.setMonth(now.getMonth() - 3)
      break
    case 'year':
      start.setFullYear(now.getFullYear() - 1)
      break
  }
  
  statisticsStore.setFilters({
    start_date: start.toISOString().split('T')[0],
    end_date: now.toISOString().split('T')[0]
  })
  
  loadData()
}

// 自定义日期确认
const onCustomDateConfirm = (values) => {
  const [startYear, startMonth, startDay] = values.selectedValues
  const [endYear, endMonth, endDay] = values.selectedValues.slice(3)
  
  const startDate = new Date(startYear, startMonth - 1, startDay)
  const endDate = new Date(endYear, endMonth - 1, endDay)
  
  statisticsStore.setFilters({
    start_date: startDate.toISOString().split('T')[0],
    end_date: endDate.toISOString().split('T')[0]
  })
  
  showCustomDate.value = false
  dateRange.value = 'custom'
  loadData()
}

// 加载数据
const loadData = async () => {
  await statisticsStore.loadAll()
  updateCharts()
}

// 更新图表
const updateCharts = () => {
  // 更新饼图
  if (pieChart && categoryData.value.length > 0) {
    const pieData = categoryData.value.map(c => ({
      name: c.name,
      value: c.amount
    }))
    
    pieChart.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{b}: ¥{c} ({d}%)'
      },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: pieData,
        label: {
          show: false
        }
      }]
    })
  }
  
  // 更新折线图
  if (lineChart && dailyData.value.length > 0) {
    const dates = dailyData.value.map(d => d.date)
    const income = dailyData.value.map(d => d.income)
    const expense = dailyData.value.map(d => d.expense)
    
    lineChart.setOption({
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['收入', '支出'],
        bottom: 0
      },
      xAxis: {
        type: 'category',
        data: dates
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          name: '收入',
          type: 'line',
          data: income,
          smooth: true,
          itemStyle: { color: '#07c160' }
        },
        {
          name: '支出',
          type: 'line',
          data: expense,
          smooth: true,
          itemStyle: { color: '#ee0a24' }
        }
      ]
    })
  }
}

// 初始化图表
const initCharts = () => {
  if (pieChartRef.value) {
    pieChart = echarts.init(pieChartRef.value)
  }
  if (lineChartRef.value) {
    lineChart = echarts.init(lineChartRef.value)
  }
}

// 监听数据变化
watch([categoryData, dailyData], () => {
  updateCharts()
}, { deep: true })

// 窗口大小变化
window.addEventListener('resize', () => {
  pieChart?.resize()
  lineChart?.resize()
})

// 初始化
onMounted(async () => {
  setDateRange('month')
  initCharts()
})
</script>

<style scoped>
.date-filter {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  color: #fff;
}

.summary-row {
  display: flex;
  justify-content: space-between;
}

.summary-row.main .summary-item {
  text-align: center;
  flex: 1;
}

.summary-row .label {
  display: block;
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 4px;
}

.summary-row .value {
  font-size: 18px;
  font-weight: 600;
}

.summary-row .value.income {
  color: #95f7a9;
}

.summary-row .value.expense {
  color: #ffb5b5;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.chart-container {
  height: 200px;
}

.project-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.project-item {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: #f7f8fa;
  border-radius: 8px;
}

.project-name {
  font-size: 14px;
  color: #323233;
}

.project-amount {
  font-size: 14px;
  font-weight: 600;
  color: #ee0a24;
}
</style>
