# 移动账本 (Mobile Ledger)

> 移动端记账应用，支持日常记账和项目记账

## 技术栈

- **前端**: Vue 3 + Vite + Vant
- **后端**: Python 3.12 + FastAPI + SQLite
- **部署**: Docker + Nginx

## 功能特性

- ✅ 日常记账
- ✅ 项目记账（有时间范围、预算、人均计算）
- ✅ 二级分类（14个一级分类 + 44个二级分类）
- ✅ 多维度统计（日常+项目交叉统计）
- ✅ 用户系统（邀请码注册、首个用户为管理员）
- ✅ 后端管理界面
- ✅ 移动端完美适配

## 快速开始

### 本地开发

```bash
# 后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 888

# 前端
cd frontend
npm install
npm run dev
```

### Docker 部署

```bash
# 方式一: 一键部署 (Ubuntu)
curl -s https://raw.githubusercontent.com/xrs-b/MyLedger/main/deploy.sh | bash

# 方式二: 手动部署
docker-compose up -d --build
```

### 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost |
| 后端 API | http://localhost:888 |

## 目录结构

```
mobile-ledger/
├── backend/          # 后端代码
│   ├── app/         # FastAPI 应用
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── schemas/
│   ├── init_categories.py  # 分类初始化
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # 前端代码
│   ├── src/        # Vue 3 源码
│   │   ├── views/
│   │   ├── components/
│   │   ├── api/
│   │   ├── stores/
│   │   └── router/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── deploy.sh        # 一键部署脚本
└── README.md
```

## API 文档

启动后端后访问: http://localhost:888/docs

### 主要 API

| 模块 | 路径 | 说明 |
|------|------|------|
| 认证 | /api/v1/auth | 注册、登录 |
| 分类 | /api/v1/categories | 分类管理 |
| 记账 | /api/v1/records | 记账 CRUD |
| 项目 | /api/v1/projects | 项目管理 |
| 统计 | /api/v1/statistics | 多维度统计 |
| 管理 | /api/v1/admin | 后台管理 |

## 部署到云服务器

### Ubuntu 24.04

```bash
# 1. 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. 克隆并部署
git clone https://github.com/xrs-b/MyLedger.git
cd MyLedger
./deploy.sh
```

### 域名配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端
    location / {
        root /var/www/myleger/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://localhost:888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### HTTPS 配置

```bash
# 使用 Let's Encrypt
certbot --nginx -d your-domain.com
```

## 配置说明

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| DATABASE_URL | sqlite:///./data/mobile_ledger.db | 数据库连接 |
| SECRET_KEY | - | JWT 密钥 (自动生成) |
| ALGORITHM | HS256 | JWT 算法 |
| ACCESS_TOKEN_EXPIRE_MINUTES | 10080 | Token 有效期 (7天) |
| INVITE_CODE | vip1123 | 注册邀请码 |

### 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端 | 888 | FastAPI 服务 |
| 前端 | 80 | Nginx 服务 |

## 默认数据

### 分类
- **支出**: 餐饮、交通、购物、娱乐、住房、通讯、人情、医疗、教育、其他
- **收入**: 工资、副业、投资、其他

### 支付方式
- 现金、银行卡、支付宝、微信、信用卡、电子钱包

## 用户系统

- **邀请码**: `vip1123` (固定)
- **首个用户**: 自动成为管理员
- **后续用户**: 普通用户

## 开发计划

- [x] Phase 1: 基础框架
- [x] Phase 2: 用户认证
- [x] Phase 3: 分类系统
- [x] Phase 4: 日常记账
- [x] Phase 5: 项目记账
- [x] Phase 6: 统计报表
- [x] Phase 7: 后端管理
- [ ] Phase 8: 部署优化

## License

MIT

## 参考

- PocketLedger: https://github.com/xrs-b/PocketLedger
