"""
User data models for Dingo Marketing system.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile model."""
    
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., description="GitHub username")
    email: Optional[str] = Field(None, description="User email")
    name: Optional[str] = Field(None, description="User display name")
    bio: Optional[str] = Field(None, description="User bio")
    location: Optional[str] = Field(None, description="User location")
    company: Optional[str] = Field(None, description="User company")
    blog: Optional[str] = Field(None, description="User blog URL")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    
    # GitHub stats
    public_repos: int = Field(0, description="Number of public repositories")
    followers: int = Field(0, description="Number of followers")
    following: int = Field(0, description="Number of following")
    
    # Activity data
    languages: List[str] = Field(default_factory=list, description="Programming languages")
    topics: List[str] = Field(default_factory=list, description="Repository topics")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Profile creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserAnalysis(BaseModel):
    """User analysis results."""
    
    user_id: str = Field(..., description="User identifier")
    
    # Technical profile
    skill_level: str = Field(..., description="Skill level (beginner, intermediate, advanced)")
    primary_languages: List[str] = Field(default_factory=list, description="Primary programming languages")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks and technologies")
    domains: List[str] = Field(default_factory=list, description="Domain expertise")
    
    # Activity patterns
    activity_score: float = Field(0.0, description="Activity score (0-100)")
    contribution_frequency: str = Field("", description="Contribution frequency")
    preferred_project_types: List[str] = Field(default_factory=list, description="Preferred project types")
    
    # Interests and preferences
    interests: List[str] = Field(default_factory=list, description="Technical interests")
    learning_goals: List[str] = Field(default_factory=list, description="Learning goals")
    
    # Engagement metrics
    engagement_score: float = Field(0.0, description="Engagement score (0-100)")
    influence_score: float = Field(0.0, description="Influence score (0-100)")
    
    # Marketing insights
    marketing_segments: List[str] = Field(default_factory=list, description="Marketing segments")
    content_preferences: List[str] = Field(default_factory=list, description="Content preferences")
    communication_style: str = Field("", description="Preferred communication style")
    
    # Analysis metadata
    analysis_date: datetime = Field(default_factory=datetime.now, description="Analysis date")
    confidence_score: float = Field(0.0, description="Analysis confidence (0-100)")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UserInteraction(BaseModel):
    """User interaction record."""
    
    interaction_id: str = Field(..., description="Interaction identifier")
    user_id: str = Field(..., description="User identifier")
    interaction_type: str = Field(..., description="Type of interaction")
    content_id: Optional[str] = Field(None, description="Related content ID")
    
    # Interaction details
    action: str = Field(..., description="Action performed")
    context: Dict[str, Any] = Field(default_factory=dict, description="Interaction context")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.now, description="Interaction timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 