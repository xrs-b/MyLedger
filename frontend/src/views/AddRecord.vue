<template>
  <div class="page-container">
    <h1 class="page-title">记一笔</h1>
    
    <!-- 类型选择 -->
    <div class="type-selector">
      <van-button 
        :type="form.type === 'expense' ? 'primary' : 'default'" 
        @click="form.type = 'expense'"
      >
        支出
      </van-button>
      <van-button 
        :type="form.type === 'income' ? 'success' : 'default'" 
        @click="form.type = 'income'"
      >
        收入
      </van-button>
    </div>
    
    <!-- 金额输入 -->
    <van-field
      v-model="amountDisplay"
      type="text"
      label="金额"
      placeholder="请输入金额"
      @input="onAmountInput"
      class="amount-field"
    >
      <template #left-icon>
        <span class="currency">¥</span>
      </template>
    </van-field>
    
    <!-- 一级分类选择 -->
    <div class="form-item" @click="showCategoryPicker = true">
      <div class="form-label">分类</div>
      <div class="form-value">
        <span v-if="selectedCategoryName">
          {{ selectedCategoryName }}
        </span>
        <span v-else class="placeholder">请选择分类</span>
        <van-icon name="arrow" />
      </div>
    </div>
    
    <!-- 日期选择 -->
    <div class="form-item" @click="showDatePicker = true">
      <div class="form-label">日期</div>
      <div class="form-value">
        <span v-if="dateDisplay">{{ dateDisplay }}</span>
        <span v-else class="placeholder">请选择日期</span>
        <van-icon name="calendar-o" />
      </div>
    </div>
    
    <!-- 支付方式选择 -->
    <div class="form-item" @click="showPaymentPicker = true">
      <div class="form-label">支付方式</div>
      <div class="form-value">
        <span v-if="paymentMethodName">{{ paymentMethodName }}</span>
        <span v-else class="placeholder">请选择支付方式</span>
        <van-icon name="arrow" />
      </div>
    </div>
    
    <!-- 备注 -->
    <van-field
      v-model="form.remark"
      type="textarea"
      label="备注"
      placeholder="添加备注..."
      rows="2"
      autosize
    />
    
    <!-- 提交按钮 -->
    <van-button 
      type="primary" 
      block 
      :loading="loading"
      @click="onSubmit"
      :disabled="!canSubmit"
      class="submit-btn"
    >
      保存
    </van-button>
    
    <!-- 一级分类选择器 -->
    <van-popup v-model:show="showCategoryPicker" position="bottom">
      <van-picker
        :columns="firstLevelColumns"
        title="选择一级分类"
        @confirm="onFirstLevelConfirm"
        @cancel="showCategoryPicker = false"
      />
    </van-popup>
    
    <!-- 二级分类选择器 -->
    <van-popup v-model:show="showSubCategoryPicker" position="bottom">
      <van-picker
        :columns="secondLevelColumns"
        title="选择二级分类"
        @confirm="onSecondLevelConfirm"
        @cancel="showSubCategoryPicker = false"
      />
    </van-popup>
    
    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        v-model:value="dateValue"
        title="选择日期"
        :min-date="new Date(2020, 0, 1)"
        :max-date="new Date()"
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
    
    <!-- 支付方式选择器 -->
    <van-popup v-model:show="showPaymentPicker" position="bottom">
      <van-picker
        :columns="paymentMethodColumns"
        title="选择支付方式"
        @confirm="onPaymentConfirm"
        @cancel="showPaymentPicker = false"
      />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, getCurrentInstance } from 'vue'
import { useRoute } from 'vue-router'
import recordApi from '@/api/record'
import categoryApi from '@/api/category'

const { proxy } = getCurrentInstance()
const route = useRoute()

const loading = ref(false)
const categories = ref({ expense: [], income: [] })
const paymentMethods = ref([])
const amountDisplay = ref('')
const dateValue = ref('')
const dateDisplay = ref('')
const showCategoryPicker = ref(false)
const showSubCategoryPicker = ref(false)
const showDatePicker = ref(false)
const showPaymentPicker = ref(false)
const paymentMethodName = ref('')
const selectedCategoryName = ref('')
const selectedFirstLevel = ref(null)

const form = reactive({
  type: 'expense',
  category_id: null,
  category_item_id: null,
  amount: 0,
  remark: '',
  payment_method_id: null,
  project_id: route.query.project_id ? parseInt(route.query.project_id) : null
})

// 一级分类选项
const firstLevelColumns = computed(() => {
  const type = form.type || 'expense'
  const typeCategories = categories.value[type] || []
  return typeCategories.map(c => ({
    text: c.name,
    value: c.id
  }))
})

