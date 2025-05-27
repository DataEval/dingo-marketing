"""
内容生成相关的 AI Agent 工具
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from openai import AsyncOpenAI
from loguru import logger

from src.config.settings import settings


class ContentGenerationInput(BaseModel):
    """内容生成工具输入"""
    content_type: str = Field(description="内容类型: blog, social, email, tutorial, documentation")
    topic: str = Field(description="内容主题")
    target_audience: str = Field(description="目标受众")
    tone: str = Field(default="professional", description="语调: professional, casual, technical, friendly")
    length: str = Field(default="medium", description="长度: short, medium, long")
    language: str = Field(default="zh", description="语言: zh, en")
    keywords: Optional[List[str]] = Field(default=None, description="关键词列表")


class ContentOptimizationInput(BaseModel):
    """内容优化工具输入"""
    content: str = Field(description="原始内容")
    optimization_type: str = Field(description="优化类型: seo, engagement, readability, technical")
    target_platform: str = Field(description="目标平台: github, twitter, linkedin, blog")
    keywords: Optional[List[str]] = Field(default=None, description="SEO 关键词")


class ContentGenerationTool(BaseTool):
    """内容生成工具"""
    
    name: str = "content_generation"
    description: str = "生成各种类型的营销和技术内容"
    args_schema: type[BaseModel] = ContentGenerationInput
    
    def __init__(self):
        super().__init__()
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    def _run(self, content_type: str, topic: str, target_audience: str, 
             tone: str = "professional", length: str = "medium", 
             language: str = "zh", keywords: Optional[List[str]] = None) -> str:
        """生成内容"""
        try:
            return asyncio.run(self._generate_content_async(
                content_type, topic, target_audience, tone, length, language, keywords
            ))
        except Exception as e:
            logger.error(f"内容生成失败: {e}")
            return f"内容生成失败: {str(e)}"
    
    async def _generate_content_async(self, content_type: str, topic: str, 
                                    target_audience: str, tone: str, length: str, 
                                    language: str, keywords: Optional[List[str]]) -> str:
        """异步生成内容"""
        try:
            # 构建提示词
            prompt = self._build_content_prompt(
                content_type, topic, target_audience, tone, length, language, keywords
            )
            
            # 调用 OpenAI API
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt(content_type, language)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=self._get_max_tokens(length)
            )
            
            content = response.choices[0].message.content
            
            # 后处理
            processed_content = self._post_process_content(content, content_type, keywords)
            
            return f"✅ {content_type} 内容生成完成:\n\n{processed_content}"
            
        except Exception as e:
            return f"内容生成失败: {str(e)}"
    
    def _build_content_prompt(self, content_type: str, topic: str, target_audience: str,
                            tone: str, length: str, language: str, 
                            keywords: Optional[List[str]]) -> str:
        """构建内容生成提示词"""
        
        # 基础提示词模板
        base_prompts = {
            "blog": "写一篇关于 {topic} 的博客文章",
            "social": "创建关于 {topic} 的社交媒体内容",
            "email": "写一封关于 {topic} 的营销邮件",
            "tutorial": "创建关于 {topic} 的教程内容",
            "documentation": "编写关于 {topic} 的技术文档"
        }
        
        # 语调描述
        tone_descriptions = {
            "professional": "专业、正式",
            "casual": "轻松、随意",
            "technical": "技术性、详细",
            "friendly": "友好、亲切"
        }
        
        # 长度描述
        length_descriptions = {
            "short": "简短（200-300字）",
            "medium": "中等长度（500-800字）",
            "long": "详细（1000-1500字）"
        }
        
        prompt = base_prompts.get(content_type, "创建关于 {topic} 的内容").format(topic=topic)
        
        prompt += f"""

