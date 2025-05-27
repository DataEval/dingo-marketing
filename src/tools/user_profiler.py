"""
User Profiler Module for Dingo Marketing System

This module analyzes user data from various sources to create
rich user profiles for targeted marketing campaigns.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

import pandas as pd
import markdown
from jinja2 import Template

from config import settings, DATA_DIR, REPORTS_DIR
from tracking.github_tracker import GitHubTracker
from tracking.web_tracker import WebTracker

logger = logging.getLogger(__name__)

class UserProfile:
    """User profile model with aggregated data."""
    
    def __init__(self, user_id: str, data: Dict[str, Any] = None):
        """Initialize user profile with optional data."""
        self.user_id = user_id
        self.data = data or {
            "user_id": user_id,
            "sources": [],
            "first_seen": datetime.now().isoformat(),
            "last_seen": datetime.now().isoformat(),
            "visits": 0,
            "activity": {},
            "interests": [],
            "engagement_score": 0,
            "segments": [],
            "technical_profile": {},
            "marketing_profile": {},
            "metadata": {}
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert profile to dictionary."""
        return self.data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserProfile":
        """Create profile from dictionary."""
        user_id = data.get("user_id", "")
        return cls(user_id, data)

class UserProfiler:
    """Analyze and profile users from multiple data sources."""
    
    def __init__(self, github_tracker: Optional[GitHubTracker] = None, 
                 web_tracker: Optional[WebTracker] = None):
        """Initialize the user profiler with data sources."""
        self.github_tracker = github_tracker
        self.web_tracker = web_tracker
        self.data_dir = DATA_DIR
        self.profiles_file = self.data_dir / "user_profiles.json"
        
        # Ensure the data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize storage
        self._profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict[str, UserProfile]:
        """Load profiles from storage or create default structure."""
        profiles = {}
        
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, "r") as f:
                    data = json.load(f)
                    for user_data in data:
                        user_id = user_data.get("user_id")
                        if user_id:
                            profiles[user_id] = UserProfile.from_dict(user_data)
            except json.JSONDecodeError:
                logger.error("Failed to load user profiles file. Creating new.")
        
        return profiles
    
    def _save_profiles(self) -> None:
        """Save profiles to storage."""
        profiles_data = [profile.to_dict() for profile in self._profiles.values()]
        
        with open(self.profiles_file, "w") as f:
            json.dump(profiles_data, f, indent=2)
    
    async def build_profiles(self) -> int:
        """Build or update user profiles from all data sources."""
        updated_count = 0
        
        # Process GitHub users if GitHub tracker is available
        if self.github_tracker:
            github_users = self.github_tracker.get_users()
            for user in github_users:
                user_id = user.get("login")
                if not user_id:
                    continue
                
                # Get or create profile
                profile = self._profiles.get(user_id)
                if not profile:
                    profile = UserProfile(user_id)
                    self._profiles[user_id] = profile
                
                # Update profile with GitHub data
                self._update_profile_from_github(profile, user)
                updated_count += 1
        
        # Process web users if web tracker is available
        if self.web_tracker:
            # This would use web analytics data to update profiles
            # Implementation depends on how web_tracker stores user data
            pass
        
        # Save updated profiles
        self._save_profiles()
        
        logger.info(f"Built {updated_count} user profiles")
        return updated_count
    
    def _update_profile_from_github(self, profile: UserProfile, github_data: Dict[str, Any]) -> None:
        """Update a user profile with GitHub data."""
        data = profile.data
        
        # Add GitHub as a data source if not already present
        if "github" not in data["sources"]:
            data["sources"].append("github")
        
        # Update basic metadata
        data["metadata"]["github"] = {
            "login": github_data.get("login"),
            "name": github_data.get("name"),
            "bio": github_data.get("bio"),
            "company": github_data.get("company"),
            "location": github_data.get("location"),
            "email": github_data.get("email"),
            "blog": github_data.get("blog"),
            "twitter": github_data.get("twitter"),
            "avatar_url": github_data.get("avatar_url"),
            "html_url": github_data.get("html_url"),
            "followers": github_data.get("followers"),
            "following": github_data.get("following"),
            "public_repos": github_data.get("public_repos"),
            "first_seen": github_data.get("first_seen") or data["first_seen"]
        }
        
        # Update last seen
        data["last_seen"] = datetime.now().isoformat()
        
        # Update technical profile
        tech_profile = data["technical_profile"]
        
        # Determine user type
        if github_data.get("type") == "contributor":
            tech_profile["user_type"] = "contributor"
            tech_profile["contributions"] = github_data.get("contributions", 0)
        else:
            tech_profile["user_type"] = "stargazer"
        
        # Infer technical interests
        interests = set(data.get("interests", []))
        
        # Add interests based on GitHub profile
        if github_data.get("bio"):
            bio_interests = self._extract_interests_from_text(github_data.get("bio", ""))
            interests.update(bio_interests)
        
        # Add language interests if available
        if "languages" in github_data:
            for lang in github_data.get("languages", []):
                interests.add(f"language:{lang}")
        
        # Add Dingo-specific interest
        interests.add("data-quality")
        interests.add("dingo")
        
        # Update interests
        data["interests"] = list(interests)
        
        # Update segments
        segments = set(data.get("segments", []))
        
        # Add basic segments
        segments.add(tech_profile["user_type"])
        
        # Add company segment if available
        if github_data.get("company"):
            segments.add("corporate")
        else:
            segments.add("individual")
        
        # Add influence segment if many followers
        if github_data.get("followers", 0) > 100:
            segments.add("high-influence")
        
        # Add recency segment
        if github_data.get("first_seen"):
            try:
                first_seen = datetime.fromisoformat(github_data["first_seen"].replace("Z", "+00:00"))
                if (datetime.now() - first_seen).days < 30:
                    segments.add("new-user")
            except (ValueError, TypeError):
                pass
        
        # Update segments
        data["segments"] = list(segments)
        
        # Calculate engagement score
        engagement_score = 0
        
        # Contributors get higher base score
        if tech_profile["user_type"] == "contributor":
            engagement_score += 50
            engagement_score += min(github_data.get("contributions", 0) * 5, 30)
        else:
            engagement_score += 10
        
        # Followers add to engagement score
        followers = github_data.get("followers", 0)
        engagement_score += min(followers * 0.2, 20)
        
        # Public activity adds to engagement score
        public_repos = github_data.get("public_repos", 0)
        engagement_score += min(public_repos * 0.5, 20)
        
        # Cap score at 100
        data["engagement_score"] = min(round(engagement_score), 100)
        
        # Update marketing profile
        marketing_profile = data["marketing_profile"]
        marketing_profile["persona"] = self._determine_persona(data)
        marketing_profile["communication_channel"] = self._determine_communication_channel(data)
        marketing_profile["content_preferences"] = self._determine_content_preferences(data)
    
    def _extract_interests_from_text(self, text: str) -> Set[str]:
        """Extract technical interests from text like bio or description."""
        interests = set()
        
        # Keywords to look for
        keywords = {
            "machine learning": ["ml", "machine learning", "ai", "artificial intelligence", "data science"],
            "data engineering": ["data engineering", "data pipeline", "etl", "data processing"],
            "web development": ["web dev", "frontend", "backend", "full stack", "javascript", "react", "node"],
            "devops": ["devops", "cicd", "ci/cd", "deployment", "kubernetes", "docker", "infrastructure"],
            "cloud": ["aws", "azure", "gcp", "cloud", "serverless"],
            "nlp": ["nlp", "natural language", "language model", "text processing"],
            "open source": ["open source", "oss", "community", "contributor"],
            "security": ["security", "infosec", "cyber", "secure coding"]
        }
        
        # Check for each keyword group
        for category, terms in keywords.items():
            for term in terms:
                if term.lower() in text.lower():
                    interests.add(category)
                    break
        
        return interests
    
    def _determine_persona(self, profile_data: Dict[str, Any]) -> str:
        """Determine the marketing persona for a user profile."""
        if "contributor" in profile_data.get("segments", []):
            if "corporate" in profile_data.get("segments", []):
                return "corporate-contributor"
            return "open-source-contributor"
        
        if "high-influence" in profile_data.get("segments", []):
            return "influencer"
            
        if "corporate" in profile_data.get("segments", []):
            return "corporate-evaluator"
            
        if profile_data.get("engagement_score", 0) > 50:
            return "engaged-user"
            
        return "casual-user"
    
    def _determine_communication_channel(self, profile_data: Dict[str, Any]) -> str:
        """Determine the best communication channel for a user."""
        github_data = profile_data.get("metadata", {}).get("github", {})
        
        if github_data.get("email"):
            return "email"
        elif github_data.get("twitter"):
            return "twitter"
        elif "contributor" in profile_data.get("segments", []):
            return "github-issues"
        
        return "github-discussions"
    
    def _determine_content_preferences(self, profile_data: Dict[str, Any]) -> List[str]:
        """Determine content preferences based on user profile."""
        preferences = []
        
        # Add preferences based on persona
        persona = profile_data.get("marketing_profile", {}).get("persona", "")
        
        if persona == "corporate-contributor":
            preferences.extend(["case-studies", "benchmarks", "technical-deep-dives"])
        elif persona == "open-source-contributor":
            preferences.extend(["technical-deep-dives", "implementation-guides", "contributor-guides"])
        elif persona == "influencer":
            preferences.extend(["industry-trends", "thought-leadership", "comparative-analysis"])
        elif persona == "corporate-evaluator":
            preferences.extend(["benchmarks", "case-studies", "integration-guides"])
        elif persona == "engaged-user":
            preferences.extend(["how-to-guides", "best-practices", "examples"])
        else:  # casual-user
            preferences.extend(["getting-started", "benefits-overview", "examples"])
        
        # Add preferences based on interests
        interests = profile_data.get("interests", [])
        for interest in interests:
            if interest == "machine learning":
                preferences.append("ml-applications")
            elif interest == "data engineering":
                preferences.append("data-pipeline-examples")
            elif interest == "nlp":
                preferences.append("nlp-use-cases")
        
        return preferences
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user profile by ID."""
        profile = self._profiles.get(user_id)
        if profile:
            return profile.to_dict()
        return None
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all user profiles."""
        return [profile.to_dict() for profile in self._profiles.values()]
    
    def analyze_user_segments(self) -> Dict[str, Any]:
        """Analyze user segments and their characteristics."""
        if not self._profiles:
            return {"segments": [], "total_users": 0}
        
        # Count users in each segment
        segment_counts = {}
        for profile in self._profiles.values():
            for segment in profile.data.get("segments", []):
                if segment not in segment_counts:
                    segment_counts[segment] = 0
                segment_counts[segment] += 1
        
        # Calculate average engagement for each segment
        segment_engagement = {}
        for profile in self._profiles.values():
            engagement = profile.data.get("engagement_score", 0)
            for segment in profile.data.get("segments", []):
                if segment not in segment_engagement:
                    segment_engagement[segment] = []
                segment_engagement[segment].append(engagement)
        
        for segment, scores in segment_engagement.items():
            segment_engagement[segment] = sum(scores) / len(scores) if scores else 0
        
        # Format response
        segments = [
            {
                "id": segment,
                "name": segment.replace("-", " ").title(),
                "count": count,
                "percentage": round(count / len(self._profiles) * 100, 1),
                "engagementRate": round(segment_engagement.get(segment, 0), 1)
            }
            for segment, count in segment_counts.items()
        ]
        
        # Sort by count
        segments.sort(key=lambda x: x["count"], reverse=True)
        
        return {
            "total_users": len(self._profiles),
            "segments": segments
        }
    
    def export_profiles_report(self, format: str = "markdown") -> str:
        """Generate a report about user profiles and export it."""
        # Create report data
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "total_profiles": len(self._profiles),
            "segments": self.analyze_user_segments()["segments"],
            "engagement": {
                "high": sum(1 for p in self._profiles.values() if p.data.get("engagement_score", 0) >= 70),
                "medium": sum(1 for p in self._profiles.values() if 30 <= p.data.get("engagement_score", 0) < 70),
                "low": sum(1 for p in self._profiles.values() if p.data.get("engagement_score", 0) < 30)
            }
        }
        
        # Calculate geographic distribution if GitHub data available
        if self.github_tracker:
            report_data["geographic_distribution"] = self.github_tracker.get_geographic_distribution()
        
        # Calculate communication channels
        channels = {}
        for profile in self._profiles.values():
            channel = profile.data.get("marketing_profile", {}).get("communication_channel", "unknown")
            if channel not in channels:
                channels[channel] = 0
            channels[channel] += 1
        
        report_data["communication_channels"] = channels
        
        # Calculate content preferences
        preferences = {}
        for profile in self._profiles.values():
            for pref in profile.data.get("marketing_profile", {}).get("content_preferences", []):
                if pref not in preferences:
                    preferences[pref] = 0
                preferences[pref] += 1
        
        report_data["content_preferences"] = preferences
        
        # Generate report
        if format == "markdown":
            return self._generate_markdown_report(report_data)
        else:
            # Default to markdown
            return self._generate_markdown_report(report_data)
    
    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """Generate a markdown report from data."""
        template = """
# Dingo User Profiles Report

*Generated: {{ data.generated_at }}*

## Summary

- **Total Profiles**: {{ data.total_profiles }}
- **High Engagement**: {{ data.engagement.high }} users ({{ (data.engagement.high / data.total_profiles * 100) | round(1) }}%)
- **Medium Engagement**: {{ data.engagement.medium }} users ({{ (data.engagement.medium / data.total_profiles * 100) | round(1) }}%)
- **Low Engagement**: {{ data.engagement.low }} users ({{ (data.engagement.low / data.total_profiles * 100) | round(1) }}%)

## User Segments

| Segment | Count | Percentage | Avg. Engagement |
|---------|-------|------------|-----------------|
{% for segment in data.segments %}
| {{ segment.name }} | {{ segment.count }} | {{ segment.percentage }}% | {{ segment.engagementRate }}% |
{% endfor %}

## Geographic Distribution

{% if data.geographic_distribution %}
| Location | Count |
|----------|-------|
{% for location, count in data.geographic_distribution.items() %}
| {{ location }} | {{ count }} |
{% endfor %}
{% else %}
*No geographic data available*
{% endif %}

## Communication Channels

{% if data.communication_channels %}
| Channel | Count | Percentage |
|---------|-------|------------|
{% for channel, count in data.communication_channels.items() %}
| {{ channel }} | {{ count }} | {{ (count / data.total_profiles * 100) | round(1) }}% |
{% endfor %}
{% else %}
*No communication channel data available*
{% endif %}

## Content Preferences

{% if data.content_preferences %}
| Preference | Count | Percentage |
|------------|-------|------------|
{% for pref, count in data.content_preferences.items() %}
| {{ pref }} | {{ count }} | {{ (count / data.total_profiles * 100) | round(1) }}% |
{% endfor %}
{% else %}
*No content preference data available*
{% endif %}

## Marketing Recommendations

Based on the user profile analysis, here are some recommendations:

1. **Target Audiences**: Focus on the largest segments: {% for segment in data.segments[:3] %}{{ segment.name }}{% if not loop.last %}, {% endif %}{% endfor %}.
2. **Content Strategy**: Create content that aligns with top preferences: {% for pref, count in data.content_preferences.items() %}{% if loop.index <= 3 %}{{ pref }}{% if not loop.last %}, {% endif %}{% endif %}{% endfor %}.
3. **Communication**: Prioritize these channels for outreach: {% for channel, count in data.communication_channels.items() %}{% if loop.index <= 2 %}{{ channel }}{% if not loop.last %}, {% endif %}{% endif %}{% endfor %}.

"""
        # Render template
        jinja_template = Template(template)
        markdown_content = jinja_template.render(data=data)
        
        # Save markdown file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = REPORTS_DIR / f"user_profiles_{timestamp}.md"
        
        with open(report_path, "w") as f:
            f.write(markdown_content)
        
        # Also save HTML version
        html_content = markdown.markdown(markdown_content, extensions=['tables'])
        html_path = REPORTS_DIR / f"user_profiles_{timestamp}.html"
        
        with open(html_path, "w") as f:
            f.write(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Dingo User Profiles Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """)
        
        logger.info(f"Generated user profile report: {report_path}")
        return str(report_path) 