"""
FastAPI 路由 - 营销自动化 API 接口
"""

import asyncio
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


# 新增市场研究请求模型
class MarketAnalysisRequest(BaseModel):
    """市场分析请求模型"""
    product_name: str = Field(..., description="产品名称")
    product_info: str = Field(..., description="产品信息描述")
    target_audience: str = Field(..., description="目标用户群体")
    language: str = Field(default="zh", description="分析报告语言: zh (中文), en (English)")


class CompetitorAnalysisRequest(BaseModel):
    """竞品分析请求模型"""
    product_name: str = Field(..., description="产品名称")
    product_info: str = Field(..., description="产品信息描述")
    competitors: List[str] = Field(..., description="竞争对手列表")
    language: str = Field(default="zh", description="分析报告语言: zh (中文), en (English)")


class UserResearchRequest(BaseModel):
    """用户研究请求模型"""
    product_name: str = Field(..., description="产品名称")
    product_info: str = Field(..., description="产品信息描述")
    target_audience: str = Field(..., description="目标用户群体")
    language: str = Field(default="zh", description="研究报告语言: zh (中文), en (English)")


class TrendForecastRequest(BaseModel):
    """趋势预测请求模型"""
    product_name: str = Field(..., description="产品名称")
    product_info: str = Field(..., description="产品信息描述")
    focus_areas: List[str] = Field(..., description="关注领域列表")
    language: str = Field(default="zh", description="预测报告语言: zh (中文), en (English)")


# 新增增强市场调研请求模型
class EnhancedMarketResearchRequest(BaseModel):
    """增强市场调研请求模型"""
    research_type: str = Field(..., description="调研类型: competitor, market_trend, user_feedback, technology")
    target: str = Field(..., description="调研目标")
    depth: str = Field(default="medium", description="调研深度: shallow, medium, deep")
    language: str = Field(default="zh", description="报告语言: zh (中文), en (English)")


class WebSearchRequest(BaseModel):
    """网络搜索请求模型"""
    query: str = Field(..., description="搜索查询")
    num_results: int = Field(default=10, description="返回结果数量")
    language: str = Field(default="zh", description="搜索语言")
    country: str = Field(default="cn", description="搜索国家")


class WebScrapeRequest(BaseModel):
    """网页抓取请求模型"""
    url: str = Field(..., description="要抓取的网页URL")
    extract_type: str = Field(default="text", description="提取类型: text, links, images, structured")
    max_length: int = Field(default=5000, description="最大内容长度")


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


class CompetitorAnalysisResponse(BaseModel):
    """竞品分析响应模型"""
    competitors: List[Dict[str, Any]]
    market_position: Dict[str, Any]
    recommendations: List[str]


class TrendAnalysisResponse(BaseModel):
    """趋势分析响应模型"""
    trends: List[Dict[str, Any]]
    emerging_technologies: List[str]
    market_opportunities: List[Dict[str, Any]]


class ProductRoadmapResponse(BaseModel):
    """产品路线图响应模型"""
    immediate_priorities: List[str]
    short_term_goals: List[str]
    medium_term_vision: List[str]
    long_term_strategy: List[str]
    competitive_advantages: List[str]
    market_opportunities: List[Dict[str, Any]]


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


