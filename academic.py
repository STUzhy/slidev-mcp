from mcp.server.fastmcp import FastMCP
from typing import Optional, Union, List, NamedTuple, Dict
import subprocess
import sys
import shutil
from pathlib import Path
import os
from utils import parse_markdown_slides
import asyncio
from crawl4ai import AsyncWebCrawler
import datetime

mcp = FastMCP('slidev-mcp-academic')

# 全局变量存储当前活动的Slidev项目
ACTIVE_SLIDEV_PROJECT: Optional[Dict] = None
SLIDEV_CONTENT: List[str] = []
ACADEMIC_THEME = 'academic'

class SlidevResult(NamedTuple):
    success: bool
    message: str
    output: Optional[Union[str, int, List[str]]] = None

def check_nodejs_installed() -> bool:
    return shutil.which("node") is not None

def run_command(command: Union[str, List[str]]) -> SlidevResult:
    try:
        result = subprocess.run(
            command,
            cwd='./',
            capture_output=True,
            text=True,
            shell=isinstance(command, str)
        )
        if result.returncode == 0:
            return SlidevResult(True, "Command executed successfully", result.stdout)
        else:
            return SlidevResult(False, f"Command failed: {result.stderr}")
    except Exception as e:
        return SlidevResult(False, f"Error executing command: {str(e)}")

def parse_markdown_slides(content: str) -> list:
    """
    解析markdown内容，按YAML front matter切分幻灯片
    """
    slides = []
    current_slide = []
    in_yaml = False
    
    for line in content.splitlines():
        if line.strip() == '---' and not in_yaml:
            # 开始YAML front matter
            if not current_slide:
                in_yaml = True
                current_slide.append(line)
            else:
                # 遇到新的幻灯片分隔符
                slides.append('\n'.join(current_slide))
                current_slide = [line]
                in_yaml = True
        elif line.strip() == '---' and in_yaml:
            # 结束YAML front matter
            current_slide.append(line)
            in_yaml = False
        else:
            current_slide.append(line)
    
    # 添加最后一个幻灯片
    if current_slide:
        slides.append('\n'.join(current_slide))
    
    return slides

def load_slidev_content(path: str) -> bool:
    global SLIDEV_CONTENT, ACTIVE_SLIDEV_PROJECT
    path = os.path.join('.slidev-mcp', path)
    
    slides_path = Path(path) / "slides.md"
    if not slides_path.exists():
        return False
    
    with open(slides_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 初始化全局变量
    ACTIVE_SLIDEV_PROJECT = {
        "path": str(path),
        "slides_path": str(slides_path)
    }
    
    slides = parse_markdown_slides(content)
    SLIDEV_CONTENT = [slide.strip() for slide in slides if slide.strip()]
    return True

def save_slidev_content() -> bool:
    global ACTIVE_SLIDEV_PROJECT, SLIDEV_CONTENT
    
    if not ACTIVE_SLIDEV_PROJECT:
        return False
    
    with open(ACTIVE_SLIDEV_PROJECT["slides_path"], 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(SLIDEV_CONTENT))
    
    return True

def transform_parameters_to_frontmatter(parameters: dict):
    frontmatter = ''
    for key in parameters.keys():
        value = parameters.get(key, '')
        frontmatter += f'{key}: {value}\n'
    return frontmatter.strip()

@mcp.prompt(
    name='guide',
    description='guide the ai to use slidev'
)
def guide_prompt():
    return """
你是一个擅长使用 slidev 进行讲演生成的 agent，如果用户给你输入超链接，你需要调用 websearch 工具来获取对应的文本。对于返回的文本，如果你看到了验证码，网络异常等等代表访问失败的信息，你需要提醒用户本地网络访问受阻，请手动填入需要生成讲演的文本。
当你生成讲演的每一页时，一定要严格按照用户输入的文本内容或者你通过 websearch 获取到的文本内容来。请记住，在获取用户输入之前，你一无所知，请不要自己编造不存在的事实，扭曲文章的原本含义，或者是不经过用户允许的情况下扩充本文的内容。
请一定要尽可能使用爬取到的文章中的图片，它们往往是以 ![](https://adwadaaw.png) 的形式存在的。

如果当前页面仅仅存在一个图片，而且文字数量超过了三行，你应该使用 figure-side 作为 layout
你必须参考的资料，下面的资料你需要使用爬虫进行爬取并得到内容：
- academic 主题的 frontmatter: https://raw.githubusercontent.com/alexanderdavide/slidev-theme-academic/refs/heads/master/README.md

遇到 `:` 开头的话语，这是命令，目前的命令有如下的：
- `:sum {{url}}`: 爬取目标网页内容并整理，如果爬取失败，你需要停下来让用户手动输入网页内容的总结。
- `:mermaid {{description}}`: 根据 description 生成符合描述的 mermaid 流程图代码，使用 ```mermaid ``` 进行包裹。

现在请爬取如下链接来获取 academic 基本的使用方法
https://raw.githubusercontent.com/alexanderdavide/slidev-theme-academic/refs/heads/master/README.md
"""

@mcp.tool(
    name='websearch',
    description='search the given https url and get the markdown text of the website'
)
async def websearch(url: str) -> SlidevResult:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url)
        return SlidevResult(True, "success", result.markdown)


