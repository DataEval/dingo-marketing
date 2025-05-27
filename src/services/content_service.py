"""
Content service for managing content generation and metrics.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import uuid

from ..core.exceptions import ValidationError, APIError
from ..models.content import ContentItem, ContentMetrics, ContentGeneration
from ..tools.content_tools import ContentTools
from ..tools.content_analyzer import ContentAnalyzer

logger = logging.getLogger(__name__)


class ContentService:
    """Service for content-related operations."""
    
    def __init__(self):
        self.content_tools = ContentTools()
        self.content_analyzer = ContentAnalyzer()
        self._content_cache: Dict[str, ContentItem] = {}
        self._metrics_cache: Dict[str, ContentMetrics] = {}
    
    async def generate_content(
        self,
        content_type: str,
        target_audience: List[str],
        topic: str,
        tone: str = "professional",
        length: str = "medium",
        keywords: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> ContentGeneration:
        """
        Generate content using AI.
        
        Args:
            content_type: Type of content (blog, social, email, etc.)
            target_audience: Target audience segments
            topic: Content topic
            tone: Content tone
            length: Content length
            keywords: Optional keywords to include
            context: Additional context for generation
            
        Returns:
            ContentGeneration object
            
        Raises:
            ValidationError: If parameters are invalid
            APIError: If content generation fails
        """
        if not content_type or not target_audience or not topic:
            raise ValidationError("Content type, target audience, and topic are required")
        
        generation_id = str(uuid.uuid4())
        
        try:
            # Prepare generation request
            generation_request = {
                "content_type": content_type,
                "target_audience": target_audience,
                "topic": topic,
                "tone": tone,
                "length": length,
                "keywords": keywords or [],
                "context": context or {}
            }
            
            logger.info(f"Generating content: {generation_id}")
            start_time = datetime.now()
            
            # Generate content using content tools
            result = await self.content_tools.generate_content(generation_request)
            
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            
            if not result or not result.get("content"):
                raise APIError("Content generation failed - no content returned")
            
            # Create ContentGeneration object
            generation = ContentGeneration(
                generation_id=generation_id,
                content_type=content_type,
                target_audience=target_audience,
                topic=topic,
                tone=tone,
                length=length,
                keywords=keywords or [],
                context=context or {},
                generated_content=result.get("content"),
                alternatives=result.get("alternatives", []),
                model_used=result.get("model", "unknown"),
                generation_time=generation_time,
                quality_score=result.get("quality_score", 0.8),
                status="completed",
                requested_at=start_time,
                completed_at=end_time
            )
            
            logger.info(f"Content generation completed: {generation_id}")
            return generation
            
        except Exception as e:
            logger.error(f"Error generating content {generation_id}: {str(e)}")
            
            # Return failed generation
            return ContentGeneration(
                generation_id=generation_id,
                content_type=content_type,
                target_audience=target_audience,
                topic=topic,
                tone=tone,
                length=length,
                keywords=keywords or [],
                context=context or {},
                status="failed",
                error_message=str(e),
                requested_at=datetime.now()
            )
    
    async def create_content_item(
        self,
        title: str,
        content: str,
        content_type: str,
        target_audience: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        tags: Optional[List[str]] = None
    ) -> ContentItem:
        """
        Create a new content item.
        
        Args:
            title: Content title
            content: Content text
            content_type: Type of content
            target_audience: Target audience segments
            keywords: Content keywords
            tags: Content tags
            
        Returns:
            ContentItem object
        """
        if not title or not content or not content_type:
            raise ValidationError("Title, content, and content type are required")
        
        content_id = str(uuid.uuid4())
        
        try:
            # Analyze content to extract additional metadata
            analysis = await self.content_analyzer.analyze_content(content)
            
            # Create content item
            item = ContentItem(
                content_id=content_id,
                title=title,
                content_type=content_type,
                content=content,
                summary=analysis.get("summary"),
                keywords=keywords or analysis.get("keywords", []),
                tags=tags or [],
                categories=analysis.get("categories", []),
                target_audience=target_audience or [],
                target_platforms=[],
                author="system",
                status="draft",
                language=analysis.get("language", "en"),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Cache the content item
            self._content_cache[content_id] = item
            logger.info(f"Created content item: {content_id}")
            
            return item
            
        except Exception as e:
            logger.error(f"Error creating content item: {str(e)}")
            raise
    
    async def get_content_item(self, content_id: str) -> Optional[ContentItem]:
        """
        Get content item by ID.
        
        Args:
            content_id: Content identifier
            
        Returns:
            ContentItem object or None
        """
        # Check cache first
        if content_id in self._content_cache:
            return self._content_cache[content_id]
        
        # In a real implementation, this would query a database
        logger.warning(f"Content item not found in cache: {content_id}")
        return None
    
    async def update_content_metrics(
        self,
        content_id: str,
        metrics_data: Dict[str, Any]
    ) -> ContentMetrics:
        """
        Update content performance metrics.
        
        Args:
            content_id: Content identifier
            metrics_data: Metrics data
            
        Returns:
            ContentMetrics object
        """
        try:
            # Create or update metrics
            metrics = ContentMetrics(
                content_id=content_id,
                views=metrics_data.get("views", 0),
                unique_views=metrics_data.get("unique_views", 0),
                avg_time_on_page=metrics_data.get("avg_time_on_page", 0.0),
                bounce_rate=metrics_data.get("bounce_rate", 0.0),
                likes=metrics_data.get("likes", 0),
                shares=metrics_data.get("shares", 0),
                comments=metrics_data.get("comments", 0),
                saves=metrics_data.get("saves", 0),
                clicks=metrics_data.get("clicks", 0),
                conversions=metrics_data.get("conversions", 0),
                conversion_rate=metrics_data.get("conversion_rate", 0.0),
                engagement_rate=metrics_data.get("engagement_rate", 0.0),
                viral_coefficient=metrics_data.get("viral_coefficient", 0.0),
                platform_metrics=metrics_data.get("platform_metrics", {}),
                last_updated=datetime.now()
            )
            
            # Cache the metrics
            self._metrics_cache[content_id] = metrics
            logger.info(f"Updated metrics for content: {content_id}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error updating content metrics for {content_id}: {str(e)}")
            raise
    
    async def get_content_metrics(self, content_id: str) -> Optional[ContentMetrics]:
        """
        Get content metrics by content ID.
        
        Args:
            content_id: Content identifier
            
        Returns:
            ContentMetrics object or None
        """
        # Check cache first
        if content_id in self._metrics_cache:
            return self._metrics_cache[content_id]
        
        # In a real implementation, this would query a database
        logger.warning(f"Content metrics not found in cache: {content_id}")
        return None
    
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
            Performance analysis results
        """
        try:
            analysis_results = {
                "total_content": len(content_ids),
                "total_views": 0,
                "total_engagement": 0,
                "avg_engagement_rate": 0.0,
                "top_performing": [],
                "content_breakdown": {}
            }
            
            total_engagement_rate = 0.0
            valid_metrics_count = 0
            
            for content_id in content_ids:
                metrics = await self.get_content_metrics(content_id)
                if metrics:
                    analysis_results["total_views"] += metrics.views
                    analysis_results["total_engagement"] += (
                        metrics.likes + metrics.shares + metrics.comments
                    )
                    total_engagement_rate += metrics.engagement_rate
                    valid_metrics_count += 1
                    
                    analysis_results["content_breakdown"][content_id] = {
                        "views": metrics.views,
                        "engagement_rate": metrics.engagement_rate,
                        "conversions": metrics.conversions
                    }
            
            if valid_metrics_count > 0:
                analysis_results["avg_engagement_rate"] = total_engagement_rate / valid_metrics_count
            
            # Sort by engagement rate to find top performing
            sorted_content = sorted(
                analysis_results["content_breakdown"].items(),
                key=lambda x: x[1]["engagement_rate"],
                reverse=True
            )
            analysis_results["top_performing"] = sorted_content[:5]
            
            logger.info(f"Analyzed performance for {len(content_ids)} content items")
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing content performance: {str(e)}")
            raise
    
    def clear_cache(self, content_id: Optional[str] = None):
        """
        Clear content cache.
        
        Args:
            content_id: Specific content ID to clear, or None to clear all
        """
        if content_id:
            self._content_cache.pop(content_id, None)
            self._metrics_cache.pop(content_id, None)
            logger.info(f"Cleared cache for content: {content_id}")
        else:
            self._content_cache.clear()
            self._metrics_cache.clear()
            logger.info("Cleared all content cache")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics
        """
        return {
            "content_items_cached": len(self._content_cache),
            "metrics_cached": len(self._metrics_cache)
        }