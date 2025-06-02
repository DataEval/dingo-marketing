"""
内容生成和优化工具
"""

import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai import LLM
from loguru import logger

from src.config.settings import settings


class ContentGenerationInput(BaseModel):
    """内容生成输入参数"""
    content_type: str = Field(..., description="内容类型: blog, social, email, tutorial")
    topic: str = Field(..., description="内容主题")
    target_audience: str = Field(default="开发者", description="目标受众")
    tone: str = Field(default="专业", description="内容语调: 专业, 友好, 幽默, 正式")
    length: str = Field(default="medium", description="内容长度: short, medium, long")
    language: str = Field(default="中文", description="内容语言")
    keywords: Optional[str] = Field(default="", description="关键词，逗号分隔")


class ContentOptimizationInput(BaseModel):
    """内容优化输入参数"""
    content: str = Field(..., description="原始内容")
    optimization_type: str = Field(default="seo", description="优化类型: seo, readability, engagement")
    target_audience: str = Field(default="开发者", description="目标受众")
    keywords: Optional[str] = Field(default="", description="SEO关键词")


def get_global_llm() -> LLM:
    """获取全局配置的 LLM 实例"""
    ai_config = settings.get_ai_config()
    return LLM(
        model=ai_config["model"],
        api_key=ai_config["api_key"],
        base_url=ai_config["base_url"],
        max_tokens=ai_config["max_tokens"],
        temperature=ai_config["temperature"]
    )


