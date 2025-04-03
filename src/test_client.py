import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def load_server_config():
    """从servers_config.json加载服务器配置"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "servers_config.json")
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["mcpServers"]["svg2png"]

async def main():
    # 加载服务器配置
    server_config = load_server_config()
    
    # 创建服务器参数
    server_params = StdioServerParameters(
        command=server_config["command"],
        args=server_config["args"]
    )

    # 测试用的SVG内容 - 杭州主题配色方案
    test_svg = '''<svg width="400" height="500" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景 -->
  <rect width="400" height="500" fill="#D1D9D8" rx="10" ry="10"/>
  
  <!-- 城市名 -->
  <text x="200" y="80" font-family="'Microsoft YaHei', sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#6B8E8C">杭 州</text>
  
  <!-- 主题色卡 -->
  <rect x="100" y="150" width="200" height="80" fill="#6B8E8C" rx="5" ry="5"/>
  <text x="200" y="180" font-family="'Microsoft YaHei', sans-serif" font-size="16" text-anchor="middle" fill="white">主题色: 青瓷绿 #6B8E8C</text>
  
  <!-- 背景色卡 -->
  <rect x="100" y="250" width="200" height="80" fill="#D1D9D8" stroke="#6B8E8C" stroke-width="2" rx="5" ry="5"/>
  <text x="200" y="280" font-family="'Microsoft YaHei', sans-serif" font-size="16" text-anchor="middle" fill="#333">背景色: 烟雨灰 #D1D9D8</text>
  
  <!-- 关键词 -->
  <rect x="50" y="350" width="300" height="120" fill="white" rx="5" ry="5"/>
  <text x="60" y="375" font-family="'Microsoft YaHei', sans-serif" font-size="14" font-weight="bold" fill="#6B8E8C">关键词解读:</text>
  <text x="60" y="400" font-family="'Microsoft YaHei', sans-serif" font-size="12" fill="#333">• 西湖烟雨 - 湖光山色与朦胧意境</text>
  <text x="60" y="420" font-family="'Microsoft YaHei', sans-serif" font-size="12" fill="#333">• 龙井茶韵 - 茶文化体现城市优雅</text>
  <text x="60" y="440" font-family="'Microsoft YaHei', sans-serif" font-size="12" fill="#333">• 南宋遗风 - 深厚的历史文化底蕴</text>
  
  <!-- 配色思路 -->
  <text x="60" y="480" font-family="'Microsoft YaHei', sans-serif" font-size="12" fill="#333" font-style="italic">青瓷绿与烟雨灰的搭配体现杭州自然与文化的和谐统一</text>
  
  <!-- 装饰元素 -->
  <path d="M50 120 Q200 80 350 120" stroke="#6B8E8C" stroke-width="2" fill="none" stroke-dasharray="5,5"/>
  <path d="M50 130 Q200 90 350 130" stroke="#6B8E8C" stroke-width="1" fill="none" stroke-dasharray="3,3"/>
</svg>'''
    
    # 工作目录
    work_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_output")
    os.makedirs(work_dir, exist_ok=True)

    print("正在连接到MCP服务器...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()
            print("连接成功！")
            
            # 列出可用工具
            tools = await session.list_tools()
            print("\n可用工具:")
            for tool in tools:
                print(f"- {tool[0]}: {tool[1]}")
            
            # 调用转换工具
            print("\n正在转换SVG到PNG...")
            try:
                result = await session.call_tool(
                    "svg_to_png",
                    arguments={
                        "svg_content": test_svg,
                        "work_dir": work_dir
                    }
                )
                print(f"\n转换成功！PNG文件保存在: {result}")
            except Exception as e:
                print(f"\n转换失败: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 