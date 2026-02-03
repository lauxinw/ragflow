# RAGFlow Processing API - 快速入门指南

## 安装

### 1. 基础安装

```bash
cd ragflow_processing_api
pip install -r requirements.txt
```

### 2. 可选组件

根据需要安装 OCR 引擎和视觉模型：

```bash
# 安装 PaddleOCR（推荐用于 OCR）
pip install paddleocr

# 或安装 Tesseract
pip install pytesseract

# 安装视觉语言模型（用于图片描述）
pip install transformers torch
```

## 快速开始

### 1. 表格处理

#### 处理 Excel 文件

```python
from ragflow_processing_api import TableProcessor

processor = TableProcessor()

# 读取 Excel 文件
tables = processor.process_excel("sales_data.xlsx")

# 遍历所有工作表
for table in tables:
    print(f"工作表: {table['sheet_name']}")
    print(f"表头: {table['headers']}")
    df = table['dataframe']
    print(df.head())
```

#### 从检测框构建表格

```python
from ragflow_processing_api.table import TableStructureRecognizer

recognizer = TableStructureRecognizer()

# 假设你已经通过 OCR 或布局检测获得了 boxes
boxes = [...]  # 包含位置和文本信息的检测框列表

# 生成 HTML 表格
html_table = recognizer.construct_table(boxes, html=True)
print(html_table)

# 生成描述性文本
text_table = recognizer.construct_table(boxes, html=False)
for row in text_table:
    print(row)
```

### 2. 图片处理

#### OCR 文字识别

```python
from ragflow_processing_api import ImageProcessor
from PIL import Image

processor = ImageProcessor()

# 从文件识别
text = processor.ocr("document.jpg", return_boxes=False)
print(f"识别的文字:\n{text}")

# 获取详细信息（包括边界框）
results = processor.ocr("document.jpg", return_boxes=True)
for bbox, (text, confidence) in results:
    print(f"文字: {text}, 置信度: {confidence:.2f}")
```

#### 图片描述

```python
from ragflow_processing_api import ImageProcessor

processor = ImageProcessor()

# 基础描述
description = processor.describe("chart.png")
print(f"图片描述: {description}")

# 带上下文的描述
description = processor.describe(
    "chart.png",
    context={
        "above": "2024年销售趋势",
        "below": "同比增长显著"
    }
)
print(f"上下文描述: {description}")
```

### 3. 列表处理

#### 提取列表

```python
from ragflow_processing_api import ListProcessor

processor = ListProcessor()

text = """
任务清单:
1. 完成报告
2. 发送邮件
3. 安排会议

注意事项:
- 检查格式
- 确认收件人
- 准备材料
"""

# 提取所有列表
lists = processor.extract(text)

for i, lst in enumerate(lists):
    print(f"\n列表 {i+1} ({lst['type']}):")
    for item in lst['items']:
        print(f"  - {item}")
```

#### 格式化列表

```python
from ragflow_processing_api import ListProcessor

processor = ListProcessor()

# 提取列表
lists = processor.extract(text)

# 转换为 HTML
html = processor.format(lists[0], format='html')
print(html)

# 转换为 Markdown
markdown = processor.format(lists[0], format='markdown')
print(markdown)
```

## 常见使用场景

### 场景 1: 文档内容提取

```python
from ragflow_processing_api import ImageProcessor, ListProcessor

# 1. 从文档图片提取文字
image_processor = ImageProcessor()
text = image_processor.ocr("document_page.jpg", return_boxes=False)

# 2. 从文字中提取列表
list_processor = ListProcessor()
lists = list_processor.extract(text)

# 3. 输出结构化数据
for lst in lists:
    print(f"列表类型: {lst['type']}")
    print(f"项目数量: {len(lst['items'])}")
    for item in lst['items']:
        print(f"  - {item}")
```

### 场景 2: 批量处理文档

```python
from ragflow_processing_api import TableProcessor
import glob

processor = TableProcessor()

# 处理目录下所有 Excel 文件
excel_files = glob.glob("data/*.xlsx")

all_data = []
for file in excel_files:
    print(f"处理: {file}")
    tables = processor.process_excel(file)
    
    for table in tables:
        all_data.append({
            'file': file,
            'sheet': table['sheet_name'],
            'rows': table['num_rows'],
            'data': table['dataframe']
        })

print(f"共处理 {len(all_data)} 个表格")
```

### 场景 3: 图表分析流程

```python
from ragflow_processing_api import ImageProcessor

processor = ImageProcessor()

# 1. OCR 识别图表中的文字
text = processor.ocr("sales_chart.png", return_boxes=False)
print(f"图表中的文字: {text}")

# 2. 生成图表描述
description = processor.describe(
    "sales_chart.png",
    context={
        "above": "2024年销售数据",
        "below": "各区域销售对比"
    }
)
print(f"图表描述: {description}")
```

