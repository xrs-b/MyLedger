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
    
    <!-- 分类选择 -->
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
    <van-field
      v-model="dateDisplay"
      readonly
      label="日期"
      placeholder="请选择日期"
      @click="showDatePicker = true"
    >
      <template #right-icon>
        <van-icon name="calendar-o" />
      </template>
    </van-field>
    
    <!-- 支付方式 -->
    <div class="form-item" @click="showPaymentPicker = true">
      <div class="form-label">支付方式</div>
      <div class="form-value">
        <span v-if="paymentMethodName">
          {{ paymentMethodName }}
        </span>
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
    
    <!-- 分类选择器 -->
    <van-popup v-model:show="showCategoryPicker" position="bottom" :style="{ height: '50%' }">
      <van-picker
        :columns="categoryColumns"
        title="选择分类"
        @confirm="onCategoryConfirm"
        @cancel="showCategoryPicker = false"
      />
    </van-popup>
    
    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-datetime-picker
        v-model="dateValue"
        type="date"
        title="选择日期"
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
    
    <!-- 支付方式选择 -->
    <van-popup v-model:show="showPaymentPicker" position="bottom">
      <van-picker
        :columns="paymentMethodOptions"
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
const dateDisplay = ref('')
const dateValue = ref(new Date())
const showCategoryPicker = ref(false)
const showDatePicker = ref(false)
const showPaymentPicker = ref(false)
const paymentMethodName = ref('')
const selectedCategoryName = ref('')

const form = reactive({
  type: 'expense',
  category_id: null,
  category_item_id: null,
  amount: 0,
  date: new Date(),
  remark: '',
  payment_method_id: null,
  project_id: route.query.project_id ? parseInt(route.query.project_id) : null
})

// 分类选项（扁平化）
const categoryColumns = computed(() => {
  const type = form.type || 'expense'
  const typeCategories = categories.value[type] || []
  const options = []
  
  typeCategories.forEach(cat => {
    if (cat.items) {
      cat.items.forEach(item => {
        options.push({
          text: `${cat.name} - ${item.name}`,
          value: item.id,
          categoryId: cat.id
        })
      })
    }
  })
  
  return options
})

// 支付方式选项
const paymentMethodOptions = computed(() => {
  return (paymentMethods.value || []).map(pm => ({
    text: pm.name,
    value: pm.id
  }))
})

// 是否可以提交
const canSubmit = computed(() => {
  return form.amount > 0 && form.category_id
})

// 显示提示
const showToast = (msg) => {
  if (proxy && proxy.$toast) {
    proxy.$toast(msg)
  } else {
    
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

// 分类确认
const onCategoryConfirm = (e) => {
  if (e.selectedValues && e.selectedValues.length > 0) {
    const idx = e.selectedValues[0]
    const selected = categoryColumns.value[idx]
    if (selected) {
      form.category_id = selected.categoryId
      form.category_item_id = selected.value
      selectedCategoryName.value = selected.text
    }
  }
  showCategoryPicker.value = false
}

// 日期确认
const onDateConfirm = () => {
  form.date = dateValue.value
  const y = dateValue.value.getFullYear()
  const m = String(dateValue.value.getMonth() + 1).padStart(2, '0')
  const d = String(dateValue.value.getDate()).padStart(2, '0')
  dateDisplay.value = `${y}-${m}-${d}`
  showDatePicker.value = false
}

// 支付方式确认
const onPaymentConfirm = (e) => {
  if (e.selectedValues && e.selectedValues.length > 0) {
    form.payment_method_id = e.selectedValues[0]
    const selected = paymentMethodOptions.value.find(p => p.value === form.payment_method_id)
    paymentMethodName.value = selected?.text || ''
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
      date: form.date.toISOString().split('T')[0],
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
  } catch (error) {
    console.error('获取数据失败:', error)
  }
  
  // 初始化日期
  const y = dateValue.value.getFullYear()
  const m = String(dateValue.value.getMonth() + 1).padStart(2, '0')
  const d = String(dateValue.value.getDate()).padStart(2, '0')
  dateDisplay.value = `${y}-${m}-${d}`
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
