# Dingo Marketing

AI-powered marketing automation platform for GitHub-based projects.

## 🚀 核心功能

- **智能用户分析**: 基于 GitHub 活动分析用户行为和兴趣
- **自动内容生成**: 使用 AI 生成个性化营销内容
- **社区互动建议**: 智能推荐最佳互动策略
- **营销活动自动化**: 自动执行营销任务和跟进

## 📋 部署特点

- **本地优先**: 支持简单的本地部署，无需复杂配置
- **轻量级**: 最小化依赖，快速启动
- **易于配置**: 简单的环境变量配置

## 🏃‍♂️ 快速开始

### 环境要求

- Python 3.10+ (推荐 3.12)
- Git

### 1. 克隆项目

```bash
git clone https://github.com/your-username/dingo-marketing.git
cd dingo-marketing
```

### 2. 安装依赖

```bash
# 使用 pip 安装依赖
pip install -r requirements.txt

# 或者使用 conda 环境 (推荐)
conda create -n dingo-marketing python=3.12 -y
conda activate dingo-marketing
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑 .env 文件，填入必要的 API 密钥
# 必需配置：
# - OPENAI_API_KEY: OpenAI API 密钥
# - GITHUB_TOKEN: GitHub 个人访问令牌
# - DATABASE_URL: 数据库连接 URL (默认使用 SQLite)

# 可选配置：
# - REDIS_URL: Redis 连接 URL
# - TWITTER_API_KEY: Twitter API 密钥 (用于社交媒体功能)
```

**重要提示**: 
- 请确保在 `.env` 文件中设置正确的 `OPENAI_API_KEY` 和 `GITHUB_TOKEN`
- 对于开发环境，使用轻量级的 JSON 文件存储（基于 SQLite 配置自动转换）
- 系统使用内存缓存，无需安装 Redis
- 所有依赖都是轻量级的，启动速度快

### 4. 启动服务

```bash
# 启动本地服务
python run.py

# 开发模式 (自动重载)
python run.py --debug --reload

# 指定端口和主机
python run.py --host 0.0.0.0 --port 8080
```

### 5. 访问服务

- API 服务: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 🛠️ 管理命令

```bash
# 查看帮助
python run.py --help

# 启动服务 (生产模式)
python run.py --host 0.0.0.0 --port 8000

# 启动服务 (开发模式)
python run.py --debug --reload --log-level debug

# 后台运行
nohup python run.py --host 0.0.0.0 --port 8000 > logs/app.log 2>&1 &

# 查看进程
ps aux | grep "python run.py"

# 停止服务
pkill -f "python run.py"
```

## 📖 API 使用示例

### 分析 GitHub 用户

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/user" \
  -H "Content-Type: application/json" \
  -d '{"username": "octocat"}'
```

### 生成营销内容

```bash
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "social_post",
    "target_audience": "developers",
    "product": "your-product"
  }'
```

### 获取社区互动建议

```bash
curl -X POST "http://localhost:8000/api/v1/engagement/suggestions" \
  -H "Content-Type: application/json" \
  -d '{"repository": "owner/repo"}'
```

## 🔧 开发模式

```bash
# 开发模式启动 (自动重载)
python run.py --debug --reload

# 运行测试
pytest tests/

# 代码格式化
black src/
isort src/

# 代码检查
flake8 src/
```

## 📁 项目结构

```
dingo-marketing/
├── src/                    # 源代码
│   ├── agents/            # AI 代理
│   ├── api/               # API 路由
│   ├── config/            # 配置管理
│   ├── core/              # 核心功能
│   ├── models/            # 数据模型
│   ├── services/          # 业务服务
│   └── tools/             # 工具模块
├── tests/                 # 测试文件
├── docs/                  # 文档
├── logs/                  # 日志文件
├── run.py                 # 应用启动文件
└── requirements.txt       # Python 依赖
```

## ⚙️ 配置说明

主要环境变量 (`.env` 文件):

```bash
# 基础配置
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# AI 服务
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here
GITHUB_REPOSITORY=owner/repo

# 数据存储 (轻量级 JSON 文件)
DATABASE_URL=sqlite:///./dingo_marketing.db

# 应用配置
CAMPAIGN_MAX_DAILY_POSTS=10
CAMPAIGN_MIN_INTERVAL_MINUTES=60
```

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   python run.py --port 8001  # 使用其他端口
   ```

2. **Python 版本过低**
   ```bash
   python --version  # 确保 3.10+，推荐 3.12
   ```

3. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **API 密钥未配置**
   - 检查 `.env` 文件中的 `OPENAI_API_KEY` 和 `GITHUB_TOKEN`

5. **CrewAI 版本冲突**
   ```bash
   pip install --upgrade pydantic>=2.8.0
   pip install crewai==0.121.1
   ```

### 查看详细日志

```bash
# 启动时查看日志
python run.py --debug --log-level debug

# 后台运行时查看日志
tail -f logs/app.log
```

## 📊 性能指标

- 启动时间: < 5 秒
- 内存使用: < 200MB
- API 响应时间: < 2 秒
- 并发请求: 支持 10+ 并发

## 🔮 未来计划

- [ ] 支持更多 AI 模型
- [ ] 增加营销分析仪表板
- [ ] 集成更多社交媒体平台
- [ ] 添加 A/B 测试功能
- [ ] 支持多语言内容生成

## 📚 文档

- [架构设计](docs/ARCHITECTURE.md)
- [开发指南](docs/DEVELOPMENT.md)
- [API 文档](http://localhost:8000/docs) (服务启动后)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

**快速开始**: `pip install -r requirements.txt && python run.py` 