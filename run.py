#!/usr/bin/env python3
"""
Dingo Marketing 应用启动文件
支持命令行参数配置
"""

import argparse
import os
import sys
import uvicorn
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Dingo Marketing API Server")
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="服务器主机地址 (默认: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口 (默认: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="启用自动重载 (开发模式)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["debug", "info", "warning", "error"],
        default="info",
        help="日志级别 (默认: info)"
    )
    
    return parser.parse_args()

def setup_environment():
    """设置环境变量"""
    # 加载 .env 文件
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("警告: python-dotenv 未安装，无法加载 .env 文件")
    
    # 设置默认环境变量
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("LOG_LEVEL", "INFO")

def main():
    """主函数"""
    args = parse_args()
    
    # 设置环境
    setup_environment()
    
    # 从环境变量或命令行参数获取配置
    host = args.host or os.getenv("HOST", "127.0.0.1")
    port = args.port or int(os.getenv("PORT", 8000))
    debug = args.debug or os.getenv("DEBUG", "false").lower() == "true"
    log_level = args.log_level or os.getenv("LOG_LEVEL", "info").lower()
    
    print(f"🚀 启动 Dingo Marketing API Server")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📚 API 文档: http://{host}:{port}/docs")
    print(f"🔧 调试模式: {'开启' if debug else '关闭'}")
    print(f"📝 日志级别: {log_level.upper()}")
    print("-" * 50)
    
    try:
        # 启动服务器
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=args.reload or debug,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 