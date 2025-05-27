"""
营销团队 AI Agent 组织架构
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from loguru import logger

from src.tools.github_tools import GitHubAnalysisTool, GitHubInteractionTool
from src.tools.content_tools import ContentGenerationTool, ContentOptimizationTool, ContentAnalysisTool
from src.config.settings import settings


class MarketingCrew:
    """营销团队 AI Agent 组织"""
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.agents = self._create_agents()
        self.crew = self._create_crew()
        logger.info("营销团队 AI Agent 组织初始化完成")
    
    def _initialize_tools(self) -> List[BaseTool]:
        """初始化工具"""
        return [
            GitHubAnalysisTool(),
            GitHubInteractionTool(),
            ContentGenerationTool(),
            ContentOptimizationTool(),
            ContentAnalysisTool(),
        ]
    
    def _create_agents(self) -> Dict[str, Agent]:
        """创建 AI Agent"""
        
        # 数据分析师 Agent
        data_analyst = Agent(
            role="数据分析师",
            goal="分析 GitHub 用户行为和社区趋势，为营销策略提供数据支持",
            backstory="""
            你是一位经验丰富的数据分析师，专门分析开源社区的用户行为和趋势。
            你擅长从 GitHub 数据中挖掘有价值的洞察，识别潜在的目标用户，
            并为营销团队提供数据驱动的建议。
            """,
            tools=[tool for tool in self.tools if tool.name in ["github_analysis"]],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
        )
        
        # 内容创作者 Agent
        content_creator = Agent(
            role="内容创作者",
            goal="创建高质量的技术内容和营销材料，吸引目标用户",
            backstory="""
            你是一位才华横溢的内容创作者，专门创建技术博客、教程和营销内容。
            你深谙技术社区的语言和文化，能够创作出既有技术深度又有吸引力的内容。
            你的内容总是能够引起开发者的共鸣并促进社区参与。
            """,
            tools=[tool for tool in self.tools if tool.name in ["content_generation", "content_optimization", "content_analysis"]],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
        )
        
        # 社区经理 Agent
        community_manager = Agent(
            role="社区经理",
            goal="管理社区互动，建立关系，提高 Dingo 项目的知名度和参与度",
            backstory="""
            你是一位热情的社区经理，专门负责开源项目的社区建设和用户关系管理。
            你擅长在 GitHub 上与用户互动，回应问题，参与讨论，并建立长期的社区关系。
            你的目标是让每个用户都感受到社区的温暖和专业。
            """,
            tools=[tool for tool in self.tools if tool.name in ["github_interaction", "github_analysis"]],
            verbose=True,
            allow_delegation=False,
            max_iter=3,
        )
        
        # 营销策略师 Agent
        marketing_strategist = Agent(
            role="营销策略师",
            goal="制定和执行营销策略，协调团队工作，确保营销目标的实现",
            backstory="""
            你是一位资深的营销策略师，专门负责开源项目的营销策略制定和执行。
            你能够综合分析数据、内容和社区反馈，制定有效的营销计划。
            你擅长协调团队工作，确保所有营销活动都能有效地推进项目目标。
            """,
            tools=self.tools,  # 策略师可以使用所有工具
            verbose=True,
            allow_delegation=True,
            max_iter=5,
        )
        
        return {
            "data_analyst": data_analyst,
            "content_creator": content_creator,
            "community_manager": community_manager,
            "marketing_strategist": marketing_strategist,
        }
    
    def _create_crew(self) -> Crew:
        """创建团队"""
        return Crew(
            agents=list(self.agents.values()),
            tasks=[],  # 任务将在执行时动态创建
            process=Process.hierarchical,
            manager_agent=self.agents["marketing_strategist"],
            verbose=True,
        )
    
    async def analyze_target_users(self, user_list: List[str]) -> Dict[str, Any]:
        """分析目标用户"""
        logger.info(f"开始分析 {len(user_list)} 个目标用户")
        
        # 创建用户分析任务
        analysis_task = Task(
            description=f"""
            分析以下 GitHub 用户列表，为每个用户生成详细的分析报告：
            用户列表: {', '.join(user_list)}
            
            对每个用户，请分析：
            1. 用户的技术背景和兴趣领域
            2. 活跃度和影响力评估
            3. 与 Dingo 项目的相关性
            4. 推荐的互动策略
            
            最后提供一个综合的目标用户画像和营销建议。
            """,
            agent=self.agents["data_analyst"],
            expected_output="详细的用户分析报告，包含每个用户的分析和综合建议"
        )
        
        # 执行任务
        self.crew.tasks = [analysis_task]
        result = self.crew.kickoff()
        
        logger.info("目标用户分析完成")
        return {"analysis_result": result, "analyzed_users": user_list}
    
    async def create_content_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """创建内容营销活动"""
        logger.info(f"开始创建内容营销活动: {campaign_config.get('name', '未命名活动')}")
        
        # 创建内容策略任务
        strategy_task = Task(
            description=f"""
            基于以下配置创建内容营销策略：
            活动名称: {campaign_config.get('name', '未命名活动')}
            目标受众: {campaign_config.get('target_audience', '开发者')}
            主要主题: {campaign_config.get('topics', ['Dingo 工具使用'])}
            内容类型: {campaign_config.get('content_types', ['blog', 'social'])}
            活动周期: {campaign_config.get('duration', '1个月')}
            
            请制定详细的内容策略，包括：
            1. 内容日历和发布计划
            2. 每种内容类型的具体要求
            3. SEO 关键词策略
            4. 社交媒体推广策略
            """,
            agent=self.agents["marketing_strategist"],
            expected_output="详细的内容营销策略和执行计划"
        )
        
        # 创建内容生成任务
        content_task = Task(
            description=f"""
            根据营销策略师的计划，创建以下内容：
            
            1. 为 {campaign_config.get('topics', ['Dingo'])[0]} 主题创建一篇技术博客文章
            2. 创建 3-5 条社交媒体内容
            3. 创建一份邮件营销模板
            
            所有内容都应该：
            - 针对 {campaign_config.get('target_audience', '开发者')} 受众
            - 体现 Dingo 工具的价值
            - 包含适当的技术深度
            - 优化 SEO 效果
            """,
            agent=self.agents["content_creator"],
            expected_output="完整的内容包，包括博客文章、社交媒体内容和邮件模板"
        )
        
        # 执行任务
        self.crew.tasks = [strategy_task, content_task]
        result = self.crew.kickoff()
        
        logger.info("内容营销活动创建完成")
        return {"campaign_result": result, "config": campaign_config}
    
    async def execute_community_engagement(self, engagement_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行社区互动活动"""
        logger.info("开始执行社区互动活动")
        
        # 创建社区分析任务
        community_analysis_task = Task(
            description=f"""
            分析 Dingo 项目的当前社区状态：
            
            1. 分析项目的 GitHub 社区活跃度
            2. 识别活跃的贡献者和用户
            3. 分析最近的 issues 和 discussions
            4. 评估社区健康度和参与度
            
            基于分析结果，提供社区互动建议。
            """,
            agent=self.agents["data_analyst"],
            expected_output="社区状态分析报告和互动建议"
        )
        
        # 创建互动执行任务
        engagement_task = Task(
            description=f"""
            基于社区分析结果，执行以下互动活动：
            
            1. 回复最近的 issues 和讨论
            2. 与活跃用户进行互动
            3. 分享有价值的技术内容
            4. 邀请用户参与项目贡献
            
            互动类型: {engagement_config.get('interaction_types', ['comment', 'issue'])}
            目标用户数: {engagement_config.get('target_count', 10)}
            
            确保所有互动都是有价值和真诚的。
            """,
            agent=self.agents["community_manager"],
            expected_output="社区互动执行报告，包括具体的互动记录"
        )
        
        # 执行任务
        self.crew.tasks = [community_analysis_task, engagement_task]
        result = self.crew.kickoff()
        
        logger.info("社区互动活动执行完成")
        return {"engagement_result": result, "config": engagement_config}
    
    async def run_comprehensive_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """运行综合营销活动"""
        logger.info("开始运行综合营销活动")
        
        # 创建综合营销任务
        comprehensive_task = Task(
            description=f"""
            执行一个综合的营销活动，包括以下步骤：
            
            1. 数据分析阶段：
               - 分析目标用户群体
               - 评估当前项目状态
               - 识别营销机会
            
            2. 内容创作阶段：
               - 创建技术博客内容
               - 制作社交媒体内容
               - 准备邮件营销材料
            
            3. 社区互动阶段：
               - 与目标用户互动
               - 参与相关讨论
               - 建立社区关系
            
            4. 效果评估阶段：
               - 监控活动效果
               - 收集用户反馈
               - 优化策略
            
            活动配置: {campaign_config}
            
            请协调团队成员，确保活动的顺利执行。
            """,
            agent=self.agents["marketing_strategist"],
            expected_output="综合营销活动执行报告，包括各阶段的详细结果和效果评估"
        )
        
        # 执行任务
        self.crew.tasks = [comprehensive_task]
        result = self.crew.kickoff()
        
        logger.info("综合营销活动执行完成")
        return {
            "campaign_result": result,
            "config": campaign_config,
            "execution_time": datetime.now().isoformat()
        }
    
    def get_team_status(self) -> Dict[str, Any]:
        """获取团队状态"""
        return {
            "agents": {
                name: {
                    "role": agent.role,
                    "goal": agent.goal,
                    "tools": [tool.name for tool in agent.tools] if agent.tools else []
                }
                for name, agent in self.agents.items()
            },
            "tools": [tool.name for tool in self.tools],
            "status": "ready",
            "last_updated": datetime.now().isoformat()
        } 