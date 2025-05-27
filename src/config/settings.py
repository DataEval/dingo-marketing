"""
应用配置管理
"""

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    DEBUG: bool = Field(default=False, description="调试模式")
    HOST: str = Field(default="0.0.0.0", description="服务器主机")
    PORT: int = Field(default=8000, description="服务器端口")
    
    # 数据库配置
    DATABASE_URL: str = Field(description="数据库连接URL")
    
    # Redis 配置
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis连接URL")
    
    # AI 服务配置
    OPENAI_API_KEY: str = Field(description="OpenAI API密钥")
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, description="Anthropic API密钥")
    
    # GitHub 配置
    GITHUB_TOKEN: str = Field(description="GitHub访问令牌")
    GITHUB_REPOSITORY: str = Field(default="DataEval/dingo", description="目标仓库")
    
    # 社交媒体配置
    TWITTER_API_KEY: Optional[str] = Field(default=None, description="Twitter API密钥")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, description="Twitter API密钥")
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(default=None, description="Twitter访问令牌")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = Field(default=None, description="Twitter访问令牌密钥")
    
    # CORS 配置
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="允许的CORS源"
    )
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO", description="日志级别")
    
    # 任务调度配置
    SCHEDULER_TIMEZONE: str = Field(default="Asia/Shanghai", description="调度器时区")
    
    # 推广配置
    CAMPAIGN_MAX_DAILY_POSTS: int = Field(default=10, description="每日最大发布数")
    CAMPAIGN_MIN_INTERVAL_MINUTES: int = Field(default=60, description="最小发布间隔(分钟)")
    
    # 用户画像配置
    PROFILING_UPDATE_INTERVAL_HOURS: int = Field(default=24, description="用户画像更新间隔(小时)")
    PROFILING_GITHUB_LOOKBACK_DAYS: int = Field(default=90, description="GitHub数据回溯天数")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings() 