目标受众: {target_audience}
语调风格: {tone_descriptions.get(tone, tone)}
内容长度: {length_descriptions.get(length, length)}
语言: {'中文' if language == 'zh' else '英文'}
"""
        
        if keywords:
            prompt += f"\n关键词: {', '.join(keywords)}"
        
        # 添加特定类型的要求
        if content_type == "blog":
            prompt += "\n\n要求:\n- 包含引人入胜的标题\n- 结构清晰，有小标题\n- 包含实用的建议或见解\n- 适合 SEO 优化"
        elif content_type == "social":
            prompt += "\n\n要求:\n- 简洁有力\n- 包含相关话题标签\n- 鼓励互动\n- 适合社交媒体传播"
        elif content_type == "email":
            prompt += "\n\n要求:\n- 有吸引力的主题行\n- 个性化的开头\n- 清晰的行动号召\n- 专业的结尾"
        elif content_type == "tutorial":
            prompt += "\n\n要求:\n- 步骤清晰\n- 包含代码示例（如适用）\n- 易于理解\n- 包含常见问题解答"
        elif content_type == "documentation":
            prompt += "\n\n要求:\n- 结构化的格式\n- 详细的说明\n- 包含示例\n- 技术准确性"
        
        return prompt
    
    def _get_system_prompt(self, content_type: str, language: str) -> str:
        """获取系统提示词"""
        if language == "zh":
            base_prompt = "你是一个专业的内容创作专家，擅长创建高质量的营销和技术内容。"
        else:
            base_prompt = "You are a professional content creation expert, skilled at creating high-quality marketing and technical content."
        
        type_specific = {
            "blog": "专注于创建有价值、有见解的博客内容",
            "social": "专注于创建引人入胜的社交媒体内容",
            "email": "专注于创建有效的营销邮件",
            "tutorial": "专注于创建清晰易懂的教程",
            "documentation": "专注于创建准确详细的技术文档"
        }
        
        return f"{base_prompt} {type_specific.get(content_type, '')}"
    
    def _get_max_tokens(self, length: str) -> int:
        """根据长度获取最大 token 数"""
        token_limits = {
            "short": 500,
            "medium": 1000,
            "long": 2000
        }
        return token_limits.get(length, 1000)
    
    def _post_process_content(self, content: str, content_type: str, 
                            keywords: Optional[List[str]]) -> str:
        """后处理内容"""
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据内容类型添加特定格式
        if content_type == "social":
            # 确保社交媒体内容有适当的格式
            if not content.startswith("#"):
                content = f"🚀 {content}"
        elif content_type == "email":
            # 确保邮件有适当的格式
            if "主题:" not in content and "Subject:" not in content:
                lines = content.split('\n')
                content = f"主题: {lines[0]}\n\n" + '\n'.join(lines[1:])
        
        # 添加元数据
        metadata = f"\n\n---\n生成时间: {timestamp}\n内容类型: {content_type}"
        if keywords:
            metadata += f"\n关键词: {', '.join(keywords)}"
        
        return content + metadata


class ContentOptimizationTool(BaseTool):
    """内容优化工具"""
    
    name: str = "content_optimization"
    description: str = "优化现有内容以提高效果"
    args_schema: type[BaseModel] = ContentOptimizationInput
    
    def __init__(self):
        super().__init__()
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    def _run(self, content: str, optimization_type: str, target_platform: str,
             keywords: Optional[List[str]] = None) -> str:
        """优化内容"""
        try:
            return asyncio.run(self._optimize_content_async(
                content, optimization_type, target_platform, keywords
            ))
        except Exception as e:
            logger.error(f"内容优化失败: {e}")
            return f"内容优化失败: {str(e)}"
    
    async def _optimize_content_async(self, content: str, optimization_type: str,
                                    target_platform: str, keywords: Optional[List[str]]) -> str:
        """异步优化内容"""
        try:
            # 构建优化提示词
            prompt = self._build_optimization_prompt(
                content, optimization_type, target_platform, keywords
            )
            
            # 调用 OpenAI API
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_optimization_system_prompt(optimization_type)},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            optimized_content = response.choices[0].message.content
            
            return f"✅ 内容优化完成 ({optimization_type}):\n\n{optimized_content}"
            
        except Exception as e:
            return f"内容优化失败: {str(e)}"
    
    def _build_optimization_prompt(self, content: str, optimization_type: str,
                                 target_platform: str, keywords: Optional[List[str]]) -> str:
        """构建优化提示词"""
        
        optimization_instructions = {
            "seo": "优化以下内容以提高搜索引擎排名",
            "engagement": "优化以下内容以提高用户参与度",
            "readability": "优化以下内容以提高可读性",
            "technical": "优化以下内容以提高技术准确性"
        }
        
        platform_requirements = {
            "github": "适合 GitHub README 或文档格式",
            "twitter": "适合 Twitter 的字符限制和格式",
            "linkedin": "适合 LinkedIn 的专业风格",
            "blog": "适合博客文章的格式和结构"
        }
        
        prompt = f"{optimization_instructions.get(optimization_type, '优化以下内容')}，"
        prompt += f"使其{platform_requirements.get(target_platform, '更适合目标平台')}。\n\n"
        
        if keywords:
            prompt += f"重点关键词: {', '.join(keywords)}\n\n"
        
        prompt += f"原始内容:\n{content}\n\n"
        
        # 添加具体优化要求
        if optimization_type == "seo":
            prompt += "优化要求:\n- 自然地融入关键词\n- 优化标题和小标题\n- 改善内容结构\n- 增加相关性"
        elif optimization_type == "engagement":
            prompt += "优化要求:\n- 增加互动元素\n- 使用更吸引人的语言\n- 添加行动号召\n- 提高情感共鸣"
        elif optimization_type == "readability":
            prompt += "优化要求:\n- 简化复杂句子\n- 改善段落结构\n- 使用更清晰的表达\n- 增加可读性"
        elif optimization_type == "technical":
            prompt += "优化要求:\n- 确保技术准确性\n- 添加必要的技术细节\n- 改善代码示例\n- 增加技术深度"
        
        return prompt
    
    def _get_optimization_system_prompt(self, optimization_type: str) -> str:
        """获取优化系统提示词"""
        base_prompt = "你是一个专业的内容优化专家。"
        
        type_specific = {
            "seo": "专注于搜索引擎优化，提高内容的搜索排名。",
            "engagement": "专注于提高用户参与度和互动性。",
            "readability": "专注于提高内容的可读性和理解性。",
            "technical": "专注于提高技术内容的准确性和深度。"
        }
        
        return f"{base_prompt} {type_specific.get(optimization_type, '')}"


class ContentAnalysisTool(BaseTool):
    """内容分析工具"""
    
    name: str = "content_analysis"
    description: str = "分析内容的质量、SEO 效果和改进建议"
    args_schema: type[BaseModel] = ContentOptimizationInput
    
    def _run(self, content: str, optimization_type: str = "general", 
             target_platform: str = "general", keywords: Optional[List[str]] = None) -> str:
        """分析内容"""
        try:
            analysis_result = self._analyze_content(content, keywords)
            return f"✅ 内容分析完成:\n\n{analysis_result}"
        except Exception as e:
            logger.error(f"内容分析失败: {e}")
            return f"内容分析失败: {str(e)}"
    
    def _analyze_content(self, content: str, keywords: Optional[List[str]]) -> str:
        """分析内容质量"""
        analysis = []
        
        # 基本统计
        word_count = len(content.split())
        char_count = len(content)
        paragraph_count = len([p for p in content.split('\n\n') if p.strip()])
        
        analysis.append(f"📊 基本统计:")
        analysis.append(f"- 字数: {word_count}")
        analysis.append(f"- 字符数: {char_count}")
        analysis.append(f"- 段落数: {paragraph_count}")
        
        # 可读性分析
        avg_words_per_paragraph = word_count / max(paragraph_count, 1)
        analysis.append(f"\n📖 可读性分析:")
        analysis.append(f"- 平均每段字数: {avg_words_per_paragraph:.1f}")
        
        if avg_words_per_paragraph > 100:
            analysis.append("- 建议: 段落过长，建议分割")
        elif avg_words_per_paragraph < 20:
            analysis.append("- 建议: 段落过短，可以适当合并")
        else:
            analysis.append("- 段落长度适中")
        
        # 关键词分析
        if keywords:
            analysis.append(f"\n🔍 关键词分析:")
            for keyword in keywords:
                count = content.lower().count(keyword.lower())
                density = (count * len(keyword.split())) / word_count * 100
                analysis.append(f"- '{keyword}': 出现 {count} 次, 密度 {density:.1f}%")
                
                if density < 1:
                    analysis.append(f"  建议: 增加 '{keyword}' 的使用频率")
                elif density > 3:
                    analysis.append(f"  建议: 减少 '{keyword}' 的使用频率")
        
        # 结构分析
        analysis.append(f"\n🏗️ 结构分析:")
        has_headings = any(line.startswith('#') for line in content.split('\n'))
        has_lists = any(line.strip().startswith(('-', '*', '1.')) for line in content.split('\n'))
        
        analysis.append(f"- 包含标题: {'是' if has_headings else '否'}")
        analysis.append(f"- 包含列表: {'是' if has_lists else '否'}")
        
        if not has_headings:
            analysis.append("- 建议: 添加标题来改善结构")
        if not has_lists and word_count > 200:
            analysis.append("- 建议: 使用列表来提高可读性")
        
        # 总体评分
        score = 0
        if 200 <= word_count <= 1500:
            score += 25
        if 20 <= avg_words_per_paragraph <= 100:
            score += 25
        if has_headings:
            score += 25
        if has_lists:
            score += 25
        
        analysis.append(f"\n⭐ 总体评分: {score}/100")
        
        if score >= 80:
            analysis.append("- 内容质量优秀")
        elif score >= 60:
            analysis.append("- 内容质量良好，有改进空间")
        else:
            analysis.append("- 内容需要显著改进")
        
        return '\n'.join(analysis) 