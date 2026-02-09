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
    <van-field
      v-model="paymentMethodName"
      readonly
      label="支付方式"
      placeholder="请选择支付方式"
      @click="showPaymentPicker = true"
    >
      <template #right-icon>
        <van-icon name="arrow" />
      </template>
    </van-field>
    
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
    
    <!-- 分类选择器 - 两列联动 -->
    <van-popup v-model:show="showCategoryPicker" position="bottom" :style="{ height: '60%' }">
      <van-picker
        :columns="categoryColumns"
        title="选择分类"
        @confirm="onCategoryConfirm"
        @cancel="showCategoryPicker = false"
        @change="onCategoryChange"
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
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useRecordStore } from '@/stores/record'
import { useCategoryStore } from '@/stores/category'
import { storeToRefs } from 'pinia'
import { Toast } from 'vant'

const route = useRoute()
const recordStore = useRecordStore()
const categoryStore = useCategoryStore()
const { categories, paymentMethods } = storeToRefs(categoryStore)

const loading = ref(false)
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

// 分类两列联动
const categoryColumns = computed(() => {
  const type = form.type || 'expense'
  const typeCategories = categories.value[type] || []
  
  // 第一列：一级分类
  const firstColumn = typeCategories.map(c => ({
    text: c.name,
    value: c.id
  }))
  
  // 默认选中第一个分类，获取其二级分类
  let secondColumn = []
  if (typeCategories.length > 0) {
    const firstCategory = typeCategories[0]
    secondColumn = (firstCategory.items || []).map(item => ({
      text: item.name,
      value: item.id,
      categoryId: firstCategory.id
    }))
  }
  
  return [
    { values: firstColumn, className: 'first-column' },
    { values: secondColumn, className: 'second-column' }
  ]
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
  return form.amount > 0 && form.category_id && form.category_item_id
})

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

// 分类变化（一级分类变化时更新二级分类）
const onCategoryChange = (picker, values, index) => {
  if (index === 0) {
    const type = form.type || 'expense'
    const typeCategories = categories.value[type] || []
    const selectedCategory = typeCategories.find(c => c.id === values[0].value)
    if (selectedCategory) {
      const secondColumn = picker.getColumnValues(1)
      const newSecondColumn = (selectedCategory.items || []).map(item => ({
        text: item.name,
        value: item.id,
        categoryId: selectedCategory.id
      }))
      picker.setColumnValues(1, newSecondColumn)
      // 默认选中第一个
      if (newSecondColumn.length > 0) {
        picker.setValues([values[0], newSecondColumn[0]])
      }
    }
  }
}

// 分类确认
const onCategoryConfirm = (picker) => {
  const values = picker.getValues()
  if (values && values.length === 2) {
    form.category_id = values[0].value
    form.category_item_id = values[1].value
    selectedCategoryName.value = `${values[0].text} - ${values[1].text}`
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
  form.payment_method_id = e.selectedValues[0]
  paymentMethodName.value = e.selectedOptions[0].text
  showPaymentPicker.value = false
}

// 提交
const onSubmit = async () => {
  if (!canSubmit.value) {
    Toast.fail('请填写完整信息')
    return
  }
  
  loading.value = true
  
  try {
    const result = await recordStore.create({
      type: form.type,
      category_id: form.category_id,
      category_item_id: form.category_item_id,
      amount: form.amount,
      date: form.date.toISOString().split('T')[0],
      remark: form.remark || null,
      payment_method_id: form.payment_method_id || null,
      project_id: form.project_id || null
    })
    
    if (result?.success) {
      Toast.success('保存成功')
      setTimeout(() => {
        window.history.back()
      }, 1000)
    } else {
      Toast.fail(result?.message || '保存失败')
    }
  } catch (error) {
    Toast.fail(error.response?.data?.detail || '保存失败')
    console.error('保存错误:', error)
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(async () => {
  await categoryStore.fetchCategories()
  await categoryStore.fetchPaymentMethods()
  
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
