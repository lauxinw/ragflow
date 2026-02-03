# Table Processing API - 详细文档

## 概述

表格处理 API 提供了从文档中提取、识别和构建表格的完整功能。

## 核心组件

### 1. TableStructureRecognizer (表格结构识别器)

#### 功能说明

`TableStructureRecognizer` 类负责识别和构建表格结构，包括：
- 识别表格行和列
- 检测表头
- 处理跨行跨列单元格
- 生成 HTML 或文本格式的表格

#### 主要方法

##### construct_table()

从检测框构建表格。

**语法:**
```python
table = TableStructureRecognizer.construct_table(
    boxes,
    is_english=False,
    html=True,
    **kwargs
)
```

**参数:**
- `boxes` (List[Dict]): 检测框列表，每个框需包含：
  - `text`: 文本内容
  - `x0`, `x1`: 水平位置
  - `top`, `bottom`: 垂直位置
  - `rn`: 行号 (可选)
  - `cn`: 列号 (可选)
  - `R`: 行标识 (可选)
  - `C`: 列标识 (可选)
  - `H`: 是否为表头 (可选)
  
- `is_english` (bool): 内容是否为英文
- `html` (bool): 返回 HTML 格式 (True) 或文本格式 (False)

**返回值:**
- 如果 `html=True`: 返回 HTML 字符串
- 如果 `html=False`: 返回描述性文本列表

**示例:**

```python
from ragflow_processing_api.table import TableStructureRecognizer

recognizer = TableStructureRecognizer()

# 准备检测框
boxes = [
    {
        "text": "姓名",
        "x0": 0, "x1": 100,
        "top": 0, "bottom": 20,
        "R": "0", "C": "0",
        "H": True
    },
    {
        "text": "年龄",
        "x0": 100, "x1": 200,
        "top": 0, "bottom": 20,
        "R": "0", "C": "1",
        "H": True
    },
    {
        "text": "张三",
        "x0": 0, "x1": 100,
        "top": 20, "bottom": 40,
        "R": "1", "C": "0"
    },
    {
        "text": "25",
        "x0": 100, "x1": 200,
        "top": 20, "bottom": 40,
        "R": "1", "C": "1"
    }
]

# 生成 HTML 表格
html_table = recognizer.construct_table(boxes, html=True)
print(html_table)
# 输出:
# <table>
# <tr><th>姓名</th><th>年龄</th></tr>
# <tr><td>张三</td><td>25</td></tr>
# </table>

# 生成描述性文本
text_table = recognizer.construct_table(boxes, html=False)
print(text_table)
# 输出: ['姓名：张三; 年龄：25']
```

##### is_caption()

判断一个框是否为表格标题。

```python
is_cap = TableStructureRecognizer.is_caption(box)
```

##### blockType()

判断文本块的类型（日期、数字、文本等）。

```python
btype = TableStructureRecognizer.blockType(box)
```

### 2. ExcelTableProcessor (Excel 表格处理器)

#### 功能说明

`ExcelTableProcessor` 类专门用于处理 Excel 文件，提供以下功能：
- 读取 Excel 工作簿
- 解析表头
- 提取表格数据
- 处理合并单元格
- 转换为 DataFrame

#### 主要方法

##### process_file()

处理 Excel 文件并提取所有表格。

**语法:**
```python
tables = processor.process_file(
    file_path_or_binary,
    from_page=0,
    to_page=10000000000,
    callback=None
)
```

**参数:**
- `file_path_or_binary`: Excel 文件路径或 BytesIO 对象
- `from_page`: 起始行号（默认 0）
- `to_page`: 结束行号（默认全部）
- `callback`: 回调函数，用于进度通知

**返回值:**
列表，每个元素包含：
- `sheet_name`: 工作表名称
- `dataframe`: pandas DataFrame 对象
- `headers`: 表头列表
- `header_rows`: 表头行数
- `num_rows`: 数据行数

**示例:**

```python
from ragflow_processing_api.table import ExcelTableProcessor

processor = ExcelTableProcessor()

# 处理 Excel 文件
tables = processor.process_file("销售数据.xlsx")

for table in tables:
    print(f"工作表: {table['sheet_name']}")
    print(f"表头: {table['headers']}")
    print(f"数据行数: {table['num_rows']}")
    print("\n数据预览:")
    print(table['dataframe'].head())
```

##### process_file_to_dict()

将 Excel 文件转换为字典列表。

```python
dict_data = processor.process_file_to_dict("data.xlsx")
```

返回的每个字典代表一行数据，包含所有列的值。

## 使用场景

### 场景 1: 从 PDF 提取表格

```python
from ragflow_processing_api.table import TableStructureRecognizer
# 假设已经通过 OCR 或布局检测获得了 boxes

recognizer = TableStructureRecognizer()

# 构建表格
html_tables = []
for page_boxes in all_pages_boxes:
    html_table = recognizer.construct_table(
        page_boxes,
        is_english=True,
        html=True
    )
    html_tables.append(html_table)
```

### 场景 2: 批量处理 Excel 文件

```python
import os
from ragflow_processing_api.table import ExcelTableProcessor

processor = ExcelTableProcessor()

# 处理目录下所有 Excel 文件
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]

all_data = []
for excel_file in excel_files:
    tables = processor.process_file(excel_file)
    for table in tables:
        all_data.append({
            'file': excel_file,
            'sheet': table['sheet_name'],
            'data': table['dataframe']
        })
```

### 场景 3: 表格转换

```python
from ragflow_processing_api.table import TableStructureRecognizer

recognizer = TableStructureRecognizer()

# 同一组 boxes 生成不同格式
html_version = recognizer.construct_table(boxes, html=True)
text_version = recognizer.construct_table(boxes, html=False)

# 保存为文件
with open('table.html', 'w', encoding='utf-8') as f:
    f.write(html_version)

with open('table.txt', 'w', encoding='utf-8') as f:
    for line in text_version:
        f.write(line + '\n')
```

## 最佳实践

1. **检测框质量**: 确保输入的 boxes 具有准确的位置信息
2. **表头识别**: 正确标记表头框（设置 `H` 属性或通过位置判断）
3. **中英文处理**: 根据内容语言设置 `is_english` 参数
4. **大文件处理**: 使用 `from_page` 和 `to_page` 参数分批处理
5. **错误处理**: 添加 try-except 捕获异常

## 常见问题

**Q: 如何处理跨页表格？**

A: 设置 boxes 中的 `page_number` 属性，系统会自动处理跨页情况。

**Q: 表格行列识别不准确怎么办？**

A: 确保 boxes 中的 `R` (行) 和 `C` (列) 属性正确，或者提供准确的位置信息。

**Q: 如何处理合并单元格？**

A: 在 boxes 中标记 `SP` 属性，并提供 `H_left`, `H_right`, `H_top`, `H_bott` 信息。
