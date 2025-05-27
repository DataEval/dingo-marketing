# Dingo Marketing 开发指南

## 📋 目录

- [开发环境设置](#开发环境设置)
- [项目结构](#项目结构)
- [开发工作流](#开发工作流)
- [代码规范](#代码规范)
- [测试指南](#测试指南)
- [调试指南](#调试指南)
- [性能优化](#性能优化)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)

## 🛠️ 开发环境设置

### 1. 系统要求

- **Python**: 3.9+
- **Git**: 2.30+
- **Node.js**: 18+ (可选，用于前端开发)

### 2. 环境安装

#### 克隆项目

```bash
git clone https://github.com/your-org/dingo-marketing.git
cd dingo-marketing
```

#### 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 使用 conda
conda create -n dingo-marketing python=3.9
conda activate dingo-marketing
```

#### 安装依赖

```bash
# 安装生产依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

#### 环境配置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑环境变量
vim .env
```

#### 启动开发环境

```bash
# 启动应用
make dev

# 或直接运行
python run.py --debug --reload
```

### 3. IDE 配置

#### VS Code 配置

创建 `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true,
        ".coverage": true,
        "htmlcov": true
    }
}
```

#### PyCharm 配置

1. 设置 Python 解释器为虚拟环境
2. 配置代码格式化工具 (Black)
3. 启用类型检查 (mypy)
4. 配置测试运行器 (pytest)

### 4. 开发工具

#### 代码质量工具

```bash
# 代码格式化
black src/ tests/

# 导入排序
isort src/ tests/

# 代码检查
flake8 src/ tests/

# 类型检查
mypy src/

# 安全检查
bandit -r src/
```

#### 预提交钩子

```bash
# 安装 pre-commit
pip install pre-commit

# 安装钩子
pre-commit install

# 手动运行
pre-commit run --all-files
```

## 📁 项目结构

```
dingo-marketing/
├── src/                    # 源代码目录
│   ├── agents/            # AI Agent 模块
│   ├── api/               # API 路由和模型
│   ├── config/            # 配置模块
│   ├── core/              # 核心基础设施
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务层
│   ├── tools/             # 工具模块
│   └── main.py            # 应用入口
├── tests/                 # 测试目录
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   ├── e2e/               # 端到端测试
│   └── fixtures/          # 测试数据
├── docs/                  # 文档目录
├── scripts/               # 脚本目录
├── .github/               # GitHub 工作流
├── requirements.txt       # 生产依赖
├── requirements-dev.txt   # 开发依赖
├── Makefile               # 构建脚本
├── pytest.ini             # 测试配置
├── .env.example           # 环境变量示例
├── deploy.sh              # 部署脚本
├── run.py                 # 应用启动文件
└── README.md              # 项目说明
```

### 模块职责

| 模块 | 职责 | 主要文件 |
|------|------|----------|
| `agents/` | AI Agent 实现 | `marketing.py`, `data_analyst.py` |
| `api/` | API 接口 | `routes.py`, `models.py` |
| `config/` | 配置管理 | `settings.py`, `logging.py` |
| `core/` | 基础设施 | `database.py`, `redis_client.py` |
| `models/` | 数据模型 | `user.py`, `campaign.py` |
| `services/` | 业务逻辑 | `user_service.py`, `campaign_service.py` |
| `tools/` | 工具集成 | `github_tools.py`, `content_tools.py` |

## 🔄 开发工作流

### 1. 功能开发流程

<div class="mermaid">
graph LR
    A[创建分支] --> B[开发功能]
    B --> C[编写测试]
    C --> D[运行测试]
    D --> E[代码审查]
    E --> F[合并主分支]
    F --> G[部署测试]
</div>

### 2. Git 工作流

#### 分支命名规范

```bash
# 功能分支
feature/user-analysis-enhancement

# 修复分支
fix/github-api-rate-limit

# 热修复分支
hotfix/critical-security-patch

# 发布分支
release/v1.2.0
```

#### 提交信息规范

```bash
# 格式: <type>(<scope>): <description>

# 示例
feat(agents): add content creator agent
fix(api): resolve rate limiting issue
docs(readme): update installation guide
test(tools): add github tools unit tests
refactor(core): improve database connection handling
```

### 3. 开发步骤

#### 创建新功能

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发功能
# 编写代码...

# 3. 运行测试
make test

# 4. 代码检查
make lint

# 5. 提交代码
git add .
git commit -m "feat(module): add new feature"

# 6. 推送分支
git push origin feature/new-feature

# 7. 创建 Pull Request
```

#### 添加新的 Agent

```python
# 1. 创建 Agent 类
# src/agents/new_agent.py
from .base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="新角色",
            goal="实现特定目标",
            backstory="角色背景故事"
        )
    
    async def execute_task(self, task_data: dict) -> dict:
        # 实现具体逻辑
        pass

# 2. 添加到营销团队
# src/agents/marketing.py
from .new_agent import NewAgent

class MarketingCrew:
    def __init__(self):
        self.new_agent = NewAgent()
        # ...

# 3. 编写测试
# tests/unit/agents/test_new_agent.py
import pytest
from src.agents.new_agent import NewAgent

class TestNewAgent:
    def test_agent_initialization(self):
        agent = NewAgent()
        assert agent.role == "新角色"
    
    async def test_execute_task(self):
        agent = NewAgent()
        result = await agent.execute_task({})
        assert result is not None
```

#### 添加新的工具

```python
# 1. 创建工具类
# src/tools/new_tool.py
from .base_tool import BaseTool

class NewTool(BaseTool):
    name = "new_tool"
    description = "工具描述"
    
    async def _run(self, **kwargs) -> str:
        # 实现工具逻辑
        return "工具执行结果"

# 2. 注册工具
# src/tools/__init__.py
from .new_tool import NewTool

__all__ = ["NewTool"]

# 3. 在 Agent 中使用
# src/agents/some_agent.py
from src.tools.new_tool import NewTool

class SomeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            tools=[NewTool()]
        )
```

#### 添加新的 API 端点

```python
# 1. 定义 API 模型
# src/api/models.py
from pydantic import BaseModel

class NewRequest(BaseModel):
    param1: str
    param2: int

class NewResponse(BaseModel):
    result: str
    status: str

# 2. 实现路由
# src/api/routes.py
from fastapi import APIRouter
from .models import NewRequest, NewResponse

router = APIRouter()

@router.post("/new-endpoint", response_model=NewResponse)
async def new_endpoint(request: NewRequest):
    # 处理逻辑
    return NewResponse(
        result="处理结果",
        status="success"
    )

# 3. 编写测试
# tests/unit/api/test_routes.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_new_endpoint():
    response = client.post(
        "/api/v1/new-endpoint",
        json={"param1": "test", "param2": 123}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

## 📏 代码规范

### 1. Python 代码规范

#### PEP 8 规范

```python
# 好的示例
class UserAnalyzer:
    """用户分析器类"""
    
    def __init__(self, github_token: str):
        self.github_token = github_token
        self.api_client = GitHubAPI(token=github_token)
    
    async def analyze_user(self, username: str) -> UserProfile:
        """分析单个用户"""
        try:
            user_data = await self.api_client.get_user(username)
            return self._process_user_data(user_data)
        except APIError as e:
            logger.error(f"Failed to analyze user {username}: {e}")
            raise
    
    def _process_user_data(self, data: dict) -> UserProfile:
        """处理用户数据"""
        return UserProfile(
            username=data["login"],
            followers=data["followers"],
            public_repos=data["public_repos"]
        )

# 避免的示例
class useranalyzer:  # 类名应该使用 PascalCase
    def __init__(self,token):  # 缺少类型注解和空格
        self.token=token  # 缺少空格
    
    def analyzeUser(self,username):  # 方法名应该使用 snake_case
        data=self.api.getUser(username)  # 缺少空格
        return data  # 缺少错误处理
```

#### 类型注解

```python
from typing import List, Dict, Optional, Union
from pydantic import BaseModel

# 函数类型注解
async def analyze_users(
    usernames: List[str],
    options: Optional[Dict[str, Any]] = None
) -> List[UserProfile]:
    """分析多个用户"""
    results = []
    for username in usernames:
        profile = await analyze_user(username)
        results.append(profile)
    return results

# 类属性类型注解
class Campaign(BaseModel):
    id: str
    name: str
    target_users: List[str]
    content: Optional[str] = None
    status: Union[str, int] = "pending"
```

#### 文档字符串

```python
def calculate_engagement_score(
    likes: int,
    comments: int,
    shares: int,
    followers: int
) -> float:
    """
    计算用户互动评分
    
    Args:
        likes: 点赞数
        comments: 评论数
        shares: 分享数
        followers: 粉丝数
    
    Returns:
        float: 互动评分 (0-100)
    
    Raises:
        ValueError: 当输入参数为负数时
    
    Example:
        >>> score = calculate_engagement_score(100, 20, 5, 1000)
        >>> print(f"Engagement score: {score:.2f}")
        Engagement score: 12.50
    """
    if any(x < 0 for x in [likes, comments, shares, followers]):
        raise ValueError("All parameters must be non-negative")
    
    if followers == 0:
        return 0.0
    
    engagement = (likes + comments * 2 + shares * 3) / followers * 100
    return min(engagement, 100.0)
```

### 2. 错误处理

```python
import logging
from typing import Optional
from src.core.exceptions import APIError, ValidationError

logger = logging.getLogger(__name__)

class GitHubService:
    async def get_user_repos(self, username: str) -> Optional[List[dict]]:
        """获取用户仓库列表"""
        try:
            # 参数验证
            if not username or not username.strip():
                raise ValidationError("Username cannot be empty")
            
            # API 调用
            response = await self.api_client.get(f"/users/{username}/repos")
            
            # 响应验证
            if response.status_code == 404:
                logger.warning(f"User {username} not found")
                return None
            
            response.raise_for_status()
            return response.json()
            
        except ValidationError:
            # 重新抛出验证错误
            raise
        except requests.RequestException as e:
            # 网络错误处理
            logger.error(f"Network error when fetching repos for {username}: {e}")
            raise APIError(f"Failed to fetch repositories: {e}")
        except Exception as e:
            # 未预期错误处理
            logger.error(f"Unexpected error in get_user_repos: {e}")
            raise APIError(f"Unexpected error: {e}")
```

### 3. 异步编程规范

```python
import asyncio
from typing import List
import aiohttp

class AsyncUserAnalyzer:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def analyze_users_batch(self, usernames: List[str]) -> List[dict]:
        """批量分析用户"""
        tasks = []
        for username in usernames:
            task = self._analyze_user_with_semaphore(username)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        successful_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Failed to analyze {usernames[i]}: {result}")
            else:
                successful_results.append(result)
        
        return successful_results
    
    async def _analyze_user_with_semaphore(self, username: str) -> dict:
        """使用信号量限制并发的用户分析"""
        async with self.semaphore:
            return await self._analyze_single_user(username)
    
    async def _analyze_single_user(self, username: str) -> dict:
        """分析单个用户"""
        async with self.session.get(f"/users/{username}") as response:
            response.raise_for_status()
            return await response.json()

# 使用示例
async def main():
    usernames = ["user1", "user2", "user3"]
    
    async with AsyncUserAnalyzer() as analyzer:
        results = await analyzer.analyze_users_batch(usernames)
        print(f"Analyzed {len(results)} users")

# 运行
if __name__ == "__main__":
    asyncio.run(main())
```

## 🧪 测试指南

### 1. 测试结构

```
tests/
├── unit/                  # 单元测试
│   ├── agents/           # Agent 测试
│   ├── api/              # API 测试
│   ├── core/             # 核心模块测试
│   ├── services/         # 服务测试
│   └── tools/            # 工具测试
├── integration/          # 集成测试
│   ├── test_api_integration.py
│   └── test_database_integration.py
├── e2e/                  # 端到端测试
│   └── test_user_journey.py
├── fixtures/             # 测试数据
│   ├── users.json
│   └── campaigns.json
└── conftest.py           # pytest 配置
```

### 2. 单元测试示例

```python
# tests/unit/agents/test_data_analyst.py
import pytest
from unittest.mock import AsyncMock, patch
from src.agents.data_analyst import DataAnalyst
from src.tools.github_tools import GitHubTool

class TestDataAnalyst:
    @pytest.fixture
    def data_analyst(self):
        """创建数据分析师实例"""
        return DataAnalyst()
    
    @pytest.fixture
    def mock_github_data(self):
        """模拟 GitHub 数据"""
        return {
            "login": "testuser",
            "followers": 100,
            "following": 50,
            "public_repos": 20
        }
    
    def test_agent_initialization(self, data_analyst):
        """测试 Agent 初始化"""
        assert data_analyst.role == "数据分析师"
        assert "GitHub" in data_analyst.goal
        assert len(data_analyst.tools) > 0
    
    @patch('src.tools.github_tools.GitHubTool.get_user')
    async def test_analyze_user_success(self, mock_get_user, data_analyst, mock_github_data):
        """测试成功分析用户"""
        # 设置模拟
        mock_get_user.return_value = mock_github_data
        
        # 执行测试
        result = await data_analyst.analyze_user("testuser")
        
        # 验证结果
        assert result["username"] == "testuser"
        assert result["followers"] == 100
        assert "analysis" in result
        mock_get_user.assert_called_once_with("testuser")
    
    @patch('src.tools.github_tools.GitHubTool.get_user')
    async def test_analyze_user_not_found(self, mock_get_user, data_analyst):
        """测试用户不存在的情况"""
        # 设置模拟抛出异常
        mock_get_user.side_effect = Exception("User not found")
        
        # 执行测试并验证异常
        with pytest.raises(Exception, match="User not found"):
            await data_analyst.analyze_user("nonexistent")
    
    @pytest.mark.parametrize("followers,expected_tier", [
        (0, "新手"),
        (100, "活跃"),
        (1000, "影响者"),
        (10000, "专家")
    ])
    async def test_user_tier_classification(self, data_analyst, followers, expected_tier):
        """测试用户等级分类"""
        tier = data_analyst._classify_user_tier(followers)
        assert tier == expected_tier
```

### 3. 集成测试示例

```python
# tests/integration/test_api_integration.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import get_database

class TestAPIIntegration:
    @pytest.fixture(scope="class")
    def client(self):
        """创建测试客户端"""
        return TestClient(app)
    
    @pytest.fixture(scope="class")
    async def setup_database(self):
        """设置测试数据库"""
        # 创建测试数据
        async with get_database() as db:
            # 插入测试数据
            pass
        yield
        # 清理测试数据
        async with get_database() as db:
            # 删除测试数据
            pass
    
    def test_health_check(self, client):
        """测试健康检查端点"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_analyze_users_endpoint(self, client, setup_database):
        """测试用户分析端点"""
        request_data = {
            "usernames": ["testuser1", "testuser2"],
            "analysis_type": "comprehensive"
        }
        
        response = client.post("/api/v1/analyze/users", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "results" in data["data"]
        assert len(data["data"]["results"]) == 2
    
    def test_create_campaign_endpoint(self, client, setup_database):
        """测试创建营销活动端点"""
        campaign_data = {
            "name": "测试活动",
            "target_users": ["user1", "user2"],
            "campaign_type": "content"
        }
        
        response = client.post("/api/v1/campaigns/content", json=campaign_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "campaign_id" in data["data"]
```

### 4. 端到端测试示例

```python
# tests/e2e/test_user_journey.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app

class TestUserJourney:
    @pytest.fixture(scope="class")
    def client(self):
        return TestClient(app)
    
    def test_complete_marketing_workflow(self, client):
        """测试完整的营销工作流程"""
        # 1. 分析目标用户
        analysis_response = client.post("/api/v1/analyze/users", json={
            "usernames": ["target_user1", "target_user2"]
        })
        assert analysis_response.status_code == 200
        
        # 2. 创建营销活动
        campaign_response = client.post("/api/v1/campaigns/comprehensive", json={
            "name": "端到端测试活动",
            "target_users": ["target_user1", "target_user2"],
            "content_type": "technical"
        })
        assert campaign_response.status_code == 201
        campaign_id = campaign_response.json()["data"]["campaign_id"]
        
        # 3. 检查活动状态
        status_response = client.get(f"/api/v1/campaigns/{campaign_id}/status")
        assert status_response.status_code == 200
        
        # 4. 获取活动结果
        # 等待活动完成（在实际测试中可能需要轮询）
        import time
        time.sleep(5)
        
        result_response = client.get(f"/api/v1/campaigns/{campaign_id}")
        assert result_response.status_code == 200
        
        result_data = result_response.json()["data"]
        assert "content" in result_data
        assert "engagement_plan" in result_data
```

### 5. 测试配置

```python
# tests/conftest.py
import pytest
import asyncio
from unittest.mock import AsyncMock
import os

# 设置测试环境变量
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///test.db"

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_openai_client():
    """模拟 OpenAI 客户端"""
    mock_client = AsyncMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = "模拟响应"
    return mock_client

@pytest.fixture
def mock_github_api():
    """模拟 GitHub API"""
    mock_api = AsyncMock()
    mock_api.get_user.return_value = {
        "login": "testuser",
        "followers": 100,
        "public_repos": 20
    }
    return mock_api

@pytest.fixture(autouse=True)
async def setup_test_database():
    """自动设置测试数据库"""
    # 创建测试表
    # ...
    yield
    # 清理测试数据
    # ...
```

### 6. 运行测试

```bash
# 运行所有测试
make test

# 运行特定测试
pytest tests/unit/agents/test_data_analyst.py

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html

# 运行测试并显示详细输出
pytest -v -s

# 运行特定标记的测试
pytest -m "slow"

# 并行运行测试
pytest -n auto
```

## 🐛 调试指南

### 1. 日志配置

```python
# src/config/logging.py
import logging
import sys
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: str = None):
    """设置日志配置"""
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    handlers = [console_handler]
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    
    # 配置根日志器
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=handlers
    )
    
    # 设置第三方库日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
```

### 2. 调试技巧

#### 使用 pdb 调试

```python
import pdb

async def analyze_user(username: str):
    """分析用户"""
    try:
        # 设置断点
        pdb.set_trace()
        
        user_data = await get_user_data(username)
        analysis = process_user_data(user_data)
        
        return analysis
    except Exception as e:
        # 异常时进入调试器
        pdb.post_mortem()
        raise
```

#### 使用 logging 调试

```python
import logging

logger = logging.getLogger(__name__)

async def complex_analysis(data: dict):
    """复杂分析函数"""
    logger.debug(f"Starting analysis with data: {data}")
    
    try:
        # 记录中间步骤
        step1_result = await step1(data)
        logger.info(f"Step 1 completed: {len(step1_result)} items")
        
        step2_result = await step2(step1_result)
        logger.info(f"Step 2 completed: {step2_result['status']}")
        
        final_result = await step3(step2_result)
        logger.info(f"Analysis completed successfully")
        
        return final_result
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise
```

#### 性能调试

```python
import time
import functools
from typing import Callable

def timing_decorator(func: Callable):
    """性能计时装饰器"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"{func.__name__} took {duration:.2f} seconds")
    return wrapper

@timing_decorator
async def slow_function():
    """耗时函数"""
    await asyncio.sleep(2)
    return "完成"
```

### 3. 常见问题排查

#### API 调用失败

```python
import httpx
import logging

logger = logging.getLogger(__name__)

async def debug_api_call(url: str, **kwargs):
    """调试 API 调用"""
    logger.debug(f"Making request to: {url}")
    logger.debug(f"Request params: {kwargs}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, **kwargs)
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            
            if response.status_code >= 400:
                logger.error(f"API error: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        raise
```

#### 数据库连接问题

```python
import asyncpg
import logging

logger = logging.getLogger(__name__)

async def debug_database_connection(database_url: str):
    """调试数据库连接"""
    try:
        logger.info("Attempting to connect to database...")
        
        conn = await asyncpg.connect(database_url)
        logger.info("Database connection successful")
        
        # 测试查询
        result = await conn.fetchval("SELECT version()")
        logger.info(f"Database version: {result}")
        
        await conn.close()
        logger.info("Database connection closed")
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
```

## ⚡ 性能优化

### 1. 异步优化

```python
import asyncio
from typing import List
import aiohttp

# 优化前：串行处理
async def analyze_users_serial(usernames: List[str]):
    """串行分析用户（慢）"""
    results = []
    for username in usernames:
        result = await analyze_single_user(username)
        results.append(result)
    return results

# 优化后：并行处理
async def analyze_users_parallel(usernames: List[str], max_concurrent: int = 10):
    """并行分析用户（快）"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def analyze_with_limit(username: str):
        async with semaphore:
            return await analyze_single_user(username)
    
    tasks = [analyze_with_limit(username) for username in usernames]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 过滤异常结果
    successful_results = [r for r in results if not isinstance(r, Exception)]
    return successful_results
```

### 2. 缓存优化

```python
import redis
import json
import hashlib
from typing import Optional, Any
from functools import wraps

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
    
    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """生成缓存键"""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        try:
            data = await self.redis.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """设置缓存"""
        try:
            await self.redis.setex(key, ttl, json.dumps(value))
        except Exception:
            pass  # 缓存失败不影响主流程

def cached(ttl: int = 3600, prefix: str = "cache"):
    """缓存装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_manager = CacheManager("redis://localhost:6379")
            cache_key = cache_manager.cache_key(prefix, *args, **kwargs)
            
            # 尝试从缓存获取
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# 使用示例
@cached(ttl=1800, prefix="user_analysis")
async def analyze_user_cached(username: str):
    """带缓存的用户分析"""
    return await analyze_user(username)
```

### 3. 数据库优化

```python
import asyncpg
from typing import List, Dict
import asyncio

class DatabaseOptimizer:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None
    
    async def init_pool(self, min_size: int = 10, max_size: int = 20):
        """初始化连接池"""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=min_size,
            max_size=max_size
        )
    
    async def batch_insert(self, table: str, records: List[Dict]):
        """批量插入优化"""
        if not records:
            return
        
        # 构建批量插入语句
        columns = list(records[0].keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(columns))])
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # 准备数据
        values_list = []
        for record in records:
            values = [record[col] for col in columns]
            values_list.append(values)
        
        # 批量执行
        async with self.pool.acquire() as conn:
            await conn.executemany(query, values_list)
    
    async def bulk_select(self, query: str, params_list: List[tuple]):
        """批量查询优化"""
        async with self.pool.acquire() as conn:
            # 使用 prepared statement
            stmt = await conn.prepare(query)
            
            tasks = []
            for params in params_list:
                task = stmt.fetch(*params)
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            return results
```

## ❓ 常见问题

### 1. 环境问题

#### Q: 虚拟环境创建失败
```bash
# 解决方案
python -m venv --clear venv
source venv/bin/activate
pip install --upgrade pip
```

#### Q: 依赖安装失败
```bash
# 解决方案
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

### 2. 开发问题

#### Q: 导入模块失败
```python
# 问题：ModuleNotFoundError: No module named 'src'

# 解决方案1：设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# 解决方案2：使用相对导入
from ..core.database import get_database

# 解决方案3：安装为可编辑包
pip install -e .
```

#### Q: 异步函数调用问题
```python
# 问题：RuntimeError: This event loop is already running

# 解决方案：使用 asyncio.create_task
async def main():
    task = asyncio.create_task(async_function())
    result = await task

# 或者使用 nest_asyncio（测试环境）
import nest_asyncio
nest_asyncio.apply()
```

### 3. 测试问题

#### Q: 测试数据库隔离
```python
# 解决方案：使用事务回滚
@pytest.fixture
async def db_transaction():
    async with get_database() as conn:
        trans = conn.transaction()
        await trans.start()
        try:
            yield conn
        finally:
            await trans.rollback()
```

#### Q: 异步测试超时
```python
# 解决方案：设置超时时间
@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_long_running_function():
    result = await long_running_function()
    assert result is not None
```

## 🤝 贡献指南

### 1. 贡献流程

1. **Fork 项目**
2. **创建功能分支**
3. **编写代码和测试**
4. **运行代码检查**
5. **提交 Pull Request**
6. **代码审查**
7. **合并代码**

### 2. Pull Request 模板

```markdown
## 变更描述
简要描述本次变更的内容和目的。

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 性能优化
- [ ] 重构
- [ ] 其他

## 测试
- [ ] 添加了新的测试
- [ ] 所有测试通过
- [ ] 手动测试通过

## 检查清单
- [ ] 代码符合项目规范
- [ ] 添加了必要的文档
- [ ] 更新了 CHANGELOG
- [ ] 没有引入破坏性变更

## 相关 Issue
关联的 Issue 编号：#123

## 截图（如适用）
如果有 UI 变更，请提供截图。
```

### 3. 代码审查标准

- **功能正确性**：代码是否实现了预期功能
- **代码质量**：是否遵循项目规范和最佳实践
- **测试覆盖**：是否有足够的测试覆盖
- **性能影响**：是否对性能有负面影响
- **安全性**：是否引入安全风险
- **文档完整性**：是否有必要的文档更新

---

*本文档将随着项目的发展持续更新。如有问题，请提交 Issue 或联系维护团队。* 