### 场景 4: 嵌套列表处理

```python
from ragflow_processing_api.list import ListExtractor, ListFormatter

extractor = ListExtractor()
formatter = ListFormatter()

text = """
项目计划:
1. 第一阶段
   - 需求分析
   - 方案设计
2. 第二阶段
   - 开发实现
   - 测试验证
3. 第三阶段
   - 部署上线
   - 运维监控
"""

# 提取嵌套结构
nested_lists = extractor.extract_nested_lists(text)

# 格式化输出
for item in nested_lists:
    markdown = formatter.format_nested_markdown(item)
    print(markdown)
```

## 高级用法

### 自定义列表提取器

```python
from ragflow_processing_api.list import ListExtractor
import re

class CustomListExtractor(ListExtractor):
    def __init__(self):
        super().__init__()
        # 添加自定义模式，如任务列表
        task_pattern = r'^\s*\[[ xX]\]\s+(.+)$'
        self.unordered_regex.append(re.compile(task_pattern, re.MULTILINE))

extractor = CustomListExtractor()

text = """
待办事项:
[x] 已完成的任务
[ ] 待完成的任务
[X] 另一个已完成的任务
"""

lists = extractor.extract_lists(text)
print(lists)
```

### 集成真实 OCR 引擎

```python
from ragflow_processing_api.image import OCRProcessor
from paddleocr import PaddleOCR

class PaddleOCRProcessor(OCRProcessor):
    def __init__(self):
        super().__init__()
        self.engine = PaddleOCR(use_angle_cls=True, lang='ch')
    
    def process_image(self, image, return_boxes=True):
        # 使用 PaddleOCR 处理
        result = self.engine.ocr(image)
        
        if return_boxes:
            boxes = []
            for line in result[0]:
                bbox = line[0]
                text, conf = line[1]
                boxes.append((bbox, (text, conf)))
            return boxes
        else:
            texts = [line[1][0] for line in result[0]]
            return "\n".join(texts)

# 使用自定义 OCR 处理器
ocr = PaddleOCRProcessor()
text = ocr.process_image("document.jpg", return_boxes=False)
```

## 性能优化建议

### 1. 批量处理

```python
from ragflow_processing_api import ImageProcessor
import glob

processor = ImageProcessor()

# 收集所有图片
images = glob.glob("documents/*.jpg")

# 批量处理而不是逐个处理
results = processor.ocr_processor.process_batch(images, return_boxes=False)
```

### 2. 并行处理

```python
from concurrent.futures import ThreadPoolExecutor
from ragflow_processing_api import TableProcessor

def process_excel(file):
    processor = TableProcessor()
    return processor.process_excel(file)

files = ["file1.xlsx", "file2.xlsx", "file3.xlsx"]

# 并行处理多个文件
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_excel, files))
```

### 3. 结果缓存

```python
from functools import lru_cache
from ragflow_processing_api import ImageProcessor

processor = ImageProcessor()

@lru_cache(maxsize=100)
def cached_ocr(image_path):
    return processor.ocr(image_path, return_boxes=False)

# 重复调用会使用缓存
text1 = cached_ocr("doc.jpg")
text2 = cached_ocr("doc.jpg")  # 从缓存获取
```

## 错误处理

```python
from ragflow_processing_api import TableProcessor, ImageProcessor

# 表格处理错误处理
table_processor = TableProcessor()
try:
    tables = table_processor.process_excel("data.xlsx")
except FileNotFoundError:
    print("文件不存在")
except Exception as e:
    print(f"处理错误: {e}")

# 图片处理错误处理
image_processor = ImageProcessor()
try:
    text = image_processor.ocr("image.jpg", return_boxes=False)
except Exception as e:
    print(f"OCR 错误: {e}")
```

## 常见问题

### Q: 如何处理大型 Excel 文件？

使用分页参数：

```python
processor = TableProcessor()
tables = processor.process_excel(
    "large_file.xlsx",
    from_page=0,
    to_page=1000  # 只处理前1000行
)
```

### Q: 如何提高 OCR 准确率？

1. 预处理图片（去噪、二值化）
2. 使用更好的 OCR 引擎
3. 调整图片分辨率

### Q: 列表识别不准确怎么办？

1. 检查文本格式和缩进
2. 添加自定义列表模式
3. 预处理文本统一格式

## 下一步

- 查看完整 API 文档: `docs/README.md`
- 运行示例脚本: `python examples/*.py`
- 集成到你的项目中
- 根据需求定制和扩展
