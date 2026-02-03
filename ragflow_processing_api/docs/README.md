# RAGFlow Processing API

A standalone API extracted from RAGFlow for processing tables, images, and lists in documents.

## 概述 (Overview)

本项目从 RAGFlow 中提取了表格、图片和列表处理的核心方法，形成了一个完全独立的 Python API。这个子系统完全克隆了 RAGFlow 的处理行为，但可以独立使用。

This project extracts the core table, image, and list processing methods from RAGFlow, forming a completely independent Python API. This subsystem fully clones RAGFlow's processing behavior but can be used independently.

## 功能特性 (Features)

### 📊 表格处理 (Table Processing)
- **表格结构识别** (Table Structure Recognition): 识别表格行、列、表头和跨行跨列单元格
- **Excel 表格解析** (Excel Table Parsing): 解析 Excel 文件，提取表格数据
- **HTML/文本转换** (HTML/Text Conversion): 将表格转换为 HTML 或描述性文本格式

### 🖼️ 图片处理 (Image Processing)
- **OCR 文字识别** (OCR Text Recognition): 从图片中提取文字
- **图片分析** (Image Analysis): 图片描述、图表理解
- **批量处理** (Batch Processing): 支持批量图片处理

### 📝 列表处理 (List Processing)
- **列表提取** (List Extraction): 自动识别和提取有序/无序列表
- **嵌套列表** (Nested Lists): 支持多层嵌套列表结构
- **格式转换** (Format Conversion): 列表转 HTML、Markdown、纯文本

## 安装 (Installation)

```bash
# 基础依赖 (Basic dependencies)
pip install numpy pandas pillow openpyxl

# 可选依赖 (Optional dependencies)
# For full OCR functionality
pip install paddleocr  # or tesseract
```

## 快速开始 (Quick Start)

### 1. 表格处理 (Table Processing)

```python
from ragflow_processing_api import TableProcessor

# 创建处理器 (Create processor)
processor = TableProcessor()

# 处理 Excel 文件 (Process Excel file)
tables = processor.process_excel("data.xlsx")
for table in tables:
    print(f"Sheet: {table['sheet_name']}")
    print(table['dataframe'])

# 从检测框构建表格 (Construct table from boxes)
html_table = processor.construct_table(boxes, html=True)
```

### 2. 图片处理 (Image Processing)

```python
from ragflow_processing_api import ImageProcessor
from PIL import Image

# 创建处理器 (Create processor)
processor = ImageProcessor()

# OCR 识别 (OCR recognition)
image = Image.open("document.jpg")
text = processor.ocr(image, return_boxes=False)
print(f"提取的文字: {text}")

# 图片描述 (Image description)
description = processor.describe(image)
print(f"图片描述: {description}")
```

### 3. 列表处理 (List Processing)

```python
from ragflow_processing_api import ListProcessor

# 创建处理器 (Create processor)
processor = ListProcessor()

# 提取列表 (Extract lists)
text = """
1. 第一项
2. 第二项
3. 第三项
"""
lists = processor.extract(text)

# 格式化输出 (Format output)
html = processor.format(lists[0], format='html')
markdown = processor.format(lists[0], format='markdown')
```

## API 文档 (API Documentation)

### 表格处理 API (Table Processing API)

#### TableStructureRecognizer

表格结构识别器，用于从检测框构建表格。

```python
from ragflow_processing_api.table import TableStructureRecognizer

recognizer = TableStructureRecognizer()

# 构建 HTML 表格
html_table = recognizer.construct_table(
    boxes,          # 检测框列表
    is_english=False,  # 是否为英文
    html=True       # 输出 HTML 格式
)

# 构建描述性文本表格
text_table = recognizer.construct_table(boxes, html=False)
```

**参数说明 (Parameters):**
- `boxes`: 检测框列表，每个框包含文本、位置、类型等信息
- `is_english`: 是否为英文内容
- `html`: True 返回 HTML，False 返回描述性文本

#### ExcelTableProcessor

Excel 表格处理器，用于解析 Excel 文件。