@mcp.tool(
    name='check_environment',
    description='check if nodejs and slidev-cli is ready'
)
def check_environment() -> SlidevResult:
    if not check_nodejs_installed():
        return SlidevResult(False, "Node.js is not installed. Please install Node.js first.")
    
    result = run_command("slidev --version")
    if not result.success:
        return run_command("npm install -g @slidev/cli")
    return SlidevResult(True, "环境就绪，slidev 可以使用", result.output)


@mcp.tool(
    name='create_slidev',
    description="""create slidev, you need to ask user to get title and author to continue the task.
you don\'t know title and author at beginning.
`path`: folder path of the project
""",
)
def create_slidev(path: str) -> SlidevResult:
    global ACTIVE_SLIDEV_PROJECT, SLIDEV_CONTENT

    # clear global var
    ACTIVE_SLIDEV_PROJECT = None
    SLIDEV_CONTENT = []
    
    env_check = check_environment()
    if not env_check.success:
        return env_check
    
    path = os.path.join('.slidev-mcp', path)
    try:
        # 创建目标文件夹
        os.makedirs(path, exist_ok=True)
        
        # 在文件夹内创建slides.md文件
        slides_path = os.path.join(path, 'slides.md')

        # 如果已经存在 slides.md，则读入内容，初始化
        if os.path.exists(slides_path):
            load_slidev_content(path)
            return SlidevResult(True, f"项目已经存在于 {path}/slides.md 中", SLIDEV_CONTENT)
        else:
            SLIDEV_CONTENT = []

        with open(slides_path, 'w') as f:
            f.write(f"""
---
theme: {ACADEMIC_THEME}
layout: cover
transition: slide-left
---

# Your title
## sub title

""".strip())
        
        # 尝试加载内容
        if not load_slidev_content(path):
            return SlidevResult(False, "successfully create project but fail to load file", path)
            
        return SlidevResult(True, f"successfully load slidev project {path}", path)
        
    except OSError as e:
        return SlidevResult(False, f"fail to create file: {str(e)}", path)
    except IOError as e:
        return SlidevResult(False, f"fail to create file: {str(e)}", path)
    except Exception as e:
        return SlidevResult(False, f"unknown error: {str(e)}", path)


@mcp.tool(
    name='load_slidev',
    description='load exist slidev project and get the current slidev markdown content',
)
def load_slidev(path: str) -> SlidevResult:
    if load_slidev_content(path):
        return SlidevResult(True, f"Slidev project loaded from {path}", SLIDEV_CONTENT)
    return SlidevResult(False, f"Failed to load Slidev project from {path}")


