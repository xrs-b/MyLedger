<template>
  <div class="page-container">
    <h1 class="page-title">MyLedger</h1>
    <div class="card">
      <p>移动端记账应用</p>
    </div>
    <div class="nav-links">
      <router-link to="/login" class="nav-link">登录</router-link>
      <router-link to="/register" class="nav-link">注册</router-link>
    </div>
  </div>
</template>

<script setup>
/**
 * 首页
 */
</script>

<style scoped>
.nav-links {
  display: flex;
  gap: 16px;
  margin-top: 24px;
}

.nav-link {
  display: inline-block;
  padding: 12px 24px;
  background-color: var(--primary-color);
  color: var(--white);
  border-radius: var(--border-radius);
  text-decoration: none;
}
</style>