```python
from ragflow_processing_api.table import ExcelTableProcessor

processor = ExcelTableProcessor()

# 处理 Excel 文件
tables = processor.process_file("data.xlsx")

# 转换为字典格式
dict_data = processor.process_file_to_dict("data.xlsx")
```

### 图片处理 API (Image Processing API)

#### OCRProcessor

OCR 处理器，用于从图片中提取文字。

```python
from ragflow_processing_api.image import OCRProcessor

ocr = OCRProcessor()

# 处理图片
results = ocr.process_image("document.jpg", return_boxes=True)

# 仅获取文字
text = ocr.process_image("document.jpg", return_boxes=False)

# 批量处理
results = ocr.process_batch([img1, img2, img3])
```

#### ImageAnalyzer

图片分析器，用于生成图片描述。

```python
from ragflow_processing_api.image import ImageAnalyzer

analyzer = ImageAnalyzer()

# 生成图片描述
description = analyzer.describe_image(image)

# 带上下文的图片描述
description = analyzer.describe_image(
    image,
    context={
        "above": "上文内容",
        "below": "下文内容"
    }
)
```

### 列表处理 API (List Processing API)

#### ListExtractor

列表提取器，用于从文本中提取列表。

```python
from ragflow_processing_api.list import ListExtractor

extractor = ListExtractor()

# 提取列表
lists = extractor.extract_lists(text)

# 提取嵌套列表
nested_lists = extractor.extract_nested_lists(text)

# 统计列表
stats = extractor.count_lists(text)
```

#### ListFormatter

列表格式化器，用于将列表转换为不同格式。

```python
from ragflow_processing_api.list import ListFormatter

formatter = ListFormatter()

# 转换为 HTML
html = formatter.format_as_html(items, ordered=True)

# 转换为 Markdown
markdown = formatter.format_as_markdown(items, ordered=True)

# 格式化嵌套列表
html = formatter.format_nested_html(nested_list)
```

## 示例脚本 (Example Scripts)

项目包含完整的示例脚本，位于 `examples/` 目录：

```bash
# 表格处理示例
python examples/table_example.py

# 图片处理示例
python examples/image_example.py

# 列表处理示例
python examples/list_example.py
```

## 架构设计 (Architecture)

```
ragflow_processing_api/
├── __init__.py           # 统一接口
├── table/                # 表格处理模块
│   ├── __init__.py
│   ├── table_recognizer.py
│   └── excel_processor.py
├── image/                # 图片处理模块
│   ├── __init__.py
│   ├── ocr_processor.py
│   └── image_analyzer.py
├── list/                 # 列表处理模块
│   ├── __init__.py
│   ├── list_extractor.py
│   └── list_formatter.py
├── examples/             # 示例脚本
│   ├── table_example.py
│   ├── image_example.py
│   └── list_example.py
└── docs/                 # 文档
    └── README.md
```

## 与 RAGFlow 的关系 (Relationship with RAGFlow)

本项目是从 RAGFlow 中提取的核心处理逻辑，具有以下特点：

1. **完全独立** (Fully Independent): 不依赖 RAGFlow 的其他组件
2. **行为一致** (Consistent Behavior): 处理逻辑与 RAGFlow 完全一致
3. **简化接口** (Simplified Interface): 提供更简洁的 API 接口
4. **易于集成** (Easy Integration): 可轻松集成到其他项目

## 注意事项 (Notes)

1. **OCR 模型** (OCR Models): OCR 功能需要集成实际的 OCR 模型（如 PaddleOCR）
2. **视觉模型** (Vision Models): 图片描述功能需要集成视觉语言模型（如 CLIP, BLIP）
3. **性能优化** (Performance): 大规模处理时建议使用批处理和 GPU 加速

## 许可证 (License)

Apache License 2.0

## 贡献 (Contributing)

欢迎贡献代码、报告问题或提出改进建议！

## 联系方式 (Contact)

- GitHub Issues: 提交问题和建议
- RAGFlow 项目: https://github.com/infiniflow/ragflow
