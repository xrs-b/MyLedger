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
import authApi from '@/api/auth'
import { Toast } from 'vant'

const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const onSubmit = async () => {
  if (!form.username || !form.password) {
    Toast.fail('请填写完整信息')
    return
  }
  
  loading.value = true
  console.log('开始登录请求...')
  
  try {
    const formData = new URLSearchParams()
    formData.append('username', form.username)
    formData.append('password', form.password)
    
    const response = await fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    })
    
    const data = await response.json()
    console.log('登录响应:', data)
    
    if (response.ok) {
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      Toast.success('登录成功！')
      setTimeout(() => router.push('/'), 1000)
    } else {
      let msg = '登录失败'
      if (data.detail) {
        if (Array.isArray(data.detail)) {
          msg = data.detail[0]?.msg || data.detail[0]?.type || JSON.stringify(data.detail[0])
        } else {
          msg = data.detail
        }
      }
      Toast.fail(msg)
    }
  } catch (error) {
    console.error('登录错误:', error)
    Toast.fail('登录失败，请重试')
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
