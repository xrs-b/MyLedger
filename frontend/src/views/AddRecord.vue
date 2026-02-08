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
        <span v-if="selectedCategory">
          {{ selectedCategory.category?.name }} - {{ selectedCategory.item?.name }}
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
    
    <!-- 分类选择器 -->
    <CategorySelector
      v-model="categorySelectorValue"
      v-model:show="showCategoryPicker"
      @confirm="onCategoryConfirm"
    />
    
    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-datetime-picker
        v-model="dateValue"
        type="datetime"
        title="选择日期时间"
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRecordStore } from '@/stores/record'
import { useCategoryStore } from '@/stores/category'
import { storeToRefs } from 'pinia'
import { Toast } from 'vant'
import CategorySelector from '@/components/CategorySelector.vue'

const route = useRoute()
const recordStore = useRecordStore()
const categoryStore = useCategoryStore()
const { paymentMethods } = storeToRefs(categoryStore)

const loading = ref(false)
const amountDisplay = ref('')
const dateDisplay = ref('')
const dateValue = ref(new Date())
const showCategoryPicker = ref(false)
const showDatePicker = ref(false)
const showPaymentPicker = ref(false)
const categorySelectorValue = ref(null)
const paymentMethodName = ref('')

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

// 分类选择器值
const selectedCategory = computed(() => {
  if (!categorySelectorValue.value) return null
  return {
    category: { id: form.category_id },
    item: { id: form.category_item_id, name: categorySelectorValue.value.name }
  }
})

// 支付方式选项
const paymentMethodOptions = computed(() => {
  return paymentMethods.value.map(pm => ({
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
  // 只允许数字和小数点
  value = value.replace(/[^\d.]/g, '')
  // 只能有一个小数点
  const parts = value.split('.')
  if (parts.length > 2) {
    value = parts[0] + '.' + parts.slice(1).join('')
  }
  // 最多两位小数
  if (parts[1] && parts[1].length > 2) {
    value = parts[0] + '.' + parts[1].slice(0, 2)
  }
  amountDisplay.value = value
  form.amount = value ? parseFloat(value) : 0
}

// 分类确认
const onCategoryConfirm = (data) => {
  form.category_id = data.categoryId
  form.category_item_id = data.item.id
  showCategoryPicker.value = false
}

// 日期确认
const onDateConfirm = () => {
  form.date = dateValue.value
  dateDisplay.value = formatDate(dateValue.value)
  showDatePicker.value = false
}

// 支付方式确认
const onPaymentConfirm = (e) => {
  form.payment_method_id = e.selectedValues[0]
  paymentMethodName.value = e.selectedOptions[0].text
  showPaymentPicker.value = false
}

// 格式化日期
const formatDate = (date) => {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
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
      date: form.date.toISOString(),
      remark: form.remark || null,
      payment_method_id: form.payment_method_id || null,
      project_id: form.project_id || null
    })
    
    if (result.success) {
      Toast.success({
        message: '保存成功',
        duration: 1000
      })
      setTimeout(() => {
        window.history.back()
      }, 1000)
    } else {
      Toast.fail(result.message || '保存失败')
    }
  } catch (error) {
    Toast.fail('保存失败')
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
  dateDisplay.value = formatDate(new Date())
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
