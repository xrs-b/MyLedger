<template>
  <div class="page-container">
    <h1 class="page-title">注册</h1>
    
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.username"
        name="username"
        label="账号名"
        placeholder="请输入账号名 (3-50字符)"
        :rules="[
          { required: true, message: '请输入账号名' },
          { min: 3, max: 50, message: '账号名需要3-50字符' }
        ]"
      />
      <van-field
        v-model="form.password"
        type="password"
        name="password"
        label="密码"
        placeholder="请输入密码 (6-50字符)"
        :rules="[
          { required: true, message: '请输入密码' },
          { min: 6, max: 50, message: '密码需要6-50字符' }
        ]"
      />
      <van-field
        v-model="form.inviteCode"
        name="inviteCode"
        label="邀请码"
        placeholder="请输入邀请码"
        :rules="[{ required: true, message: '请输入邀请码' }]"
      />
      <van-button 
        type="primary" 
        native-type="submit" 
        block 
        :loading="loading"
        class="submit-btn"
      >
        注册
      </van-button>
    </van-form>
    
    <router-link to="/login" class="link">
      已有账号？去登录
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
  password: '',
  inviteCode: ''
})

const loading = ref(false)

const onSubmit = async () => {
  loading.value = true
  
  try {
    await authStore.register(
      form.username,
      form.password,
      form.inviteCode
    )
    
    Toast.success('注册成功！')
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    // 解析错误信息
    let errorMsg = '注册失败，请重试'
    
    if (error?.data?.detail) {
      const detail = error.data.detail
      if (Array.isArray(detail) && detail.length > 0) {
        // FastAPI 返回的验证错误是数组
        errorMsg = detail[0]?.msg || detail[0]?.type || JSON.stringify(detail[0])
      } else if (typeof detail === 'string') {
        errorMsg = detail
      } else {
        errorMsg = JSON.stringify(detail)
      }
    } else if (error?.data?.message) {
      errorMsg = error.data.message
    } else if (error?.message) {
      errorMsg = error.message
    }
    
    Toast.fail(errorMsg)
    console.error('注册错误:', error)
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
