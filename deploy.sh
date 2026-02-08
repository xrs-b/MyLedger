#!/bin/bash
# =============================================================================
# MyLedger 一键部署脚本
# =============================================================================
# 使用方法:
#   curl -s https://raw.githubusercontent.com/xrs-b/MyLedger/main/deploy.sh | bash
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为 root 用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_warn "建议使用 root 用户运行此脚本"
    fi
}

# 检查系统
check_system() {
    log_info "检查系统环境..."
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        log_info "检测到系统: $PRETTY_NAME"
        
        if [ "$ID" != "ubuntu" ] && [ "$ID" != "debian" ]; then
            log_warn "此脚本主要针对 Ubuntu/Debian 系统优化"
        fi
    else
        log_warn "无法识别系统版本"
    fi
}

# 检查 Docker
check_docker() {
    log_info "检查 Docker..."
    
    if ! command -v docker &> /dev/null; then
        log_warn "Docker 未安装，正在安装..."
        install_docker
    else
        log_info "Docker 已安装: $(docker --version)"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_warn "Docker Compose 未安装，正在安装..."
        install_docker_compose
    else
        log_info "Docker Compose 已安装: $(docker-compose --version)"
    fi
}

# 安装 Docker
install_docker() {
    log_info "安装 Docker..."
    
    # 安装依赖
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    
    # 添加 Docker 官方 GPG 密钥
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    
    # 添加 Docker 仓库
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    # 安装 Docker
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # 启动 Docker
    systemctl start docker
    systemctl enable docker
    
    log_info "Docker 安装完成"
}

# 安装 Docker Compose
install_docker_compose() {
    log_info "安装 Docker Compose..."
    
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    log_info "Docker Compose 安装完成"
}

# 创建部署目录
create_deploy_dir() {
    log_info "创建部署目录..."
    
    DEPLOY_DIR="/var/www/myleger"
    
    if [ ! -d "$DEPLOY_DIR" ]; then
        mkdir -p "$DEPLOY_DIR"
        log_info "创建目录: $DEPLOY_DIR"
    else
        log_warn "目录已存在: $DEPLOY_DIR"
    fi
}

# 下载代码
download_code() {
    log_info "下载代码..."
    
    DEPLOY_DIR="/var/www/myleger"
    
    if [ -d "$DEPLOY_DIR/.git" ]; then
        log_info "拉取最新代码..."
        cd "$DEPLOY_DIR"
        git pull
    else
        log_info "克隆代码仓库..."
        git clone https://github.com/xrs-b/MyLedger.git "$DEPLOY_DIR"
        cd "$DEPLOY_DIR"
    fi
}

# 配置环境变量
configure_env() {
    log_info "配置环境变量..."
    
    DEPLOY_DIR="/var/www/myleger"
    
    # 创建环境变量文件
    cat > "$DEPLOY_DIR/.env" << EOF
# MyLedger 环境配置
# 请根据实际情况修改

# 数据库 (SQLite)
DATABASE_URL=sqlite:///./data/mobile_ledger.db

# JWT 配置
SECRET_KEY=$(openssl rand -base64 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# 服务配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=888
FRONTEND_PORT=80

# 邀请码
INVITE_CODE=vip1123
EOF
    
    log_info "环境变量文件已创建: $DEPLOY_DIR/.env"
    log_warn "请根据需要修改 .env 文件中的配置"
}

# 初始化数据
init_data() {
    log_info "初始化数据..."
    
    DEPLOY_DIR="/var/www/myleger"
    
    cd "$DEPLOY_DIR"
    
    # 创建数据目录
    mkdir -p data
    
    # 初始化分类数据
    if [ -f "backend/init_categories.py" ]; then
        log_info "初始化分类数据..."
        docker-compose run --rm backend python init_categories.py || true
    fi
}

# 启动服务
start_services() {
    log_info "启动服务..."
    
    DEPLOY_DIR="/var/www/myleger"
    cd "$DEPLOY_DIR"
    
    # 构建并启动
    docker-compose up -d --build
    
    log_info "服务启动中..."
    sleep 5
    
    # 检查状态
    if docker-compose ps | grep -q "Up"; then
        log_info "所有服务已启动"
        docker-compose ps
    else
        log_error "部分服务启动失败，请检查日志"
        docker-compose logs
    fi
}

# 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    # 开放端口
    if command -v ufw &> /dev/null; then
        ufw allow 80/tcp
        ufw allow 443/tcp
        ufw allow 888/tcp
        log_info "已开放端口 80, 443, 888"
    fi
}

# 测试部署
test_deployment() {
    log_info "测试部署..."
    
    # 测试后端 API
    if curl -s http://localhost:888/health | grep -q "ok"; then
        log_info "后端 API 测试通过"
    else
        log_warn "后端 API 测试失败"
    fi
    
    # 测试前端
    if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
        log_info "前端测试通过"
    else
        log_warn "前端测试失败"
    fi
}

# 显示部署信息
show_info() {
    log_info "========================================"
    log_info "  MyLedger 部署完成！"
    log_info "========================================"
    echo ""
    log_info "访问地址:"
    echo "  - 前端: http://$(hostname -I | awk '{print $1}')"
    echo "  - 后端 API: http://$(hostname -I | awk '{print $1}'):888"
    echo ""
    log_info "管理命令:"
    echo "  - 查看日志: docker-compose logs -f"
    echo "  - 重启服务: docker-compose restart"
    echo "  - 停止服务: docker-compose down"
    echo "  - 更新代码: cd /var/www/myleger && git pull && docker-compose up -d --build"
    echo ""
    log_info "配置文件: /var/www/myleger/.env"
    log_info "数据目录: /var/www/myleger/data"
    echo ""
}

# 主函数
main() {
    echo "========================================"
    echo "  MyLedger 一键部署脚本"
    echo "========================================"
    echo ""
    
    check_root
    check_system
    check_docker
    create_deploy_dir
    download_code
    configure_env
    init_data
    start_services
    configure_firewall
    test_deployment
    show_info
}

# 执行主函数
main
