"""
增强的市场调研工具 - 集成网络搜索和网页抓取功能
"""

import asyncio
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai import LLM
from loguru import logger

from src.config.settings import settings


class WebSearchInput(BaseModel):
    """网络搜索输入参数"""
    query: str = Field(..., description="搜索查询")
    num_results: int = Field(default=10, description="返回结果数量")
    language: str = Field(default="zh", description="搜索语言")
    country: str = Field(default="cn", description="搜索国家")


class WebScrapeInput(BaseModel):
    """网页抓取输入参数"""
    url: str = Field(..., description="要抓取的网页URL")
    extract_type: str = Field(default="text", description="提取类型: text, links, images, structured")
    max_length: int = Field(default=5000, description="最大内容长度")


class MarketResearchInput(BaseModel):
    """市场调研输入参数"""
    research_type: str = Field(..., description="调研类型: competitor, market_trend, user_feedback, technology")
    target: str = Field(..., description="调研目标")
    depth: str = Field(default="medium", description="调研深度: shallow, medium, deep")
    language: str = Field(default="zh", description="报告语言")


class WebSearchTool(BaseTool):
    """网络搜索工具 - 基于Serper API"""
    
    name: str = "web_search"
    description: str = "使用Serper API进行网络搜索，获取最新信息"
    args_schema: type[BaseModel] = WebSearchInput
    
    def _run(self, query: str, num_results: int = 10, language: str = "zh", country: str = "cn") -> str:
        """执行网络搜索"""
        try:
            if not settings.SERPER_API_KEY:
                return "错误：未配置SERPER_API_KEY，无法进行网络搜索"
            
            # 构建搜索请求
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": settings.SERPER_API_KEY,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": query,
                "num": num_results,
                "gl": country,
                "hl": language
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # 解析搜索结果
            results = []
            if "organic" in data:
                for item in data["organic"]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "date": item.get("date", "")
                    })
            
            # 格式化返回结果
            formatted_results = f"搜索查询: {query}\n"
            formatted_results += f"找到 {len(results)} 个结果:\n\n"
            
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   链接: {result['link']}\n"
                formatted_results += f"   摘要: {result['snippet']}\n"
                if result['date']:
                    formatted_results += f"   日期: {result['date']}\n"
                formatted_results += "\n"
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"网络搜索失败: {e}")
            return f"搜索失败: {str(e)}"


