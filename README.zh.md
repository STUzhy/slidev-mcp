
<div align="center">
  <h1>
    <img src="https://api.iconify.design/logos:slidev.svg" width="40" height="40" alt="Slidev"/>
    slidev-mcp 
    <img src="https://api.iconify.design/logos:openai-icon.svg" width="40" height="40" alt="AI"/>
  </h1>
  <p>让 AI 帮你轻松创建专业幻灯片演示！</p>
  
  <p>
    <a href="README.md">English</a> | <strong>中文</strong>
  </p>
  
  <div>
    <img src="https://img.shields.io/badge/Slidev-@latest-blue?logo=slidev" alt="Slidev"/>
    <img src="https://img.shields.io/badge/AI-大模型-orange?logo=openai" alt="AI"/>
    <img src="https://img.shields.io/badge/TypeScript-4.9.5-blue?logo=typescript" alt="TypeScript"/>
    <img src="https://img.shields.io/badge/Vue-3.3-green?logo=vue.js" alt="Vue 3"/>
  </div>
</div>

## ✨ 项目介绍

slidev-mcp 是一个基于 [Slidev](https://github.com/slidevjs/slidev) 的智能幻灯片生成工具，通过集成大语言模型技术，让用户只需简单描述需求，即可自动生成专业的在线PPT演示文稿。

<img src="https://api.iconify.design/mdi:robot-happy-outline.svg" width="20" height="20" alt="AI"/> **核心价值**：
- 大幅降低 Slidev 使用门槛
- 自然语言交互式创建幻灯片
- 自动化生成专业级演示文稿


## 🚀 快速开始

详细的设置和使用说明，请查看[快速开始指南](docs/quickstart.zh.md)。

## 🔧 可用工具

MCP 服务器提供以下工具用于幻灯片创建和管理：

### 环境与项目管理

| 工具名称 | 输入参数 | 输出结果 | 作用 |
|---------|---------|---------|------|
| `check_environment` | 无 | 环境状态和版本信息 | 验证依赖项是否已安装 |
| `create_slidev` | `path` (字符串), `title` (字符串), `author` (字符串) | 项目创建状态和路径 | 初始化新的 Slidev 项目 |
| `load_slidev` | `path` (字符串) | 项目内容和幻灯片数据 | 加载现有演示文稿 |

### 幻灯片内容管理

| 工具名称 | 输入参数 | 输出结果 | 作用 |
|---------|---------|---------|------|
| `make_cover` | `title` (字符串), `subtitle` (字符串, 可选), `author` (字符串, 可选), `background` (字符串, 可选), `python_string_template` (字符串, 可选) | 封面创建状态 | 创建/更新封面页 |
| `add_page` | `content` (字符串), `layout` (字符串, 可选) | 新幻灯片索引 | 向演示文稿添加新幻灯片 |
| `set_page` | `index` (整数), `content` (字符串), `layout` (字符串, 可选) | 更新状态 | 修改现有幻灯片内容 |
| `get_page` | `index` (整数) | Markdown 格式的幻灯片内容 | 获取指定幻灯片内容 |

### 实用工具

| 工具名称 | 输入参数 | 输出结果 | 作用 |
|---------|---------|---------|------|
| `websearch` | `url` (字符串) | 提取的 Markdown 文本 | 从网络收集幻灯片内容 |
| `get_slidev_usage` | 无 | Slidev 布局指南和模板 | 提供布局文档参考 |
| `start_slidev` | 无 | 服务器启动命令字符串 | 启动演示文稿服务器 |

### AI 助手

| 工具名称 | 输入参数 | 输出结果 | 作用 |
|---------|---------|---------|------|
| `guide` | 无 | 系统提示 | 指导 AI 有效使用工具 |

> **注释**: `可选` = 可选参数

## 📄 开源协议

MIT License © 2023 [LSTM-Kirigaya](https://github.com/LSTM-Kirigaya)
