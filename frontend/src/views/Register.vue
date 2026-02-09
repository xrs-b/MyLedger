<template>
  <div class="page-container">
    <h1 class="page-title">注册</h1>
    
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.username"
        name="username"
        label="账号名"
        placeholder="请输入账号名 (3-50字符)"
      />
      <van-field
        v-model="form.password"
        type="password"
        name="password"
        label="密码"
        placeholder="请输入密码 (6-50字符)"
      />
      <van-field
        v-model="form.inviteCode"
        name="inviteCode"
        label="邀请码"
        placeholder="请输入邀请码"
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
import { ref, reactive, getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'

const { proxy } = getCurrentInstance()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
  inviteCode: ''
})

const loading = ref(false)

const showToast = (msg) => {
  if (proxy && proxy.$toast) {
    proxy.$toast(msg)
  } else {
    alert(msg)
  }
}

const onSubmit = async () => {
  if (!form.username || !form.password || !form.inviteCode) {
    showToast('请填写完整信息')
    return
  }
  
  loading.value = true
  
  try {
    const formData = new URLSearchParams()
    formData.append('username', form.username)
    formData.append('password', form.password)
    formData.append('invite_code', form.inviteCode)
    
    const response = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData.toString()
    })
    
    const data = await response.json()
    
    if (response.ok) {
      showToast('注册成功！')
      setTimeout(() => router.push('/login'), 2000)
    } else {
      let msg = '注册失败'
      if (data.detail) {
        msg = Array.isArray(data.detail) ? data.detail[0]?.msg : data.detail
      } else if (data.message) {
        msg = data.message
      }
      showToast(msg)
    }
  } catch (error) {
    showToast('注册失败，请重试')
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