# 新增市场研究 API 端点
@router.post("/research/market-analysis", response_model=Dict[str, Any])
async def conduct_market_analysis(
    request: MarketAnalysisRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """进行市场分析"""
    try:
        logger.info(f"开始市场分析: {request.product_name}, 语言: {request.language}")
        
        result = await crew.conduct_market_analysis(
            product_name=request.product_name,
            product_info=request.product_info,
            target_audience=request.target_audience,
            language=request.language
        )
        
        return {
            "task_id": f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed" if result.get("success") else "failed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"市场分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"市场分析失败: {str(e)}")


@router.post("/research/competitor-analysis", response_model=Dict[str, Any])
async def analyze_competitors(
    request: CompetitorAnalysisRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """分析竞争对手"""
    try:
        logger.info(f"开始竞品分析: {request.competitors}, 语言: {request.language}")
        
        result = await crew.analyze_competitors(
            product_name=request.product_name,
            product_info=request.product_info,
            competitors=request.competitors,
            language=request.language
        )
        
        return {
            "task_id": f"competitor_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed" if result.get("success") else "failed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"竞品分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"竞品分析失败: {str(e)}")


@router.post("/research/user-research", response_model=Dict[str, Any])
async def research_user_needs(
    request: UserResearchRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """研究用户需求"""
    try:
        logger.info(f"开始用户需求研究: {request.product_name}, 语言: {request.language}")
        
        result = await crew.research_user_needs(
            product_name=request.product_name,
            product_info=request.product_info,
            target_audience=request.target_audience,
            language=request.language
        )
        
        return {
            "task_id": f"user_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed" if result.get("success") else "failed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"用户需求研究失败: {e}")
        raise HTTPException(status_code=500, detail=f"用户需求研究失败: {str(e)}")


@router.post("/research/trend-forecast", response_model=Dict[str, Any])
async def forecast_trends(
    request: TrendForecastRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """预测趋势"""
    try:
        logger.info(f"开始趋势预测: {request.focus_areas}, 语言: {request.language}")
        
        result = await crew.forecast_trends(
            product_name=request.product_name,
            product_info=request.product_info,
            focus_areas=request.focus_areas,
            language=request.language
        )
        
        return {
            "task_id": f"trend_forecast_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed" if result.get("success") else "failed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"趋势预测失败: {e}")
        raise HTTPException(status_code=500, detail=f"趋势预测失败: {str(e)}")


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


@router.post("/api/v1/market/comprehensive")
async def comprehensive_market_analysis(
    request: MarketAnalysisRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """
    综合市场分析
    """
    try:
        logger.info(f"开始综合市场分析: {request.product_name}, 语言: {request.language}")
        
        # 并行执行多个分析任务
        market_task = crew.conduct_market_analysis(
            product_name=request.product_name,
            product_info=request.product_info,
            target_audience=request.target_audience,
            language=request.language
        )
        
        # 如果有竞争对手信息，也进行竞品分析
        # 这里可以根据实际需求扩展
        
        # 等待市场分析完成
        market_result = await market_task
        
        # 生成综合报告
        report = {
            "executive_summary": {
                "product_name": request.product_name,
                "analysis_date": datetime.now().isoformat(),
                "analysis_language": request.language,
                "status": "completed" if market_result.get("success") else "failed"
            },
            "market_analysis": market_result,
            "actionable_recommendations": [
                {
                    "category": "市场定位" if request.language == "zh" else "Market Positioning",
                    "priority": "高" if request.language == "zh" else "High",
                    "action": "基于市场分析，明确产品定位" if request.language == "zh" else "Define product positioning based on market analysis",
                    "timeline": "立即执行" if request.language == "zh" else "Immediate"
                },
                {
                    "category": "产品开发" if request.language == "zh" else "Product Development",
                    "priority": "高" if request.language == "zh" else "High", 
                    "action": "优先开发用户最需要的功能" if request.language == "zh" else "Prioritize development of most needed features",
                    "timeline": "3个月内" if request.language == "zh" else "Within 3 months"
                },
                {
                    "category": "市场推广" if request.language == "zh" else "Marketing",
                    "priority": "中" if request.language == "zh" else "Medium",
                    "action": "制定针对性的内容策略" if request.language == "zh" else "Develop targeted content strategy",
                    "timeline": "持续进行" if request.language == "zh" else "Ongoing"
                }
            ]
        }
        
        return report
        
    except Exception as e:
        logger.error(f"综合市场分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"综合市场分析失败: {str(e)}")


# 新增增强市场调研API端点
@router.post("/research/enhanced", response_model=Dict[str, Any])
async def enhanced_market_research(
    request: EnhancedMarketResearchRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """
    增强市场调研 - 使用网络搜索和网页抓取
    """
    try:
        logger.info(f"开始增强市场调研: {request.research_type} - {request.target}")
        
        # 使用增强市场调研工具
        from src.tools.research_tools import EnhancedMarketResearchTool
        research_tool = EnhancedMarketResearchTool()
        
        result = research_tool._run(
            research_type=request.research_type,
            target=request.target,
            depth=request.depth,
            language=request.language
        )
        
        return {
            "research_id": f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "research_type": request.research_type,
            "target": request.target,
            "depth": request.depth,
            "language": request.language,
            "result": result,
            "metadata": {
                "tools_used": ["web_search", "web_scrape", "enhanced_market_research"],
                "research_date": datetime.now().isoformat(),
                "data_sources": ["Google Search", "Web Scraping", "AI Analysis"]
            }
        }
        
    except Exception as e:
        logger.error(f"增强市场调研失败: {e}")
        raise HTTPException(status_code=500, detail=f"增强市场调研失败: {str(e)}")


@router.post("/tools/web-search", response_model=Dict[str, Any])
async def web_search(
    request: WebSearchRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """
    网络搜索工具
    """
    try:
        logger.info(f"执行网络搜索: {request.query}")
        
        from src.tools.research_tools import WebSearchTool
        search_tool = WebSearchTool()
        
        result = search_tool._run(
            query=request.query,
            num_results=request.num_results,
            language=request.language,
            country=request.country
        )
        
        return {
            "search_id": f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "query": request.query,
            "num_results": request.num_results,
            "language": request.language,
            "country": request.country,
            "result": result,
            "metadata": {
                "search_date": datetime.now().isoformat(),
                "data_source": "Serper API"
            }
        }
        
    except Exception as e:
        logger.error(f"网络搜索失败: {e}")
        raise HTTPException(status_code=500, detail=f"网络搜索失败: {str(e)}")


@router.post("/tools/web-scrape", response_model=Dict[str, Any])
async def web_scrape(
    request: WebScrapeRequest,
    crew: MarketingCrew = Depends(get_marketing_crew)
):
    """
    网页抓取工具
    """
    try:
        logger.info(f"执行网页抓取: {request.url}")
        
        from src.tools.research_tools import WebScrapeTool
        scrape_tool = WebScrapeTool()
        
        result = scrape_tool._run(
            url=request.url,
            extract_type=request.extract_type,
            max_length=request.max_length
        )
        
        return {
            "scrape_id": f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed",
            "url": request.url,
            "extract_type": request.extract_type,
            "max_length": request.max_length,
            "result": result,
            "metadata": {
                "scrape_date": datetime.now().isoformat(),
                "content_length": len(result)
            }
        }
        
    except Exception as e:
        logger.error(f"网页抓取失败: {e}")
        raise HTTPException(status_code=500, detail=f"网页抓取失败: {str(e)}") 