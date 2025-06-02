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
    language: str = Field(default="zh", description="分析报告语言: zh (中文), en (English)")


class ContentCampaignRequest(BaseModel):
    """内容营销活动请求"""
    name: str = Field(..., description="活动名称")
    target_audience: str = Field(..., description="目标受众")
    topics: List[str] = Field(..., description="主要主题列表")
    content_types: List[str] = Field(default=["blog", "social"], description="内容类型")
    duration: str = Field(default="1个月", description="活动周期")
    keywords: Optional[List[str]] = Field(default=None, description="关键词列表")
    language: str = Field(default="zh", description="内容语言: zh (中文), en (English)")


class CommunityEngagementRequest(BaseModel):
    """社区互动请求"""
    repository: str = Field(..., description="目标仓库地址 (格式: owner/repo)")
    interaction_types: List[str] = Field(default=["comment", "issue"], description="互动类型")
    target_count: int = Field(default=10, description="目标用户数量")
    lookback_days: int = Field(default=30, description="回溯天数")
    engagement_level: str = Field(default="moderate", description="互动强度: light, moderate, intensive")
    language: str = Field(default="zh", description="互动语言: zh (中文), en (English)")


class ComprehensiveCampaignRequest(BaseModel):
    """综合营销活动请求"""
    target_users: List[str] = Field(..., description="目标用户列表")
    target_repositories: List[str] = Field(default=[], description="目标仓库列表")
    duration: str = Field(default="30天", description="活动周期")
    budget: str = Field(default="标准", description="预算级别")
    metrics: List[str] = Field(default=["参与度", "转化率", "知名度"], description="成功指标")
    language: str = Field(default="zh", description="活动语言: zh (中文), en (English)")


class ContentGenerationRequest(BaseModel):
    """内容生成请求"""
    content_type: str = Field(..., description="内容类型: blog, social, email, tutorial, documentation")
    topic: str = Field(..., description="内容主题")
    target_audience: str = Field(..., description="目标受众")
    tone: str = Field(default="professional", description="语调")
    length: str = Field(default="medium", description="长度")
    language: str = Field(default="zh", description="语言")
    keywords: Optional[List[str]] = Field(default=None, description="关键词")


class ContentOptimizationRequest(BaseModel):
    """内容优化请求"""
    content: str = Field(..., description="原始内容")
    optimization_type: str = Field(default="general", description="优化类型: seo, engagement, readability, technical")
    target_platform: str = Field(default="general", description="目标平台: github, twitter, linkedin, blog")
    keywords: Optional[List[str]] = Field(default=None, description="SEO 关键词")


class ContentAnalysisRequest(BaseModel):
    """内容分析请求"""
    content: str = Field(..., description="要分析的内容")
    optimization_type: str = Field(default="general", description="分析类型")
    target_platform: str = Field(default="general", description="目标平台")
    keywords: Optional[List[str]] = Field(default=None, description="关键词")


