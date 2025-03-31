# 作者: 筱可
# 日期: 2025 年 3 月 31 日
# 版权所有 (c) 2025 筱可 & 筱可AI研习社. 保留所有权利.
# BSD 3-Clause License
# 
# 本软件的再分发和使用，无论是源代码还是二进制形式，
# 无论是否修改，都必须满足以下条件：
# 
# * 源代码的再分发必须保留上述版权声明、此条件列表和以下免责声明。
# 
# * 以二进制形式再分发必须在文档和/或再分发提供的其他材料中复制上述版权声明、
#   此条件列表和以下免责声明。
# 
# * 未经特定事先书面许可，不得使用版权持有人和贡献者的姓名来
#   推广或宣传从本软件衍生的产品。

import os
import argparse
import json
from pathlib import Path


def convert_notebook_to_markdown(notebook):
    """
    将Jupyter笔记本JSON对象转换为Markdown字符串
    
    参数:
        notebook (dict): Jupyter笔记本的JSON对象
    
    返回:
        str: 转换后的Markdown字符串
    """
    markdown = ""
    
    # 尝试获取标题/元数据
    if "metadata" in notebook and isinstance(notebook["metadata"], dict):
        metadata = notebook["metadata"]
        if "title" in metadata and isinstance(metadata["title"], str):
            markdown += f"# {metadata['title']}\n\n"
    
    # 处理单元格
    if "cells" in notebook and isinstance(notebook["cells"], list):
        for cell in notebook["cells"]:
            cell_type = cell.get("cell_type", "code")
            
            if cell_type == "markdown":
                # 直接添加Markdown内容
                if "source" in cell:
                    if isinstance(cell["source"], list):
                        for line in cell["source"]:
                            if isinstance(line, str):
                                markdown += line
                    elif isinstance(cell["source"], str):
                        markdown += cell["source"]
                    markdown += "\n\n"
            
            elif cell_type == "code":
                # 添加代码块
                markdown += "```python\n"
                if "source" in cell:
                    if isinstance(cell["source"], list):
                        for line in cell["source"]:
                            if isinstance(line, str):
                                markdown += line
                    elif isinstance(cell["source"], str):
                        markdown += cell["source"]
                markdown += "\n```\n\n"
                
                # 处理代码输出
                if "outputs" in cell and isinstance(cell["outputs"], list):
                    for output in cell["outputs"]:
                        output_type = output.get("output_type", "")
                        
                        if output_type == "stream":
                            markdown += "output:\n\n```\n"
                            if "text" in output:
                                if isinstance(output["text"], list):
                                    for line in output["text"]:
                                        if isinstance(line, str):
                                            markdown += line
                                elif isinstance(output["text"], str):
                                    markdown += output["text"]
                            markdown += "\n```\n\n"
                        
                        elif output_type in ["execute_result", "display_data"]:
                            # 处理输出数据
                            if "data" in output and isinstance(output["data"], dict):
                                # 处理文本/html输出
                                if "text/plain" in output["data"]:
                                    text_plain = output["data"]["text/plain"]
                                    markdown += "result:\n\n```\n"
                                    if isinstance(text_plain, list):
                                        for line in text_plain:
                                            if isinstance(line, str):
                                                markdown += line
                                    elif isinstance(text_plain, str):
                                        markdown += text_plain
                                    markdown += "\n```\n\n"
                                
                                # TODO: 如果需要，可以添加对图像等其他输出类型的处理
    
    return markdown


def convert_jupyter_to_markdown(input_dir, output_dir):
    """
    将输入目录中的所有Jupyter笔记本转换为输出目录中的Markdown文件。

    参数:
        input_dir (str): 包含Jupyter笔记本文件的目录
        output_dir (str): 保存Markdown文件的目录
    """
    # 如果输出目录不存在，则创建
    os.makedirs(output_dir, exist_ok=True)

    # 获取输入目录中的所有.ipynb文件
    input_path = Path(input_dir)
    jupyter_files = list(input_path.glob("**/*.ipynb"))

    if not jupyter_files:
        print(f"在 {input_dir} 中未找到Jupyter笔记本")
        return

    print(f"找到 {len(jupyter_files)} 个需要转换的Jupyter笔记本")

    # 处理每个笔记本
    for jupyter_file in jupyter_files:
        # 获取相对路径以保持目录结构
        rel_path = jupyter_file.relative_to(input_path)

        # 如果需要，在output_dir中创建子目录
        output_subdir = Path(output_dir) / rel_path.parent
        os.makedirs(output_subdir, exist_ok=True)

        # 确定输出文件名：将.ipynb替换为.md
        file_stem = jupyter_file.stem
        output_file_path = output_subdir / f"{file_stem}.md"
        
        print(f"正在转换 {jupyter_file} 到 {output_file_path}")
        
        try:
            # 读取ipynb文件
            with open(jupyter_file, 'r', encoding='utf-8') as f:
                notebook_content = f.read()
            
            # 解析JSON
            notebook = json.loads(notebook_content)
            
            # 将笔记本转换为Markdown
            markdown = convert_notebook_to_markdown(notebook)
            
            # 写入Markdown文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
                
        except Exception as e:
            print(f"转换 {jupyter_file} 时出错: {str(e)}")
    
    print("转换完成！")


def main():
    parser = argparse.ArgumentParser(description="将Jupyter笔记本转换为Markdown文件")
    parser.add_argument(
        "-i", "--input_dir", required=True, help="包含Jupyter笔记本文件的目录"
    )
    parser.add_argument(
        "-o", "--output_dir", required=True, help="保存Markdown文件的目录"
    )

    args = parser.parse_args()
    try:
        convert_jupyter_to_markdown(args.input_dir, args.output_dir)
        return 0
    except Exception as e:
        print(f"错误: {str(e)}")
        return 1


if __name__ == "__main__":
    main()
