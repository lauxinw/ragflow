# Image Processing API - 详细文档

## 概述

图片处理 API 提供了 OCR 文字识别和图片分析功能。

## 核心组件

### 1. OCRProcessor (OCR 处理器)

#### 功能说明

`OCRProcessor` 类提供 OCR (Optical Character Recognition) 功能，用于从图片中提取文字。

**注意**: 这是一个简化的接口。在生产环境中，需要集成实际的 OCR 引擎（如 RAGFlow 的 OCR 模型、PaddleOCR 或 Tesseract）。

#### 主要方法

##### process_image()

处理单张图片，提取文字。

**语法:**
```python
result = ocr.process_image(
    image,
    return_boxes=True
)
```

**参数:**
- `image`: 输入图片，支持多种格式：
  - numpy 数组
  - PIL Image 对象
  - 文件路径字符串
  - 二进制数据 (bytes)
- `return_boxes`: 是否返回边界框信息

**返回值:**
- 如果 `return_boxes=True`: 返回 `[(bbox, (text, confidence)), ...]`
- 如果 `return_boxes=False`: 返回拼接的文字字符串

**示例:**

```python
from ragflow_processing_api.image import OCRProcessor
from PIL import Image

ocr = OCRProcessor()

# 从文件处理
result = ocr.process_image("document.jpg", return_boxes=False)
print(f"提取的文字: {result}")

# 从 PIL Image 处理
image = Image.open("document.jpg")
results = ocr.process_image(image, return_boxes=True)
for bbox, (text, confidence) in results:
    print(f"文字: {text}, 置信度: {confidence}")
```

##### process_batch()

批量处理多张图片。

```python
results = ocr.process_batch(
    images,
    return_boxes=True
)
```

##### process_image_region()

处理图片的特定区域。

```python
text = ocr.process_image_region(
    image,
    region=(x0, y0, x1, y1)
)
```

#### OCRResult 类

OCR 结果的容器类，提供便捷的数据访问方法。

```python
from ragflow_processing_api.image import OCRResult

result = OCRResult(ocr_results)

# 获取所有文字
text = result.get_text(separator="\n")

# 获取所有边界框
boxes = result.get_boxes()

# 获取所有置信度
confidences = result.get_confidences()

# 按置信度过滤
filtered = result.filter_by_confidence(0.8)

# 转换为字典
dict_data = result.to_dict()
```

### 2. ImageAnalyzer (图片分析器)

#### 功能说明

`ImageAnalyzer` 类提供图片分析功能，包括：
- 图片描述/说明生成
- 图表理解
- 上下文感知的图片分析

**注意**: 这是一个简化的接口。在生产环境中，需要集成视觉语言模型（如 CLIP、BLIP、LLaVA）。

#### 主要方法

##### describe_image()

生成图片描述。

**语法:**
```python
description = analyzer.describe_image(
    image,
    prompt=None,
    context=None
)
```

**参数:**
- `image`: 输入图片
- `prompt`: 可选的提示词，指导描述生成
- `context`: 可选的上下文字典，包含 'above' 和 'below' 键

**示例:**

```python
from ragflow_processing_api.image import ImageAnalyzer
from PIL import Image

analyzer = ImageAnalyzer()

# 基本描述
image = Image.open("chart.png")
description = analyzer.describe_image(image)
print(description)

# 带提示词
description = analyzer.describe_image(
    image,
    prompt="请详细描述这张图表中的数据趋势"
)

# 带上下文
description = analyzer.describe_image(
    image,
    context={
        "above": "2024年销售数据",
        "below": "总销售额同比增长25%"
    }
)
```

##### extract_figures()

从文档中提取和分析图表。

```python
results = analyzer.extract_figures(
    images,
    contexts=None
)
```

##### batch_describe()

批量生成图片描述。

```python
descriptions = analyzer.batch_describe(
    images,
    prompts=None
)
```

