"""
Content analysis module for the Dingo Marketing Automation system.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

import pandas as pd
from pydantic import BaseModel

from config import settings, DATA_DIR

# Set up logging
logger = logging.getLogger(__name__)

class ContentMetrics(BaseModel):
    """Model for content metrics."""
    content_id: str
    title: str
    type: str  # 'blog', 'docs', 'social', 'newsletter', etc.
    url: Optional[str] = None
    publication_date: str
    views: int = 0
    unique_visitors: int = 0
    avg_time_on_page: float = 0.0
    bounce_rate: float = 0.0
    conversion_rate: float = 0.0
    engagement_rate: float = 0.0
    shares: int = 0
    likes: int = 0
    comments: int = 0
    keywords: List[str] = []
    categories: List[str] = []
    tags: List[str] = []
    last_updated: str

class ContentPerformance(BaseModel):
    """Model for content performance analysis."""
    top_content: List[Dict[str, Any]] = []
    content_by_type: Dict[str, int] = {}
    content_by_category: Dict[str, int] = {}
    trending_keywords: Dict[str, int] = {}
    engagement_by_type: Dict[str, float] = {}
    avg_time_by_type: Dict[str, float] = {}
    publication_timeline: Dict[str, int] = {}
    total_views: int = 0
    total_shares: int = 0
    total_pieces: int = 0

class ContentAnalyzer:
    """
    Analyzes content performance and trends for marketing insights.
    """
    
    def __init__(self):
        """Initialize the content analyzer."""
        self.content_dir = os.path.join(DATA_DIR, 'content')
        os.makedirs(self.content_dir, exist_ok=True)
    
    def register_content(self, content: ContentMetrics) -> bool:
        """
        Register or update a piece of content.
        
        Args:
            content: Content metrics to register
            
        Returns:
            True if successful, False otherwise
        """
        file_path = os.path.join(self.content_dir, f"{content.content_id}.json")
        
        try:
            with open(file_path, 'w') as f:
                f.write(content.json(indent=2))
            return True
        except Exception as e:
            logger.error(f"Error registering content {content.content_id}: {e}")
            return False
    
    def get_content(self, content_id: str) -> Optional[ContentMetrics]:
        """
        Get content metrics by ID.
        
        Args:
            content_id: Content ID
            
        Returns:
            Content metrics or None if not found
        """
        file_path = os.path.join(self.content_dir, f"{content_id}.json")
        
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return ContentMetrics(**data)
        except Exception as e:
            logger.error(f"Error loading content {content_id}: {e}")
            return None
    
    def get_all_content(self) -> List[ContentMetrics]:
        """
        Get all content metrics.
        
        Returns:
            List of all content metrics
        """
        content_list = []
        
        for filename in os.listdir(self.content_dir):
            if not filename.endswith('.json'):
                continue
                
            content_id = filename[:-5]  # Remove .json extension
            content = self.get_content(content_id)
            
            if content:
                content_list.append(content)
        
        return content_list
    
    def update_metrics(self, content_id: str, metrics: Dict[str, Any]) -> bool:
        """
        Update metrics for a piece of content.
        
        Args:
            content_id: Content ID
            metrics: Metrics to update (field-value pairs)
            
        Returns:
            True if successful, False otherwise
        """
        content = self.get_content(content_id)
        
        if not content:
            logger.error(f"Content {content_id} not found")
            return False
        
        try:
            # Update fields
            for field, value in metrics.items():
                if hasattr(content, field):
                    setattr(content, field, value)
            
            # Update last_updated timestamp
            content.last_updated = datetime.now().isoformat()
            
            # Save updated content
            return self.register_content(content)
        except Exception as e:
            logger.error(f"Error updating metrics for content {content_id}: {e}")
            return False
    
    def analyze_performance(self, days: int = 90) -> ContentPerformance:
        """
        Analyze content performance over the specified period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Content performance analysis
        """
        all_content = self.get_all_content()
        
        if not all_content:
            return ContentPerformance()
        
        # Set date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter content by publication date
        filtered_content = [
            c for c in all_content 
            if datetime.fromisoformat(c.publication_date) >= start_date
        ]
        
        if not filtered_content:
            return ContentPerformance()
        
        performance = ContentPerformance()
        
        # Calculate total metrics
        performance.total_pieces = len(filtered_content)
        performance.total_views = sum(c.views for c in filtered_content)
        performance.total_shares = sum(c.shares for c in filtered_content)
        
        # Top content by views
        top_content = sorted(
            [
                {
                    "id": c.content_id,
                    "title": c.title,
                    "type": c.type,
                    "views": c.views,
                    "engagement_rate": c.engagement_rate,
                    "publication_date": c.publication_date
                }
                for c in filtered_content
            ],
            key=lambda x: x["views"],
            reverse=True
        )[:10]  # Top 10 content pieces
        performance.top_content = top_content
        
        # Content by type
        content_by_type = {}
        for c in filtered_content:
            if c.type not in content_by_type:
                content_by_type[c.type] = 0
            content_by_type[c.type] += 1
        performance.content_by_type = content_by_type
        
        # Content by category
        content_by_category = {}
        for c in filtered_content:
            for category in c.categories:
                if category not in content_by_category:
                    content_by_category[category] = 0
                content_by_category[category] += 1
        performance.content_by_category = content_by_category
        
        # Trending keywords
        keywords_count = {}
        for c in filtered_content:
            for keyword in c.keywords:
                if keyword not in keywords_count:
                    keywords_count[keyword] = 0
                keywords_count[keyword] += 1
                
        # Sort keywords by count and take top 20
        performance.trending_keywords = dict(
            sorted(
                keywords_count.items(),
                key=lambda item: item[1],
                reverse=True
            )[:20]
        )
        
        # Average engagement by content type
        engagement_by_type = {}
        type_counts = {}
        for c in filtered_content:
            if c.type not in engagement_by_type:
                engagement_by_type[c.type] = 0
                type_counts[c.type] = 0
            engagement_by_type[c.type] += c.engagement_rate
            type_counts[c.type] += 1
            
        # Calculate averages
        for content_type, total in engagement_by_type.items():
            if type_counts[content_type] > 0:
                engagement_by_type[content_type] = total / type_counts[content_type]
        performance.engagement_by_type = engagement_by_type
        
        # Average time on page by content type
        avg_time_by_type = {}
        for c in filtered_content:
            if c.type not in avg_time_by_type:
                avg_time_by_type[c.type] = 0
                # type_counts already calculated above
            avg_time_by_type[c.type] += c.avg_time_on_page
            
        # Calculate averages
        for content_type, total in avg_time_by_type.items():
            if type_counts[content_type] > 0:
                avg_time_by_type[content_type] = total / type_counts[content_type]
        performance.avg_time_by_type = avg_time_by_type
        
        # Publication timeline (by month)
        timeline = {}
        for c in filtered_content:
            pub_date = datetime.fromisoformat(c.publication_date)
            month_key = pub_date.strftime("%Y-%m")
            if month_key not in timeline:
                timeline[month_key] = 0
            timeline[month_key] += 1
        performance.publication_timeline = dict(sorted(timeline.items()))
        
        return performance
    
    def identify_content_gaps(self) -> Dict[str, Any]:
        """
        Identify content gaps based on performance data.
        
        Returns:
            Dictionary with content gap analysis results
        """
        all_content = self.get_all_content()
        
        if not all_content:
            return {
                "underperforming_types": [],
                "missing_categories": [],
                "stale_content": [],
                "content_frequency": {},
                "keyword_coverage": {}
            }
        
        # Performance by content type
        type_metrics = {}
        for c in all_content:
            if c.type not in type_metrics:
                type_metrics[c.type] = {
                    "count": 0,
                    "total_views": 0,
                    "total_engagement": 0,
                    "avg_views": 0,
                    "avg_engagement": 0
                }
            
            type_metrics[c.type]["count"] += 1
            type_metrics[c.type]["total_views"] += c.views
            type_metrics[c.type]["total_engagement"] += c.engagement_rate
        
        # Calculate averages
        for content_type, metrics in type_metrics.items():
            if metrics["count"] > 0:
                metrics["avg_views"] = metrics["total_views"] / metrics["count"]
                metrics["avg_engagement"] = metrics["total_engagement"] / metrics["count"]
        
        # Find underperforming content types
        global_avg_views = sum(m["total_views"] for m in type_metrics.values()) / len(all_content)
        global_avg_engagement = sum(m["total_engagement"] for m in type_metrics.values()) / len(all_content)
        
        underperforming_types = [
            {
                "type": content_type,
                "avg_views": metrics["avg_views"],
                "global_avg_views": global_avg_views,
                "avg_engagement": metrics["avg_engagement"],
                "global_avg_engagement": global_avg_engagement
            }
            for content_type, metrics in type_metrics.items()
            if metrics["avg_views"] < global_avg_views * 0.8 or metrics["avg_engagement"] < global_avg_engagement * 0.8
        ]
        
        # Find stale content (not updated in last 90 days but still gets some traffic)
        stale_threshold = datetime.now() - timedelta(days=90)
        stale_content = [
            {
                "id": c.content_id,
                "title": c.title,
                "type": c.type,
                "views": c.views,
                "last_updated": c.last_updated
            }
            for c in all_content
            if (datetime.fromisoformat(c.last_updated) < stale_threshold and c.views > 0)
        ]
        
        # Analyze content publication frequency
        publication_dates = [datetime.fromisoformat(c.publication_date) for c in all_content]
        publication_dates.sort()
        
        if len(publication_dates) > 1:
            # Calculate days between publications
            days_between = [(publication_dates[i] - publication_dates[i-1]).days 
                           for i in range(1, len(publication_dates))]
            
            content_frequency = {
                "avg_days_between": sum(days_between) / len(days_between),
                "max_gap": max(days_between),
                "min_gap": min(days_between),
                "total_content": len(all_content)
            }
        else:
            content_frequency = {
                "avg_days_between": 0,
                "max_gap": 0,
                "min_gap": 0,
                "total_content": len(all_content)
            }
        
        # Analyze keyword coverage
        all_keywords = {}
        for c in all_content:
            for keyword in c.keywords:
                if keyword not in all_keywords:
                    all_keywords[keyword] = 0
                all_keywords[keyword] += 1
        
        # Find keywords with low coverage (only 1 content piece)
        low_coverage_keywords = [k for k, count in all_keywords.items() if count == 1]
        
        # Expected categories for a complete content strategy
        expected_categories = [
            'data_quality',
            'nlp',
            'rag',
            'llm_evaluation', 
            'data_cleaning',
            'prompt_engineering',
            'machine_learning',
            'tutorials',
            'case_studies',
            'benchmarks'
        ]
        
        # Find existing categories
        existing_categories = set()
        for c in all_content:
            existing_categories.update(c.categories)
        
        # Find missing categories
        missing_categories = [c for c in expected_categories if c not in existing_categories]
        
        return {
            "underperforming_types": underperforming_types,
            "missing_categories": missing_categories,
            "stale_content": stale_content,
            "content_frequency": content_frequency,
            "low_coverage_keywords": low_coverage_keywords[:20]  # Top 20 low coverage keywords
        }
    
    def recommend_content(self) -> List[Dict[str, Any]]:
        """
        Generate content recommendations based on performance data.
        
        Returns:
            List of content recommendations
        """
        # Get performance data
        performance = self.analyze_performance()
        
        # Get content gaps
        gaps = self.identify_content_gaps()
        
        recommendations = []
        
        # Recommend content for missing categories
        for category in gaps["missing_categories"]:
            recommendations.append({
                "type": "new_content",
                "priority": "high",
                "category": category,
                "title": f"Create content for {category.replace('_', ' ')}",
                "description": f"No content exists for the {category.replace('_', ' ')} category. Create introductory content to fill this gap."
            })
        
        # Recommend updates for stale content
        for content in gaps["stale_content"][:3]:  # Top 3 stale content
            recommendations.append({
                "type": "update_content",
                "priority": "medium",
                "content_id": content["id"],
                "title": f"Update {content['title']}",
                "description": f"This content is getting views but hasn't been updated in 90+ days. Review and refresh."
            })
        
        # Recommend new content for underperforming types
        for content_type in gaps["underperforming_types"]:
            recommendations.append({
                "type": "new_content",
                "priority": "medium",
                "content_type": content_type["type"],
                "title": f"Create better {content_type['type']} content",
                "description": f"{content_type['type'].capitalize()} content is performing below average. Create more engaging content of this type."
            })
        
        # Recommend content frequency adjustments
        if gaps["content_frequency"]["avg_days_between"] > 14:  # If average is more than 2 weeks
            recommendations.append({
                "type": "frequency_adjustment",
                "priority": "medium",
                "title": "Increase content publication frequency",
                "description": f"Current average is {gaps['content_frequency']['avg_days_between']:.1f} days between posts. Aim for weekly content."
            })
        
        # Recommend content for trending keywords
        if performance.trending_keywords:
            top_keywords = list(performance.trending_keywords.keys())[:3]  # Top 3 trending keywords
            for keyword in top_keywords:
                recommendations.append({
                    "type": "new_content",
                    "priority": "low",
                    "keyword": keyword,
                    "title": f"Create content around '{keyword}'",
                    "description": f"'{keyword}' is a trending keyword. Create more content to leverage this interest."
                })
        
        return recommendations
    
    def export_content_report(self, output_file: str = "content_report.md") -> str:
        """
        Export a markdown report of content performance.
        
        Args:
            output_file: Output file path
            
        Returns:
            Path to the generated report file
        """
        # Get performance data
        performance = self.analyze_performance()
        
        # Get content gaps
        gaps = self.identify_content_gaps()
        
        # Get recommendations
        recommendations = self.recommend_content()
        
        # Create report
        report_lines = [
            "# Dingo Content Performance Report",
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Overview",
            f"Total Content Pieces: {performance.total_pieces}",
            f"Total Views: {performance.total_views}",
            f"Total Shares: {performance.total_shares}",
            "",
            "## Top Performing Content",
            ""
        ]
        
        # Add top content
        for i, content in enumerate(performance.top_content, 1):
            pub_date = datetime.fromisoformat(content["publication_date"]).strftime("%Y-%m-%d")
            report_lines.append(f"{i}. **{content['title']}** ({content['type']})")
            report_lines.append(f"   - Views: {content['views']}")
            report_lines.append(f"   - Engagement Rate: {content['engagement_rate'] * 100:.1f}%")
            report_lines.append(f"   - Published: {pub_date}")
            report_lines.append("")
        
        report_lines.extend([
            "## Content Distribution",
            ""
        ])
        
        # Add content by type
        report_lines.append("### By Type")
        for content_type, count in performance.content_by_type.items():
            percentage = (count / performance.total_pieces) * 100 if performance.total_pieces else 0
            report_lines.append(f"- **{content_type.capitalize()}**: {count} pieces ({percentage:.1f}%)")
        
        report_lines.append("")
        report_lines.append("### By Category")
        for category, count in performance.content_by_category.items():
            percentage = (count / performance.total_pieces) * 100 if performance.total_pieces else 0
            report_lines.append(f"- **{category.replace('_', ' ').capitalize()}**: {count} pieces ({percentage:.1f}%)")
        
        report_lines.extend([
            "",
            "## Trending Keywords",
            ""
        ])
        
        # Add trending keywords
        for keyword, count in performance.trending_keywords.items():
            report_lines.append(f"- **{keyword}**: {count} occurrences")
        
        report_lines.extend([
            "",
            "## Engagement Analysis",
            ""
        ])
        
        # Add engagement by type
        report_lines.append("### Average Engagement Rate by Content Type")
        for content_type, rate in performance.engagement_by_type.items():
            report_lines.append(f"- **{content_type.capitalize()}**: {rate * 100:.1f}%")
        
        report_lines.append("")
        report_lines.append("### Average Time on Page by Content Type")
        for content_type, time in performance.avg_time_by_type.items():
            report_lines.append(f"- **{content_type.capitalize()}**: {time:.1f} seconds")
        
        report_lines.extend([
            "",
            "## Publication Timeline",
            ""
        ])
        
        # Add publication timeline
        for month, count in performance.publication_timeline.items():
            report_lines.append(f"- **{month}**: {count} pieces")
        
        report_lines.extend([
            "",
            "## Content Gaps",
            ""
        ])
        
        # Add missing categories
        report_lines.append("### Missing Categories")
        if gaps["missing_categories"]:
            for category in gaps["missing_categories"]:
                report_lines.append(f"- {category.replace('_', ' ').capitalize()}")
        else:
            report_lines.append("- No missing categories identified")
        
        report_lines.append("")
        report_lines.append("### Stale Content")
        if gaps["stale_content"]:
            for content in gaps["stale_content"][:5]:  # Top 5 stale content
                last_updated = datetime.fromisoformat(content["last_updated"]).strftime("%Y-%m-%d")
                report_lines.append(f"- **{content['title']}** (Last updated: {last_updated})")
        else:
            report_lines.append("- No stale content identified")
        
        report_lines.extend([
            "",
            "## Recommendations",
            ""
        ])
        
        # Add recommendations
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"### {i}. {rec['title']}")
            report_lines.append(f"Priority: **{rec['priority'].capitalize()}**")
            report_lines.append("")
            report_lines.append(rec["description"])
            report_lines.append("")
        
        # Save report to file
        report_path = os.path.join(DATA_DIR, output_file)
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        return report_path


# For testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create analyzer
    analyzer = ContentAnalyzer()
    
    # Create some test content
    sample_content = [
        ContentMetrics(
            content_id="blog-001",
            title="Getting Started with Dingo",
            type="blog",
            url="/blog/getting-started",
            publication_date=datetime.now().isoformat(),
            views=1200,
            unique_visitors=950,
            avg_time_on_page=120.5,
            bounce_rate=0.25,
            engagement_rate=0.65,
            shares=85,
            likes=120,
            comments=15,
            keywords=["dingo", "data quality", "getting started", "tutorial"],
            categories=["tutorials", "data_quality"],
            tags=["beginner", "guide", "data_quality"],
            last_updated=datetime.now().isoformat()
        ),
        ContentMetrics(
            content_id="blog-002",
            title="Advanced Data Cleaning with Dingo",
            type="blog",
            url="/blog/advanced-data-cleaning",
            publication_date=(datetime.now() - timedelta(days=30)).isoformat(),
            views=850,
            unique_visitors=700,
            avg_time_on_page=180.2,
            bounce_rate=0.15,
            engagement_rate=0.78,
            shares=120,
            likes=95,
            comments=23,
            keywords=["dingo", "data cleaning", "advanced", "techniques"],
            categories=["data_cleaning", "tutorials"],
            tags=["advanced", "data_cleaning"],
            last_updated=(datetime.now() - timedelta(days=30)).isoformat()
        ),
        ContentMetrics(
            content_id="doc-001",
            title="Dingo API Documentation",
            type="documentation",
            url="/docs/api",
            publication_date=(datetime.now() - timedelta(days=60)).isoformat(),
            views=2500,
            unique_visitors=1800,
            avg_time_on_page=240.0,
            bounce_rate=0.10,
            engagement_rate=0.45,
            shares=35,
            likes=50,
            comments=8,
            keywords=["dingo", "api", "documentation", "reference"],
            categories=["documentation"],
            tags=["api", "reference"],
            last_updated=(datetime.now() - timedelta(days=100)).isoformat()
        )
    ]
    
    # Register test content
    for content in sample_content:
        analyzer.register_content(content)
    
    # Analyze performance
    performance = analyzer.analyze_performance()
    logger.info(f"Content performance: {json.dumps(performance.dict(), indent=2)}")
    
    # Identify content gaps
    gaps = analyzer.identify_content_gaps()
    logger.info(f"Content gaps: {json.dumps(gaps, indent=2)}")
    
    # Get recommendations
    recommendations = analyzer.recommend_content()
    logger.info(f"Recommendations: {json.dumps(recommendations, indent=2)}")
    
    # Export report
    report_path = analyzer.export_content_report()
    logger.info(f"Report exported to {report_path}") 