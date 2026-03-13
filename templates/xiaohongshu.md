# 小红书文案模板

## 风格规则

- 全文中文
- 语气专业但易读，面向技术人群（开发者、AI 从业者）
- 生成 3 个版本：(1) 技术向，(2) 场景向，(3) 简短版
- 不要过度使用 emoji，最多在标题或关键位置少量使用
- 每个版本结尾附带标签（从项目配置 platforms.xiaohongshu.tags 读取）
- 始终包含：项目名、版本号、安装命令、GitHub 地址
- 如有 SaaS URL，作为首要亮点

## 版本 1：技术向

```
**{项目名} {版本} 发布 — {标题}**

[1-2 句项目介绍]

[如有 SaaS，先介绍平台]

[核心新功能，每个一小段]

安装：{install_command}
GitHub：{repo}

#{tags}
```

## 版本 2：场景向

```
**{场景化标题，以用户痛点切入}**

[描述痛点 -> 解决方案]

[新版本亮点列表，4-5 条]

{saas_url 或 install_command}

#{tags}
```

## 版本 3：简短版

```
**{项目名} {版本} | {一句话定位}**

[3-4 条亮点]

{install_command}
GitHub：{repo}

#{tags}
```

## 示例

参考：dingo/docs/posts/v2.1.0_xiaohongshu.md
