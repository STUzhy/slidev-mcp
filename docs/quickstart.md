# Quick Start Guide

## Prerequisites

Please ensure that your system has the following software installed with the specified requirements.

| Software | Version Requirement | Description |
| -- | -- | -- |
| Python | >=3.13 | Base environment for running MCP server |
| Node.js | >=18.0 | Slidev runtime environment |
| UV | - | Python package management tool |

### Software Installation

#### 1. Install Python (>=3.13)
- Visit [Python Official Website](https://www.python.org/downloads/) to download and install the latest version
- Please check "Add Python to PATH" option during installation

#### 2. Install UV
```bash
# Windows
pip install uv

# Or use official installation script (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. Install Node.js (>=20.0)
- Visit [Node.js Official Website](https://nodejs.org/) to download and install the LTS version
- After installation, run `node --version` in command line to verify the installation

## Install Project Dependencies

### 1. Create Virtual Environment

First create a virtual environment. You can skip this step if you don't need a virtual environment.

```bash
uv venv # Create virtual environment
```

### 2. Activate Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# Linux/macOS  
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
uv sync  # Install project dependencies
```

### 4. Install Slidev CLI

```bash
npm install -g @slidev/cli
```

## Verify Installation

### 1. Check Environment

Run the following commands to check if all dependencies are correctly installed:

```bash
# Check Python version
python --version

# Check Node.js version  
node --version

# Check UV
uv --version

# Check Slidev CLI
slidev --version
```

### 2. Test MCP Server

```bash
# Activate virtual environment (if using)
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# Run MCP server
uv run main.py
```

If there are no errors, the server has started successfully.

## Usage Guide

### Development Mode

If you want to develop or debug, we recommend using [OpenMCP](https://marketplace.visualstudio.com/items?itemName=kirigaya.openmcp):

1. Download the OpenMCP VSCode extension.
2. Open the OpenMCP extension.
3. Create a new MCP Server, select stdio, and enter the command `uv --directory E:\\node-project\\slidev-mcp run main.py`.

> **Note**: Please replace the path `E:\\node-project\\slidev-mcp` with your actual project path.

### Production Usage

For daily use, we recommend using Claude Desktop:

Add the following configuration to Claude Desktop's configuration file:

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

> **Note**: Please replace the path `E:\\node-project\\slidev-mcp` with your actual project path.

## Additional Features

After installation, you can:

- Create slides using natural language
- Automatically generate professional Slidev presentations
- Use AI assistance for content writing
- Customize slide themes and layouts

For more usage methods, please refer to the project's [README documentation](../README.md).