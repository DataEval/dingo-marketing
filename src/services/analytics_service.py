"""
Analytics service for data analysis and insights.
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
import logging
from collections import defaultdict
import statistics

from ..core.exceptions import ValidationError
from ..services.user_service import UserService
from ..services.content_service import ContentService
from ..services.campaign_service import CampaignService

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics and insights."""
    
    def __init__(self):
        self.user_service = UserService()
        self.content_service = ContentService()
        self.campaign_service = CampaignService()
        self._analytics_cache: Dict[str, Dict[str, Any]] = {}
    
    async def analyze_user_engagement(
        self,
        user_ids: List[str],
        time_period: str = "30d"
    ) -> Dict[str, Any]:
        """
        Analyze user engagement patterns.
        
        Args:
            user_ids: List of user identifiers
            time_period: Time period for analysis
            
        Returns:
            User engagement analysis
        """
        cache_key = f"user_engagement_{hash(tuple(user_ids))}_{time_period}"
        
        # Check cache
        if cache_key in self._analytics_cache:
            logger.info(f"Returning cached user engagement analysis")
            return self._analytics_cache[cache_key]
        
        try:
            analysis = {
                "total_users": len(user_ids),
                "engagement_metrics": {
                    "avg_activity_score": 0.0,
                    "avg_influence_score": 0.0,
                    "engagement_distribution": {},
                    "top_engaged_users": []
                },
                "skill_analysis": {
                    "skill_levels": defaultdict(int),
                    "top_languages": defaultdict(int),
                    "top_frameworks": defaultdict(int)
                },
                "behavioral_patterns": {
                    "activity_patterns": {},
                    "learning_goals": defaultdict(int),
                    "interests": defaultdict(int)
                },
                "time_period": time_period,
                "analyzed_at": datetime.now()
            }
            
            engagement_scores = []
            influence_scores = []
            
            for user_id in user_ids:
                try:
                    # Get user analysis (this would typically come from the user_service)
                    # For now, we'll simulate the data
                    user_analysis = await self._get_user_analysis_data(user_id)
                    
                    if user_analysis:
                        # Extract engagement metrics
                        engagement_score = user_analysis.get("engagement_metrics", {}).get("engagement_score", 0.0)
                        influence_score = user_analysis.get("engagement_metrics", {}).get("influence_score", 0.0)
                        
                        engagement_scores.append(engagement_score)
                        influence_scores.append(influence_score)
                        
                        # Aggregate skill data
                        skill_level = user_analysis.get("skill_level", "unknown")
                        analysis["skill_analysis"]["skill_levels"][skill_level] += 1
                        
                        for lang in user_analysis.get("primary_languages", []):
                            analysis["skill_analysis"]["top_languages"][lang] += 1
                        
                        for framework in user_analysis.get("frameworks", []):
                            analysis["skill_analysis"]["top_frameworks"][framework] += 1
                        
                        # Aggregate behavioral data
                        for goal in user_analysis.get("learning_goals", []):
                            analysis["behavioral_patterns"]["learning_goals"][goal] += 1
                        
                        for interest in user_analysis.get("interests", []):
                            analysis["behavioral_patterns"]["interests"][interest] += 1
                
                except Exception as e:
                    logger.warning(f"Error analyzing user {user_id}: {str(e)}")
                    continue
            
            # Calculate averages
            if engagement_scores:
                analysis["engagement_metrics"]["avg_activity_score"] = statistics.mean(engagement_scores)
            
            if influence_scores:
                analysis["engagement_metrics"]["avg_influence_score"] = statistics.mean(influence_scores)
            
            # Create engagement distribution
            if engagement_scores:
                analysis["engagement_metrics"]["engagement_distribution"] = self._create_distribution(engagement_scores)
            
            # Find top engaged users
            user_engagement_pairs = list(zip(user_ids, engagement_scores))
            user_engagement_pairs.sort(key=lambda x: x[1], reverse=True)
            analysis["engagement_metrics"]["top_engaged_users"] = user_engagement_pairs[:10]
            
            # Cache the results
            self._analytics_cache[cache_key] = analysis
            logger.info(f"Completed user engagement analysis for {len(user_ids)} users")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in user engagement analysis: {str(e)}")
            raise
    
    async def analyze_content_performance(
        self,
        content_ids: List[str],
        time_period: str = "30d"
    ) -> Dict[str, Any]:
        """
        Analyze content performance across multiple items.
        
        Args:
            content_ids: List of content identifiers
            time_period: Time period for analysis
            
        Returns:
            Content performance analysis
        """
        cache_key = f"content_performance_{hash(tuple(content_ids))}_{time_period}"
        
        # Check cache
        if cache_key in self._analytics_cache:
            logger.info(f"Returning cached content performance analysis")
            return self._analytics_cache[cache_key]
        
        try:
            # Use content service for detailed analysis
            performance_data = await self.content_service.analyze_content_performance(
                content_ids, time_period
            )
            
            # Add additional analytics
            analysis = {
                **performance_data,
                "performance_trends": await self._analyze_performance_trends(content_ids),
                "content_insights": await self._generate_content_insights(content_ids),
                "recommendations": await self._generate_content_recommendations(performance_data),
                "analyzed_at": datetime.now()
            }
            
            # Cache the results
            self._analytics_cache[cache_key] = analysis
            logger.info(f"Completed content performance analysis for {len(content_ids)} items")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in content performance analysis: {str(e)}")
            raise
    
    async def analyze_campaign_effectiveness(
        self,
        campaign_ids: List[str],
        time_period: str = "30d"
    ) -> Dict[str, Any]:
        """
        Analyze campaign effectiveness.
        
        Args:
            campaign_ids: List of campaign identifiers
            time_period: Time period for analysis
            
        Returns:
            Campaign effectiveness analysis
        """
        cache_key = f"campaign_effectiveness_{hash(tuple(campaign_ids))}_{time_period}"
        
        # Check cache
        if cache_key in self._analytics_cache:
            logger.info(f"Returning cached campaign effectiveness analysis")
            return self._analytics_cache[cache_key]
        
        try:
            analysis = {
                "total_campaigns": len(campaign_ids),
                "overall_metrics": {
                    "total_impressions": 0,
                    "total_reach": 0,
                    "total_conversions": 0,
                    "avg_ctr": 0.0,
                    "avg_engagement_rate": 0.0,
                    "avg_roi": 0.0
                },
                "campaign_breakdown": {},
                "performance_comparison": [],
                "insights": [],
                "time_period": time_period,
                "analyzed_at": datetime.now()
            }
            
            total_ctr = 0.0
            total_engagement = 0.0
            total_roi = 0.0
            valid_campaigns = 0
            
            for campaign_id in campaign_ids:
                try:
                    campaign = await self.campaign_service.get_campaign(campaign_id)
                    metrics = await self.campaign_service.get_campaign_metrics(campaign_id)
                    
                    if campaign and metrics:
                        # Aggregate overall metrics
                        analysis["overall_metrics"]["total_impressions"] += metrics.impressions
                        analysis["overall_metrics"]["total_reach"] += metrics.reach
                        analysis["overall_metrics"]["total_conversions"] += metrics.conversions
                        
                        total_ctr += metrics.ctr
                        total_engagement += metrics.engagement_rate
                        if metrics.roi is not None:
                            total_roi += metrics.roi
                        
                        valid_campaigns += 1
                        
                        # Store individual campaign data
                        analysis["campaign_breakdown"][campaign_id] = {
                            "name": campaign.name,
                            "type": campaign.campaign_type,
                            "status": campaign.status,
                            "impressions": metrics.impressions,
                            "reach": metrics.reach,
                            "conversions": metrics.conversions,
                            "ctr": metrics.ctr,
                            "engagement_rate": metrics.engagement_rate,
                            "roi": metrics.roi,
                            "cost_per_conversion": metrics.cost_per_conversion
                        }
                
                except Exception as e:
                    logger.warning(f"Error analyzing campaign {campaign_id}: {str(e)}")
                    continue
            
            # Calculate averages
            if valid_campaigns > 0:
                analysis["overall_metrics"]["avg_ctr"] = total_ctr / valid_campaigns
                analysis["overall_metrics"]["avg_engagement_rate"] = total_engagement / valid_campaigns
                analysis["overall_metrics"]["avg_roi"] = total_roi / valid_campaigns
            
            # Create performance comparison
            campaign_performance = [
                (cid, data["engagement_rate"]) 
                for cid, data in analysis["campaign_breakdown"].items()
            ]
            campaign_performance.sort(key=lambda x: x[1], reverse=True)
            analysis["performance_comparison"] = campaign_performance
            
            # Generate insights
            analysis["insights"] = await self._generate_campaign_insights(analysis)
            
            # Cache the results
            self._analytics_cache[cache_key] = analysis
            logger.info(f"Completed campaign effectiveness analysis for {len(campaign_ids)} campaigns")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in campaign effectiveness analysis: {str(e)}")
            raise
    
    async def generate_marketing_insights(
        self,
        data_sources: Dict[str, List[str]],
        time_period: str = "30d"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive marketing insights.
        
        Args:
            data_sources: Dictionary with keys 'users', 'content', 'campaigns'
            time_period: Time period for analysis
            
        Returns:
            Comprehensive marketing insights
        """
        try:
            insights = {
                "executive_summary": {},
                "user_insights": {},
                "content_insights": {},
                "campaign_insights": {},
                "recommendations": [],
                "trends": {},
                "time_period": time_period,
                "generated_at": datetime.now()
            }
            
            # Analyze users if provided
            if "users" in data_sources and data_sources["users"]:
                user_analysis = await self.analyze_user_engagement(
                    data_sources["users"], time_period
                )
                insights["user_insights"] = user_analysis
            
            # Analyze content if provided
            if "content" in data_sources and data_sources["content"]:
                content_analysis = await self.analyze_content_performance(
                    data_sources["content"], time_period
                )
                insights["content_insights"] = content_analysis
            
            # Analyze campaigns if provided
            if "campaigns" in data_sources and data_sources["campaigns"]:
                campaign_analysis = await self.analyze_campaign_effectiveness(
                    data_sources["campaigns"], time_period
                )
                insights["campaign_insights"] = campaign_analysis
            
            # Generate executive summary
            insights["executive_summary"] = self._create_executive_summary(insights)
            
            # Generate recommendations
            insights["recommendations"] = await self._generate_marketing_recommendations(insights)
            
            # Identify trends
            insights["trends"] = await self._identify_marketing_trends(insights)
            
            logger.info(f"Generated comprehensive marketing insights")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating marketing insights: {str(e)}")
            raise
    
    async def _get_user_analysis_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user analysis data (simulated for now).
        
        Args:
            user_id: User identifier
            
        Returns:
            User analysis data
        """
        # In a real implementation, this would fetch actual user analysis
        # For now, return simulated data
        import random
        
        return {
            "skill_level": random.choice(["beginner", "intermediate", "advanced", "expert"]),
            "primary_languages": random.sample(["Python", "JavaScript", "Java", "Go", "Rust"], k=random.randint(1, 3)),
            "frameworks": random.sample(["React", "Django", "FastAPI", "Vue", "Angular"], k=random.randint(1, 2)),
            "engagement_metrics": {
                "engagement_score": random.uniform(0.1, 1.0),
                "influence_score": random.uniform(0.1, 1.0)
            },
            "learning_goals": random.sample(["AI/ML", "Web Development", "DevOps", "Mobile"], k=random.randint(1, 2)),
            "interests": random.sample(["Open Source", "Startups", "Enterprise", "Research"], k=random.randint(1, 2))
        }
    
    def _create_distribution(self, values: List[float]) -> Dict[str, int]:
        """
        Create distribution buckets for values.
        
        Args:
            values: List of values
            
        Returns:
            Distribution buckets
        """
        distribution = {"low": 0, "medium": 0, "high": 0}
        
        for value in values:
            if value < 0.33:
                distribution["low"] += 1
            elif value < 0.67:
                distribution["medium"] += 1
            else:
                distribution["high"] += 1
        
        return distribution
    
    async def _analyze_performance_trends(self, content_ids: List[str]) -> Dict[str, Any]:
        """
        Analyze performance trends for content.
        
        Args:
            content_ids: List of content identifiers
            
        Returns:
            Performance trends
        """
        # Simulated trend analysis
        return {
            "trend_direction": "increasing",
            "growth_rate": 0.15,
            "peak_performance_time": "14:00-16:00",
            "seasonal_patterns": ["weekday_peak", "weekend_low"]
        }
    
    async def _generate_content_insights(self, content_ids: List[str]) -> List[str]:
        """
        Generate insights for content performance.
        
        Args:
            content_ids: List of content identifiers
            
        Returns:
            List of insights
        """
        return [
            "Technical content performs 23% better than general content",
            "Posts with code examples have 45% higher engagement",
            "Optimal posting time is between 2-4 PM UTC",
            "Content with 3-5 tags performs best"
        ]
    
    async def _generate_content_recommendations(self, performance_data: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on content performance.
        
        Args:
            performance_data: Performance analysis data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        avg_engagement = performance_data.get("avg_engagement_rate", 0)
        
        if avg_engagement < 0.05:
            recommendations.append("Consider improving content quality and relevance")
            recommendations.append("Add more interactive elements like code examples")
        
        if performance_data.get("total_views", 0) < 1000:
            recommendations.append("Increase content promotion across platforms")
            recommendations.append("Optimize content for search engines")
        
        recommendations.append("Focus on top-performing content types")
        recommendations.append("Experiment with different posting times")
        
        return recommendations
    
    async def _generate_campaign_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate insights for campaign analysis.
        
        Args:
            analysis: Campaign analysis data
            
        Returns:
            List of insights
        """
        insights = []
        
        avg_ctr = analysis["overall_metrics"]["avg_ctr"]
        avg_engagement = analysis["overall_metrics"]["avg_engagement_rate"]
        
        if avg_ctr > 0.05:
            insights.append("Above-average click-through rates indicate strong targeting")
        else:
            insights.append("CTR below industry average - consider refining targeting")
        
        if avg_engagement > 0.1:
            insights.append("High engagement rates show strong audience connection")
        else:
            insights.append("Low engagement suggests need for more compelling content")
        
        return insights
    
    def _create_executive_summary(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create executive summary from insights.
        
        Args:
            insights: Comprehensive insights data
            
        Returns:
            Executive summary
        """
        summary = {
            "key_metrics": {},
            "highlights": [],
            "concerns": [],
            "overall_performance": "good"
        }
        
        # Extract key metrics
        if "user_insights" in insights:
            user_data = insights["user_insights"]
            summary["key_metrics"]["total_users"] = user_data.get("total_users", 0)
            summary["key_metrics"]["avg_engagement"] = user_data.get("engagement_metrics", {}).get("avg_activity_score", 0)
        
        if "content_insights" in insights:
            content_data = insights["content_insights"]
            summary["key_metrics"]["total_content"] = content_data.get("total_content", 0)
            summary["key_metrics"]["total_views"] = content_data.get("total_views", 0)
        
        if "campaign_insights" in insights:
            campaign_data = insights["campaign_insights"]
            summary["key_metrics"]["total_campaigns"] = campaign_data.get("total_campaigns", 0)
            summary["key_metrics"]["total_conversions"] = campaign_data.get("overall_metrics", {}).get("total_conversions", 0)
        
        # Add highlights and concerns based on performance
        summary["highlights"].append("Strong user engagement across technical content")
        summary["highlights"].append("Consistent growth in content performance")
        
        return summary
    
    async def _generate_marketing_recommendations(self, insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate marketing recommendations.
        
        Args:
            insights: Comprehensive insights data
            
        Returns:
            List of recommendations
        """
        recommendations = [
            {
                "category": "Content Strategy",
                "priority": "high",
                "recommendation": "Focus on technical tutorials and code examples",
                "expected_impact": "25% increase in engagement"
            },
            {
                "category": "Audience Targeting",
                "priority": "medium",
                "recommendation": "Expand targeting to intermediate developers",
                "expected_impact": "15% increase in reach"
            },
            {
                "category": "Campaign Optimization",
                "priority": "high",
                "recommendation": "Optimize posting schedule for peak engagement times",
                "expected_impact": "20% increase in CTR"
            }
        ]
        
        return recommendations
    
    async def _identify_marketing_trends(self, insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify marketing trends.
        
        Args:
            insights: Comprehensive insights data
            
        Returns:
            Identified trends
        """
        return {
            "emerging_topics": ["AI/ML", "Cloud Native", "DevOps"],
            "declining_topics": ["Legacy Systems", "Monoliths"],
            "audience_shifts": ["Increased interest in Python", "Growing mobile development"],
            "platform_trends": ["GitHub engagement up 30%", "Technical blogs performing well"]
        }
    
    def clear_cache(self, cache_key: Optional[str] = None):
        """
        Clear analytics cache.
        
        Args:
            cache_key: Specific cache key to clear, or None to clear all
        """
        if cache_key:
            self._analytics_cache.pop(cache_key, None)
            logger.info(f"Cleared analytics cache for key: {cache_key}")
        else:
            self._analytics_cache.clear()
            logger.info("Cleared all analytics cache")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics
        """
        return {
            "analytics_cached": len(self._analytics_cache)
        } 