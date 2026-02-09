<template>
  <div class="page-container">
    <h1 class="page-title">新建项目</h1>
    
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.title"
        name="title"
        label="项目标题"
        placeholder="请输入项目标题"
        :rules="[{ required: true, message: '请输入项目标题' }]"
      />
      
      <!-- 开始日期 -->
      <van-field
        v-model="startDateDisplay"
        readonly
        label="开始日期"
        placeholder="请选择开始日期"
        @click="showStartDatePicker = true"
        :rules="[{ required: true, message: '请选择开始日期' }]"
      >
        <template #right-icon>
          <van-icon name="calendar-o" />
        </template>
      </van-field>
      
      <!-- 结束日期 -->
      <van-field
        v-model="endDateDisplay"
        readonly
        label="结束日期"
        placeholder="请选择结束日期"
        @click="showEndDatePicker = true"
        :rules="[{ required: true, message: '请选择结束日期' }]"
      >
        <template #right-icon>
          <van-icon name="calendar-o" />
        </template>
      </van-field>
      
      <van-field
        v-model="form.budget"
        type="digit"
        name="budget"
        label="预算金额"
        placeholder="请输入预算金额"
        :rules="[{ required: true, message: '请输入预算金额' }]"
      />
      
      <van-field
        v-model="form.member_count"
        type="digit"
        name="member_count"
        label="参与人数"
        placeholder="请输入参与人数"
        :rules="[{ required: true, message: '请输入参与人数' }]"
      />
      
      <van-field
        v-model="form.description"
        type="textarea"
        name="description"
        label="项目描述"
        placeholder="请输入项目描述（可选）"
        rows="3"
        autosize
      />
      
      <van-button 
        type="primary" 
        native-type="submit" 
        block 
        :loading="loading"
        class="submit-btn"
      >
        创建项目
      </van-button>
    </van-form>
    
    <!-- 开始日期选择器 -->
    <van-popup v-model:show="showStartDatePicker" position="bottom">
      <van-date-picker
        v-model="startDateValue"
        title="选择开始日期"
        @confirm="onStartDateConfirm"
        @cancel="showStartDatePicker = false"
      />
    </van-popup>
    
    <!-- 结束日期选择器 -->
    <van-popup v-model:show="showEndDatePicker" position="bottom">
      <van-date-picker
        v-model="endDateValue"
        title="选择结束日期"
        @confirm="onEndDateConfirm"
        @cancel="showEndDatePicker = false"
      />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { Toast } from 'vant'

const router = useRouter()
const projectStore = useProjectStore()

const loading = ref(false)
const showStartDatePicker = ref(false)
const showEndDatePicker = ref(false)
const today = new Date()
const todayStr = [today.getFullYear(), String(today.getMonth() + 1).padStart(2, '0'), String(today.getDate()).padStart(2, '0')]

const startDateValue = ref([...todayStr])
const endDateValue = ref([...todayStr])

const startDateDisplay = ref('')
const endDateDisplay = ref('')

const form = reactive({
  title: '',
  start_date: null,
  end_date: null,
  budget: '',
  member_count: '1',
  description: ''
})

const formatDateDisplay = (dateArr) => {
  if (!dateArr || dateArr.length < 3) return ''
  const date = new Date(dateArr[0], dateArr[1] - 1, dateArr[2])
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const onStartDateConfirm = () => {
  form.start_date = new Date(startDateValue.value[0], startDateValue.value[1] - 1, startDateValue.value[2])
  startDateDisplay.value = formatDateDisplay(startDateValue.value)
  showStartDatePicker.value = false
}

const onEndDateConfirm = () => {
  form.end_date = new Date(endDateValue.value[0], endDateValue.value[1] - 1, endDateValue.value[2])
  endDateDisplay.value = formatDateDisplay(endDateValue.value)
  showEndDatePicker.value = false
}

const onSubmit = async () => {
  if (!form.title) {
    Toast.fail('请输入项目标题')
    return
  }
  
  if (!form.start_date) {
    Toast.fail('请选择开始日期')
    return
  }
  
  if (!form.end_date) {
    Toast.fail('请选择结束日期')
    return
  }
  
  if (!form.budget) {
    Toast.fail('请输入预算金额')
    return
  }
  
  if (form.end_date < form.start_date) {
    Toast.fail('结束日期不能早于开始日期')
    return
  }
  
  loading.value = true
  
  try {
    const result = await projectStore.create({
      title: form.title,
      start_date: formatDateDisplay(startDateValue.value),
      end_date: formatDateDisplay(endDateValue.value),
      budget: parseFloat(form.budget),
      member_count: parseInt(form.member_count),
      description: form.description || null
    })
    
    if (result?.success) {
      Toast.success('创建成功')
      setTimeout(() => {
        router.push('/projects')
      }, 1000)
    } else {
      Toast.fail(result?.message || '创建失败')
    }
  } catch (error) {
    Toast.fail(error.response?.data?.detail || '创建失败')
    console.error('创建项目错误:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.submit-btn {
  margin-top: 24px;
}
</style>
