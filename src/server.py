from mcp.server.fastmcp import FastMCP
from svg2png import SVG2PNG

# 创建MCP服务器
mcp = FastMCP("SVG to PNG Server")
converter = SVG2PNG()

@mcp.tool()
def svg_to_png(svg_content: str, work_dir: str) -> str:
    """
    MCP工具：将SVG转换为PNG
    :param svg_content: SVG代码字符串
    :param work_dir: 工作目录路径
    :return: 生成的PNG文件路径
    """
    try:
        return converter.convert(svg_content, work_dir)
    except Exception as e:
        raise Exception(f"转换失败: {str(e)}")

if __name__ == "__main__":
    mcp.run() 