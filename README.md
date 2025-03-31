# nb2md - Jupyter笔记本转换为Markdown工具

## 项目简介

nb2md是一个简单而高效的Python工具，用于将Jupyter笔记本(.ipynb文件)批量转换为Markdown格式(.md文件)。该工具采用原生Python实现，无需依赖外部命令行工具，能够保留Jupyter笔记本中的代码块、输出结果以及Markdown文本等内容。

同时，我们也提供了Rust实现版本，具有更高的性能和效率，适合处理大规模笔记本转换任务。

## 功能特点

- 递归扫描目录，批量转换所有找到的Jupyter笔记本
- 保留原始目录结构
- 直接解析.ipynb文件的JSON内容，无需调用外部命令
- 支持代码单元格和Markdown单元格的转换
- 代码输出结果也会被正确地转换为Markdown中的代码块

## 安装方法

### Python版本

1. 克隆或下载本仓库

```bash
git clone https://github.com/li-xiu-qi/nb2md.git
cd nb2md
```

2. 安装依赖（无需额外依赖，只使用Python标准库）

### Rust版本

如果您希望使用性能更高的Rust实现版本：
(注意：需要Rust环境)

```bash
git clone https://github.com/li-xiu-qi/nb2md-rs.git
cd nb2md-rs
cargo build --release
```

## 使用方法

### 命令行使用

```bash
python main.py -i <输入目录> -o <输出目录>
```

参数说明:

- `-i, --input_dir`: 包含Jupyter笔记本(.ipynb文件)的目录
- `-o, --output_dir`: 保存转换后Markdown文件(.md文件)的目录

### 示例

```bash
python main.py -i ./jupyter_notebooks -o ./markdown_files
```

上述命令会将`./jupyter_notebooks`目录（包括所有子目录）中的所有.ipynb文件转换为Markdown格式，并保存到`./markdown_files`目录中，同时保持原始的目录结构。

## 转换过程

转换过程如下：

1. 扫描输入目录及其所有子目录，查找所有.ipynb文件
2. 对于每个找到的.ipynb文件：
   - 读取并解析文件内容（JSON格式）
   - 提取笔记本中的各个单元格（代码、Markdown等）
   - 将这些单元格转换为Markdown格式
   - 保存转换后的内容到对应的.md文件

## 项目结构

```
nb2md/
├── main.py  # 主程序
└── README.md  # 本文档
```

## 编译为可执行文件

如果你希望将此工具编译为独立的可执行程序（.exe文件），可以按照以下步骤使用PyInstaller实现：

### 安装PyInstaller

```bash
pip install pyinstaller
```

### 编译项目

在项目目录下执行以下命令：

```bash
# 基本编译（生成目录）
pyinstaller main.py --name nb2md

# 或者生成单文件
pyinstaller --onefile main.py --name nb2md
```

### 优化选项

为了减小文件体积和提高启动速度，可以考虑以下选项：

```bash

# 如果需要保留控制台输出
pyinstaller --onefile --console main.py --name nb2md
```

### 使用编译后的可执行文件

编译完成后，可以在`dist`目录中找到生成的可执行文件。使用方式与Python脚本类似：

```bash
# Windows
nb2md.exe -i <输入目录> -o <输出目录>
```

### 注意事项

1. 编译后的可执行文件体积会较大，因为它包含了Python解释器和所有依赖库
2. 如果项目使用了动态加载的资源文件，可能需要额外的配置来确保这些文件被正确包含
3. 在不同的系统上编译的可执行文件通常不能跨平台使用

## 贡献指南

欢迎贡献！如果你有兴趣改进这个工具，可以通过以下方式参与：

1. Fork本仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

本项目采用BSD 3-Clause许可证 - 详情请参阅LICENSE文件
