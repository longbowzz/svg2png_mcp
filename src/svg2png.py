import os
import cairosvg
import re

class SVG2PNG:
    def convert(self, svg_content: str, work_dir: str) -> str:
        """
        将SVG代码转换为PNG图片
        :param svg_content: SVG代码字符串
        :param work_dir: 工作目录路径
        :return: 生成的PNG文件路径
        """
        # 确保工作目录存在
        os.makedirs(work_dir, exist_ok=True)
        
        # 生成输出PNG文件路径
        png_file = os.path.join(work_dir, "output.png")
        
        try:
            # 检查并添加SVG尺寸
            if "<svg" in svg_content:
                # 检查是否已有width和height属性
                has_width = bool(re.search(r'<svg[^>]*\bwidth\s*=', svg_content))
                has_height = bool(re.search(r'<svg[^>]*\bheight\s*=', svg_content))
                
                # 准备SVG属性
                svg_attrs = []
                if not has_width:
                    svg_attrs.append('width="800"')
                if not has_height:
                    svg_attrs.append('height="600"')
                
                # 添加命名空间
                if 'xmlns=' not in svg_content:
                    svg_attrs.append('xmlns="http://www.w3.org/2000/svg"')
                
                # 构建新的SVG标签
                if svg_attrs:
                    svg_content = re.sub(
                        r'<svg([^>]*)>',
                        lambda m: f'<svg{m.group(1)} {" ".join(svg_attrs)}>',
                        svg_content,
                        1
                    )

                # 添加全局字体样式
                if "<defs>" not in svg_content:
                    svg_content = re.sub(
                        r'<svg([^>]*)>',
                        r'''<svg\1>
                        <defs>
                            <style type="text/css">
                                text { font-family: "Heiti SC", "STHeiti", "SimHei", sans-serif; }
                            </style>
                        </defs>''',
                        svg_content,
                        1
                    )

                # 替换所有字体声明
                svg_content = re.sub(
                    r'font-family="[^"]*"',
                    'font-family="Heiti SC, STHeiti, SimHei, sans-serif"',
                    svg_content
                )
                
                # 替换单引号版本
                svg_content = re.sub(
                    r"font-family='[^']*'",
                    "font-family='Heiti SC, STHeiti, SimHei, sans-serif'",
                    svg_content
                )
            
            # 使用cairosvg直接将SVG转换为PNG
            cairosvg.svg2png(
                bytestring=svg_content.encode('utf-8'),
                write_to=png_file,
                output_width=None,  # 保持原始宽度
                output_height=None  # 保持原始高度
            )
            return png_file
            
        except Exception as e:
            raise Exception(f"转换失败：{str(e)}") 