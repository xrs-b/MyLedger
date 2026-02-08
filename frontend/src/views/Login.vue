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
  loading.value = true
  
  try {
    const result = await authStore.login(form.username, form.password)
    
    if (result.success) {
      Toast.success({
        message: '登录成功！',
        duration: 1000
      })
      
      // 跳转首页
      setTimeout(() => {
        router.push('/')
      }, 1000)
    } else {
      Toast.fail(result.message)
    }
  } catch (error) {
    Toast.fail('登录失败，请重试')
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
