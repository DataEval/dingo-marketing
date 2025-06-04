"""
营销团队 AI Agent 组织架构
"""

import json
import yaml
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from loguru import logger

from src.tools.github_tools import GitHubAnalysisTool, GitHubInteractionTool
from src.tools.content_tools import ContentGenerationTool, ContentOptimizationTool, ContentAnalysisTool
from src.tools.research_tools import WebSearchTool, WebScrapeTool, EnhancedMarketResearchTool
from src.config.settings import settings


def decode_unicode_escapes(text: str) -> str:
    """解码Unicode转义字符"""
    try:
        # 尝试解码JSON转义的Unicode字符
        return json.loads(f'"{text}"')
    except:
        return text


class MarketingCrew:
    """营销团队 AI Agent 组织"""
    
    def __init__(self):
        # 配置全局LLM
        self.llm = self._configure_global_llm()
        self.tools = self._initialize_tools()
        
        # 加载配置文件
        self.agents_config = self._load_agents_config()
        self.tasks_config = self._load_tasks_config()
        
        # 创建 agents 和 crew
        self.agents = self._create_agents()
        self.crew = self._create_crew()
        
        # 获取配置的仓库地址
        self.target_repository = settings.GITHUB_REPOSITORY or "DataEval/dingo"
        logger.info(f"营销团队 AI Agent 组织初始化完成，目标仓库: {self.target_repository}")
    
    def _load_agents_config(self) -> Dict[str, Any]:
        """加载 agents 配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'agents.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Agents 配置文件未找到: {config_path}，使用默认配置")
            return {}
        except Exception as e:
            logger.error(f"加载 agents 配置文件失败: {e}，使用默认配置")
            return {}
    
    def _load_tasks_config(self) -> Dict[str, Any]:
        """加载 tasks 配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tasks.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Tasks 配置文件未找到: {config_path}，使用默认配置")
            return {}
        except Exception as e:
            logger.error(f"加载 tasks 配置文件失败: {e}，使用默认配置")
            return {}
    
    def _configure_global_llm(self) -> LLM:
        """配置全局LLM"""
        ai_config = settings.get_ai_config()
        return LLM(
            model=ai_config["model"],
            api_key=ai_config["api_key"],
            base_url=ai_config["base_url"],
            max_tokens=ai_config["max_tokens"],
            temperature=ai_config["temperature"]
        )
    
    def _initialize_tools(self) -> List[BaseTool]:
        """初始化工具"""
        tools = []
        
        # GitHub 工具
        tools.append(GitHubAnalysisTool())
        tools.append(GitHubInteractionTool())
        
        # 内容工具
        tools.append(ContentGenerationTool())
        tools.append(ContentOptimizationTool())
        tools.append(ContentAnalysisTool())
        
        # 增强的市场调研工具
        tools.append(WebSearchTool())
        tools.append(WebScrapeTool())
        tools.append(EnhancedMarketResearchTool())
        
        return tools
    
    def _create_agent_from_config(self, agent_key: str, agent_config: Dict[str, Any], tools: List[BaseTool] = None) -> Agent:
        """从配置创建 Agent"""
        if tools is None:
            tools = []
            
        return Agent(
            role=agent_config.get('role', agent_key),
            goal=agent_config.get('goal', ''),
            backstory=agent_config.get('backstory', ''),
            tools=tools,
            verbose=True,
            allow_delegation=agent_key == 'growth_strategist',  # 只有策略师可以委派任务
            max_iter=5 if agent_key == 'growth_strategist' else 3,
            llm=self.llm,
        )
    
    def _create_agents(self) -> Dict[str, Agent]:
        """创建 AI Agent"""
        agents = {}
        
        # 如果有配置文件，使用配置文件创建 agents
        if self.agents_config:
            # 市场情报分析师 (整合了原来的市场研究、竞品分析、趋势预测)
            if 'market_intelligence_analyst' in self.agents_config:
                agents['market_intelligence_analyst'] = self._create_agent_from_config(
                    'market_intelligence_analyst',
                    self.agents_config['market_intelligence_analyst'],
                    [tool for tool in self.tools if tool.name in ["github_analysis", "web_search", "web_scrape", "enhanced_market_research"]]
                )
            
            # 用户行为分析师 (整合了原来的用户洞察和数据分析)
            if 'user_behavior_analyst' in self.agents_config:
                agents['user_behavior_analyst'] = self._create_agent_from_config(
                    'user_behavior_analyst',
                    self.agents_config['user_behavior_analyst'],
                    [tool for tool in self.tools if tool.name in ["github_analysis"]]
                )
            
            # 技术研究专家 (专注技术层面的竞争分析)
            if 'technical_research_specialist' in self.agents_config:
                agents['technical_research_specialist'] = self._create_agent_from_config(
                    'technical_research_specialist',
                    self.agents_config['technical_research_specialist'],
                    [tool for tool in self.tools if tool.name in ["github_analysis"]]
                )
            
            # 内容创作者
            if 'content_creator' in self.agents_config:
                agents['content_creator'] = self._create_agent_from_config(
                    'content_creator',
                    self.agents_config['content_creator'],
                    [tool for tool in self.tools if tool.name in ["content_generation", "content_optimization", "content_analysis"]]
                )
            
            # 社区经理
            if 'community_manager' in self.agents_config:
                agents['community_manager'] = self._create_agent_from_config(
                    'community_manager',
                    self.agents_config['community_manager'],
                    [tool for tool in self.tools if tool.name in ["github_interaction", "github_analysis"]]
                )
            
            # 增长策略师 (原营销策略师)
            if 'growth_strategist' in self.agents_config:
                agents['growth_strategist'] = self._create_agent_from_config(
                    'growth_strategist',
                    self.agents_config['growth_strategist'],
                    []  # Manager agent 不应该有工具
                )
        
        # 如果没有配置文件或配置不完整，使用默认配置
        if not agents.get('market_intelligence_analyst'):
            agents['market_intelligence_analyst'] = Agent(
                role="市场情报分析师",
                goal="综合分析市场环境、竞争格局和行业趋势，提供全面的市场情报支持",
                backstory="""
                你是一位资深的市场情报分析师，专门研究数据质量和AI工具市场。
                你的专长是整合多维度信息：市场规模、竞争对手动态、技术趋势、用户需求变化。
                你能够从宏观和微观两个层面分析市场，为产品战略提供全景式的市场洞察。
                你能够根据任务要求使用不同语言进行分析和报告。
                """,
                tools=[tool for tool in self.tools if tool.name in ["github_analysis", "web_search", "web_scrape", "enhanced_market_research"]],
                verbose=True,
                allow_delegation=False,
                max_iter=3,
                llm=self.llm,
            )
        
        if not agents.get('user_behavior_analyst'):
            agents['user_behavior_analyst'] = Agent(
                role="用户行为分析师",
                goal="深度分析用户行为数据，挖掘用户需求和使用模式，指导产品优化",
                backstory="""
                你是一位专业的用户行为分析师，专注于开发者、数据科学家和ML工程师群体。
                你擅长从GitHub活动、社区讨论、使用反馈中提取用户行为模式，
                识别用户痛点、使用场景和未满足的需求。
                你能够根据任务要求使用不同语言进行分析和报告。
                """,
                tools=[tool for tool in self.tools if tool.name in ["github_analysis"]],
                verbose=True,
                allow_delegation=False,
                max_iter=3,
                llm=self.llm,
            )
        
        if not agents.get('technical_research_specialist'):
            agents['technical_research_specialist'] = Agent(
                role="技术研究专家",
                goal="深度研究技术实现、架构设计和工程实践，提供技术层面的竞争分析",
                backstory="""
                你是一位技术研究专家，专门分析数据质量工具的技术架构和实现方案。
                你能够深入理解开源项目的代码结构、技术选型和工程实践，
                识别技术优势和劣势，为产品的技术路线图提供专业建议。
                你能够根据任务要求使用不同语言进行分析和报告。
                """,
                tools=[tool for tool in self.tools if tool.name in ["github_analysis"]],
                verbose=True,
                allow_delegation=False,
                max_iter=3,
                llm=self.llm,
            )
        
        if not agents.get('content_creator'):
            agents['content_creator'] = Agent(
                role="内容创作者",
                goal="创建高质量的技术内容和营销材料，吸引目标用户",
                backstory="""
                你是一位才华横溢的内容创作者，专门创建技术博客、教程和营销内容。
                你深谙技术社区的语言和文化，能够创作出既有技术深度又有吸引力的内容。
                你的内容总是能够引起开发者的共鸣并促进社区参与。
                你能够根据任务要求使用不同语言进行内容创作和报告。
                """,
                tools=[tool for tool in self.tools if tool.name in ["content_generation", "content_optimization", "content_analysis"]],
                verbose=True,
                allow_delegation=False,
                max_iter=3,
                llm=self.llm,
            )
        
        if not agents.get('community_manager'):
            agents['community_manager'] = Agent(
                role="社区经理",
                goal="管理社区互动，建立关系，提高 Dingo 项目的知名度和参与度",
                backstory="""
                你是一位热情的社区经理，专门负责开源项目的社区建设和用户关系管理。
                你擅长在 GitHub 上与用户互动，回应问题，参与讨论，并建立长期的社区关系。
                你的目标是让每个用户都感受到社区的温暖和专业。
                你能够根据任务要求使用不同语言进行社区分析和策略制定。
                """,
                tools=[tool for tool in self.tools if tool.name in ["github_interaction", "github_analysis"]],
                verbose=True,
                allow_delegation=False,
                max_iter=3,
                llm=self.llm,
            )
        
        if not agents.get('growth_strategist'):
            agents['growth_strategist'] = Agent(
                role="增长策略师",
                goal="制定和执行增长策略，协调团队工作，确保营销目标的实现",
                backstory="""
                你是一位资深的增长策略师，专门负责开源项目的增长策略制定和执行。
                你能够综合分析市场情报、用户行为和技术趋势，制定有效的增长计划。
                你擅长协调团队工作，将研究洞察转化为可执行的营销行动。
                你能够根据任务要求使用不同语言进行策略制定和团队协调，
                并在委派任务给团队成员时明确指定所需的语言。
                """,
                tools=[],  # Manager agent 不应该有工具
                verbose=True,
                allow_delegation=True,  # 只有策略师可以委派任务
                max_iter=5,
                llm=self.llm,
            )
        
        return agents
    
    def _create_task_from_config(self, task_key: str, task_config: Dict[str, Any], agent: Agent, **kwargs) -> Task:
        """从配置创建 Task"""
        description = task_config.get('description', '').format(**kwargs)
        expected_output = task_config.get('expected_output', '').format(**kwargs)
        
        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    def _create_crew(self) -> Crew:
        """创建团队"""
        # 使用分层流程，营销策略师作为管理者协调团队
        agents_list = [
            agent for key, agent in self.agents.items() 
            if key != 'growth_strategist'
        ]
        
        return Crew(
            agents=agents_list,
            tasks=[],  # 任务将在执行时动态创建
            process=Process.hierarchical,  # 使用分层流程
            manager_agent=self.agents["growth_strategist"],
            verbose=True,
        )

    # 新增市场研究功能
    async def conduct_market_analysis(self, product_name: str, product_info: str, target_audience: str, language: str = "zh") -> Dict[str, Any]:
        """进行市场分析"""
        logger.info(f"开始进行市场分析: {product_name}，使用语言: {language}")
        
        if 'market_analysis_task' not in self.tasks_config:
            logger.error("市场分析任务配置未找到")
            return {"error": "市场分析任务配置未找到"}
        
        # 选择合适的 agent
        agent = self.agents.get('market_intelligence_analyst') or self.agents.get('technical_research_specialist')
        if not agent:
            logger.error("未找到合适的市场研究分析师")
            return {"error": "未找到合适的市场研究分析师"}
        
        # 创建任务
        task = self._create_task_from_config(
            'market_analysis_task',
            self.tasks_config['market_analysis_task'],
            agent,
            product_name=product_name,
            product_info=product_info,
            target_audience=target_audience,
            language=language
        )
        
        # 创建临时 crew 执行任务
        temp_crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        try:
            result = temp_crew.kickoff()
            logger.info("市场分析完成")
            return {
                "success": True,
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"市场分析执行失败: {e}")
            return {"error": f"市场分析执行失败: {str(e)}"}
    
    async def analyze_competitors(self, product_name: str, product_info: str, competitors: List[str], language: str = "zh") -> Dict[str, Any]:
        """分析竞争对手"""
        logger.info(f"开始分析竞争对手: {competitors}，使用语言: {language}")
        
        if 'competitor_analysis_task' not in self.tasks_config:
            logger.error("竞品分析任务配置未找到")
            return {"error": "竞品分析任务配置未找到"}
        
        # 选择合适的 agent
        agent = self.agents.get('market_intelligence_analyst') or self.agents.get('technical_research_specialist')
        if not agent:
            logger.error("未找到合适的竞品情报专家")
            return {"error": "未找到合适的竞品情报专家"}
        
        # 创建任务
        task = self._create_task_from_config(
            'competitor_analysis_task',
            self.tasks_config['competitor_analysis_task'],
            agent,
            product_name=product_name,
            product_info=product_info,
            competitors=', '.join(competitors),
            language=language
        )
        
        # 创建临时 crew 执行任务
        temp_crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        try:
            result = temp_crew.kickoff()
            logger.info("竞品分析完成")
            return {
                "success": True,
                "analysis": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"竞品分析执行失败: {e}")
            return {"error": f"竞品分析执行失败: {str(e)}"}
    
    async def research_user_needs(self, product_name: str, product_info: str, target_audience: str, language: str = "zh") -> Dict[str, Any]:
        """研究用户需求"""
        logger.info(f"开始研究用户需求: {product_name}，使用语言: {language}")
        
        if 'user_research_task' not in self.tasks_config:
            logger.error("用户研究任务配置未找到")
            return {"error": "用户研究任务配置未找到"}
        
        # 选择合适的 agent
        agent = self.agents.get('user_behavior_analyst') or self.agents.get('technical_research_specialist')
        if not agent:
            logger.error("未找到合适的用户洞察研究员")
            return {"error": "未找到合适的用户洞察研究员"}
        
        # 创建任务
        task = self._create_task_from_config(
            'user_research_task',
            self.tasks_config['user_research_task'],
            agent,
            product_name=product_name,
            product_info=product_info,
            target_audience=target_audience,
            language=language
        )
        
        # 创建临时 crew 执行任务
        temp_crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        try:
            result = temp_crew.kickoff()
            logger.info("用户需求研究完成")
            return {
                "success": True,
                "research": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"用户需求研究执行失败: {e}")
            return {"error": f"用户需求研究执行失败: {str(e)}"}
    
    async def forecast_trends(self, product_name: str, product_info: str, focus_areas: List[str], language: str = "zh") -> Dict[str, Any]:
        """预测趋势"""
        logger.info(f"开始预测趋势: {focus_areas}，使用语言: {language}")
        
        if 'trend_analysis_task' not in self.tasks_config:
            logger.error("趋势分析任务配置未找到")
            return {"error": "趋势分析任务配置未找到"}
        
        # 选择合适的 agent
        agent = self.agents.get('market_intelligence_analyst') or self.agents.get('technical_research_specialist')
        if not agent:
            logger.error("未找到合适的趋势预测分析师")
            return {"error": "未找到合适的趋势预测分析师"}
        
        # 创建任务
        task = self._create_task_from_config(
            'trend_analysis_task',
            self.tasks_config['trend_analysis_task'],
            agent,
            product_name=product_name,
            product_info=product_info,
            focus_areas=', '.join(focus_areas),
            language=language
        )
        
        # 创建临时 crew 执行任务
        temp_crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )
        
        try:
            result = temp_crew.kickoff()
            logger.info("趋势预测完成")
            return {
                "success": True,
                "forecast": result,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"趋势预测执行失败: {e}")
            return {"error": f"趋势预测执行失败: {str(e)}"}

    async def analyze_target_users(self, user_list: List[str], language: str = "zh") -> Dict[str, Any]:
        """分析目标用户"""
        logger.info(f"开始分析 {len(user_list)} 个目标用户，使用语言: {language}")
        
        # 使用英文任务描述避免编码问题，但要求输出指定语言
        output_language = "Chinese" if language.lower() == "zh" else "English"
        
        task_description = f"""
        As a growth strategist, please coordinate the team to complete the following user analysis task:
        Target users: {', '.join(user_list)}
        Target project: {self.target_repository}
        
        **IMPORTANT: All analysis and reports must be in {output_language}. Ensure all team member tasks also output in {output_language}.**
        
        Please execute the following steps:
        
        Step 1 - Delegate technical analysis to technical research specialist:
        Guide the technical research specialist to use github_analysis tool to analyze each user:
        - analysis_type: "user"
        - username: [specific username]
        - lookback_days: 30
        
        Technical research specialist should focus on (report in {output_language}):
        1. User's technical background and programming language preferences
        2. Project contribution history and code quality
        3. Technical influence and expertise level
        4. Relevance to target project
        5. Activity and contribution frequency data
        
        Step 2 - Delegate community manager to develop interaction strategy:
        Based on technical research specialist's technical analysis results, guide community manager to develop (report in {output_language}):
        1. Analysis of each user's community participation patterns
        2. Personalized communication and interaction strategies
        3. Identification of potential collaboration opportunities
        4. Long-term relationship building plans
        
        Step 3 - Comprehensive analysis and recommendations:
        Integrate analysis results from both team members, provide (report in {output_language}):
        1. Complete user profiles
        2. Priority ranking recommendations
        3. Overall marketing strategy recommendations
        
        Please ensure team collaboration is reflected and clearly mark the responsible person and analysis perspective for each section.
        **Final report must be in {output_language}, ensuring all content is in {output_language}.**
        """
        
        expected_output = f"Complete user analysis report (in {output_language}) containing technical analysis, community strategy, and comprehensive recommendations, demonstrating team collaboration results"
        
        # 创建综合用户分析任务
        user_analysis_task = Task(
            description=task_description,
            agent=self.agents["growth_strategist"],
            expected_output=expected_output
        )
        
        # 执行任务
        self.crew.tasks = [user_analysis_task]
        result = self.crew.kickoff()
        
        logger.info("目标用户分析完成")
        return {"analysis_result": result, "analyzed_users": user_list}
    
    async def create_content_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """创建内容营销活动"""
        logger.info(f"开始创建内容营销活动: {campaign_config.get('name', '未命名活动')}")
        
        # 获取项目名称（从仓库地址中提取）
        project_name = self.target_repository.split('/')[-1] if self.target_repository else "目标项目"
        
        # 创建内容策略任务
        strategy_task = Task(
            description=f"""
            基于以下配置创建内容营销策略：
            活动名称: {campaign_config.get('name', '未命名活动')}
            目标项目: {self.target_repository}
            目标受众: {campaign_config.get('target_audience', '开发者')}
            主要主题: {campaign_config.get('topics', [f'{project_name} 工具使用'])}
            内容类型: {campaign_config.get('content_types', ['blog', 'social'])}
            活动周期: {campaign_config.get('duration', '1个月')}
            
            请制定详细的内容策略，包括：
            1. 内容日历和发布计划
            2. 每种内容类型的具体要求
            3. SEO 关键词策略
            4. 社交媒体推广策略
            """,
            agent=self.agents["growth_strategist"],
            expected_output="详细的内容营销策略和执行计划"
        )
        
        # 创建内容生成任务
        content_task = Task(
            description=f"""
            根据增长策略师的计划，创建以下内容：
            
            1. 为 {campaign_config.get('topics', [project_name])[0]} 主题创建一篇技术博客文章
            2. 创建 3-5 条社交媒体内容
            3. 创建一份邮件营销模板
            
            所有内容都应该：
            - 针对 {campaign_config.get('target_audience', '开发者')} 受众
            - 体现 {project_name} 工具的价值
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
        logger.info(f"开始执行社区互动活动，目标仓库: {self.target_repository}")
        
        # 获取语言设置
        language = engagement_config.get('language', 'zh')
        
        # 根据语言设置任务描述
        if language.lower() == "en":
            community_analysis_description = f"""
            Use GitHub analysis tool to analyze the current community status of the target project:
            
            Please use github_analysis tool with parameters:
            - analysis_type: "community"
            - repository: "{self.target_repository}"
            - lookback_days: {engagement_config.get('lookback_days', 30)}
            
            Analysis should include:
            1. Analyze GitHub community activity of {self.target_repository} project
            2. Identify active contributors and users
            3. Analyze recent issues and discussions
            4. Evaluate community health and engagement
            
            Based on analysis results, provide community interaction recommendations.
            
            Note:
            - Ensure using correct analysis type "community"
            - Use configured repository address "{self.target_repository}"
            - If repository access issues occur, check if repository address is correct
            """
            
            engagement_description = f"""
            Based on community analysis results, execute the following interaction activities:
            
            Use GitHub interaction tools to interact with target project community:
            - Target repository: {self.target_repository}
            - Interaction types: {engagement_config.get('interaction_types', ['comment', 'issue'])}
            - Target user count: {engagement_config.get('target_count', 10)}
            
            Specific tasks:
            1. Use github_interaction tool to reply to recent issues and discussions
            2. Interact with active users
            3. Share valuable technical content
            4. Invite users to participate in project contributions
            
            Tool parameter format:
            - repository: "{self.target_repository}"
            - interaction_type: "comment" or "issue"
            - content: [interaction content]
            - target_id: [issue or PR number, if commenting]
            
            Note:
            - Ensure all interactions are valuable and sincere
            - Use configured repository address "{self.target_repository}"
            - If permission issues occur, record and continue other interactions
            """
            
            community_expected_output = "Community status analysis report and interaction recommendations"
            engagement_expected_output = "Community interaction execution report, including specific interaction records"
        else:
            community_analysis_description = f"""
            使用 GitHub 分析工具分析目标项目的当前社区状态：
            
            请使用 github_analysis 工具，参数设置为：
            - analysis_type: "community"
            - repository: "{self.target_repository}"
            - lookback_days: {engagement_config.get('lookback_days', 30)}
            
            分析内容包括：
            1. 分析 {self.target_repository} 项目的 GitHub 社区活跃度
            2. 识别活跃的贡献者和用户
            3. 分析最近的 issues 和 discussions
            4. 评估社区健康度和参与度
            
            基于分析结果，提供社区互动建议。
            
            注意：
            - 请确保使用正确的分析类型 "community"
            - 使用配置的仓库地址 "{self.target_repository}"
            - 如果遇到仓库访问问题，请检查仓库地址是否正确
            """
            
            engagement_description = f"""
            基于社区分析结果，执行以下互动活动：
            
            使用 GitHub 互动工具与目标项目社区进行互动：
            - 目标仓库：{self.target_repository}
            - 互动类型: {engagement_config.get('interaction_types', ['comment', 'issue'])}
            - 目标用户数: {engagement_config.get('target_count', 10)}
            
            具体任务：
            1. 使用 github_interaction 工具回复最近的 issues 和讨论
            2. 与活跃用户进行互动
            3. 分享有价值的技术内容
            4. 邀请用户参与项目贡献
            
            工具参数格式：
            - repository: "{self.target_repository}"
            - interaction_type: "comment" 或 "issue"
            - content: [互动内容]
            - target_id: [issue或PR编号，如果是评论的话]
            
            注意：
            - 确保所有互动都是有价值和真诚的
            - 使用配置的仓库地址 "{self.target_repository}"
            - 如果遇到权限问题，请记录并继续其他互动
            """
            
            community_expected_output = "社区状态分析报告和互动建议"
            engagement_expected_output = "社区互动执行报告，包括具体的互动记录"
        
        # 创建社区分析任务
        community_analysis_task = Task(
            description=community_analysis_description,
            agent=self.agents["community_manager"],
            expected_output=community_expected_output
        )
        
        # 创建互动执行任务
        engagement_task = Task(
            description=engagement_description,
            agent=self.agents["community_manager"],
            expected_output=engagement_expected_output
        )
        
        # 执行任务
        self.crew.tasks = [community_analysis_task, engagement_task]
        result = self.crew.kickoff()
        
        logger.info("社区互动活动执行完成")
        return {"engagement_result": result, "config": engagement_config}
    
    async def run_comprehensive_campaign(self, campaign_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行综合营销活动"""
        logger.info("开始执行综合营销活动")
        
        # 获取语言设置
        language = campaign_config.get('language', 'zh')
        
        # 根据语言设置任务描述
        if language.lower() == "en":
            task_description = f"""
            Execute a comprehensive marketing campaign with the following phases:
            
            Phase 1: Data Analysis
            - Analyze target users: {campaign_config.get('target_users', [])}
            - Analyze target repositories: {campaign_config.get('target_repositories', [])}
            - Identify market opportunities and user needs
            
            Phase 2: Content Creation
            - Create content marketing materials based on analysis results
            - Generate blog posts, tutorials, and documentation
            - Develop social media content and promotional materials
            
            Phase 3: Community Interaction
            - Execute community engagement activities
            - Interact with target users and communities
            - Build relationships and increase brand awareness
            
            Phase 4: Effect Evaluation
            - Monitor campaign performance metrics
            - Analyze user engagement and conversion rates
            - Provide optimization recommendations
            
            Team Coordination:
            - Technical Research Specialist: Responsible for user and market analysis
            - Content Creator: Responsible for content creation and optimization
            - Community Manager: Responsible for community interaction and relationship building
            - Growth Strategist: Coordinate overall campaign execution and strategy optimization
            
            Expected Deliverables:
            1. Comprehensive market analysis report
            2. Content marketing strategy and materials
            3. Community engagement execution report
            4. Campaign performance evaluation and optimization recommendations
            
            Campaign Configuration:
            - Target users: {campaign_config.get('target_users', [])}
            - Target repositories: {campaign_config.get('target_repositories', [])}
            - Campaign duration: {campaign_config.get('duration', '30 days')}
            - Budget allocation: {campaign_config.get('budget', 'Standard')}
            - Success metrics: {campaign_config.get('metrics', ['engagement', 'conversion', 'awareness'])}
            """
            expected_output = "Comprehensive marketing campaign execution report with detailed results from all phases"
        else:
            task_description = f"""
            执行综合营销活动，包含以下阶段：
            
            第一阶段：数据分析
            - 分析目标用户：{campaign_config.get('target_users', [])}
            - 分析目标仓库：{campaign_config.get('target_repositories', [])}
            - 识别市场机会和用户需求
            
            第二阶段：内容创作
            - 基于分析结果创建内容营销素材
            - 生成博客文章、教程和文档
            - 开发社交媒体内容和推广材料
            
            第三阶段：社区互动
            - 执行社区参与活动
            - 与目标用户和社区进行互动
            - 建立关系并提高品牌知名度
            
            第四阶段：效果评估
            - 监控活动效果指标
            - 分析用户参与度和转化率
            - 提供优化建议
            
            团队协调：
            - 技术研究专家：负责用户和市场分析
            - 内容创作者：负责内容创作和优化
            - 社区管理员：负责社区互动和关系建设
            - 增长策略师：协调整体活动执行和策略优化
            
            预期交付物：
            1. 综合市场分析报告
            2. 内容营销策略和素材
            3. 社区参与执行报告
            4. 活动效果评估和优化建议
            
            活动配置：
            - 目标用户：{campaign_config.get('target_users', [])}
            - 目标仓库：{campaign_config.get('target_repositories', [])}
            - 活动周期：{campaign_config.get('duration', '30天')}
            - 预算分配：{campaign_config.get('budget', '标准')}
            - 成功指标：{campaign_config.get('metrics', ['参与度', '转化率', '知名度'])}
            """
            expected_output = "综合营销活动执行报告，包含各阶段详细结果"
        
        # 创建综合营销任务
        campaign_task = Task(
            description=task_description,
            agent=self.agents["growth_strategist"],
            expected_output=expected_output
        )
        
        # 执行任务
        self.crew.tasks = [campaign_task]
        result = self.crew.kickoff()
        
        logger.info("综合营销活动执行完成")
        return {"campaign_result": result, "config": campaign_config}
    
    def set_target_repository(self, repository: str) -> Dict[str, Any]:
        """设置目标仓库"""
        old_repository = self.target_repository
        self.target_repository = repository
        logger.info(f"目标仓库已从 {old_repository} 更改为 {repository}")
        
        return {
            "old_repository": old_repository,
            "new_repository": repository,
            "status": "success",
            "message": f"目标仓库已更新为 {repository}"
        }
    
    def get_target_repository(self) -> str:
        """获取当前目标仓库"""
        return self.target_repository

    def get_team_status(self) -> Dict[str, Any]:
        """获取团队状态"""
        return {
            "target_repository": self.target_repository,
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