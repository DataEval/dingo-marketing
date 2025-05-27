"""
Campaign service for managing marketing campaigns.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
import uuid

from ..core.exceptions import ValidationError, NotFoundError
from ..models.campaign import Campaign, CampaignMetrics, CampaignTask
from ..services.content_service import ContentService
from ..services.user_service import UserService

logger = logging.getLogger(__name__)


class CampaignService:
    """Service for campaign-related operations."""
    
    def __init__(self):
        self.content_service = ContentService()
        self.user_service = UserService()
        self._campaigns_cache: Dict[str, Campaign] = {}
        self._metrics_cache: Dict[str, CampaignMetrics] = {}
        self._tasks_cache: Dict[str, List[CampaignTask]] = {}
    
    async def create_campaign(
        self,
        name: str,
        campaign_type: str,
        target_audience: List[str],
        description: Optional[str] = None,
        budget: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Campaign:
        """
        Create a new marketing campaign.
        
        Args:
            name: Campaign name
            campaign_type: Type of campaign
            target_audience: Target audience segments
            description: Campaign description
            budget: Campaign budget
            start_date: Campaign start date
            end_date: Campaign end date
            
        Returns:
            Campaign object
            
        Raises:
            ValidationError: If parameters are invalid
        """
        if not name or not campaign_type or not target_audience:
            raise ValidationError("Name, campaign type, and target audience are required")
        
        if start_date and end_date and start_date >= end_date:
            raise ValidationError("Start date must be before end date")
        
        campaign_id = str(uuid.uuid4())
        
        try:
            campaign = Campaign(
                campaign_id=campaign_id,
                name=name,
                description=description,
                campaign_type=campaign_type,
                status="draft",
                target_audience=target_audience,
                budget=budget,
                start_date=start_date,
                end_date=end_date,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Cache the campaign
            self._campaigns_cache[campaign_id] = campaign
            logger.info(f"Created campaign: {campaign_id}")
            
            return campaign
            
        except Exception as e:
            logger.error(f"Error creating campaign: {str(e)}")
            raise
    
    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """
        Get campaign by ID.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Campaign object or None
        """
        # Check cache first
        if campaign_id in self._campaigns_cache:
            return self._campaigns_cache[campaign_id]
        
        # In a real implementation, this would query a database
        logger.warning(f"Campaign not found in cache: {campaign_id}")
        return None
    
    async def update_campaign(
        self,
        campaign_id: str,
        updates: Dict[str, Any]
    ) -> Campaign:
        """
        Update campaign details.
        
        Args:
            campaign_id: Campaign identifier
            updates: Fields to update
            
        Returns:
            Updated Campaign object
            
        Raises:
            NotFoundError: If campaign not found
        """
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise NotFoundError(f"Campaign not found: {campaign_id}")
        
        try:
            # Update allowed fields
            allowed_fields = {
                "name", "description", "status", "target_audience", 
                "target_platforms", "budget", "start_date", "end_date",
                "goals", "kpis", "tags"
            }
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(campaign, field):
                    setattr(campaign, field, value)
            
            campaign.updated_at = datetime.now()
            
            # Update cache
            self._campaigns_cache[campaign_id] = campaign
            logger.info(f"Updated campaign: {campaign_id}")
            
            return campaign
            
        except Exception as e:
            logger.error(f"Error updating campaign {campaign_id}: {str(e)}")
            raise
    
    async def launch_campaign(self, campaign_id: str) -> bool:
        """
        Launch a campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Success status
            
        Raises:
            NotFoundError: If campaign not found
            ValidationError: If campaign cannot be launched
        """
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise NotFoundError(f"Campaign not found: {campaign_id}")
        
        if campaign.status != "draft":
            raise ValidationError(f"Campaign must be in draft status to launch")
        
        if not campaign.content_items:
            raise ValidationError("Campaign must have content items to launch")
        
        try:
            # Update campaign status
            await self.update_campaign(campaign_id, {
                "status": "active",
                "start_date": campaign.start_date or datetime.now()
            })
            
            # Create campaign tasks
            await self._create_campaign_tasks(campaign_id)
            
            logger.info(f"Launched campaign: {campaign_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error launching campaign {campaign_id}: {str(e)}")
            return False
    
    async def pause_campaign(self, campaign_id: str) -> bool:
        """
        Pause a running campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Success status
        """
        try:
            await self.update_campaign(campaign_id, {"status": "paused"})
            logger.info(f"Paused campaign: {campaign_id}")
            return True
        except Exception as e:
            logger.error(f"Error pausing campaign {campaign_id}: {str(e)}")
            return False
    
    async def stop_campaign(self, campaign_id: str) -> bool:
        """
        Stop a campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            Success status
        """
        try:
            await self.update_campaign(campaign_id, {
                "status": "stopped",
                "end_date": datetime.now()
            })
            logger.info(f"Stopped campaign: {campaign_id}")
            return True
        except Exception as e:
            logger.error(f"Error stopping campaign {campaign_id}: {str(e)}")
            return False
    
    async def add_content_to_campaign(
        self,
        campaign_id: str,
        content_id: str
    ) -> bool:
        """
        Add content item to campaign.
        
        Args:
            campaign_id: Campaign identifier
            content_id: Content identifier
            
        Returns:
            Success status
        """
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            raise NotFoundError(f"Campaign not found: {campaign_id}")
        
        try:
            if content_id not in campaign.content_items:
                campaign.content_items.append(content_id)
                campaign.updated_at = datetime.now()
                
                # Update cache
                self._campaigns_cache[campaign_id] = campaign
                logger.info(f"Added content {content_id} to campaign {campaign_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding content to campaign: {str(e)}")
            return False
    
    async def get_campaign_metrics(self, campaign_id: str) -> Optional[CampaignMetrics]:
        """
        Get campaign performance metrics.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            CampaignMetrics object or None
        """
        # Check cache first
        if campaign_id in self._metrics_cache:
            return self._metrics_cache[campaign_id]
        
        # In a real implementation, this would aggregate metrics from various sources
        logger.warning(f"Campaign metrics not found in cache: {campaign_id}")
        return None
    
    async def update_campaign_metrics(
        self,
        campaign_id: str,
        metrics_data: Dict[str, Any]
    ) -> CampaignMetrics:
        """
        Update campaign metrics.
        
        Args:
            campaign_id: Campaign identifier
            metrics_data: Metrics data
            
        Returns:
            CampaignMetrics object
        """
        try:
            metrics = CampaignMetrics(
                campaign_id=campaign_id,
                impressions=metrics_data.get("impressions", 0),
                reach=metrics_data.get("reach", 0),
                frequency=metrics_data.get("frequency", 0.0),
                clicks=metrics_data.get("clicks", 0),
                likes=metrics_data.get("likes", 0),
                shares=metrics_data.get("shares", 0),
                comments=metrics_data.get("comments", 0),
                saves=metrics_data.get("saves", 0),
                conversions=metrics_data.get("conversions", 0),
                conversion_rate=metrics_data.get("conversion_rate", 0.0),
                cost_per_conversion=metrics_data.get("cost_per_conversion"),
                ctr=metrics_data.get("ctr", 0.0),
                engagement_rate=metrics_data.get("engagement_rate", 0.0),
                roi=metrics_data.get("roi"),
                platform_metrics=metrics_data.get("platform_metrics", {}),
                daily_metrics=metrics_data.get("daily_metrics", []),
                last_updated=datetime.now()
            )
            
            # Cache the metrics
            self._metrics_cache[campaign_id] = metrics
            logger.info(f"Updated metrics for campaign: {campaign_id}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error updating campaign metrics for {campaign_id}: {str(e)}")
            raise
    
    async def _create_campaign_tasks(self, campaign_id: str):
        """
        Create tasks for a campaign.
        
        Args:
            campaign_id: Campaign identifier
        """
        campaign = await self.get_campaign(campaign_id)
        if not campaign:
            return
        
        tasks = []
        
        # Create content publishing tasks
        for content_id in campaign.content_items:
            task = CampaignTask(
                task_id=str(uuid.uuid4()),
                campaign_id=campaign_id,
                task_type="publish_content",
                title=f"Publish content {content_id}",
                description=f"Publish content item {content_id} for campaign {campaign.name}",
                scheduled_at=campaign.start_date,
                parameters={"content_id": content_id},
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            tasks.append(task)
        
        # Create metrics collection task
        metrics_task = CampaignTask(
            task_id=str(uuid.uuid4()),
            campaign_id=campaign_id,
            task_type="collect_metrics",
            title="Collect campaign metrics",
            description=f"Collect performance metrics for campaign {campaign.name}",
            scheduled_at=campaign.start_date + timedelta(hours=1) if campaign.start_date else datetime.now() + timedelta(hours=1),
            parameters={"frequency": "hourly"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        tasks.append(metrics_task)
        
        # Cache tasks
        self._tasks_cache[campaign_id] = tasks
        logger.info(f"Created {len(tasks)} tasks for campaign: {campaign_id}")
    
    async def get_campaign_tasks(self, campaign_id: str) -> List[CampaignTask]:
        """
        Get tasks for a campaign.
        
        Args:
            campaign_id: Campaign identifier
            
        Returns:
            List of CampaignTask objects
        """
        return self._tasks_cache.get(campaign_id, [])
    
    async def list_campaigns(
        self,
        status: Optional[str] = None,
        campaign_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Campaign]:
        """
        List campaigns with optional filters.
        
        Args:
            status: Filter by status
            campaign_type: Filter by campaign type
            limit: Maximum number of campaigns to return
            
        Returns:
            List of Campaign objects
        """
        campaigns = list(self._campaigns_cache.values())
        
        # Apply filters
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        
        if campaign_type:
            campaigns = [c for c in campaigns if c.campaign_type == campaign_type]
        
        # Sort by creation date (newest first)
        campaigns.sort(key=lambda x: x.created_at, reverse=True)
        
        return campaigns[:limit]
    
    def clear_cache(self, campaign_id: Optional[str] = None):
        """
        Clear campaign cache.
        
        Args:
            campaign_id: Specific campaign ID to clear, or None to clear all
        """
        if campaign_id:
            self._campaigns_cache.pop(campaign_id, None)
            self._metrics_cache.pop(campaign_id, None)
            self._tasks_cache.pop(campaign_id, None)
            logger.info(f"Cleared cache for campaign: {campaign_id}")
        else:
            self._campaigns_cache.clear()
            self._metrics_cache.clear()
            self._tasks_cache.clear()
            logger.info("Cleared all campaign cache")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics
        """
        return {
            "campaigns_cached": len(self._campaigns_cache),
            "metrics_cached": len(self._metrics_cache),
            "tasks_cached": sum(len(tasks) for tasks in self._tasks_cache.values())
        } 