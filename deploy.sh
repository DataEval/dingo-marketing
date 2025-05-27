#!/bin/bash

# Dingo Marketing 部署脚本
# 支持本地部署

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    cat << EOF
Dingo Marketing 部署脚本

用法: $0 <command> [options]

命令:
    setup       初始化环境和依赖
    start       启动服务
    stop        停止服务
    restart     重启服务
    status      查看状态
    logs        查看日志
    clean       清理环境

选项:
    -h, --help      显示此帮助信息
    -v, --verbose   详细输出
    -p, --port      指定端口 (默认: 8000)

示例:
    $0 setup        初始化本地环境
    $0 start        启动本地服务
    $0 start -p 8080  在端口 8080 启动
    $0 logs         查看日志
EOF
}

# 检查 Python 环境
check_python() {
    log_info "检查 Python 环境..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 未安装，请先安装 Python 3.9+"
        exit 1
    fi
    
    # 检查 Python 版本
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$python_version < 3.9" | bc -l) -eq 1 ]]; then
        log_error "Python 版本过低，需要 3.9+，当前版本: $python_version"
        exit 1
    fi
    
    log_success "Python 环境检查通过: $python_version"
}

# 检查环境文件
check_env_file() {
    local env_type=${1:-"local"}
    local env_file=".env"
    
    if [ ! -f "$env_file" ]; then
        log_warning "环境文件 $env_file 不存在"
        
        if [ -f ".env.example" ]; then
            log_info "复制 .env.example 到 .env"
            cp .env.example .env
            log_warning "请编辑 .env 文件，填入正确的 API 密钥"
            log_info "必需配置："
            log_info "  - OPENAI_API_KEY"
            log_info "  - GITHUB_TOKEN"
            log_info "  - GITHUB_REPOSITORY"
            return 1
        fi
        
        log_error "无法找到环境配置文件"
        exit 1
    fi
    
    # 检查必需的环境变量
    source $env_file
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
        log_error "请在 .env 文件中设置 OPENAI_API_KEY"
        return 1
    fi
    
    if [ -z "$GITHUB_TOKEN" ] || [ "$GITHUB_TOKEN" = "your_github_token_here" ]; then
        log_error "请在 .env 文件中设置 GITHUB_TOKEN"
        return 1
    fi
    
    log_success "环境文件检查通过: $env_file"
    return 0
}

# 设置虚拟环境
setup_venv() {
    log_info "设置 Python 虚拟环境..."
    
    if [ ! -d "venv" ]; then
        log_info "创建虚拟环境..."
        python3 -m venv venv
    fi
    
    log_info "激活虚拟环境..."
    source venv/bin/activate
    
    log_info "升级 pip..."
    pip install --upgrade pip
    
    log_success "虚拟环境设置完成"
}

# 安装依赖
install_dependencies() {
    log_info "安装项目依赖..."
    
    source venv/bin/activate
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        log_error "找不到依赖文件 requirements.txt"
        exit 1
    fi
    
    log_success "依赖安装完成"
}

# 创建必要目录
create_directories() {
    log_info "创建必要目录..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p .run
    
    log_success "目录创建完成"
}

# 初始化环境
setup_environment() {
    log_info "初始化 Dingo Marketing 环境..."
    
    check_python
    setup_venv
    install_dependencies
    create_directories
    
    if ! check_env_file "local"; then
        log_warning "请配置环境变量后再启动服务"
        exit 1
    fi
    
    log_success "环境初始化完成！"
    log_info "下一步: $0 start"
}

# 启动本地服务
start_service() {
    log_info "启动 Dingo Marketing 服务..."
    
    # 检查环境
    if [ ! -d "venv" ]; then
        log_error "虚拟环境不存在，请先运行: $0 setup"
        exit 1
    fi
    
    if ! check_env_file "local"; then
        exit 1
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 检查端口
    local port=${PORT:-8000}
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        log_error "端口 $port 已被占用"
        log_info "请使用其他端口: $0 start -p 8001"
        exit 1
    fi
    
    # 启动服务
    log_info "在端口 $port 启动服务..."
    
    # 创建 PID 文件
    echo $$ > .run/dingo.pid
    
    # 启动应用
    if [ "$VERBOSE" = true ]; then
        python run.py --host 0.0.0.0 --port $port --debug
    else
        nohup python run.py --host 0.0.0.0 --port $port > logs/app.log 2>&1 &
        echo $! > .run/dingo.pid
        log_success "服务已启动 (PID: $(cat .run/dingo.pid))"
        log_info "访问地址: http://localhost:$port"
        log_info "API 文档: http://localhost:$port/docs"
        log_info "查看日志: $0 logs"
    fi
}

# 停止服务
stop_service() {
    log_info "停止 Dingo Marketing 服务..."
    
    if [ -f ".run/dingo.pid" ]; then
        local pid=$(cat .run/dingo.pid)
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            log_success "服务已停止 (PID: $pid)"
        else
            log_warning "进程 $pid 不存在"
        fi
        rm -f .run/dingo.pid
    else
        log_warning "PID 文件不存在，尝试查找进程..."
        pkill -f "python run.py" || log_warning "未找到运行中的服务"
    fi
}

# 重启服务
restart_service() {
    log_info "重启 Dingo Marketing 服务..."
    stop_service
    sleep 2
    start_service
}

# 查看服务状态
show_status() {
    log_info "检查 Dingo Marketing 服务状态..."
    
    if [ -f ".run/dingo.pid" ]; then
        local pid=$(cat .run/dingo.pid)
        if ps -p $pid > /dev/null 2>&1; then
            log_success "服务正在运行 (PID: $pid)"
            
            # 检查端口
            local port=$(lsof -Pan -p $pid -i | grep LISTEN | awk '{print $9}' | cut -d: -f2)
            if [ ! -z "$port" ]; then
                log_info "监听端口: $port"
                log_info "访问地址: http://localhost:$port"
            fi
        else
            log_error "服务未运行 (PID 文件存在但进程不存在)"
            rm -f .run/dingo.pid
        fi
    else
        log_warning "服务未运行 (无 PID 文件)"
    fi
}

# 查看日志
show_logs() {
    log_info "显示 Dingo Marketing 日志..."
    
    if [ -f "logs/app.log" ]; then
        tail -f logs/app.log
    else
        log_warning "日志文件不存在"
        log_info "如果服务正在运行，请检查是否在前台模式启动"
    fi
}

# 清理环境
clean_environment() {
    log_info "清理 Dingo Marketing 环境..."
    
    # 停止服务
    stop_service
    
    # 清理文件
    rm -rf venv/
    rm -rf logs/*
    rm -rf data/*
    rm -rf .run/*
    rm -rf __pycache__/
    rm -rf src/__pycache__/
    find . -name "*.pyc" -delete
    find . -name "*.pyo" -delete
    find . -name "*.pyd" -delete
    find . -name ".DS_Store" -delete
    
    log_success "环境清理完成"
}

# 解析命令行参数
VERBOSE=false
PORT=8000
FORCE=false
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        setup|start|stop|restart|status|logs|clean)
            command="$1"
            shift
            break
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查命令
if [ -z "$command" ]; then
    log_error "请指定命令"
    show_help
    exit 1
fi

# 执行命令
case "$command" in
    "setup")
        setup_environment
        ;;
    "start")
        start_service
        ;;
    "stop")
        stop_service
        ;;
    "restart")
        restart_service
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        clean_environment
        ;;
    *)
        log_error "未知命令: $command"
        show_help
        exit 1
        ;;
esac 