class ContentGenerationTool(BaseTool):
    """内容生成工具"""
    name: str = "content_generation"
    description: str = "生成高质量的技术内容，包括博客文章、社交媒体内容、邮件模板等"
    
    def _run(
        self,
        content_type: str,
        topic: str,
        target_audience: str = "开发者",
        tone: str = "专业",
        length: str = "medium",
        language: str = "中文",
        keywords: str = ""
    ) -> str:
        """执行内容生成"""
        try:
            # 构建提示词
            prompt = self._build_generation_prompt(
                content_type, topic, target_audience, tone, length, language, keywords
            )
            
            # 使用全局 LLM 生成内容
            llm = get_global_llm()
            
            # 同步调用 LLM
            result = asyncio.create_task(self._generate_content_async(llm, prompt))
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果事件循环正在运行，使用 run_coroutine_threadsafe
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._generate_content_async(llm, prompt))
                    return future.result()
            else:
                return loop.run_until_complete(self._generate_content_async(llm, prompt))
                
        except Exception as e:
            logger.error(f"内容生成失败: {e}")
            return f"内容生成失败: {str(e)}"
    
    async def _generate_content_async(self, llm: LLM, prompt: str) -> str:
        """异步生成内容"""
        try:
            response = llm.call(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return f"内容生成失败: {str(e)}"
    
    def _build_generation_prompt(
        self, content_type: str, topic: str, target_audience: str, 
        tone: str, length: str, language: str, keywords: str
    ) -> str:
        """构建内容生成提示词"""
        
        # 内容类型特定的指导
        type_guidance = {
            "blog": "创建一篇结构清晰的技术博客文章，包含引言、主体内容和结论",
            "social": "创建适合社交媒体的简洁有趣内容，包含话题标签",
            "email": "创建专业的邮件内容，包含主题行和正文",
            "tutorial": "创建详细的教程内容，包含步骤说明和代码示例"
        }
        
        # 长度指导
        length_guidance = {
            "short": "简洁明了，200-500字",
            "medium": "适中篇幅，500-1000字", 
            "long": "详细深入，1000-2000字"
        }
        
        prompt = f"""
作为一位专业的{target_audience}内容创作者，请为以下主题创建{content_type}内容：

主题: {topic}
目标受众: {target_audience}
语调: {tone}
长度要求: {length_guidance.get(length, "适中篇幅")}
语言: {language}
关键词: {keywords if keywords else "无特定要求"}

内容要求:
{type_guidance.get(content_type, "创建高质量的内容")}

请确保内容：
1. 针对{target_audience}的知识水平和兴趣
2. 采用{tone}的语调
3. 包含实用价值和见解
4. 结构清晰，易于阅读
5. 如有关键词要求，自然融入内容中

请直接输出内容，不需要额外说明：
"""
        return prompt


class ContentOptimizationTool(BaseTool):
    """内容优化工具"""
    name: str = "content_optimization"
    description: str = "优化现有内容的SEO、可读性和参与度"
    
    def _run(
        self,
        content: str,
        optimization_type: str = "seo",
        target_audience: str = "开发者",
        keywords: str = ""
    ) -> str:
        """执行内容优化"""
        try:
            prompt = self._build_optimization_prompt(content, optimization_type, target_audience, keywords)
            
            # 使用全局 LLM 优化内容
            llm = get_global_llm()
            
            # 同步调用
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._optimize_content_async(llm, prompt))
                    return future.result()
            else:
                return loop.run_until_complete(self._optimize_content_async(llm, prompt))
                
        except Exception as e:
            logger.error(f"内容优化失败: {e}")
            return f"内容优化失败: {str(e)}"
    
    async def _optimize_content_async(self, llm: LLM, prompt: str) -> str:
        """异步优化内容"""
        try:
            response = llm.call(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return f"内容优化失败: {str(e)}"
    
    def _build_optimization_prompt(self, content: str, optimization_type: str, target_audience: str, keywords: str) -> str:
        """构建内容优化提示词"""
        
        optimization_guidance = {
            "seo": "优化搜索引擎排名，合理使用关键词，改善标题和元描述",
            "readability": "提高可读性，优化段落结构，使用清晰的标题和列表",
            "engagement": "增强用户参与度，添加互动元素，使内容更有吸引力"
        }
        
        prompt = f"""
请对以下内容进行{optimization_type}优化：

原始内容:
{content}

优化目标: {optimization_guidance.get(optimization_type, "全面优化")}
目标受众: {target_audience}
关键词: {keywords if keywords else "无特定要求"}

优化要求:
1. 保持原始内容的核心信息和价值
2. 针对{target_audience}进行优化
3. 根据{optimization_type}优化重点进行改进
4. 如有关键词要求，自然融入内容中
5. 提供具体的优化建议

请输出优化后的内容和优化说明：
"""
        return prompt


class ContentAnalysisTool(BaseTool):
    """内容分析工具"""
    name: str = "content_analysis"
    description: str = "分析内容质量、SEO效果和用户参与度"
    
    def _run(self, content: str, analysis_type: str = "comprehensive") -> str:
        """执行内容分析"""
        try:
            prompt = self._build_analysis_prompt(content, analysis_type)
            
            # 使用全局 LLM 分析内容
            llm = get_global_llm()
            
            # 同步调用
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._analyze_content_async(llm, prompt))
                    return future.result()
            else:
                return loop.run_until_complete(self._analyze_content_async(llm, prompt))
                
        except Exception as e:
            logger.error(f"内容分析失败: {e}")
            return f"内容分析失败: {str(e)}"
    
    async def _analyze_content_async(self, llm: LLM, prompt: str) -> str:
        """异步分析内容"""
        try:
            response = llm.call(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            return f"内容分析失败: {str(e)}"
    
    def _build_analysis_prompt(self, content: str, analysis_type: str) -> str:
        """构建内容分析提示词"""
        
        prompt = f"""
请对以下内容进行{analysis_type}分析：

内容:
{content}

分析维度:
1. 内容质量评估 (1-10分)
   - 信息准确性
   - 逻辑结构
   - 语言表达
   
2. SEO 效果分析
   - 关键词密度
   - 标题优化
   - 内容结构
   
3. 用户参与度预测
   - 内容吸引力
   - 互动潜力
   - 分享价值
   
4. 改进建议
   - 具体优化点
   - 实施建议
   - 预期效果

请提供详细的分析报告：
"""
        return prompt 