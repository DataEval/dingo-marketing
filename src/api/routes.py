"""
FastAPI 路由 - 营销自动化 API 接口
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from loguru import logger

from src.agents.marketing import MarketingCrew
from src.config.settings import settings


# 请求模型
class UserAnalysisRequest(BaseModel):
    """用户分析请求"""
    user_list: List[str] = Field(..., description="GitHub 用户名列表")
    analysis_depth: str = Field(default="standard", description="分析深度: basic, standard, deep")


class ContentCampaignRequest(BaseModel):
    """内容营销活动请求"""
    name: str = Field(..., description="活动名称")
    target_audience: str = Field(..., description="目标受众")
    topics: List[str] = Field(..., description="主要主题列表")
    content_types: List[str] = Field(default=["blog", "social"], description="内容类型")
    duration: str = Field(default="1个月", description="活动周期")
    keywords: Optional[List[str]] = Field(default=None, description="关键词列表")


class CommunityEngagementRequest(BaseModel):
    """社区互动请求"""
    interaction_types: List[str] = Field(default=["comment", "issue"], description="互动类型")
    target_count: int = Field(default=10, description="目标用户数量")
    engagement_level: str = Field(default="moderate", description="互动强度: light, moderate, intensive")


class ComprehensiveCampaignRequest(BaseModel):
    """综合营销活动请求"""
    name: str = Field(..., description="活动名称")
    objectives: List[str] = Field(..., description="活动目标")
    target_audience: str = Field(..., description="目标受众")
    duration: str = Field(..., description="活动周期")
    budget_level: str = Field(default="medium", description="预算级别: low, medium, high")
    priority_channels: List[str] = Field(default=["github", "social"], description="优先渠道")


class ContentGenerationRequest(BaseModel):
    """内容生成请求"""
    content_type: str = Field(..., description="内容类型: blog, social, email, tutorial, documentation")
    topic: str = Field(..., description="内容主题")
    target_audience: str = Field(..., description="目标受众")
    tone: str = Field(default="professional", description="语调")
    length: str = Field(default="medium", description="长度")
    language: str = Field(default="zh", description="语言")
    keywords: Optional[List[str]] = Field(default=None, description="关键词")


# 响应模型
class TaskResponse(BaseModel):
    """任务响应"""
    task_id: str
    status: str
    message: str
    created_at: datetime


class AnalysisResponse(BaseModel):
    """分析响应"""
    analysis_result: str
    analyzed_users: List[str]
    insights: Dict[str, Any]
    recommendations: List[str]


# 创建路由器
router = APIRouter(prefix="/api/v1", tags=["marketing"])

# 全局变量存储营销团队实例
marketing_crew: Optional[MarketingCrew] = None


def get_marketing_crew() -> MarketingCrew:
    """获取营销团队实例"""
    global marketing_crew
    if marketing_crew is None:
        marketing_crew = MarketingCrew()
    return marketing_crew


@router.get("/status")
async def get_system_status():
    """获取系统状态"""
    try:
        crew = get_marketing_crew()
        team_status = crew.get_team_status()
        
        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "team_status": team_status,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"系统状态检查失败: {str(e)}")


@router.post("/analyze/users", response_model=Dict[str, Any])
async def analyze_users(
    request: UserAnalysisRequest,
    background_tasks: BackgroundTasks,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """分析目标用户"""
    try:
        logger.info(f"开始分析用户: {request.user_list}")
        
        # 执行用户分析
        result = await crew.analyze_target_users(request.user_list)
        
        # 处理分析结果
        analysis_insights = {
            "total_users": len(request.user_list),
            "analysis_depth": request.analysis_depth,
            "completion_time": datetime.now().isoformat()
        }
        
        return {
            "task_id": f"user_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "result": result,
            "insights": analysis_insights,
            "recommendations": [
                "基于分析结果制定个性化互动策略",
                "优先关注高影响力和高活跃度用户",
                "针对不同技术背景的用户调整内容策略"
            ]
        }
        
    except Exception as e:
        logger.error(f"用户分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"用户分析失败: {str(e)}")


@router.post("/campaigns/content", response_model=Dict[str, Any])
async def create_content_campaign(
    request: ContentCampaignRequest,
    background_tasks: BackgroundTasks,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """创建内容营销活动"""
    try:
        logger.info(f"创建内容营销活动: {request.name}")
        
        # 构建活动配置
        campaign_config = {
            "name": request.name,
            "target_audience": request.target_audience,
            "topics": request.topics,
            "content_types": request.content_types,
            "duration": request.duration,
            "keywords": request.keywords or []
        }
        
        # 执行内容营销活动
        result = await crew.create_content_campaign(campaign_config)
        
        return {
            "campaign_id": f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "result": result,
            "config": campaign_config,
            "next_steps": [
                "审核生成的内容",
                "安排发布时间表",
                "监控内容表现",
                "收集用户反馈"
            ]
        }
        
    except Exception as e:
        logger.error(f"内容营销活动创建失败: {e}")
        raise HTTPException(status_code=500, detail=f"内容营销活动创建失败: {str(e)}")


@router.post("/engagement/community", response_model=Dict[str, Any])
async def execute_community_engagement(
    request: CommunityEngagementRequest,
    background_tasks: BackgroundTasks,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """执行社区互动"""
    try:
        logger.info("执行社区互动活动")
        
        # 构建互动配置
        engagement_config = {
            "interaction_types": request.interaction_types,
            "target_count": request.target_count,
            "engagement_level": request.engagement_level
        }
        
        # 执行社区互动
        result = await crew.execute_community_engagement(engagement_config)
        
        return {
            "engagement_id": f"community_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "result": result,
            "config": engagement_config,
            "metrics": {
                "planned_interactions": request.target_count,
                "interaction_types": len(request.interaction_types),
                "engagement_level": request.engagement_level
            }
        }
        
    except Exception as e:
        logger.error(f"社区互动执行失败: {e}")
        raise HTTPException(status_code=500, detail=f"社区互动执行失败: {str(e)}")


@router.post("/campaigns/comprehensive", response_model=Dict[str, Any])
async def run_comprehensive_campaign(
    request: ComprehensiveCampaignRequest,
    background_tasks: BackgroundTasks,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """运行综合营销活动"""
    try:
        logger.info(f"启动综合营销活动: {request.name}")
        
        # 构建活动配置
        campaign_config = {
            "name": request.name,
            "objectives": request.objectives,
            "target_audience": request.target_audience,
            "duration": request.duration,
            "budget_level": request.budget_level,
            "priority_channels": request.priority_channels
        }
        
        # 执行综合营销活动
        result = await crew.run_comprehensive_campaign(campaign_config)
        
        return {
            "campaign_id": f"comprehensive_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "result": result,
            "config": campaign_config,
            "timeline": {
                "start_time": datetime.now().isoformat(),
                "estimated_duration": request.duration,
                "phases": ["分析", "内容创作", "社区互动", "效果评估"]
            }
        }
        
    except Exception as e:
        logger.error(f"综合营销活动执行失败: {e}")
        raise HTTPException(status_code=500, detail=f"综合营销活动执行失败: {str(e)}")


@router.post("/content/generate", response_model=Dict[str, Any])
async def generate_content(
    request: ContentGenerationRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """生成内容"""
    try:
        logger.info(f"生成内容: {request.content_type} - {request.topic}")
        
        # 使用内容生成工具
        from src.tools.content_tools import ContentGenerationTool
        content_tool = ContentGenerationTool()
        
        result = content_tool._run(
            content_type=request.content_type,
            topic=request.topic,
            target_audience=request.target_audience,
            tone=request.tone,
            length=request.length,
            language=request.language,
            keywords=request.keywords
        )
        
        return {
            "content_id": f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "content": result,
            "metadata": {
                "content_type": request.content_type,
                "topic": request.topic,
                "target_audience": request.target_audience,
                "language": request.language,
                "generated_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"内容生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"内容生成失败: {str(e)}")


@router.get("/analytics/dashboard")
async def get_analytics_dashboard():
    """获取分析仪表板数据"""
    try:
        # 模拟分析数据
        dashboard_data = {
            "overview": {
                "total_campaigns": 12,
                "active_campaigns": 3,
                "total_users_analyzed": 156,
                "content_pieces_created": 45
            },
            "recent_activity": [
                {
                    "type": "user_analysis",
                    "description": "分析了 15 个目标用户",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "type": "content_creation",
                    "description": "创建了技术博客文章",
                    "timestamp": datetime.now().isoformat()
                },
                {
                    "type": "community_engagement",
                    "description": "在 GitHub 上进行了 8 次互动",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            "performance_metrics": {
                "user_engagement_rate": 0.68,
                "content_quality_score": 0.85,
                "campaign_success_rate": 0.72,
                "community_growth_rate": 0.15
            },
            "top_performing_content": [
                {
                    "title": "Dingo 数据质量评估最佳实践",
                    "type": "blog",
                    "engagement_score": 0.92
                },
                {
                    "title": "如何使用 Dingo 提升数据质量",
                    "type": "tutorial",
                    "engagement_score": 0.88
                }
            ]
        }
        
        return {
            "status": "success",
            "data": dashboard_data,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"获取分析仪表板失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取分析仪表板失败: {str(e)}")


@router.get("/tools/status")
async def get_tools_status(crew: MarketingCrew = Depends(get_marketing_crew)):
    """获取工具状态"""
    try:
        tools_status = []
        
        for tool in crew.tools:
            tools_status.append({
                "name": tool.name,
                "description": tool.description,
                "status": "operational",
                "last_used": datetime.now().isoformat()
            })
        
        return {
            "status": "success",
            "tools": tools_status,
            "total_tools": len(crew.tools)
        }
        
    except Exception as e:
        logger.error(f"获取工具状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取工具状态失败: {str(e)}")


@router.post("/test/workflow")
async def test_workflow(crew: MarketingCrew = Depends(get_marketing_crew)):
    """测试工作流程"""
    try:
        logger.info("开始测试工作流程")
        
        # 测试用户分析
        test_users = ["octocat", "defunkt"]
        analysis_result = await crew.analyze_target_users(test_users)
        
        # 测试内容生成
        test_campaign_config = {
            "name": "测试活动",
            "target_audience": "开发者",
            "topics": ["Dingo 工具介绍"],
            "content_types": ["blog"],
            "duration": "1周"
        }
        content_result = await crew.create_content_campaign(test_campaign_config)
        
        return {
            "status": "success",
            "test_results": {
                "user_analysis": "completed",
                "content_generation": "completed",
                "workflow_status": "operational"
            },
            "details": {
                "analysis_result": analysis_result,
                "content_result": content_result
            },
            "test_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"工作流程测试失败: {e}")
        raise HTTPException(status_code=500, detail=f"工作流程测试失败: {str(e)}") 