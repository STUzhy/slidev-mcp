<div align="center">
  <h1>
    <img src="https://api.iconify.design/logos:slidev.svg" width="40" height="40" alt="Slidev"/>
    slidev-mcp 
    <img src="https://api.iconify.design/logos:openai-icon.svg" width="40" height="40" alt="AI"/>
  </h1>
  <p>AI-powered Professional Slide Creation Made Easy!</p>
  
  <div>
    <img src="https://img.shields.io/badge/Slidev-@latest-blue?logo=slidev" alt="Slidev"/>
    <img src="https://img.shields.io/badge/AI-Large%20Language%20Model-orange?logo=openai" alt="AI"/>
    <img src="https://img.shields.io/badge/TypeScript-4.9.5-blue?logo=typescript" alt="TypeScript"/>
    <img src="https://img.shields.io/badge/Vue-3.3-green?logo=vue.js" alt="Vue 3"/>
  </div>
</div>

## ✨ Introduction

slidev-mcp is an intelligent slide generation tool based on [Slidev](https://github.com/slidevjs/slidev) that integrates large language model technology, allowing users to automatically generate professional online PPT presentations with simple descriptions.

<img src="https://api.iconify.design/mdi:robot-happy-outline.svg" width="20" height="20" alt="AI"/> **Key Features**:
- Dramatically lowers the barrier to using Slidev
- Natural language interactive slide creation
- Automated generation of professional presentations

## 🚀 Quick Start

1. **Install Python, UV and NodeJS**


2. configure
    ```json
    {
      "mcpServers": {
        "slidev-mcp": {
          "command": "/path/to/uv",
          "args": [
            "--directory",
            "/path/to/slidev-mcp",
            "run",
            "main.py"
          ],
          "description": ""
        }
      }
    }
    ```

3. Open Claude Desktop or other MCP client (such as OpenMCP, Cherry Studio)

## 🛠️ Developement

1. [**Download OpenMCP**](https://kirigaya.cn/openmcp/plugin-tutorial/quick-start/acquire-openmcp.html)

2. Open vscode
3. Open main.py and start OpenMCP

For detailed installation instructions, please see [Install Guide](docs/install.md).

## 📄 License

MIT License © 2023 [LSTM-Kirigaya](https://github.com/LSTM-Kirigaya)