// 二级分类选项
const secondLevelColumns = computed(() => {
  if (!selectedFirstLevel.value) return []
  const type = form.type || 'expense'
  const typeCategories = categories.value[type] || []
  const category = typeCategories.find(c => c.id === selectedFirstLevel.value)
  if (!category || !category.items) return []
  return category.items.map(item => ({
    text: item.name,
    value: item.id
  }))
})

// 支付方式选项
const paymentMethodColumns = computed(() => {
  return (paymentMethods.value || []).map(pm => ({
    text: pm.name,
    value: pm.id
  }))
})

// 是否可以提交
const canSubmit = computed(() => {
  return form.amount > 0 && form.category_id && form.category_item_id
})

// 显示提示
const showToast = (msg) => {
  if (proxy && proxy.$toast) {
    proxy.$toast(msg)
  }
}

// 金额输入处理
const onAmountInput = (e) => {
  let value = e.target.value
  value = value.replace(/[^\d.]/g, '')
  const parts = value.split('.')
  if (parts.length > 2) {
    value = parts[0] + '.' + parts.slice(1).join('')
  }
  if (parts[1] && parts[1].length > 2) {
    value = parts[0] + '.' + parts[1].slice(0, 2)
  }
  amountDisplay.value = value
  form.amount = value ? parseFloat(value) : 0
}

// 一级分类确认
const onFirstLevelConfirm = (e) => {
  if (e.selectedValues && e.selectedValues.length > 0) {
    selectedFirstLevel.value = e.selectedValues[0]
    const type = form.type || 'expense'
    const typeCategories = categories.value[type] || []
    const category = typeCategories.find(c => c.id === selectedFirstLevel.value)
    if (category) {
      form.category_id = category.id
      form.category_item_id = null
      selectedCategoryName.value = category.name
      // 显示二级分类选择器
      showCategoryPicker.value = false
      showSubCategoryPicker.value = true
    }
  }
}

// 二级分类确认
const onSecondLevelConfirm = (e) => {
  if (e.selectedValues && e.selectedValues.length > 0) {
    form.category_item_id = e.selectedValues[0]
    const type = form.type || 'expense'
    const typeCategories = categories.value[type] || []
    const category = typeCategories.find(c => c.id === form.category_id)
    const item = category?.items?.find(i => i.id === form.category_item_id)
    if (category && item) {
      selectedCategoryName.value = `${category.name} - ${item.name}`
    }
  }
  showSubCategoryPicker.value = false
}

// 日期确认
const onDateConfirm = (e) => {
  const { year, month, day } = e
  const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  dateValue.value = dateStr
  dateDisplay.value = dateStr
  showDatePicker.value = false
}

// 支付方式确认
const onPaymentConfirm = (e) => {
  if (e.selectedValues && e.selectedValues.length > 0) {
    form.payment_method_id = e.selectedValues[0]
    const pm = paymentMethods.value.find(p => p.id === form.payment_method_id)
    paymentMethodName.value = pm?.name || ''
  }
  showPaymentPicker.value = false
}

// 提交
const onSubmit = async () => {
  if (!canSubmit.value) {
    showToast('请填写完整信息')
    return
  }
  
  loading.value = true
  
  try {
    const data = {
      type: form.type,
      category_id: form.category_id,
      category_item_id: form.category_item_id,
      amount: form.amount,
      date: dateDisplay.value,
      remark: form.remark || null,
      payment_method_id: form.payment_method_id || null,
      project_id: form.project_id || null
    }
    
    await recordApi.create(data)
    showToast('保存成功')
    
    setTimeout(() => {
      window.history.back()
    }, 1000)
  } catch (error) {
    console.error('保存错误:', error)
    showToast(error?.data?.detail || '保存失败')
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(async () => {
  try {
    // 获取分类
    const cats = await categoryApi.getAll()
    categories.value = cats.data || { expense: [], income: [] }
    
    // 获取支付方式
    const pays = await categoryApi.getPaymentMethods()
    paymentMethods.value = pays.data || []
    
    console.log('分类数据:', categories.value)
    console.log('支付方式:', paymentMethods.value)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
  
  // 初始化日期
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const dateStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  dateValue.value = dateStr
  dateDisplay.value = dateStr
})
</script>

<style scoped>
.type-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.type-selector .van-button {
  flex: 1;
}

.amount-field {
  font-size: 24px;
  font-weight: 600;
}

.amount-field .currency {
  font-size: 16px;
  color: #323233;
  margin-right: 4px;
}

.form-item {
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #ebedf0;
  cursor: pointer;
}

.form-label {
  font-size: 14px;
  color: #969799;
  margin-bottom: 8px;
}

.form-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #323233;
}

.form-value .placeholder {
  color: #c8c9cc;
}

.submit-btn {
  margin-top: 24px;
}
</style>
