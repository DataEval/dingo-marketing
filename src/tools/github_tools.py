"""
GitHub 相关的 AI Agent 工具
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta, timezone

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, model_validator
from github import Github
from loguru import logger

from src.config.settings import settings


class GitHubAnalysisInput(BaseModel):
    """GitHub 分析工具输入"""
    username: Optional[str] = Field(None, description="GitHub 用户名")
    repository: Optional[str] = Field(None, description="仓库名称 (格式: owner/repo)")
    analysis_type: str = Field(description="分析类型: user, repo, community")
    lookback_days: int = Field(default=30, description="回溯天数")


class GitHubInteractionInput(BaseModel):
    """GitHub 互动工具输入"""
    repository: str = Field(description="目标仓库 (格式: owner/repo)")
    interaction_type: str = Field(description="互动类型: comment, issue, pr")
    content: str = Field(description="互动内容")
    target_id: Optional[int] = Field(None, description="目标 ID (issue/pr 编号)")


class GitHubAnalysisTool(BaseTool):
    """GitHub 分析工具"""
    
    name: str = "github_analysis"
    description: str = "分析 GitHub 用户、仓库或社区的数据和行为模式"
    args_schema: type[BaseModel] = GitHubAnalysisInput
    github: Optional[Github] = Field(default=None, exclude=True)
    
    def model_post_init(self, __context: Any) -> None:
        """初始化 GitHub 客户端"""
        super().model_post_init(__context)
        if not self.github:
            self.github = Github(settings.GITHUB_TOKEN)
    
    def _run(self, username: Optional[str] = None, repository: Optional[str] = None, 
             analysis_type: str = "user", lookback_days: int = 30) -> str:
        """执行 GitHub 分析"""
        try:
            if analysis_type == "user" and username:
                return self._analyze_user(username, lookback_days)
            elif analysis_type == "repo" and repository:
                return self._analyze_repository(repository, lookback_days)
            elif analysis_type == "community":
                return self._analyze_community(lookback_days)
            else:
                return "错误：缺少必要参数或分析类型不支持"
        except Exception as e:
            logger.error(f"GitHub 分析失败: {e}")
            return f"分析失败: {str(e)}"
    
    def _analyze_user(self, username: str, lookback_days: int) -> str:
        """分析用户"""
        try:
            user = self.github.get_user(username)
            
            # 基本信息
            user_info = {
                "username": user.login,
                "name": user.name,
                "bio": user.bio,
                "company": user.company,
                "location": user.location,
                "followers": user.followers,
                "following": user.following,
                "public_repos": user.public_repos,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            
            # 分析仓库
            try:
                repos = list(user.get_repos()[:20])  # 限制数量
            except Exception as e:
                logger.warning(f"获取用户仓库失败: {e}")
                repos = []
            
            repo_analysis = {
                "total_repos": len(repos),
                "total_stars": sum(repo.stargazers_count for repo in repos if repo.stargazers_count),
                "languages": {},
                "topics": [],
            }
            
            # 统计编程语言
            for repo in repos:
                try:
                    if repo.language:
                        repo_analysis["languages"][repo.language] = \
                            repo_analysis["languages"].get(repo.language, 0) + 1
                    # 安全获取topics
                    try:
                        topics = repo.get_topics()
                        repo_analysis["topics"].extend(topics)
                    except Exception:
                        pass  # 忽略topics获取失败
                except Exception as e:
                    logger.warning(f"处理仓库 {repo.name} 失败: {e}")
                    continue
            
            # 分析最近活动
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=lookback_days)
            recent_events = []
            
            try:
                for event in user.get_events()[:50]:
                    try:
                        # 确保 event.created_at 有时区信息
                        event_created_at = event.created_at
                        if event_created_at.tzinfo is None:
                            event_created_at = event_created_at.replace(tzinfo=timezone.utc)
                        
                        if event_created_at >= cutoff_date:
                            recent_events.append({
                                "type": event.type,
                                "repo": event.repo.name if event.repo else None,
                                "created_at": event.created_at.isoformat() if event.created_at else None
                            })
                    except Exception:
                        continue  # 跳过有问题的事件
            except Exception as e:
                logger.warning(f"获取用户事件失败: {e}")
                recent_events = []
            
            # 计算活跃度分数
            activity_score = min(len(recent_events) * 2, 100)
            influence_score = min((user.followers * 0.1 + repo_analysis["total_stars"] * 0.05), 100)
            
            # 安全获取主要编程语言
            main_languages = list(repo_analysis['languages'].keys())[:3] if repo_analysis['languages'] else ["未知"]
            
            analysis_result = {
                "user_info": user_info,
                "repository_analysis": repo_analysis,
                "recent_activity": {
                    "events_count": len(recent_events),
                    "activity_score": activity_score,
                    "events": recent_events[:10]  # 只返回前10个事件
                },
                "scores": {
                    "activity_score": activity_score,
                    "influence_score": influence_score,
                    "overall_score": (activity_score + influence_score) / 2
                },
                "recommendations": self._generate_user_recommendations(user_info, repo_analysis, activity_score)
            }
            
            return f"用户 {username} 分析完成:\n" + \
                   f"- 影响力分数: {influence_score:.1f}/100\n" + \
                   f"- 活跃度分数: {activity_score:.1f}/100\n" + \
                   f"- 主要编程语言: {', '.join(main_languages)}\n" + \
                   f"- 总星标数: {repo_analysis['total_stars']}\n" + \
                   f"- 关注者数: {user.followers}\n" + \
                   f"- 推荐策略: {analysis_result['recommendations']}"
            
        except Exception as e:
            logger.error(f"用户分析失败: {e}")
            return f"用户分析失败: {str(e)}"
    
    def _analyze_repository(self, repository: str, lookback_days: int) -> str:
        """分析仓库"""
        try:
            repo = self.github.get_repo(repository)
            
            # 基本信息
            repo_info = {
                "name": repo.name,
                "description": repo.description,
                "language": repo.language,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "open_issues": repo.open_issues_count,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
            }
            
            # 分析贡献者
            contributors = list(repo.get_contributors()[:20])
            contributor_analysis = {
                "total_contributors": len(contributors),
                "top_contributors": [
                    {"login": c.login, "contributions": c.contributions}
                    for c in contributors[:5]
                ]
            }
            
            # 分析最近活动
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=lookback_days)
            recent_issues = []
            recent_prs = []
            
            try:
                for issue in repo.get_issues(state="all", since=cutoff_date)[:20]:
                    recent_issues.append({
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "user": issue.user.login,
                        "created_at": issue.created_at.isoformat()
                    })
            except Exception as e:
                logger.warning(f"获取issues失败: {e}")
            
            try:
                for pr in repo.get_pulls(state="all")[:10]:
                    # 确保 pr.created_at 有时区信息，如果没有则假设为 UTC
                    pr_created_at = pr.created_at
                    if pr_created_at.tzinfo is None:
                        pr_created_at = pr_created_at.replace(tzinfo=timezone.utc)
                    
                    if pr_created_at >= cutoff_date:
                        recent_prs.append({
                            "number": pr.number,
                            "title": pr.title,
                            "state": pr.state,
                            "user": pr.user.login,
                            "created_at": pr.created_at.isoformat()
                        })
            except Exception as e:
                logger.warning(f"获取PRs失败: {e}")
            
            # 计算活跃度
            activity_score = min((len(recent_issues) + len(recent_prs)) * 5, 100)
            popularity_score = min(repo.stargazers_count / 100 * 10, 100)
            
            return f"仓库 {repository} 分析完成:\n" + \
                   f"- 星标数: {repo.stargazers_count}\n" + \
                   f"- 分叉数: {repo.forks_count}\n" + \
                   f"- 贡献者数: {len(contributors)}\n" + \
                   f"- 最近 {lookback_days} 天活动: {len(recent_issues)} 个 issues, {len(recent_prs)} 个 PRs\n" + \
                   f"- 活跃度分数: {activity_score:.1f}/100\n" + \
                   f"- 受欢迎程度: {popularity_score:.1f}/100"
            
        except Exception as e:
            return f"仓库分析失败: {str(e)}"
    
    def _analyze_community(self, lookback_days: int) -> str:
        """分析 Dingo 社区"""
        try:
            # 检查GITHUB_REPOSITORY配置
            if not settings.GITHUB_REPOSITORY:
                return "社区分析失败: 未配置GITHUB_REPOSITORY"
            
            # 分析 Dingo 仓库
            dingo_repo = self.github.get_repo(settings.GITHUB_REPOSITORY)
            
            # 获取相关用户
            try:
                stargazers = list(dingo_repo.get_stargazers()[:50])
            except Exception as e:
                logger.warning(f"获取stargazers失败: {e}")
                stargazers = []
            
            try:
                contributors = list(dingo_repo.get_contributors()[:20])
            except Exception as e:
                logger.warning(f"获取contributors失败: {e}")
                contributors = []
            
            # 分析用户特征
            user_analysis = {
                "total_stargazers": dingo_repo.stargazers_count,
                "total_contributors": len(contributors),
                "user_locations": {},
                "user_companies": {},
                "common_languages": {},
            }
            
            # 分析用户分布
            for user in stargazers[:20]:  # 限制分析数量
                try:
                    user_detail = self.github.get_user(user.login)
                    if user_detail.location:
                        loc = user_detail.location
                        user_analysis["user_locations"][loc] = \
                            user_analysis["user_locations"].get(loc, 0) + 1
                    if user_detail.company:
                        comp = user_detail.company
                        user_analysis["user_companies"][comp] = \
                            user_analysis["user_companies"].get(comp, 0) + 1
                except Exception:
                    continue
            
            # 分析最近趋势
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=lookback_days)
            recent_activity = {
                "new_stars": 0,
                "new_issues": 0,
                "new_prs": 0,
            }
            
            # 安全获取主要地区和公司
            main_locations = list(user_analysis['user_locations'].keys())[:3] if user_analysis['user_locations'] else ["未知"]
            main_companies = list(user_analysis['user_companies'].keys())[:3] if user_analysis['user_companies'] else ["未知"]
            
            return f"Dingo 社区分析完成:\n" + \
                   f"- 总星标数: {user_analysis['total_stargazers']}\n" + \
                   f"- 贡献者数: {user_analysis['total_contributors']}\n" + \
                   f"- 主要地区: {', '.join(main_locations)}\n" + \
                   f"- 主要公司: {', '.join(main_companies)}\n" + \
                   f"- 社区活跃度: 中等"
            
        except Exception as e:
            logger.error(f"社区分析失败: {e}")
            return f"社区分析失败: {str(e)}"
    
    def _generate_user_recommendations(self, user_info: Dict, repo_analysis: Dict, activity_score: float) -> str:
        """生成用户推荐策略"""
        recommendations = []
        
        # 基于活跃度的推荐
        if activity_score > 70:
            recommendations.append("高活跃用户，适合直接互动")
        elif activity_score > 30:
            recommendations.append("中等活跃用户，可以通过有价值的内容吸引")
        else:
            recommendations.append("低活跃用户，需要特别有吸引力的内容")
        
        # 基于技术栈的推荐
        languages = list(repo_analysis.get("languages", {}).keys())
        if "Python" in languages:
            recommendations.append("Python 开发者，对 Dingo 工具可能有兴趣")
        if "Jupyter Notebook" in languages:
            recommendations.append("数据科学背景，是理想的目标用户")
        
        # 基于影响力的推荐
        if user_info.get("followers", 0) > 100:
            recommendations.append("有一定影响力，值得重点关注")
        
        return "; ".join(recommendations)


class GitHubInteractionTool(BaseTool):
    """GitHub 互动工具"""
    
    name: str = "github_interaction"
    description: str = "在 GitHub 上进行互动，如评论、创建 issue 等"
    args_schema: type[BaseModel] = GitHubInteractionInput
    github: Optional[Github] = Field(default=None, exclude=True)
    
    def model_post_init(self, __context: Any) -> None:
        """初始化 GitHub 客户端"""
        super().model_post_init(__context)
        if not self.github:
            self.github = Github(settings.GITHUB_TOKEN)
    
    def _run(self, repository: str, interaction_type: str, content: str, 
             target_id: Optional[int] = None) -> str:
        """执行 GitHub 互动"""
        try:
            repo = self.github.get_repo(repository)
            
            if interaction_type == "comment" and target_id:
                return self._add_comment(repo, target_id, content)
            elif interaction_type == "issue":
                return self._create_issue(repo, content)
            elif interaction_type == "star":
                return self._star_repository(repo)
            else:
                return "错误：不支持的互动类型或缺少必要参数"
                
        except Exception as e:
            logger.error(f"GitHub 互动失败: {e}")
            return f"互动失败: {str(e)}"
    
    def _add_comment(self, repo, issue_number: int, content: str) -> str:
        """添加评论"""
        try:
            issue = repo.get_issue(issue_number)
            
            # 检查是否已经评论过
            comments = list(issue.get_comments())
            current_user = self.github.get_user()
            
            for comment in comments:
                if comment.user.login == current_user.login:
                    return f"已经在 issue #{issue_number} 中评论过了"
            
            # 添加评论
            comment = issue.create_comment(content)
            return f"成功在 {repo.full_name} 的 issue #{issue_number} 中添加评论"
            
        except Exception as e:
            return f"添加评论失败: {str(e)}"
    
    def _create_issue(self, repo, content: str) -> str:
        """创建 issue"""
        try:
            # 解析内容，提取标题和正文
            lines = content.split('\n', 1)
            title = lines[0].replace('# ', '').strip()
            body = lines[1] if len(lines) > 1 else ""
            
            issue = repo.create_issue(title=title, body=body)
            return f"成功在 {repo.full_name} 中创建 issue #{issue.number}: {title}"
            
        except Exception as e:
            return f"创建 issue 失败: {str(e)}"
    
    def _star_repository(self, repo) -> str:
        """给仓库加星"""
        try:
            current_user = self.github.get_user()
            current_user.add_to_starred(repo)
            return f"成功给 {repo.full_name} 加星"
            
        except Exception as e:
            return f"加星失败: {str(e)}" 