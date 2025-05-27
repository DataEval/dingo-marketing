"""
Data models for Dingo Marketing system.
"""

from .user import UserProfile, UserAnalysis
from .content import ContentItem, ContentMetrics
from .campaign import Campaign, CampaignMetrics

__all__ = [
    'UserProfile',
    'UserAnalysis', 
    'ContentItem',
    'ContentMetrics',
    'Campaign',
    'CampaignMetrics',
] 