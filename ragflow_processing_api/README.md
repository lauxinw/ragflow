# RAGFlow Processing API

[English](#english) | [中文](#中文)

---

## English

### Overview

RAGFlow Processing API is a standalone API extracted from [RAGFlow](https://github.com/infiniflow/ragflow) for processing tables, images, and lists in documents. This subsystem provides independent Python APIs that clone RAGFlow's document processing behavior.

### Key Features

- **📊 Table Processing**: Extract and recognize table structures from documents and Excel files
- **🖼️ Image Processing**: OCR text recognition and image analysis
- **📝 List Processing**: Automatic detection and extraction of ordered/unordered lists

### Installation

```bash
cd ragflow_processing_api
pip install -r requirements.txt
```

### Quick Start

```python
from ragflow_processing_api import TableProcessor, ImageProcessor, ListProcessor

# Table processing
table_processor = TableProcessor()
tables = table_processor.process_excel("data.xlsx")

# Image processing
image_processor = ImageProcessor()
text = image_processor.ocr("document.jpg")

# List processing
list_processor = ListProcessor()
lists = list_processor.extract(text)
```

### Documentation

- [README](docs/README.md) - Complete documentation
- [Table API](docs/TABLE_API.md) - Table processing API
- [Image API](docs/IMAGE_API.md) - Image processing API
- [List API](docs/LIST_API.md) - List processing API

### Examples

Run the example scripts:

```bash
python examples/table_example.py
python examples/image_example.py
python examples/list_example.py
```

### Architecture

```
ragflow_processing_api/
├── __init__.py           # Unified interface
├── table/                # Table processing module
├── image/                # Image processing module
├── list/                 # List processing module
├── examples/             # Example scripts
└── docs/                 # Documentation
```

### License

Apache License 2.0

---

## 中文

### 概述

RAGFlow Processing API 是从 [RAGFlow](https://github.com/infiniflow/ragflow) 中提取的文档处理核心功能的独立 API。这个子系统提供了独立的 Python API，完全克隆了 RAGFlow 的文档处理行为。

### 核心功能

- **📊 表格处理**: 从文档和 Excel 文件中提取和识别表格结构
- **🖼️ 图片处理**: OCR 文字识别和图片分析
- **📝 列表处理**: 自动检测和提取有序/无序列表

### 安装方法

```bash
cd ragflow_processing_api
pip install -r requirements.txt
```

### 快速开始

```python
from ragflow_processing_api import TableProcessor, ImageProcessor, ListProcessor

# 表格处理
table_processor = TableProcessor()
tables = table_processor.process_excel("data.xlsx")

# 图片处理
image_processor = ImageProcessor()
text = image_processor.ocr("document.jpg")

# 列表处理
list_processor = ListProcessor()
lists = list_processor.extract(text)
```

### 文档

- [完整文档](docs/README.md) - 完整使用文档
- [表格 API](docs/TABLE_API.md) - 表格处理 API 文档
- [图片 API](docs/IMAGE_API.md) - 图片处理 API 文档
- [列表 API](docs/LIST_API.md) - 列表处理 API 文档

### 示例

运行示例脚本：

```bash
python examples/table_example.py
python examples/image_example.py
python examples/list_example.py
```

### 目录结构

```
ragflow_processing_api/
├── __init__.py           # 统一接口
├── table/                # 表格处理模块
├── image/                # 图片处理模块
├── list/                 # 列表处理模块
├── examples/             # 示例脚本
└── docs/                 # 文档
```

### 许可证

Apache License 2.0