@mcp.tool(
    name='make_cover',
    description="""Create or update slidev cover.
`python_string_template` is python string template, you can use {title}, {subtitle} to format the string.
If user give enough information, you can use it to update cover page, otherwise you must ask the lacking information. `background` must be a valid url of image""",
)
def make_cover(title: str, subtitle: str = "", author: str = "", background: str = "", python_string_template: str = "") -> SlidevResult:
    global SLIDEV_CONTENT
    
    if not ACTIVE_SLIDEV_PROJECT:
        return SlidevResult(False, "No active Slidev project. Please create or load one first.")
    
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if python_string_template:
        template = f"""
---
theme: {ACADEMIC_THEME}
layout: cover
transition: slide-left
coverAuthor: {author}
coverBackgroundUrl: {background}
---

{python_string_template.format(title=title, subtitle=subtitle)}
""".strip()

    else:
        template = f"""
---
theme: {ACADEMIC_THEME}
layout: cover
transition: slide-left
coverAuthor: {author}
background: {background}
---

# {title}
## {subtitle}
""".strip()

    # 更新或添加封面页
    SLIDEV_CONTENT[0] = template
    
    save_slidev_content()
    return SlidevResult(True, "Cover page updated", 0)

@mcp.tool(
    name='add_page',
    description="""Add new page.
- `content` is markdown format text to describe page content.
- `layout`: layout of the page
- `parameters`: frontmatter parameters of the page
"""
)
def add_page(content: str, layout: str = "default", parameters: dict = {}) -> SlidevResult:
    global SLIDEV_CONTENT
    
    if not ACTIVE_SLIDEV_PROJECT:
        return SlidevResult(False, "No active Slidev project. Please create or load one first.")
    
    parameters['layout'] = layout
    parameters['transition'] = 'slide-left'
    frontmatter_string = transform_parameters_to_frontmatter(parameters)

    template = f"""
---
{frontmatter_string}
---

{content}

""".strip()

    SLIDEV_CONTENT.append(template)
    page_index = len(SLIDEV_CONTENT) - 1
    save_slidev_content()
    
    return SlidevResult(True, f"Page added at index {page_index}", page_index)


@mcp.tool(
    name='set_page',
    description="""
`index`: the index of the page to set. 0 is cover, so you should use index in [1, {len(SLIDEV_CONTENT) - 1}]
`content`: the markdown content to set.
- You can use ```code ```, latex or mermaid to represent more complex idea or concept. 
- Too long or short content is forbidden.
`layout`: the layout of the page.
`parameters`: frontmatter parameters.
""",
)
def set_page(index: int, content: str, layout: str = "", parameters: dict = {}) -> SlidevResult:
    global SLIDEV_CONTENT
    
    if not ACTIVE_SLIDEV_PROJECT:
        return SlidevResult(False, "No active Slidev project. Please create or load one first.")
    
    if index < 0 or index >= len(SLIDEV_CONTENT):
        return SlidevResult(False, f"Invalid page index: {index}")
    
    parameters['layout'] = layout
    parameters['transition'] = 'slide-left'
    frontmatter_string = transform_parameters_to_frontmatter(parameters)
    
    template = f"""
---
{frontmatter_string}
---

{content}

""".strip()
    
    SLIDEV_CONTENT[index] = template
    save_slidev_content()
    
    return SlidevResult(True, f"Page {index} updated", index)

@mcp.tool(
    name='get_page',
    description='get the content of the `index` th page',
)
def get_page(index: int) -> SlidevResult:
    if not ACTIVE_SLIDEV_PROJECT:
        return SlidevResult(False, "No active Slidev project. Please create or load one first.")
    
    if index < 0 or index >= len(SLIDEV_CONTENT):
        return SlidevResult(False, f"Invalid page index: {index}")
    
    return SlidevResult(True, f"Content of page {index}", SLIDEV_CONTENT[index])

if __name__ == "__main__":
    mcp.run(transport='stdio')