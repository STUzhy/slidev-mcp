# 快速开始指南

## 前置依赖

首先，请先确保您的系统已经安装满足如下要求的软件。

|软件名称|版本要求|说明|
| -- | -- | -- |
|Python|>=3.13|运行 MCP 服务器的基础环境|
|Node.js|>=18.0|Slidev 运行环境|
|UV|-|Python 包管理工具|

### 安装软件

#### 1. 安装 Python（>=3.13）
- 访问 [Python 官网](https://www.python.org/downloads/) 下载并安装最新版本
- 安装时请勾选"Add Python to PATH"选项

#### 2. 安装 UV
```bash
# Windows
pip install uv

# 或者使用官方安装脚本（Linux/macOS）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. 安装 Node.js（>=20.0）
- 访问 [Node.js 官网](https://nodejs.org/) 下载并安装 LTS 版本
- 安装完成后在命令行中运行 `node --version` 验证安装


## 安装项目依赖

### 1. 创建虚拟环境

首先创建虚拟环境，如果您不需要虚拟环境可以跳过该步骤。

```bash
uv venv # 创建虚拟环境
```

### 2. 激活虚拟环境

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS  
source .venv/bin/activate
```

### 3. 安装 Python 依赖

```bash
uv sync  # 安装项目依赖
```

### 4. 安装 Slidev CLI

```bash
npm install -g @slidev/cli
```

## 验证安装

### 1. 检查环境

运行以下命令检查所有依赖是否正确安装：

```bash
# 检查 Python 版本
python --version

# 检查 Node.js 版本  
node --version

# 检查 UV
uv --version

# 检查 Slidev CLI
slidev --version
```

### 2. 测试 MCP 服务器

```bash
# 激活虚拟环境（如果使用）
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# 运行 MCP 服务器
uv run main.py
```

如果没有报错，说明服务器启动成功。



## 使用指南

### 开发模式

如果您想要进行开发或调试，推荐使用 [OpenMCP](https://marketplace.visualstudio.com/items?itemName=kirigaya.openmcp)：

1. 下载OpenMCP VScode插件。
2. 打开 OpenMCP 插件。
3. 新建MCPServer，选择stdio，命令输入`uv --directory E:\\node-project\\slidev-mcp run main.py`。 

> **注意**: 请将路径 `E:\\node-project\\slidev-mcp` 替换为您实际的项目路径。


### 生产使用

对于日常使用，建议使用 Claude Desktop：

在 Claude Desktop 的配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "slidev-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "E:\\node-project\\slidev-mcp",
        "run",
        "main.py"
      ],
      "description": "AI-powered Slidev slide creation tool"
    }
  }
}
```

> **注意**: 请将路径 `E:\\node-project\\slidev-mcp` 替换为您实际的项目路径。

## 更多功能

安装完成后，您可以：

- 使用自然语言创建幻灯片
- 自动生成专业的 Slidev 演示文稿
- 利用 AI 辅助进行内容编写
- 自定义幻灯片主题和布局

更多使用方法请参考项目的 [README 文档](../README.zh.md)。