class RepositoryConfigRequest(BaseModel):
    """仓库配置请求"""
    repository: str = Field(..., description="GitHub 仓库地址 (格式: owner/repo)")


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
router = APIRouter(tags=["marketing"])

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
        logger.info(f"开始分析用户: {request.user_list}, 语言: {request.language}")
        
        # 执行用户分析
        result = await crew.analyze_target_users(request.user_list, request.language)
        
        # 处理分析结果
        analysis_insights = {
            "total_users": len(request.user_list),
            "analysis_depth": request.analysis_depth,
            "language": request.language,
            "completion_time": datetime.now().isoformat()
        }
        
        return {
            "task_id": f"user_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "result": result,
            "insights": analysis_insights,
            "recommendations": [
                "基于分析结果制定个性化互动策略" if request.language == "zh" else "Develop personalized interaction strategies based on analysis results",
                "优先关注高影响力和高活跃度用户" if request.language == "zh" else "Prioritize high-influence and high-activity users",
                "针对不同技术背景的用户调整内容策略" if request.language == "zh" else "Adjust content strategies for users with different technical backgrounds"
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
            "keywords": request.keywords or [],
            "language": request.language
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


@router.post("/community/engage")
async def engage_community(request: CommunityEngagementRequest):
    """执行社区互动活动"""
    try:
        logger.info(f"开始社区互动，目标仓库: {request.repository}, 语言: {request.language}")
        
        # 设置目标仓库
        crew = get_marketing_crew()
        crew.set_target_repository(request.repository)
        
        # 准备互动配置
        engagement_config = {
            "repository": request.repository,
            "interaction_types": request.interaction_types,
            "target_count": request.target_count,
            "lookback_days": request.lookback_days,
            "language": request.language  # 添加语言参数
        }
        
        # 执行社区互动
        result = await crew.execute_community_engagement(engagement_config)
        
        # 根据语言返回不同的响应
        if request.language.lower() == "en":
            insights = "Community engagement activities completed successfully. Check the detailed report for interaction results and community feedback."
            recommendations = [
                "Continue monitoring community response to interactions",
                "Follow up with engaged users for deeper relationships",
                "Analyze interaction effectiveness for future campaigns"
            ]
        else:
            insights = "社区互动活动已成功完成。请查看详细报告了解互动结果和社区反馈。"
            recommendations = [
                "继续监控社区对互动的响应",
                "跟进已互动的用户以建立更深层次的关系",
                "分析互动效果以优化未来的活动"
            ]
        
        return {
            "status": "success",
            "task_id": f"community_engagement_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "engagement_result": result,
            "insights": insights,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"社区互动执行失败: {str(e)}")
        error_message = f"Community engagement failed: {str(e)}" if request.language.lower() == "en" else f"社区互动执行失败: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


@router.post("/campaigns/comprehensive")
async def run_comprehensive_campaign(request: ComprehensiveCampaignRequest):
    """执行综合营销活动"""
    try:
        logger.info(f"开始综合营销活动，目标用户: {request.target_users}, 语言: {request.language}")
        
        # 准备活动配置
        crew = get_marketing_crew()
        campaign_config = {
            "target_users": request.target_users,
            "target_repositories": request.target_repositories,
            "duration": request.duration,
            "budget": request.budget,
            "metrics": request.metrics,
            "language": request.language  # 添加语言参数
        }
        
        # 执行综合营销活动
        result = await crew.run_comprehensive_campaign(campaign_config)
        
        # 根据语言返回不同的响应
        if request.language.lower() == "en":
            insights = "Comprehensive marketing campaign executed successfully. The campaign covered data analysis, content creation, community interaction, and performance evaluation phases."
            recommendations = [
                "Monitor campaign performance metrics regularly",
                "Optimize content based on user engagement data",
                "Scale successful interaction strategies",
                "Prepare follow-up campaigns based on results"
            ]
        else:
            insights = "综合营销活动已成功执行。活动涵盖了数据分析、内容创作、社区互动和效果评估等阶段。"
            recommendations = [
                "定期监控活动效果指标",
                "基于用户参与数据优化内容",
                "扩大成功的互动策略",
                "基于结果准备后续活动"
            ]
        
        return {
            "status": "success",
            "task_id": f"comprehensive_campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "campaign_result": result,
            "insights": insights,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"综合营销活动执行失败: {str(e)}")
        error_message = f"Comprehensive campaign failed: {str(e)}" if request.language.lower() == "en" else f"综合营销活动执行失败: {str(e)}"
        raise HTTPException(status_code=500, detail=error_message)


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
        
        # 将关键词列表转换为字符串
        keywords_str = ",".join(request.keywords) if request.keywords else ""
        
        result = content_tool._run(
            content_type=request.content_type,
            topic=request.topic,
            target_audience=request.target_audience,
            tone=request.tone,
            length=request.length,
            language=request.language,
            keywords=keywords_str
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


@router.post("/content/optimize", response_model=Dict[str, Any])
async def optimize_content(
    request: ContentOptimizationRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """优化内容"""
    try:
        logger.info(f"优化内容: {request.optimization_type} - {request.target_platform}")
        
        # 使用内容优化工具
        from src.tools.content_tools import ContentOptimizationTool
        optimization_tool = ContentOptimizationTool()
        
        # 将关键词列表转换为字符串
        keywords_str = ",".join(request.keywords) if request.keywords else ""
        
        result = optimization_tool._run(
            content=request.content,
            optimization_type=request.optimization_type,
            target_audience="开发者",  # 使用默认值
            keywords=keywords_str
        )
        
        return {
            "optimization_id": f"optimize_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "optimized_content": result,
            "metadata": {
                "optimization_type": request.optimization_type,
                "target_platform": request.target_platform,
                "keywords": request.keywords,
                "optimized_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"内容优化失败: {e}")
        raise HTTPException(status_code=500, detail=f"内容优化失败: {str(e)}")


@router.post("/content/analyze", response_model=Dict[str, Any])
async def analyze_content(
    request: ContentAnalysisRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """分析内容"""
    try:
        logger.info(f"分析内容: {request.optimization_type} - {request.target_platform}")
        
        # 使用内容分析工具
        from src.tools.content_tools import ContentAnalysisTool
        analysis_tool = ContentAnalysisTool()
        
        result = analysis_tool._run(
            content=request.content,
            analysis_type=request.optimization_type
        )
        
        return {
            "analysis_id": f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "analysis_result": result,
            "metadata": {
                "analysis_type": request.optimization_type,
                "target_platform": request.target_platform,
                "keywords": request.keywords,
                "analyzed_at": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"内容分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"内容分析失败: {str(e)}")


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


@router.get("/repository")
async def get_target_repository(crew: MarketingCrew = Depends(get_marketing_crew)):
    """获取当前目标仓库"""
    try:
        repository = crew.get_target_repository()
        return {
            "repository": repository,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"获取目标仓库失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取目标仓库失败: {str(e)}")


@router.post("/repository")
async def set_target_repository(
    request: RepositoryConfigRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """设置目标仓库"""
    try:
        # 验证仓库地址格式
        if "/" not in request.repository or len(request.repository.split("/")) != 2:
            raise HTTPException(
                status_code=400, 
                detail="仓库地址格式错误，应为 'owner/repo' 格式"
            )
        
        result = crew.set_target_repository(request.repository)
        
        return {
            **result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"设置目标仓库失败: {e}")
        raise HTTPException(status_code=500, detail=f"设置目标仓库失败: {str(e)}") 