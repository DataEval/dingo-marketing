"""
Content data models for Dingo Marketing system.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class ContentItem(BaseModel):
    """Content item model."""
    
    content_id: str = Field(..., description="Unique content identifier")
    title: str = Field(..., description="Content title")
    content_type: str = Field(..., description="Content type (blog, social, email, etc.)")
    
    # Content data
    content: str = Field(..., description="Main content text")
    summary: Optional[str] = Field(None, description="Content summary")
    keywords: List[str] = Field(default_factory=list, description="Content keywords")
    tags: List[str] = Field(default_factory=list, description="Content tags")
    categories: List[str] = Field(default_factory=list, description="Content categories")
    
    # Targeting
    target_audience: List[str] = Field(default_factory=list, description="Target audience segments")
    target_platforms: List[str] = Field(default_factory=list, description="Target platforms")
    
    # Metadata
    author: Optional[str] = Field(None, description="Content author")
    status: str = Field("draft", description="Content status")
    language: str = Field("en", description="Content language")
    
    # URLs and media
    url: Optional[str] = Field(None, description="Content URL")
    image_url: Optional[str] = Field(None, description="Featured image URL")
    media_urls: List[str] = Field(default_factory=list, description="Additional media URLs")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    published_at: Optional[datetime] = Field(None, description="Publication time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContentMetrics(BaseModel):
    """Content performance metrics."""
    
    content_id: str = Field(..., description="Content identifier")
    
    # View metrics
    views: int = Field(0, description="Total views")
    unique_views: int = Field(0, description="Unique views")
    avg_time_on_page: float = Field(0.0, description="Average time on page (seconds)")
    bounce_rate: float = Field(0.0, description="Bounce rate (0-1)")
    
    # Engagement metrics
    likes: int = Field(0, description="Number of likes")
    shares: int = Field(0, description="Number of shares")
    comments: int = Field(0, description="Number of comments")
    saves: int = Field(0, description="Number of saves/bookmarks")
    
    # Conversion metrics
    clicks: int = Field(0, description="Number of clicks")
    conversions: int = Field(0, description="Number of conversions")
    conversion_rate: float = Field(0.0, description="Conversion rate (0-1)")
    
    # Calculated metrics
    engagement_rate: float = Field(0.0, description="Engagement rate (0-1)")
    viral_coefficient: float = Field(0.0, description="Viral coefficient")
    
    # Platform-specific metrics
    platform_metrics: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Platform-specific metrics"
    )
    
    # Timestamps
    last_updated: datetime = Field(default_factory=datetime.now, description="Last metrics update")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContentGeneration(BaseModel):
    """Content generation request and result."""
    
    generation_id: str = Field(..., description="Generation identifier")
    
    # Request parameters
    content_type: str = Field(..., description="Type of content to generate")
    target_audience: str = Field(..., description="Target audience description")
    topic: str = Field(..., description="Content topic")
    tone: str = Field("professional", description="Content tone")
    length: str = Field("medium", description="Content length (short, medium, long)")
    
    # Additional parameters
    keywords: List[str] = Field(default_factory=list, description="Keywords to include")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    
    # Generation results
    generated_content: Optional[str] = Field(None, description="Generated content")
    alternatives: List[str] = Field(default_factory=list, description="Alternative versions")
    
    # Metadata
    model_used: Optional[str] = Field(None, description="AI model used")
    generation_time: Optional[float] = Field(None, description="Generation time (seconds)")
    quality_score: Optional[float] = Field(None, description="Quality score (0-100)")
    
    # Status
    status: str = Field("pending", description="Generation status")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Timestamps
    requested_at: datetime = Field(default_factory=datetime.now, description="Request time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 