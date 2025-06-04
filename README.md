# Dingo Marketing

AI-powered marketing automation platform for GitHub-based projects.

## 🚀 核心功能

- **智能用户分析**: 基于 GitHub 活动分析用户行为和兴趣
- **自动内容生成**: 使用 AI 生成个性化营销内容
- **社区互动建议**: 智能推荐最佳互动策略
- **营销活动自动化**: 自动执行营销任务和跟进
- **市场调研**: 实时网络搜索、竞品分析、技术趋势监控、用户反馈分析

> 💡 **技术架构**: 了解系统的详细技术架构和设计理念，请参考 [架构设计文档](docs/ARCHITECTURE.md)

## 📋 部署特点

- **本地优先**: 支持简单的本地部署，无需复杂配置
- **轻量级**: 最小化依赖，快速启动
- **易于配置**: 简单的环境变量配置
- **实时数据**: 集成网络搜索，获取最新市场信息

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
# - OPENAI_API_KEY: AI服务API密钥（支持DeepSeek、Qwen、OpenAI等）
# - GITHUB_TOKEN: GitHub 个人访问令牌
# - GITHUB_REPOSITORY: 目标GitHub仓库

# 增强功能配置：
# - SERPER_API_KEY: 网络搜索API密钥 (用于实时市场调研)

# 可选配置：
# - TWITTER_API_KEY: Twitter API 密钥 (用于社交媒体功能)
# - LINKEDIN_API_KEY: LinkedIn API 密钥 (用于专业社交网络)
```

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

- API 服务: http://localhost:8080
- API 文档: http://localhost:8080/docs
- 健康检查: http://localhost:8080/api/v1/status

## 🖥️ Web 界面

为了让非技术用户也能轻松使用 AI 营销功能，我们提供了直观易用的 Web 界面。

### 启动 Web 界面

```bash
# 方法一：直接打开（推荐）
cd frontend
open index.html  # macOS
start index.html  # Windows

# 方法二：使用 HTTP 服务器
cd frontend
python -m http.server 3000
# 然后访问 http://localhost:3000
```

### 界面预览

![Dingo Marketing Web界面](docs/assets/demo_GUI.png)

*Web界面提供了直观的操作面板，支持用户分析、内容生成、社区互动等核心功能*

## 🛠️ 管理命令

```bash
# 查看帮助
python run.py --help

# 启动服务 (生产模式)
python run.py --host 0.0.0.0 --port 8080

# 启动服务 (开发模式)
python run.py --debug --reload --log-level debug

```

## 🚀 API 使用示例

### 🎯 核心使用场景

#### 场景一：自动化宣传推广
针对产品功能和潜在用户出现的地方，进行针对性的自动化扩大宣传。

**1. 综合营销活动 - 一站式推广解决方案**
```bash
curl -X POST "http://localhost:8080/api/v1/campaigns/comprehensive" \
  -H "Content-Type: application/json" \
  -d '{
    "target_users": ["目标用户1", "目标用户2"],
    "target_repositories": ["您的产品仓库"],
    "duration": "30天",
    "budget": "标准",
    "metrics": ["参与度", "转化率", "知名度"],
    "language": "zh"
  }'
```
**自动执行：** 用户分析 → 内容创作 → 社区互动 → 效果评估

**2. 社区精准互动 - 定向推广**
```bash
curl -X POST "http://localhost:8080/api/v1/community/engage" \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "目标项目/仓库名",
    "interaction_types": ["comment", "issue", "star", "follow"],
    "target_count": 20,
    "lookback_days": 30,
    "language": "zh"
  }'
```
**自动执行：** 识别目标用户 → 智能互动 → 建立关系 → 跟踪效果

**3. 内容营销活动 - 内容驱动推广**
```bash
curl -X POST "http://localhost:8080/api/v1/campaigns/content" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "产品推广活动",
    "target_audience": "Python开发者和数据工程师",
    "topics": ["数据质量", "Python工具", "开源项目"],
    "content_types": ["blog", "social", "email", "tutorial"],
    "duration": "2周",
    "keywords": ["数据质量", "Python", "开源"],
    "language": "zh"
  }'
```
**自动执行：** 内容策略制定 → 多类型内容生成 → 发布计划 → SEO优化

#### 场景二：市场调研分析
深入了解市场动态、竞争对手和用户需求，为产品决策提供数据支持。

**1. 竞争对手分析**
```bash
curl -X POST "http://localhost:8080/api/v1/research/enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "research_type": "competitor",
    "target": "Great Expectations",
    "depth": "medium",
    "language": "zh",
    "requirements": "重点关注功能对比和定价策略"
  }'
```

**2. 技术趋势研究**
```bash
curl -X POST "http://localhost:8080/api/v1/research/enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "research_type": "technology",
    "target": "数据质量评估工具",
    "depth": "deep",
    "language": "zh",
    "requirements": "分析最新技术发展和实现方案"
  }'
```

**3. 市场趋势分析**
```bash
curl -X POST "http://localhost:8080/api/v1/research/enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "research_type": "market",
    "target": "数据质量工具市场",
    "depth": "medium",
    "language": "zh",
    "requirements": "关注市场规模和增长趋势"
  }'
