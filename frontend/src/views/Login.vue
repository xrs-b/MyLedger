<template>
  <div class="page-container">
    <h1 class="page-title">登录</h1>
    
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.username"
        name="username"
        label="账号名"
        placeholder="请输入账号名"
      />
      <van-field
        v-model="form.password"
        type="password"
        name="password"
        label="密码"
        placeholder="请输入密码"
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
import { ref, reactive, getCurrentInstance } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const { proxy } = getCurrentInstance()
const router = useRouter()
const route = useRoute()

const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const showToast = (msg) => {
  if (proxy && proxy.$toast) {
    proxy.$toast(msg)
  } else {
    console.log('Toast:', msg)
  }
}

const onSubmit = async () => {
  if (!form.username || !form.password) {
    showToast('请填写完整信息')
    return
  }
  
  loading.value = true
  
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
    
    if (response.ok) {
      // 存储 token 和用户信息
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      
      showToast('登录成功！')
      
      // 跳转到 Profile 或首页
      setTimeout(() => {
        window.location.href = '/profile'
      }, 1000)
    } else {
      let msg = '登录失败'
      if (data.detail) {
        msg = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail
      }
      showToast(msg)
    }
  } catch (error) {
    showToast('登录失败，请重试')
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
