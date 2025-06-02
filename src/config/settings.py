"""
应用配置管理
"""

from typing import List, Optional, Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    LOG_LEVEL: str = "INFO"
    
    # 数据库配置
    DATABASE_URL: str = "dingo_marketing.json"
    
    # 任务调度配置
    ENABLE_SCHEDULER: bool = True
    SCHEDULER_TIMEZONE: str = "Asia/Shanghai"
    
    # 用户画像配置
    USER_PROFILING_ENABLED: bool = True
    USER_PROFILING_CACHE_TTL: int = 3600
    
    # 推广配置
    CAMPAIGN_MAX_DAILY_POSTS: int = 10
    CAMPAIGN_MIN_INTERVAL_MINUTES: int = 60
    
    # AI 服务配置 - 通用配置
    API_KEY: str = ""
    MODEL: str = "deepseek-chat"
    BASE_URL: str = "https://api.deepseek.com/v1"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.7
    
    # GitHub 配置
    GITHUB_TOKEN: str = ""
    GITHUB_REPOSITORY: str = ""
    
    # 社交媒体 API 配置
    TWITTER_API_KEY: str = ""
    TWITTER_API_SECRET: str = ""
    LINKEDIN_API_KEY: str = ""
    
    # CORS 配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # 允许额外的环境变量
    
    def get_ai_config(self) -> Dict[str, Any]:
        """获取AI服务配置"""
        return {
            "model": self.MODEL,
            "api_key": self.API_KEY,
            "base_url": self.BASE_URL,
            "max_tokens": self.MAX_TOKENS,
            "temperature": self.TEMPERATURE
        }


# 创建全局配置实例
settings = Settings() 