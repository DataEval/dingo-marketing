"""
User service for managing user profiles and analysis.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from ..core.exceptions import NotFoundError, ValidationError
from ..models.user import UserProfile, UserAnalysis, UserInteraction
from ..tools.github_tools import GitHubTools
from ..tools.user_profiler import UserProfiler

logger = logging.getLogger(__name__)


class UserService:
    """Service for user-related operations."""
    
    def __init__(self):
        self.github_tools = GitHubTools()
        self.user_profiler = UserProfiler()
        self._user_cache: Dict[str, UserProfile] = {}
        self._analysis_cache: Dict[str, UserAnalysis] = {}
    
    async def get_user_profile(self, username: str, force_refresh: bool = False) -> UserProfile:
        """
        Get user profile from GitHub.
        
        Args:
            username: GitHub username
            force_refresh: Force refresh from GitHub API
            
        Returns:
            UserProfile object
            
        Raises:
            NotFoundError: If user not found
            ValidationError: If username is invalid
        """
        if not username or not username.strip():
            raise ValidationError("Username cannot be empty")
        
        username = username.strip().lower()
        
        # Check cache first
        if not force_refresh and username in self._user_cache:
            logger.info(f"Returning cached profile for user: {username}")
            return self._user_cache[username]
        
        try:
            # Fetch from GitHub
            github_data = await self.github_tools.get_user_info(username)
            if not github_data:
                raise NotFoundError(f"User not found: {username}")
            
            # Convert to UserProfile
            profile = UserProfile(
                user_id=str(github_data.get("id")),
                username=github_data.get("login"),
                email=github_data.get("email"),
                name=github_data.get("name"),
                bio=github_data.get("bio"),
                location=github_data.get("location"),
                company=github_data.get("company"),
                blog_url=github_data.get("blog"),
                avatar_url=github_data.get("avatar_url"),
                github_stats={
                    "public_repos": github_data.get("public_repos", 0),
                    "followers": github_data.get("followers", 0),
                    "following": github_data.get("following", 0)
                },
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Cache the profile
            self._user_cache[username] = profile
            logger.info(f"Cached profile for user: {username}")
            
            return profile
            
        except Exception as e:
            logger.error(f"Error fetching user profile for {username}: {str(e)}")
            raise
    
    async def analyze_user(self, username: str, force_refresh: bool = False) -> UserAnalysis:
        """
        Analyze user profile and activity.
        
        Args:
            username: GitHub username
            force_refresh: Force refresh analysis
            
        Returns:
            UserAnalysis object
        """
        username = username.strip().lower()
        
        # Check cache first
        if not force_refresh and username in self._analysis_cache:
            logger.info(f"Returning cached analysis for user: {username}")
            return self._analysis_cache[username]
        
        try:
            # Get user profile first
            profile = await self.get_user_profile(username, force_refresh)
            
            # Perform analysis using user profiler
            analysis_data = await self.user_profiler.analyze_user(username)
            
            # Convert to UserAnalysis
            analysis = UserAnalysis(
                user_id=profile.user_id,
                skill_level=analysis_data.get("skill_level", "intermediate"),
                primary_languages=analysis_data.get("primary_languages", []),
                frameworks=analysis_data.get("frameworks", []),
                domains=analysis_data.get("domains", []),
                activity_patterns=analysis_data.get("activity_patterns", {}),
                interests=analysis_data.get("interests", []),
                learning_goals=analysis_data.get("learning_goals", []),
                engagement_metrics=analysis_data.get("engagement_metrics", {}),
                marketing_insights=analysis_data.get("marketing_insights", {}),
                analysis_date=datetime.now(),
                confidence_score=analysis_data.get("confidence_score", 0.8),
                data_sources=analysis_data.get("data_sources", ["github"])
            )
            
            # Cache the analysis
            self._analysis_cache[username] = analysis
            logger.info(f"Cached analysis for user: {username}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing user {username}: {str(e)}")
            raise
    
    async def get_user_repositories(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's repositories.
        
        Args:
            username: GitHub username
            limit: Maximum number of repositories to return
            
        Returns:
            List of repository data
        """
        try:
            repos = await self.github_tools.get_user_repos(username, limit)
            return repos or []
        except Exception as e:
            logger.error(f"Error fetching repositories for {username}: {str(e)}")
            return []
    
    async def record_interaction(self, interaction: UserInteraction) -> bool:
        """
        Record user interaction.
        
        Args:
            interaction: UserInteraction object
            
        Returns:
            Success status
        """
        try:
            # In a real implementation, this would save to a database
            logger.info(f"Recording interaction: {interaction.interaction_type} for user {interaction.user_id}")
            return True
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
            return False
    
    def clear_cache(self, username: Optional[str] = None):
        """
        Clear user cache.
        
        Args:
            username: Specific username to clear, or None to clear all
        """
        if username:
            username = username.strip().lower()
            self._user_cache.pop(username, None)
            self._analysis_cache.pop(username, None)
            logger.info(f"Cleared cache for user: {username}")
        else:
            self._user_cache.clear()
            self._analysis_cache.clear()
            logger.info("Cleared all user cache")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics.
        
        Returns:
            Cache statistics
        """
        return {
            "profiles_cached": len(self._user_cache),
            "analyses_cached": len(self._analysis_cache)
        } 