### 3. FigureExtractor (图表提取器)

辅助类，用于从文档中提取图表。

```python
from ragflow_processing_api.image import FigureExtractor, ImageAnalyzer

analyzer = ImageAnalyzer()
extractor = FigureExtractor(analyzer)

# 从位置信息提取图表
results = extractor.extract_from_positions(
    figures_data,
    figure_contexts
)
```

## 使用场景

### 场景 1: 文档 OCR 识别

```python
from ragflow_processing_api.image import OCRProcessor
import os

ocr = OCRProcessor()

# 处理文档图片
doc_images = ["page1.jpg", "page2.jpg", "page3.jpg"]
all_text = []

for img_path in doc_images:
    text = ocr.process_image(img_path, return_boxes=False)
    all_text.append(text)

# 合并所有页面文字
full_text = "\n\n".join(all_text)
print(full_text)
```

### 场景 2: 图表分析

```python
from ragflow_processing_api.image import ImageAnalyzer

analyzer = ImageAnalyzer()

# 分析多个图表
charts = ["sales_chart.png", "revenue_chart.png"]
for chart in charts:
    desc = analyzer.describe_image(chart)
    print(f"{chart}: {desc}")
```

### 场景 3: 带上下文的图片理解

```python
from ragflow_processing_api.image import ImageAnalyzer

analyzer = ImageAnalyzer()

# 从 PDF 提取的图片，带周围文字上下文
context_above = "图1: 2024年第一季度销售业绩"
context_below = "从图中可以看出，销售额稳步增长"

description = analyzer.analyze_figure_with_context(
    image,
    context_above=context_above,
    context_below=context_below
)
```

### 场景 4: 批量处理文档图片

```python
from ragflow_processing_api.image import OCRProcessor, ImageAnalyzer
import glob

ocr = OCRProcessor()
analyzer = ImageAnalyzer()

# 获取所有图片
images = glob.glob("documents/*.jpg")

# OCR 处理
print("执行 OCR...")
ocr_results = ocr.process_batch(images, return_boxes=False)

# 图片分析
print("生成描述...")
descriptions = analyzer.batch_describe(images)

# 合并结果
for img, ocr_text, desc in zip(images, ocr_results, descriptions):
    print(f"\n文件: {img}")
    print(f"OCR 文字: {ocr_text[:100]}...")
    print(f"图片描述: {desc}")
```

## 集成实际 OCR 引擎

### 集成 PaddleOCR

```python
from paddleocr import PaddleOCR
from ragflow_processing_api.image import OCRProcessor

class PaddleOCRProcessor(OCRProcessor):
    def __init__(self):
        super().__init__()
        self.engine = PaddleOCR(use_angle_cls=True, lang='ch')
    
    def process_image(self, image, return_boxes=True):
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
```

### 集成 Tesseract

```python
import pytesseract
from PIL import Image

class TesseractOCRProcessor(OCRProcessor):
    def __init__(self):
        super().__init__()
    
    def process_image(self, image, return_boxes=True):
        if isinstance(image, str):
            image = Image.open(image)
        
        if return_boxes:
            data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT
            )
            # 处理并返回结果
            # ...
        else:
            text = pytesseract.image_to_string(image)
            return text
```

## 最佳实践

1. **图片预处理**: 在 OCR 前进行图片预处理（去噪、二值化等）
2. **批量处理**: 使用批量方法提高效率
3. **GPU 加速**: 使用 GPU 加速 OCR 和图片分析
4. **缓存结果**: 缓存处理结果避免重复计算
5. **错误处理**: 添加异常处理和重试机制

## 性能优化

```python
from concurrent.futures import ThreadPoolExecutor
from ragflow_processing_api.image import OCRProcessor

ocr = OCRProcessor()

def process_single_image(image_path):
    return ocr.process_image(image_path, return_boxes=False)

# 并行处理
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(process_single_image, image_list))
```
