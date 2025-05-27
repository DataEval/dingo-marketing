"""
测试主应用功能
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

# 模拟依赖项
@pytest.fixture
def mock_dependencies():
    """模拟应用依赖项"""
    with patch('src.main.init_database') as mock_db, \
         patch('src.main.init_redis') as mock_redis, \
         patch('src.main.init_scheduler') as mock_scheduler, \
         patch('src.main.MarketingCrew') as mock_crew:
        
        mock_db.return_value = AsyncMock()
        mock_redis.return_value = AsyncMock()
        mock_scheduler.return_value = AsyncMock()
        mock_crew.return_value = AsyncMock()
        
        yield {
            'db': mock_db,
            'redis': mock_redis,
            'scheduler': mock_scheduler,
            'crew': mock_crew
        }

@pytest.fixture
def client(mock_dependencies):
    """创建测试客户端"""
    from src.main import app
    return TestClient(app)

def test_root_endpoint(client):
    """测试根端点"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Dingo Marketing" in data["message"]

def test_health_endpoint(client):
    """测试健康检查端点"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data

def test_api_status_endpoint(client):
    """测试 API 状态端点"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_user_analysis_endpoint(client):
    """测试用户分析端点"""
    test_data = {
        "user_list": ["octocat", "defunkt"],
        "analysis_depth": "standard"
    }
    
    with patch('src.api.routes.get_marketing_crew') as mock_get_crew:
        mock_crew = AsyncMock()
        mock_crew.analyze_target_users.return_value = {
            "task_id": "test-123",
            "status": "completed",
            "results": {"analyzed_users": 2}
        }
        mock_get_crew.return_value = mock_crew
        
        response = client.post("/api/v1/analyze/users", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

@pytest.mark.asyncio
async def test_content_generation_endpoint(client):
    """测试内容生成端点"""
    test_data = {
        "content_type": "blog",
        "topic": "测试主题",
        "target_audience": "开发者",
        "tone": "professional",
        "length": "medium",
        "language": "zh"
    }
    
    with patch('src.api.routes.get_marketing_crew') as mock_get_crew:
        mock_crew = AsyncMock()
        mock_crew.create_content_campaign.return_value = {
            "task_id": "content-123",
            "status": "completed",
            "content": "生成的内容"
        }
        mock_get_crew.return_value = mock_crew
        
        response = client.post("/api/v1/content/generate", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

def test_invalid_request_data(client):
    """测试无效请求数据"""
    # 测试缺少必需字段的请求
    invalid_data = {"invalid_field": "value"}
    
    response = client.post("/api/v1/analyze/users", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_cors_headers(client):
    """测试 CORS 头部"""
    response = client.options("/api/v1/status")
    assert response.status_code == 200
    # 检查是否有 CORS 相关头部（如果配置了的话）

@pytest.mark.asyncio
async def test_campaign_creation(client):
    """测试营销活动创建"""
    test_data = {
        "name": "测试活动",
        "target_audience": "Python 开发者",
        "topics": ["数据质量", "自动化"],
        "content_types": ["blog", "social"],
        "duration": "1个月"
    }
    
    with patch('src.api.routes.get_marketing_crew') as mock_get_crew:
        mock_crew = AsyncMock()
        mock_crew.create_content_campaign.return_value = {
            "task_id": "campaign-123",
            "status": "started",
            "campaign_name": "测试活动"
        }
        mock_get_crew.return_value = mock_crew
        
        response = client.post("/api/v1/campaigns/content", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

@pytest.mark.asyncio
async def test_community_engagement(client):
    """测试社区互动"""
    test_data = {
        "interaction_types": ["comment", "issue"],
        "target_count": 5,
        "engagement_level": "moderate"
    }
    
    with patch('src.api.routes.get_marketing_crew') as mock_get_crew:
        mock_crew = AsyncMock()
        mock_crew.execute_community_engagement.return_value = {
            "task_id": "engagement-123",
            "status": "started",
            "target_interactions": 5
        }
        mock_get_crew.return_value = mock_crew
        
        response = client.post("/api/v1/engagement/community", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

def test_analytics_dashboard(client):
    """测试分析仪表板"""
    with patch('src.api.routes.get_marketing_crew') as mock_get_crew:
        mock_crew = AsyncMock()
        mock_crew.get_analytics_data = AsyncMock(return_value={
            "total_campaigns": 5,
            "active_users": 100,
            "engagement_rate": 0.15
        })
        mock_get_crew.return_value = mock_crew
        
        response = client.get("/api/v1/analytics/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "analytics" in data

def test_tools_status(client):
    """测试工具状态"""
    response = client.get("/api/v1/tools/status")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert isinstance(data["tools"], list) 