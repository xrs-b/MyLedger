# MyLedger 部署教程

> 部署到 Ubuntu 24.04 LTS 云服务器
> 
> **项目地址**: https://github.com/xrs-b/MyLedger

---

## 目录

1. [准备工作](#1-准备工作)
2. [安装 Docker](#2-安装-docker)
3. [部署项目](#3-部署项目)
4. [配置域名](#4-配置域名)
5. [配置 HTTPS](#5-配置-https)
6. [日常维护](#6-日常维护)
7. [常见问题](#7-常见问题)

---

## 1. 准备工作

### 1.1 服务器要求

| 配置 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 1 核 | 2 核 |
| 内存 | 1GB | 2GB |
| 磁盘 | 10GB | 20GB SSD |
| 系统 | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

### 1.2 登录服务器

```bash
# SSH 登录服务器
ssh root@your-server-ip

# 输入密码（服务器提供商提供的密码）
```

### 1.3 更新系统

```bash
# 更新软件包列表
apt update

# 升级已安装的软件包
apt upgrade -y
```

---

## 2. 安装 Docker

### 2.1 安装 Docker

```bash
# 安装依赖
apt install -y apt-transport-https ca-certificates curl software-properties-common

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加 Docker 仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动 Docker
systemctl start docker
systemctl enable docker

# 验证安装
docker --version
docker compose version
```

### 2.2 配置 Docker 镜像加速（可选）

```bash
# 编辑 Docker 配置
mkdir -p /etc/docker
tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF

# 重启 Docker
systemctl daemon-reload
systemctl restart docker
```

---

## 3. 部署项目

### 3.1 克隆项目

```bash
# 创建部署目录
mkdir -p /var/www
cd /var/www

# 克隆项目
git clone https://github.com/xrs-b/MyLedger.git
cd MyLedger
```

### 3.2 配置环境变量

```bash
# 创建环境变量文件
cat > .env << 'EOF'
# MyLedger 环境配置

# 数据库 (SQLite)
DATABASE_URL=sqlite:///./data/mobile_ledger.db

# JWT 配置
SECRET_KEY=$(openssl rand -base64 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# 邀请码
INVITE_CODE=vip1123
EOF

# 创建数据目录
mkdir -p data
```

### 3.3 初始化数据

```bash
# 初始化分类数据
docker compose run --rm backend python init_categories.py
```

### 3.4 启动服务

```bash
# 构建并启动
docker compose up -d --build

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 3.5 验证部署

```bash
# 测试后端 API
curl http://localhost:888/health
# 预期返回: {"status":"ok","message":"MyLedger API is running"}

# 测试前端
curl http://localhost
# 预期返回: HTML 页面
```

---

## 4. 配置域名

### 4.1 域名解析

在域名服务商控制台添加 A 记录：

| 记录类型 | 主机记录 | 记录值 |
|----------|----------|--------|
| A | @ | 你的服务器 IP |
| A | www | 你的服务器 IP |

### 4.2 配置 Nginx

```bash
# 安装 Nginx
apt install -y nginx

# 创建配置文件
cat > /etc/nginx/sites-available/myleger << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # 重定向到 HTTPS（配置 HTTPS 后启用）
    # return 301 https://$server_name$request_uri;

    # 前端静态文件
    root /var/www/MyLedger/frontend/dist;
    index index.html;

    # Vue Router 支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理
    location /api/ {
        proxy_pass http://localhost:888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 健康检查
    location /health {
        proxy_pass http://localhost:888/health;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/myleger /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

### 4.3 开放端口

```bash
# 开放 HTTP 和 HTTPS 端口
ufw allow 80/tcp
ufw allow 443/tcp

# 重启防火墙
ufw reload
```

---

## 5. 配置 HTTPS

### 5.1 安装 Certbot

```bash
# 安装 Certbot
apt install -y certbot python3-certbot-nginx

# 或使用 snap 安装
snap install --classic certbot
```

### 5.2 获取 SSL 证书

```bash
# 自动配置 Nginx 并获取证书
certbot --nginx -d your-domain.com -d www.your-domain.com

# 或仅获取证书（手动配置）
certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

### 5.3 手动配置 HTTPS

如果使用自动配置，Certbot 会自动修改 Nginx 配置。

手动配置示例：

```bash
# 查看证书位置
ls -la /etc/letsencrypt/live/your-domain.com/
```

修改 Nginx 配置（HTTPS）：

```bash
cat > /etc/nginx/sites-available/myleger << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL 证书配置
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS 头
    add_header Strict-Transport-Security "max-age=63072000" always;

    # 前端静态文件
    root /var/www/MyLedger/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# 测试并重载
nginx -t
systemctl reload nginx
```

### 5.4 续期证书

```bash
# 测试续期
certbot renew --dry-run

# 手动续期
certbot renew

# 添加自动续期任务
crontab -e

# 添加以下行（每天凌晨 2 点检查续期）
0 2 * * * /usr/bin/certbot renew --quiet
```

---

## 6. 日常维护

### 6.1 服务管理

```bash
# 进入项目目录
cd /var/www/MyLedger

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend

# 重启服务
docker compose restart

# 重启单个服务
docker compose restart backend

# 停止服务
docker compose down

# 停止并删除数据卷（危险！）
docker compose down -v
```

### 6.2 更新项目

```bash
cd /var/www/MyLedger

# 拉取最新代码
git pull

# 重新构建并启动
docker compose up -d --build

# 清理旧镜像
docker image prune -f
```

### 6.3 数据备份

```bash
# 备份数据目录
cp -r /var/www/MyLedger/data /backup/myleger-data-$(date +%Y%m%d)

# 或使用 Docker 卷备份
docker run --rm -v myledger_data:/data -v /backup:/backup alpine tar czf /backup/myleger-volume-$(date +%Y%m%d).tar.gz -C /data .
```

### 6.4 监控服务

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
docker system df

# 查看容器日志（最近 100 行）
docker compose logs --tail 100
```

---

## 7. 常见问题

### Q1: 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep :888

# 或
lsof -i :888

# 停止占用端口的进程
kill -9 <PID>
```

### Q2: Docker 构建失败

```bash
# 清理 Docker 缓存
docker system prune -a

# 重新构建
docker compose build --no-cache
docker compose up -d
```

### Q3: 前端页面 404

```bash
# 检查前端是否构建
ls -la /var/www/MyLedger/frontend/dist/

# 重新构建前端
cd /var/www/MyLedger/frontend
npm install
npm run build
```

### Q4: API 无法访问

```bash
# 检查后端容器状态
docker compose ps backend

# 进入容器检查
docker compose exec backend sh

# 检查环境变量
env | grep DATABASE
```

### Q5: 数据库初始化失败

```bash
# 手动初始化
cd /var/www/MyLedger
docker compose run --rm backend python init_categories.py
```

### Q6: 重置所有数据

```bash
cd /var/www/MyLedger

# 停止服务
docker compose down

# 删除数据
rm -rf data/*

# 重新初始化
docker compose up -d
docker compose exec backend python init_categories.py
```

---

## 8. 快速参考

### 常用命令速查

```bash
# 服务管理
cd /var/www/MyLedger
docker compose up -d          # 启动
docker compose down           # 停止
docker compose restart        # 重启
docker compose ps             # 状态
docker compose logs -f        # 日志

# 更新
git pull
docker compose up -d --build

# 备份
cp -r data /backup/myleger-data-$(date +%Y%m%d)

# 清理
docker system prune -a
```

### 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 80/443 | HTTP/HTTPS |
| 后端 | 888 | API 服务 |

### 访问地址

| 环境 | 地址 |
|------|------|
| 本地 | http://localhost |
| 服务器 | http://你的服务器IP |
| 域名 | http://你的域名 |

### API 文档

启动后访问：http://你的域名/docs

---

## 9. 联系支持

如果遇到问题，请：

1. 查看日志：`docker compose logs`
2. 检查 Docker 状态：`docker compose ps`
3. 搜索常见问题

---

*文档版本: 1.0*  
*最后更新: 2026-02-09*
