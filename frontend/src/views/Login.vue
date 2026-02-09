<template>
  <div class="page-container">
    <h1 class="page-title">登录</h1>
    
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.username"
        name="username"
        label="账号名"
        placeholder="请输入账号名"
        :rules="[{ required: true, message: '请输入账号名' }]"
      />
      <van-field
        v-model="form.password"
        type="password"
        name="password"
        label="密码"
        placeholder="请输入密码"
        :rules="[{ required: true, message: '请输入密码' }]"
      />
      <van-button 
        type="primary" 
        native-type="submit" 
        block 
        :loading="loading"
        class="submit-btn"
      >
        登录
      </van-button>
    </van-form>
    
    <router-link to="/register" class="link">
      还没有账号？去注册
    </router-link>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Toast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const onSubmit = async () => {
  if (loading.value) return
  
  loading.value = true
  Toast.loading('登录中...')
  
  try {
    const result = await authStore.login(form.username, form.password)
    Toast.clear()
    
    if (result?.success) {
      Toast.success('登录成功！')
      router.push('/')
    } else {
      Toast.fail(result?.message || '登录失败')
    }
  } catch (error) {
    Toast.clear()
    
    let errorMsg = '登录失败，请重试'
    if (error?.data?.detail) {
      const detail = error.data.detail
      if (Array.isArray(detail) && detail.length > 0) {
        errorMsg = detail[0]?.msg || detail[0]?.type || JSON.stringify(detail[0])
      } else if (typeof detail === 'string') {
        errorMsg = detail
      }
    }
    
    Toast.fail(errorMsg)
    console.error('登录错误:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.submit-btn {
  margin-top: 24px;
}

.link {
  display: block;
  margin-top: 24px;
  text-align: center;
  color: #1989fa;
}
</style>
