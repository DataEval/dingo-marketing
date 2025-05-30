"""
轻量级任务调度器
提供基本的定时任务功能
"""

import asyncio
from typing import Dict, Callable, Any, Optional
from datetime import datetime, timedelta
from loguru import logger

from src.config.settings import settings

# 任务存储
_scheduled_tasks: Dict[str, Dict] = {}
_running_tasks: Dict[str, asyncio.Task] = {}
_scheduler_running = False


async def init_scheduler():
    """初始化任务调度器"""
    global _scheduler_running
    
    try:
        logger.info("初始化任务调度器...")
        
        # 启动调度器主循环
        _scheduler_running = True
        asyncio.create_task(_scheduler_loop())
        
        logger.info("✅ 任务调度器启动完成")
        
    except Exception as e:
        logger.error(f"❌ 任务调度器初始化失败: {e}")
        raise


async def _scheduler_loop():
    """调度器主循环"""
    while _scheduler_running:
        try:
            current_time = datetime.now()
            
            # 检查需要执行的任务
            for task_id, task_info in _scheduled_tasks.items():
                if task_info['next_run'] <= current_time:
                    if task_id not in _running_tasks:
                        # 启动任务
                        task = asyncio.create_task(_run_task(task_id, task_info))
                        _running_tasks[task_id] = task
                    
                    # 计算下次执行时间
                    if task_info['interval']:
                        task_info['next_run'] = current_time + timedelta(seconds=task_info['interval'])
            
            # 清理已完成的任务
            completed_tasks = []
            for task_id, task in _running_tasks.items():
                if task.done():
                    completed_tasks.append(task_id)
            
            for task_id in completed_tasks:
                del _running_tasks[task_id]
            
            # 等待一段时间再检查
            await asyncio.sleep(10)  # 每10秒检查一次
            
        except Exception as e:
            logger.error(f"调度器循环出错: {e}")
            await asyncio.sleep(10)


async def _run_task(task_id: str, task_info: Dict):
    """执行任务"""
    try:
        logger.info(f"执行任务: {task_id}")
        
        func = task_info['func']
        args = task_info.get('args', ())
        kwargs = task_info.get('kwargs', {})
        
        if asyncio.iscoroutinefunction(func):
            await func(*args, **kwargs)
        else:
            func(*args, **kwargs)
        
        logger.info(f"任务执行完成: {task_id}")
        
    except Exception as e:
        logger.error(f"任务执行失败 {task_id}: {e}")


def schedule_task(
    task_id: str,
    func: Callable,
    interval: Optional[int] = None,
    delay: int = 0,
    args: tuple = (),
    kwargs: dict = None
):
    """调度任务
    
    Args:
        task_id: 任务ID
        func: 要执行的函数
        interval: 重复间隔（秒），None表示只执行一次
        delay: 延迟执行时间（秒）
        args: 函数参数
        kwargs: 函数关键字参数
    """
    if kwargs is None:
        kwargs = {}
    
    next_run = datetime.now() + timedelta(seconds=delay)
    
    _scheduled_tasks[task_id] = {
        'func': func,
        'interval': interval,
        'next_run': next_run,
        'args': args,
        'kwargs': kwargs
    }
    
    logger.info(f"任务已调度: {task_id}, 下次执行: {next_run}")


def cancel_task(task_id: str):
    """取消任务"""
    if task_id in _scheduled_tasks:
        del _scheduled_tasks[task_id]
        logger.info(f"任务已取消: {task_id}")
    
    if task_id in _running_tasks:
        _running_tasks[task_id].cancel()
        del _running_tasks[task_id]
        logger.info(f"运行中的任务已停止: {task_id}")


def get_scheduled_tasks() -> Dict[str, Dict]:
    """获取所有调度的任务"""
    return _scheduled_tasks.copy()


def get_running_tasks() -> Dict[str, asyncio.Task]:
    """获取所有运行中的任务"""
    return _running_tasks.copy()


async def check_scheduler_health():
    """检查调度器健康状态"""
    try:
        return _scheduler_running
    except Exception as e:
        logger.error(f"调度器健康检查失败: {e}")
        return False


async def close_scheduler():
    """关闭调度器"""
    global _scheduler_running
    
    try:
        _scheduler_running = False
        
        # 取消所有运行中的任务
        for task_id, task in _running_tasks.items():
            task.cancel()
            logger.info(f"任务已停止: {task_id}")
        
        _running_tasks.clear()
        _scheduled_tasks.clear()
        
        logger.info("✅ 任务调度器已关闭")
        
    except Exception as e:
        logger.error(f"关闭调度器时出错: {e}")


# 便捷函数
def schedule_daily_task(task_id: str, func: Callable, hour: int = 9, minute: int = 0):
    """调度每日任务"""
    now = datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # 如果今天的时间已过，调度到明天
    if target_time <= now:
        target_time += timedelta(days=1)
    
    delay = (target_time - now).total_seconds()
    schedule_task(task_id, func, interval=24*3600, delay=int(delay))


def schedule_hourly_task(task_id: str, func: Callable, minute: int = 0):
    """调度每小时任务"""
    now = datetime.now()
    target_time = now.replace(minute=minute, second=0, microsecond=0)
    
    # 如果这小时的时间已过，调度到下小时
    if target_time <= now:
        target_time += timedelta(hours=1)
    
    delay = (target_time - now).total_seconds()
    schedule_task(task_id, func, interval=3600, delay=int(delay)) 