# Dingo Marketing 前端界面

## 📖 简介

这是 Dingo Marketing AI 营销系统的 Web 前端界面，提供了直观易用的图形化操作界面，让非技术用户也能轻松使用 AI 营销功能。

## 🎨 设计特色

- **简洁现代**：参考 YouWare 设计风格，采用绿色主题色
- **响应式布局**：支持桌面和移动设备
- **交互友好**：模态框操作，实时状态反馈
- **功能完整**：覆盖所有核心营销功能

## 🚀 快速开始

### 1. 启动后端服务

确保 Dingo Marketing 后端服务正在运行：

```bash
# 在项目根目录
python main.py
```

后端服务将在 `http://localhost:8080` 启动。

### 2. 部署前端

#### 方法一：直接打开（推荐）

```bash
# 进入前端目录
cd frontend

# 直接用浏览器打开
open index.html
# 或者在 Windows 上
start index.html
```

#### 方法二：使用 HTTP 服务器

```bash
# 使用 Python 内置服务器
cd frontend
python -m http.server 3000

# 或使用 Node.js
npx serve .
```

然后在浏览器中访问 `http://localhost:3000`

## 🎯 功能说明

### 主要功能模块

1. **🔍 用户分析**
   - 分析 GitHub 用户技术背景
   - 评估社区影响力
   - 支持中英文报告

2. **✨ AI 内容生成**
   - 博客文章生成
   - 社交媒体内容
   - 邮件营销文案
   - 技术文档

3. **🤝 社区互动**
   - GitHub 自动化互动
   - 关注、点赞、评论
   - 社区关系管理

4. **📈 营销活动**
   - 完整营销工作流
   - 多代理协作
   - 效果跟踪分析

### 操作流程

1. **点击功能卡片**：选择要使用的功能
2. **填写表单**：输入必要的参数信息
3. **提交任务**：系统自动处理请求
4. **查看结果**：获取任务执行结果

## 🔧 配置说明

### API 地址配置

前端默认连接到 `http://localhost:8080/api/v1`，如需修改：

```javascript
// 在 script.js 中修改
const API_BASE_URL = 'http://your-api-server:port/api/v1';
```

### 功能开关

可以通过修改 HTML 和 CSS 来启用/禁用特定功能：

```html
<!-- 隐藏某个功能卡片 -->
<div class="feature-card" data-type="analyze" style="display: none;">
```

## 📱 响应式设计

界面支持多种设备：

- **桌面端**：完整功能展示
- **平板端**：自适应布局
- **手机端**：简化导航，垂直布局

## 🎨 自定义样式

### 主题色修改

在 `styles.css` 中修改主题色：

```css
:root {
  --primary-color: #059669;  /* 主色调 */
  --primary-hover: #047857; /* 悬停色 */
}
```

### 布局调整

- 修改 `.features-grid` 调整卡片布局
- 修改 `.hero` 调整首页展示
- 修改 `.modal` 调整弹窗样式

## 🔍 故障排除

### 常见问题

1. **API 连接失败**
   - 检查后端服务是否启动
   - 确认 API 地址配置正确
   - 检查浏览器控制台错误信息

2. **功能按钮无响应**
   - 检查 JavaScript 是否正确加载
   - 确认浏览器支持现代 JavaScript 特性

3. **样式显示异常**
   - 检查 CSS 文件是否正确加载
   - 确认字体文件网络连接正常

### 调试模式

打开浏览器开发者工具（F12）查看：
- **Console**：JavaScript 错误信息
- **Network**：API 请求状态
- **Elements**：DOM 结构和样式

## 📄 文件结构

```
frontend/
├── index.html      # 主页面
├── styles.css      # 样式文件
├── script.js       # 交互逻辑
└── README.md       # 说明文档
```

## 🤝 贡献指南

欢迎提交改进建议：

1. 界面优化建议
2. 新功能需求
3. 用户体验改进
4. 浏览器兼容性问题

## 📞 技术支持

如遇问题，请：

1. 查看浏览器控制台错误
2. 检查后端服务日志
3. 提交 Issue 描述问题详情 