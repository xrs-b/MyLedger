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
      
      <van-field
        v-model="dateRange"
        readonly
        label="时间范围"
        placeholder="请选择时间范围"
        @click="showDatePicker = true"
        :rules="[{ required: true, message: '请选择时间范围' }]"
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
      >
        <template #left-icon>
          <span>¥</span>
        </template>
      </van-field>
      
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
    
    <!-- 日期范围选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        v-model="dateValues"
        type="range"
        title="选择日期范围"
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
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
const showDatePicker = ref(false)
const dateValues = ref([
  new Date().getFullYear(),
  String(new Date().getMonth() + 1).padStart(2, '0'),
  String(new Date().getDate()).padStart(2, '0')
])
const dateRange = ref('')

const form = reactive({
  title: '',
  start_date: null,
  end_date: null,
  budget: '',
  member_count: '1',
  description: ''
})

const onDateConfirm = () => {
  const startDate = new Date(dateValues.value[0], dateValues.value[1] - 1, dateValues.value[2])
  const endDate = new Date(dateValues.value[3], dateValues.value[4] - 1, dateValues.value[5])
  
  form.start_date = startDate
  form.end_date = endDate
  
  dateRange.value = `${startDate.getMonth() + 1}月${startDate.getDate()}日 - ${endDate.getMonth() + 1}月${endDate.getDate()}日`
  
  showDatePicker.value = false
}

const onSubmit = async () => {
  if (!form.title || !form.start_date || !form.end_date || !form.budget) {
    Toast.fail('请填写完整信息')
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
      start_date: form.start_date.toISOString().split('T')[0],
      end_date: form.end_date.toISOString().split('T')[0],
      budget: parseFloat(form.budget),
      member_count: parseInt(form.member_count),
      description: form.description || null
    })
    
    if (result.success) {
      Toast.success({
        message: '创建成功',
        duration: 1000
      })
      setTimeout(() => {
        router.push('/projects')
      }, 1000)
    } else {
      Toast.fail(result.message || '创建失败')
    }
  } catch (error) {
    Toast.fail('创建失败')
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
