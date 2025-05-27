"""
Campaign data models for Dingo Marketing system.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Campaign(BaseModel):
    """Marketing campaign model."""
    
    campaign_id: str = Field(..., description="Unique campaign identifier")
    name: str = Field(..., description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    
    # Campaign configuration
    campaign_type: str = Field(..., description="Campaign type (awareness, engagement, conversion)")
    status: str = Field("draft", description="Campaign status")
    
    # Targeting
    target_audience: List[str] = Field(default_factory=list, description="Target audience segments")
    target_platforms: List[str] = Field(default_factory=list, description="Target platforms")
    target_locations: List[str] = Field(default_factory=list, description="Target locations")
    
    # Content
    content_items: List[str] = Field(default_factory=list, description="Content item IDs")
    messaging: Dict[str, str] = Field(default_factory=dict, description="Key messaging")
    
    # Budget and scheduling
    budget: Optional[float] = Field(None, description="Campaign budget")
    start_date: Optional[datetime] = Field(None, description="Campaign start date")
    end_date: Optional[datetime] = Field(None, description="Campaign end date")
    
    # Goals and KPIs
    goals: List[str] = Field(default_factory=list, description="Campaign goals")
    kpis: Dict[str, float] = Field(default_factory=dict, description="Key performance indicators")
    
    # Metadata
    created_by: Optional[str] = Field(None, description="Campaign creator")
    tags: List[str] = Field(default_factory=list, description="Campaign tags")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CampaignMetrics(BaseModel):
    """Campaign performance metrics."""
    
    campaign_id: str = Field(..., description="Campaign identifier")
    
    # Reach metrics
    impressions: int = Field(0, description="Total impressions")
    reach: int = Field(0, description="Unique reach")
    frequency: float = Field(0.0, description="Average frequency")
    
    # Engagement metrics
    clicks: int = Field(0, description="Total clicks")
    likes: int = Field(0, description="Total likes")
    shares: int = Field(0, description="Total shares")
    comments: int = Field(0, description="Total comments")
    saves: int = Field(0, description="Total saves")
    
    # Conversion metrics
    conversions: int = Field(0, description="Total conversions")
    conversion_rate: float = Field(0.0, description="Conversion rate (0-1)")
    cost_per_conversion: Optional[float] = Field(None, description="Cost per conversion")
    
    # Calculated metrics
    ctr: float = Field(0.0, description="Click-through rate (0-1)")
    engagement_rate: float = Field(0.0, description="Engagement rate (0-1)")
    roi: Optional[float] = Field(None, description="Return on investment")
    
    # Platform breakdown
    platform_metrics: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Platform-specific metrics"
    )
    
    # Time series data
    daily_metrics: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Daily metrics breakdown"
    )
    
    # Timestamps
    last_updated: datetime = Field(default_factory=datetime.now, description="Last metrics update")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CampaignTask(BaseModel):
    """Campaign task model."""
    
    task_id: str = Field(..., description="Task identifier")
    campaign_id: str = Field(..., description="Campaign identifier")
    
    # Task details
    task_type: str = Field(..., description="Task type")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    
    # Scheduling
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled execution time")
    executed_at: Optional[datetime] = Field(None, description="Actual execution time")
    
    # Status and results
    status: str = Field("pending", description="Task status")
    result: Optional[Dict[str, Any]] = Field(None, description="Task result")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Configuration
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    retry_count: int = Field(0, description="Number of retries")
    max_retries: int = Field(3, description="Maximum retries")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 