# MyLedger - Phase 1: 项目基础框架实现计划

> **项目名**: MyLedger  
> **Phase**: 1  
> **目标**: 创建后端和前端基础框架  
> **创建时间**: 2026-02-09

---

## 任务清单

### 1.1 后端基础框架

#### 1.1.1 创建 FastAPI 应用入口
**文件**: `backend/app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MyLedger API",
    description="移动账本后端 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "message": "MyLedger API is running"}

@app.get("/")
async def root():
    return {"name": "MyLedger", "version": "1.0.0"}
```

**验收标准**:
- ✅ API 返回健康检查状态
- ✅ 支持 CORS
- ✅ 本地访问 http://localhost:8000 返回版本信息

#### 1.1.2 创建数据库配置
**文件**: `backend/app/database.py`
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/mobile_ledger.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**验收标准**:
- ✅ 连接到 SQLite 数据库
- ✅ 支持依赖注入获取数据库会话

#### 1.1.3 创建数据模型基类
**文件**: `backend/app/models/__init__.py`
```python
from .user import User
from .category import Category, CategoryItem
from .payment_method import PaymentMethod
from .record import Record
from .project import Project
```

**验收标准**:
- ✅ 所有模型可导入
- ✅ 与数据库表对应

---

### 1.2 前端基础框架

#### 1.2.1 创建 Vue 应用入口
**文件**: `frontend/src/main.js`
```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Vant from 'vant'
import 'vant/lib/index.css'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Vant)

app.mount('#app')
```

**验收标准**:
- ✅ Vue 3 正常启动
- ✅ Pinia 状态管理可用
- ✅ Vant 组件可用

#### 1.2.2 创建根组件
**文件**: `frontend/src/App.vue`
```vue
<template>
  <router-view />
</template>

<script setup>
// 根组件
</script>
```

**验收标准**:
- ✅ 路由正常工作
- ✅ 页面正常渲染

#### 1.2.3 创建路由配置
**文件**: `frontend/src/router/index.js`
```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

**验收标准**:
- ✅ 路由正常工作
- ✅ 页面可访问

#### 1.2.4 创建基础样式
**文件**: `frontend/src/style.css`
```css
/* 全局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden; /* 禁止横向滚动 */
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  background-color: #f7f8fa;
}

/* 移动端适配 */
@media (max-width: 768px) {
  html, body {
    width: 100vw;
  }
}
```

**验收标准**:
- ✅ 禁止横向滚动
- ✅ 背景色舒适

---

## 验收测试

### 后端测试
```bash
# 启动后端
cd backend
uvicorn app.main:app --reload --port 8000

# 测试
curl http://localhost:8000/health
# 预期: {"status":"ok","message":"MyLedger API is running"}

curl http://localhost:8000/
# 预期: {"name":"MyLedger","version":"1.0.0"}
```

### 前端测试
```bash
# 启动前端
cd frontend
npm install
npm run dev

# 访问 http://localhost:3000
# 预期: 看到首页
```

---

## 文件清单

### 后端文件
| 文件 | 说明 |
|------|------|
| `backend/app/main.py` | FastAPI 应用入口 |
| `backend/app/database.py` | 数据库配置 |
| `backend/app/models/__init__.py` | 模型导出 |

### 前端文件
| 文件 | 说明 |
|------|------|
| `frontend/src/main.js` | Vue 应用入口 |
| `frontend/src/App.vue` | 根组件 |
| `frontend/src/router/index.js` | 路由配置 |
| `frontend/src/style.css` | 全局样式 |

---

## 风险预防

### 1. 开发中断恢复
- ✅ 所有文件已创建并提交到 Git
- ✅ 详细记录了验收标准和测试方法
- ✅ 每个文件都有明确的说明

### 2. 技术问题
- ✅ 使用已有经验的 Vue 3 + FastAPI
- ✅ 参考 PocketLedger 项目

---

## 进度

| 任务 | 状态 | 开始时间 | 完成时间 |
|------|------|----------|----------|
| 1.1.1 FastAPI 入口 | ⏳ 待开始 | - | - |
| 1.1.2 数据库配置 | ⏳ 待开始 | - | - |
| 1.1.3 模型基类 | ⏳ 待开始 | - | - |
| 1.2.1 Vue 入口 | ⏳ 待开始 | - | - |
| 1.2.2 根组件 | ⏳ 待开始 | - | - |
| 1.2.3 路由配置 | ⏳ 待开始 | - | - |
| 1.2.4 基础样式 | ⏳ 待开始 | - | - |

---

*文档版本: 1.0*
*创建时间: 2026-02-09*
