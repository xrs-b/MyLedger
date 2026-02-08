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
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

### Docker 部署

```bash
docker-compose up -d --build
```

## 目录结构

```
mobile-ledger/
├── backend/          # 后端代码
│   ├── app/         # FastAPI 应用
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/        # 前端代码
│   ├── src/        # Vue 3 源码
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 部署

```bash
# 一键部署到 Ubuntu
curl -s https://raw.githubusercontent.com/xrs-b/mobile-ledger/main/deploy.sh | bash
```

## 参考

- PocketLedger: https://github.com/xrs-b/PocketLedger