```

**4. 用户反馈分析**
```bash
curl -X POST "http://localhost:8080/api/v1/research/enhanced" \
  -H "Content-Type: application/json" \
  -d '{
    "research_type": "user_feedback",
    "target": "开源数据工具用户体验",
    "depth": "shallow",
    "language": "zh",
    "requirements": "收集用户痛点和需求建议"
  }'
```

### 🔧 辅助功能

#### 用户分析
```bash
# 快速用户画像分析
curl -X POST "http://localhost:8080/api/v1/analyze/users" \
  -H "Content-Type: application/json" \
  -d '{
    "user_list": ["octocat", "gvanrossum"],
    "analysis_depth": "basic",
    "language": "zh"
  }'
```

#### 内容生成
```bash
# 生成技术博客
curl -X POST "http://localhost:8080/api/v1/content/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "blog",
    "topic": "如何使用Dingo提升数据质量",
    "target_audience": "数据工程师",
    "language": "zh",
    "keywords": ["数据质量", "Python", "自动化"]
  }'
```

#### 系统状态检查
```bash
# 检查系统状态
curl http://localhost:8080/api/v1/status
```

### 💡 使用建议

#### 推广策略
1. **启动阶段**：使用综合营销活动进行全面推广
2. **增长阶段**：结合社区互动和内容营销持续扩大影响
3. **优化阶段**：基于市场调研结果调整推广策略

#### 调研深度选择
- `shallow`: 快速概览，适合日常监控
- `medium`: 标准分析，平衡效率和详细度  
- `deep`: 深度分析，适合重要决策

#### 语言和受众
- 根据目标市场选择合适的语言（zh/en）
- 明确指定目标受众的技术背景
- 使用相关的行业关键词提高精准度

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

## 🔮 功能支持

### 核心功能
- [x] 智能用户分析 (GitHub用户画像)
- [x] AI内容生成 (博客、社交媒体、邮件)
- [x] 社区互动自动化 (GitHub互动)
- [x] 营销活动管理 (综合营销策略)
- [x] Web界面 (用户友好的操作界面)
- [x] API接口 (RESTful API)
- [x] 多语言支持 (中文/英文)
- [x] **市场调研** (实时网络搜索、竞品分析、技术趋势)
- [x] **网络数据获取** (网页搜索、内容抓取、数据分析)

### 市场调研功能
- [x] **竞品分析** (产品功能对比、定价策略、用户评价)
- [x] **技术调研** (技术原理、实现方案、性能对比)
- [x] **市场趋势监控** (行业发展、市场规模、技术趋势)
- [x] **用户反馈分析** (用户评价、需求挖掘、满意度调研)
- [x] **实时网络搜索** (Google搜索集成、多语言支持)
- [x] **网页内容抓取** (智能内容提取、结构化数据)

### 技术架构
- [x] 多Agent协作系统 (CrewAI框架)
- [x] 模块化设计 (可扩展架构)
- [x] 配置管理 (环境变量配置)
- [x] 日志系统 (结构化日志)
- [x] 错误处理 (优雅的异常处理)
- [x] **网络集成** (Serper API、网页抓取)

### AI模型支持
- [x] DeepSeek API
- [x] Qwen API  
- [x] OpenAI API
- [ ] Claude API
- [ ] Gemini API
- [ ] 本地模型支持 (Ollama)

### 平台集成
- [x] GitHub (用户分析、社区互动)
- [x] **Google搜索** (实时信息获取)
- [x] **网页抓取** (内容提取和分析)
- [ ] Twitter/X (社交媒体营销)
- [ ] LinkedIn (专业社交网络)
- [ ] Discord (社区管理)
- [ ] Slack (团队协作)

### 内容类型
- [x] 技术博客文章
- [x] 社交媒体内容
- [x] 邮件营销内容
- [x] 技术文档
- [x] **市场调研报告** (竞品分析、趋势报告)
- [ ] 视频脚本
- [ ] 播客大纲
- [ ] 新闻稿

### 分析功能
- [x] 用户技术栈分析
- [x] 社区活跃度分析
- [x] 贡献者识别
- [x] **实时竞品分析** (功能对比、市场地位、定价策略)
- [x] **技术趋势监控** (技术发展、市场动态)
- [x] **用户反馈挖掘** (评价分析、需求识别)
- [x] **市场规模评估** (市场容量、增长趋势)
- [ ] 营销效果分析
- [ ] A/B测试支持
- [ ] 数据可视化仪表板

### 部署方式
- [x] 本地部署
- [x] 开发模式 (热重载)
- [ ] Docker容器化
- [ ] 云平台部署 (AWS/Azure/GCP)
- [ ] Kubernetes支持

### 用户体验
- [x] 直观的Web界面
- [x] 实时状态显示
- [x] 详细的执行报告
- [x] **结构化调研报告** (Markdown格式、易于阅读)
- [ ] 移动端适配
- [ ] 暗色主题
- [ ] 多用户支持
- [ ] 权限管理

### 开发工具
- [x] 交互式演示脚本 (`demo_scenarios.py`)
- [x] 系统状态监控
- [x] 配置管理工具
- [x] 日志系统
- [x] 错误处理机制
- [x] **API测试工具** (cURL示例、Postman集合)
- [ ] 单元测试框架
- [ ] 性能监控工具
- [ ] 代码质量检查

## 📚 文档

- [架构设计](docs/ARCHITECTURE.md)
- [开发指南](docs/DEVELOPMENT.md)
- [API 文档](http://localhost:8080/docs) (服务启动后)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request
