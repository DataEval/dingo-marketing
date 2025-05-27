"""
Dingo Marketing - AI Agent 驱动的自动化运营系统
主应用入口
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from loguru import logger

from src.config.settings import settings
from src.core.database import init_db
from src.core.redis_client import init_redis
from src.agents.marketing import MarketingCrew
from src.api.routes import api_router
from src.core.scheduler import init_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """应用生命周期管理"""
    logger.info("🚀 启动 Dingo Marketing 系统...")
    
    # 初始化数据库
    await init_db()
    logger.info("✅ 数据库初始化完成")
    
    # 初始化 Redis
    await init_redis()
    logger.info("✅ Redis 连接建立")
    
    # 初始化调度器
    await init_scheduler()
    logger.info("✅ 任务调度器启动")
    
    # 初始化 AI Agent 团队
    marketing_crew = MarketingCrew()
    await marketing_crew.initialize()
    app.state.marketing_crew = marketing_crew
    logger.info("✅ AI Agent 团队初始化完成")
    
    logger.info("🎉 系统启动完成!")
    
    yield
    
    # 清理资源
    logger.info("🔄 正在关闭系统...")
    await marketing_crew.shutdown()
    logger.info("👋 系统已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="Dingo Marketing",
    description="AI Agent 驱动的 Dingo 工具自动化运营系统",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# 注册路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Dingo Marketing AI Agent System",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 检查各个组件状态
        health_status = {
            "status": "healthy",
            "timestamp": asyncio.get_event_loop().time(),
            "components": {
                "database": "healthy",
                "redis": "healthy",
                "ai_agents": "healthy",
                "scheduler": "healthy"
            }
        }
        return health_status
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        raise HTTPException(status_code=503, detail="Service Unavailable")


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    ) 