class WebScrapeTool(BaseTool):
    """网页抓取工具"""
    
    name: str = "web_scrape"
    description: str = "抓取网页内容并提取有用信息"
    args_schema: type[BaseModel] = WebScrapeInput
    
    def _run(self, url: str, extract_type: str = "text", max_length: int = 5000) -> str:
        """执行网页抓取"""
        try:
            # 设置请求头
            headers = {
                "User-Agent": settings.SCRAPING_USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
            }
            
            # 发送请求
            response = requests.get(
                url, 
                headers=headers, 
                timeout=settings.SCRAPING_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            if extract_type == "text":
                return self._extract_text(soup, max_length)
            elif extract_type == "links":
                return self._extract_links(soup, url)
            elif extract_type == "images":
                return self._extract_images(soup, url)
            elif extract_type == "structured":
                return self._extract_structured(soup, max_length)
            else:
                return self._extract_text(soup, max_length)
                
        except Exception as e:
            logger.error(f"网页抓取失败: {e}")
            return f"抓取失败: {str(e)}"
    
    def _extract_text(self, soup: BeautifulSoup, max_length: int) -> str:
        """提取文本内容"""
        # 优先提取主要内容区域
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|main|article'))
        
        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            text = soup.get_text(separator='\n', strip=True)
        
        # 清理文本
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        clean_text = '\n'.join(lines)
        
        # 限制长度
        if len(clean_text) > max_length:
            clean_text = clean_text[:max_length] + "..."
        
        return clean_text
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> str:
        """提取链接"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            
            # 转换相对链接为绝对链接
            if href.startswith('/'):
                href = urljoin(base_url, href)
            elif not href.startswith(('http://', 'https://')):
                continue
            
            if text and href not in [link['url'] for link in links]:
                links.append({"text": text, "url": href})
        
        result = f"从 {base_url} 提取到 {len(links)} 个链接:\n\n"
        for i, link in enumerate(links[:20], 1):  # 限制显示数量
            result += f"{i}. {link['text']}\n   {link['url']}\n\n"
        
        return result
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> str:
        """提取图片"""
        images = []
        for img in soup.find_all('img', src=True):
            src = img['src']
            alt = img.get('alt', '')
            
            # 转换相对链接为绝对链接
            if src.startswith('/'):
                src = urljoin(base_url, src)
            elif not src.startswith(('http://', 'https://')):
                continue
            
            images.append({"alt": alt, "src": src})
        
        result = f"从 {base_url} 提取到 {len(images)} 个图片:\n\n"
        for i, img in enumerate(images[:10], 1):  # 限制显示数量
            result += f"{i}. {img['alt'] or '无描述'}\n   {img['src']}\n\n"
        
        return result
    
    def _extract_structured(self, soup: BeautifulSoup, max_length: int) -> str:
        """提取结构化内容"""
        result = []
        
        # 提取标题
        for i in range(1, 7):
            headers = soup.find_all(f'h{i}')
            if headers:
                result.append(f"H{i} 标题:")
                for h in headers[:5]:  # 限制数量
                    result.append(f"  - {h.get_text(strip=True)}")
                result.append("")
        
        # 提取列表
        lists = soup.find_all(['ul', 'ol'])
        if lists:
            result.append("列表内容:")
            for lst in lists[:3]:  # 限制数量
                items = lst.find_all('li')
                for item in items[:5]:  # 限制每个列表的项目数
                    result.append(f"  • {item.get_text(strip=True)}")
                result.append("")
        
        # 提取表格
        tables = soup.find_all('table')
        if tables:
            result.append("表格内容:")
            for table in tables[:2]:  # 限制数量
                rows = table.find_all('tr')
                for row in rows[:5]:  # 限制行数
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                    if cells:
                        result.append(f"  | {' | '.join(cells)} |")
                result.append("")
        
        structured_text = '\n'.join(result)
        
        # 限制长度
        if len(structured_text) > max_length:
            structured_text = structured_text[:max_length] + "..."
        
        return structured_text


class EnhancedMarketResearchTool(BaseTool):
    """增强的市场调研工具 - 集成网络搜索和网页抓取"""
    
    name: str = "enhanced_market_research"
    description: str = "使用网络搜索和网页抓取进行深度市场调研"
    args_schema: type[BaseModel] = MarketResearchInput
    
    def _run(self, research_type: str, target: str, depth: str = "medium", language: str = "zh") -> str:
        """执行增强的市场调研"""
        try:
            logger.info(f"开始{research_type}调研: {target}")
            
            # 在运行时创建工具实例
            search_tool = WebSearchTool()
            scrape_tool = WebScrapeTool()
            
            if research_type == "competitor":
                return self._research_competitor(target, depth, language, search_tool, scrape_tool)
            elif research_type == "market_trend":
                return self._research_market_trend(target, depth, language, search_tool, scrape_tool)
            elif research_type == "user_feedback":
                return self._research_user_feedback(target, depth, language, search_tool, scrape_tool)
            elif research_type == "technology":
                return self._research_technology(target, depth, language, search_tool, scrape_tool)
            else:
                return f"不支持的调研类型: {research_type}"
                
        except Exception as e:
            logger.error(f"市场调研失败: {e}")
            return f"调研失败: {str(e)}"
    
    def _research_competitor(self, competitor: str, depth: str, language: str, search_tool: WebSearchTool, scrape_tool: WebScrapeTool) -> str:
        """竞品调研"""
        results = []
        results.append(f"# {competitor} 竞品调研报告\n")
        results.append(f"调研时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 1. 基础信息搜索
        search_queries = [
            f"{competitor} 产品介绍",
            f"{competitor} 功能特性",
            f"{competitor} 定价策略",
            f"{competitor} 用户评价"
        ]
        
        if depth in ["medium", "deep"]:
            search_queries.extend([
                f"{competitor} 技术架构",
                f"{competitor} 市场份额",
                f"{competitor} 最新动态"
            ])
        
        for query in search_queries:
            search_result = search_tool._run(query, num_results=5, language=language)
            results.append(f"## 搜索: {query}\n")
            results.append(search_result)
            results.append("\n---\n")
        
        # 2. 深度分析（如果需要）
        if depth == "deep":
            # 尝试抓取官网信息
            official_sites = self._find_official_sites(competitor, search_tool)
            for site in official_sites[:2]:  # 限制数量
                scraped_content = scrape_tool._run(site, extract_type="structured", max_length=2000)
                results.append(f"## 官网内容分析: {site}\n")
                results.append(scraped_content)
                results.append("\n---\n")
        
        return '\n'.join(results)
    
    def _research_market_trend(self, market: str, depth: str, language: str, search_tool: WebSearchTool, scrape_tool: WebScrapeTool) -> str:
        """市场趋势调研"""
        results = []
        results.append(f"# {market} 市场趋势调研报告\n")
        results.append(f"调研时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 趋势搜索查询
        trend_queries = [
            f"{market} 市场趋势 2024",
            f"{market} 行业发展",
            f"{market} 技术发展趋势",
            f"{market} 市场规模"
        ]
        
        if depth in ["medium", "deep"]:
            trend_queries.extend([
                f"{market} 投资动态",
                f"{market} 新兴技术",
                f"{market} 用户需求变化"
            ])
        
        for query in trend_queries:
            search_result = search_tool._run(query, num_results=8, language=language)
            results.append(f"## 趋势分析: {query}\n")
            results.append(search_result)
            results.append("\n---\n")
        
        return '\n'.join(results)
    
    def _research_user_feedback(self, product: str, depth: str, language: str, search_tool: WebSearchTool, scrape_tool: WebScrapeTool) -> str:
        """用户反馈调研"""
        results = []
        results.append(f"# {product} 用户反馈调研报告\n")
        results.append(f"调研时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 用户反馈搜索
        feedback_queries = [
            f"{product} 用户评价",
            f"{product} 使用体验",
            f"{product} 优缺点",
            f"{product} 用户反馈"
        ]
        
        if depth in ["medium", "deep"]:
            feedback_queries.extend([
                f"{product} GitHub issues",
                f"{product} 社区讨论",
                f"{product} 用户案例"
            ])
        
        for query in feedback_queries:
            search_result = search_tool._run(query, num_results=6, language=language)
            results.append(f"## 用户反馈: {query}\n")
            results.append(search_result)
            results.append("\n---\n")
        
        return '\n'.join(results)
    
    def _research_technology(self, technology: str, depth: str, language: str, search_tool: WebSearchTool, scrape_tool: WebScrapeTool) -> str:
        """技术调研"""
        results = []
        results.append(f"# {technology} 技术调研报告\n")
        results.append(f"调研时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 技术搜索查询
        tech_queries = [
            f"{technology} 技术原理",
            f"{technology} 实现方案",
            f"{technology} 最佳实践",
            f"{technology} 性能对比"
        ]
        
        if depth in ["medium", "deep"]:
            tech_queries.extend([
                f"{technology} 开源项目",
                f"{technology} 技术文档",
                f"{technology} 案例研究"
            ])
        
        for query in tech_queries:
            search_result = search_tool._run(query, num_results=6, language=language)
            results.append(f"## 技术分析: {query}\n")
            results.append(search_result)
            results.append("\n---\n")
        
        return '\n'.join(results)
    
    def _find_official_sites(self, company: str, search_tool: WebSearchTool) -> List[str]:
        """查找官方网站"""
        search_result = search_tool._run(f"{company} 官网", num_results=3)
        
        # 简单的URL提取（实际应用中可能需要更复杂的逻辑）
        urls = []
        lines = search_result.split('\n')
        for line in lines:
            if 'https://' in line or 'http://' in line:
                # 提取URL
                import re
                url_pattern = r'https?://[^\s]+'
                matches = re.findall(url_pattern, line)
                urls.extend(matches)
        
        return list(set(urls))  # 去重 