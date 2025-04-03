import os
import subprocess
from PIL import Image

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
        
        # 生成临时SVG文件
        temp_svg = os.path.join(work_dir, "temp.svg")
        with open(temp_svg, "w") as f:
            f.write(svg_content)
        
        # 生成输出PNG文件路径
        png_file = os.path.join(work_dir, "output.png")
        
        try:
            # 检查是否安装了Inkscape
            try:
                subprocess.run(['inkscape', '--version'], check=True, capture_output=True)
            except FileNotFoundError:
                print("未找到Inkscape，正在安装...")
                subprocess.run(['brew', 'install', 'inkscape'], check=True)
                print("Inkscape安装完成")
            
            # 构建Inkscape命令
            cmd = ['inkscape', temp_svg, '--export-filename', png_file]
            
            # 执行转换
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"转换失败：{result.stderr}")
            
            # 清理临时文件
            os.remove(temp_svg)
            
            return png_file
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"错误：{str(e)}")
        except Exception as e:
            # 确保清理临时文件
            if os.path.exists(temp_svg):
                os.remove(temp_svg)
            raise Exception(f"转换失败：{str(e)}") 