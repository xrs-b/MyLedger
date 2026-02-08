# MyLedger - Phase 2: 用户认证系统实现计划

> **项目名**: MyLedger  
> **Phase**: 2  
> **目标**: 创建用户认证系统（注册、登录、JWT）  
> **创建时间**: 2026-02-09

---

## 任务清单

### 2.1 后端 - 用户认证 API

#### 2.1.1 创建用户 Schema (Pydantic 模型)
**文件**: `backend/app/schemas/user.py`
```python
from pydantic import BaseModel
from typing import Optional

# 注册请求
class UserCreate(BaseModel):
    username: str
    password: str
    invite_code: str

# 登录请求
class UserLogin(BaseModel):
    username: str
    password: str

# 用户响应
class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    is_active: bool
    created_at: datetime

# Token 响应
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

#### 2.1.2 创建用户 CRUD API
**文件**: `backend/app/routers/auth.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# API 路由
router = APIRouter(prefix="/api/v1/auth", tags=["认证"])

@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 验证邀请码
    if user.invite_code != "vip1123":
        raise HTTPException(status_code=400, detail="邀请码错误")
    
    # 检查用户名
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查是否是第一个用户
    is_first_user = db.query(User).count() == 0
    
    # 创建用户
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        is_admin=is_first_user  # 第一个用户是管理员
    )
    db.add(db_user)
    db.commit()
    
    return {"message": "注册成功", "is_admin": is_first_user}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 验证用户
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="账户已禁用")
    
    # 创建 Token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

#### 2.1.3 创建 Token 工具函数
```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token 无效")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_token(token)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user
```

---

### 2.2 前端 - 认证页面

#### 2.2.1 创建 API 层
**文件**: `frontend/src/api/auth.js`
```javascript
import axios from 'axios'

const API_URL = '/api/v1/auth'

export const authApi = {
  // 注册
  register(data) {
    return axios.post(`${API_URL}/register`, data)
  },
  
  // 登录
  login(data) {
    return axios.post(`${API_URL}/login`, data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  
  // 获取当前用户
  me() {
    return axios.get(`${API_URL}/me`)
  }
}
```

#### 2.2.2 创建认证 Store
**文件**: `frontend/src/stores/auth.js`
```javascript
import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),
  
  actions: {
    async login(username, password) {
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)
      
      const response = await authApi.login(formData)
      this.token = response.data.access_token
      localStorage.setItem('token', this.token)
      return response.data
    },
    
    async register(username, password, inviteCode) {
      const response = await authApi.register({
        username,
        password,
        invite_code: inviteCode
      })
      return response.data
    },
    
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  },
  
  getters: {
    isLoggedIn: (state) => !!state.token
  }
})
```

#### 2.2.3 创建注册页面
**文件**: `frontend/src/views/Register.vue`
```vue
<template>
  <div class="page-container">
    <h1 class="page-title">注册</h1>
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
      <van-field
        v-model="form.inviteCode"
        name="inviteCode"
        label="邀请码"
        placeholder="请输入邀请码"
        :rules="[{ required: true, message: '请输入邀请码' }]"
      />
      <van-button type="primary" native-type="submit" block>
        注册
      </van-button>
    </van-form>
    <router-link to="/login" class="link">
      已有账号？去登录
    </router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { Toast } from 'vant'

const authStore = useAuthStore()
const form = ref({
  username: '',
  password: '',
  inviteCode: ''
})

const onSubmit = async () => {
  try {
    await authStore.register(
      form.value.username,
      form.value.password,
      form.value.inviteCode
    )
    Toast.success('注册成功')
    setTimeout(() => {
      window.location.href = '/login'
    }, 2000)
  } catch (error) {
    Toast.fail(error.response?.data?.detail || '注册失败')
  }
}
</script>
```

#### 2.2.4 创建登录页面
**文件**: `frontend/src/views/Login.vue`
```vue
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
      <van-button type="primary" native-type="submit" block>
        登录
      </van-button>
    </van-form>
    <router-link to="/register" class="link">
      还没有账号？去注册
    </router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Toast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({
  username: '',
  password: ''
})

const onSubmit = async () => {
  try {
    await authStore.login(form.value.username, form.value.password)
    Toast.success('登录成功')
    router.push('/')
  } catch (error) {
    Toast.fail(error.response?.data?.detail || '登录失败')
  }
}
</script>
```

---

## 验收测试

### 后端测试
```bash
# 启动后端
cd backend
uvicorn app.main:app --reload --port 888

# 测试注册
curl -X POST http://localhost:888/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456","invite_code":"vip1123"}'

# 测试登录
curl -X POST http://localhost:888/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=123456"
```

### 前端测试
```bash
# 启动前端
cd frontend
npm run dev

# 访问 http://localhost:666/register
# 预期: 看到注册表单
# 输入邀请码 vip1123 注册
# 预期: 2秒后自动跳转登录页
```

---

## 文件清单

### 后端文件
| 文件 | 说明 |
|------|------|
| `backend/app/schemas/user.py` | 用户 Schema |
| `backend/app/routers/auth.py` | 认证 API |
| `backend/app/main.py` | 注册路由 |

### 前端文件
| 文件 | 说明 |
|------|------|
| `frontend/src/api/auth.js` | 认证 API 层 |
| `frontend/src/stores/auth.js` | 认证 Store |
| `frontend/src/views/Register.vue` | 注册页面 |
| `frontend/src/views/Login.vue` | 登录页面 |

---

## 风险预防

- ✅ 每个任务都有详细代码示例
- ✅ 验收测试方法明确
- ✅ 依赖版本已锁定

---

## 进度

| 任务 | 状态 | 开始时间 | 完成时间 |
|------|------|----------|----------|
| 2.1.1 用户 Schema | ⏳ 待开始 | - | - |
| 2.1.2 认证 API | ⏳ 待开始 | - | - |
| 2.1.3 Token 工具 | ⏳ 待开始 | - | - |
| 2.2.1 认证 API 层 | ⏳ 待开始 | - | - |
| 2.2.2 认证 Store | ⏳ 待开始 | - | - |
| 2.2.3 注册页面 | ⏳ 待开始 | - | - |
| 2.2.4 登录页面 | ⏳ 待开始 | - | - |

---

*文档版本: 1.0*
*创建时间: 2026-02-09*
