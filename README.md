# SVG to PNG MCP Server

这是一个基于Model Context Protocol (MCP)的SVG转PNG工具服务器。

## 功能特点

- 将SVG代码转换为PNG图片
- 支持指定工作目录
- 基于MCP协议，可与其他MCP客户端集成

## SVG转PNG方案说明

目前支持两种SVG转PNG的转换方案：

1. CairoSVG方案（当前使用）
   - 使用`cairosvg`库进行转换
   - 优点：
     - 转换速度快
     - 依赖少，安装简单
     - 适合简单的SVG图形转换
   - 缺点：
     - 中文字体支持需要特殊处理
     - 某些复杂SVG特性支持有限

2. Inkscape方案（备选）
   - 使用Inkscape命令行工具进行转换
   - 优点：
     - 完整支持SVG所有特性
     - 更好的字体渲染支持
     - 转换效果更准确
   - 缺点：
     - 需要安装Inkscape软件
     - 转换速度相对较慢
     - 系统依赖较多

注意：当前版本默认使用CairoSVG方案，如果遇到字体渲染问题或复杂SVG转换问题，可以考虑切换到Inkscape方案。

## 项目结构

```
svg2png_mcp/
├── src/
│   ├── server.py          # MCP服务器实现
│   ├── svg2png.py         # SVG转PNG的业务逻辑
│   └── test_client.py     # 测试客户端
├── servers_config.example.json    # MCP服务器配置示例
└── requirements.txt       # 依赖文件
```

## 安装

1. 创建并激活虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# 在 macOS/Linux 上：
source venv/bin/activate
# 在 Windows 上：
.\venv\Scripts\activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

1. 复制配置文件示例：
```bash
cp servers_config.example.json servers_config.json
```

2. 编辑 `servers_config.json`，**必须使用绝对路径**：
```json
{
    "mcpServers": {
        "svg2png": {
            "command": "/absolute/path/to/venv/bin/python",
            "args": [
                "/absolute/path/to/svg2png_mcp/src/server.py"
            ]
        }
    }
}
```

⚠️ **重要说明**：
- `command` 必须是虚拟环境中 Python 解释器的**绝对路径**
- `args` 中的 `server.py` 路径必须是**绝对路径**
- 这是为了确保其他 MCP 客户端能够正确找到并启动服务器

获取路径的方法：
```bash
# 获取Python解释器的绝对路径（在虚拟环境中运行）
which python  # macOS/Linux
where python  # Windows

# 获取项目根目录的绝对路径
pwd  # macOS/Linux
cd   # Windows
```

示例（macOS/Linux）：
```json
{
    "mcpServers": {
        "svg2png": {
            "command": "/Users/username/projects/svg2png_mcp/venv/bin/python",
            "args": [
                "/Users/username/projects/svg2png_mcp/src/server.py"
            ]
        }
    }
}
```

示例（Windows）：
```json
{
    "mcpServers": {
        "svg2png": {
            "command": "C:\\Users\\username\\projects\\svg2png_mcp\\venv\\Scripts\\python.exe",
            "args": [
                "C:\\Users\\username\\projects\\svg2png_mcp\\src\\server.py"
            ]
        }
    }
}
```

## 使用方法

运行测试客户端：
```bash
# 确保虚拟环境已激活
source venv/bin/activate  # macOS/Linux
# 运行客户端
python src/test_client.py
```

如果运行正常，将在test_output目录生成一张名为output.png的图片。

将servers_config.json中的内容填入Cursor、Claude desktop等MCP客户端即可使用。


注意：
- MCP客户端会自动根据 `servers_config.json` 中的配置启动服务器
- 确保 `servers_config.json` 中使用了正确的绝对路径
- 确保在运行客户端时已激活虚拟环境

## 技术实现

### 服务器架构
- 使用 FastMCP 框架实现 MCP 服务器
- 提供 `svg_to_png` 工具接口
- 支持异步操作和错误处理

### 核心功能
- SVG 到 PNG 的转换使用 cairosvg 库
- 支持自定义工作目录
- 提供完整的错误处理和日志记录

### 客户端集成
- 支持标准 MCP 客户端接入
- 提供测试客户端示例
- 支持工具发现和异步调用

## 依赖

- mcp：MCP 协议实现
- cairosvg：SVG 转换核心库
- Pillow：图像处理支持 