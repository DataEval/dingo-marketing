"""
轻量级数据库初始化和管理
使用简单的文件存储，避免重型数据库依赖
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger

from src.config.settings import settings

# 简单的内存数据存储
_memory_store: Dict[str, Any] = {}
_data_file: Optional[Path] = None


async def init_db():
    """初始化轻量级数据存储"""
    global _data_file
    
    try:
        # 解析数据库 URL，如果是 SQLite，使用文件存储
        database_url = settings.DATABASE_URL
        logger.info(f"初始化数据存储: {database_url}")
        
        if database_url.startswith("sqlite"):
            # 从 SQLite URL 提取文件路径
            db_path = database_url.replace("sqlite:///", "").replace("sqlite://", "")
            _data_file = Path(db_path).with_suffix('.json')
            
            # 确保目录存在
            _data_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 加载现有数据
            if _data_file.exists():
                try:
                    with open(_data_file, 'r', encoding='utf-8') as f:
                        _memory_store.update(json.load(f))
                    logger.info(f"✅ 从文件加载数据: {_data_file}")
                except Exception as e:
                    logger.warning(f"加载数据文件失败，使用空存储: {e}")
            else:
                logger.info("✅ 创建新的数据存储文件")
        else:
            # 其他情况使用内存存储
            logger.info("✅ 使用内存数据存储")
        
        # 初始化基础数据结构
        if 'users' not in _memory_store:
            _memory_store['users'] = {}
        if 'campaigns' not in _memory_store:
            _memory_store['campaigns'] = {}
        if 'content' not in _memory_store:
            _memory_store['content'] = {}
        if 'analytics' not in _memory_store:
            _memory_store['analytics'] = {}
        
        logger.info("✅ 数据存储初始化完成")
        
    except Exception as e:
        logger.error(f"❌ 数据存储初始化失败: {e}")
        raise


async def save_data():
    """保存数据到文件"""
    if _data_file:
        try:
            with open(_data_file, 'w', encoding='utf-8') as f:
                json.dump(_memory_store, f, ensure_ascii=False, indent=2)
            logger.debug(f"数据已保存到: {_data_file}")
        except Exception as e:
            logger.error(f"保存数据失败: {e}")


async def get_data(collection: str, key: str = None) -> Any:
    """获取数据"""
    if collection not in _memory_store:
        return None if key else {}
    
    if key:
        return _memory_store[collection].get(key)
    return _memory_store[collection]


async def set_data(collection: str, key: str, value: Any):
    """设置数据"""
    if collection not in _memory_store:
        _memory_store[collection] = {}
    
    _memory_store[collection][key] = value
    await save_data()


async def delete_data(collection: str, key: str = None):
    """删除数据"""
    if collection not in _memory_store:
        return
    
    if key:
        _memory_store[collection].pop(key, None)
    else:
        _memory_store[collection] = {}
    
    await save_data()


async def check_db_health():
    """检查数据存储健康状态"""
    try:
        # 简单的健康检查
        test_key = "_health_check"
        await set_data("system", test_key, {"timestamp": asyncio.get_event_loop().time()})
        result = await get_data("system", test_key)
        await delete_data("system", test_key)
        return result is not None
    except Exception as e:
        logger.error(f"数据存储健康检查失败: {e}")
        return False


async def close_db():
    """关闭数据存储"""
    try:
        await save_data()
        logger.info("✅ 数据存储已关闭")
    except Exception as e:
        logger.error(f"关闭数据存储时出错: {e}")


# 便捷函数
async def get_user_data(user_id: str) -> Optional[Dict]:
    """获取用户数据"""
    return await get_data("users", user_id)


async def save_user_data(user_id: str, data: Dict):
    """保存用户数据"""
    await set_data("users", user_id, data)


async def get_campaign_data(campaign_id: str) -> Optional[Dict]:
    """获取营销活动数据"""
    return await get_data("campaigns", campaign_id)


async def save_campaign_data(campaign_id: str, data: Dict):
    """保存营销活动数据"""
    await set_data("campaigns", campaign_id, data) 