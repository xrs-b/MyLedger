#!/bin/bash
# =============================================================================
# MyLedger 快速重新部署脚本
# =============================================================================

set -e

echo "========================================"
echo "  MyLedger 快速重新部署"
echo "========================================"

# 1. 拉取最新代码
echo ""
echo "[1/5] 拉取最新代码..."
cd /var/www/MyLedger
git fetch --all
git reset --hard origin/main

# 2. 构建前端
echo ""
echo "[2/5] 构建前端..."
cd /var/www/MyLedger/frontend
npm install
npm run build

# 3. 停止旧容器
echo ""
echo "[3/5] 停止旧容器..."
cd /var/www/MyLedger
docker compose down -v

# 4. 重新构建并启动
echo ""
echo "[4/5] 重新构建并启动..."
docker compose up -d --build

# 5. 等待启动
echo ""
echo "[5/5] 等待启动..."
sleep 30

# 测试
echo ""
echo "========================================"
echo "  测试部署..."
echo "========================================"

curl -s http://localhost:888/health && echo ""

echo ""
echo "========================================"
echo "  部署完成！"
echo "========================================"
echo ""
echo "访问地址:"
echo "  - 前端: http://$(hostname -I | awk '{print $1}')"
echo "  - 后端 API: http://$(hostname -I | awk '{print $1}'):888"
echo ""
