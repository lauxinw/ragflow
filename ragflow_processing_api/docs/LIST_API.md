# List Processing API - 详细文档

## 概述

列表处理 API 提供了从文本中提取和格式化列表的完整功能。

## 核心组件

### 1. ListExtractor (列表提取器)

#### 功能说明

`ListExtractor` 类用于从文本中自动识别和提取列表，支持：
- 有序列表（数字、字母、罗马数字）
- 无序列表（各种bullet符号）
- 嵌套列表
- 列表统计

#### 支持的列表格式

##### 有序列表
```
1. 第一项
2. 第二项
3. 第三项

a. 选项A
b. 选项B

i. 罗马数字一
ii. 罗马数字二
```

##### 无序列表
```
- 项目一
- 项目二

• 要点一
• 要点二

* 列表项
* 另一项
```

#### 主要方法

##### extract_lists()

提取文本中的所有列表。

**语法:**
```python
lists = extractor.extract_lists(text)
```

**返回值:**
列表，每个元素包含：
- `type`: 'ordered' 或 'unordered'
- `items`: 列表项内容
- `markers`: 列表标记（仅有序列表）
- `indentation`: 缩进级别

**示例:**

```python
from ragflow_processing_api.list import ListExtractor

extractor = ListExtractor()

text = """
购物清单:
1. 牛奶
2. 面包
3. 鸡蛋

注意事项:
- 选择新鲜的
- 检查保质期
- 注意价格
"""

lists = extractor.extract_lists(text)

for i, lst in enumerate(lists):
    print(f"\n列表 {i+1}:")
    print(f"类型: {lst['type']}")
    print(f"项目: {lst['items']}")
    if 'markers' in lst:
        print(f"标记: {lst['markers']}")
```

##### extract_nested_lists()

提取嵌套列表结构。

**语法:**
```python
nested_lists = extractor.extract_nested_lists(text)
```

**返回值:**
树形结构的列表，每个节点包含：
- `type`: 列表类型
- `content`: 内容
- `marker`: 标记
- `level`: 层级
- `children`: 子列表

**示例:**

```python
text = """
课程大纲:
1. 第一章：介绍
   - 背景知识
   - 学习目标
2. 第二章：基础
   - 基本概念
   - 实践练习
3. 第三章：进阶
"""

nested = extractor.extract_nested_lists(text)

def print_tree(items, indent=0):
    for item in items:
        print("  " * indent + f"- {item['content']}")
        if item.get('children'):
            print_tree(item['children'], indent + 1)

print_tree(nested)
```

##### count_lists()

统计文本中的列表信息。

```python
stats = extractor.count_lists(text)
# 返回: {
#   'total': 总列表数,
#   'ordered': 有序列表数,
#   'unordered': 无序列表数,
#   'total_items': 总项目数
# }
```

##### extract_list_items_only()

仅提取列表项内容，返回扁平列表。

```python
items = extractor.extract_list_items_only(text)
# 返回: ['项目1', '项目2', '项目3', ...]
```

##### is_list_content()

检查文本是否包含列表。

```python
has_lists = extractor.is_list_content(text)
# 返回: True 或 False
```

### 2. ListFormatter (列表格式化器)

#### 功能说明

`ListFormatter` 类用于将列表转换为不同的输出格式。

#### 主要方法

##### format_as_html()

格式化为 HTML。

**语法:**
```python
html = formatter.format_as_html(
    items,
    ordered=False,
    nested=False
)
```

**示例:**

```python
from ragflow_processing_api.list import ListFormatter

formatter = ListFormatter()

items = ['Python', 'Java', 'JavaScript']

# 有序列表
html = formatter.format_as_html(items, ordered=True)
print(html)
# 输出:
# <ol>
# <li>Python</li>
# <li>Java</li>
# <li>JavaScript</li>
# </ol>

# 无序列表
html = formatter.format_as_html(items, ordered=False)
print(html)
# 输出:
# <ul>
# <li>Python</li>
# <li>Java</li>
# <li>JavaScript</li>
# </ul>
```

##### format_as_markdown()

格式化为 Markdown。

```python
markdown = formatter.format_as_markdown(
    items,
    ordered=False,
    start_number=1
)
```

**示例:**

```python
items = ['第一步', '第二步', '第三步']

# 有序列表
md = formatter.format_as_markdown(items, ordered=True)
print(md)
# 输出:
# 1. 第一步
# 2. 第二步
# 3. 第三步

# 无序列表
md = formatter.format_as_markdown(items, ordered=False)
print(md)
# 输出:
# - 第一步
# - 第二步
# - 第三步
```

##### format_as_text()

格式化为纯文本。

```python
text = formatter.format_as_text(
    items,
    indent='  ',
    bullet='•'
)
```

##### format_nested_html()

格式化嵌套列表为 HTML。

```python
html = formatter.format_nested_html(nested_list)
```

##### format_nested_markdown()

格式化嵌套列表为 Markdown。

```python
markdown = formatter.format_nested_markdown(
    nested_list,
    level=0,
    indent='  '
)
```

## 使用场景

### 场景 1: 从文档提取所有列表

```python
from ragflow_processing_api.list import ListExtractor

extractor = ListExtractor()

# 读取文档
with open('document.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取所有列表
lists = extractor.extract_lists(text)

# 保存为 JSON
import json
with open('lists.json', 'w', encoding='utf-8') as f:
    json.dump(lists, f, ensure_ascii=False, indent=2)
```

### 场景 2: 列表格式转换

```python
from ragflow_processing_api import ListProcessor

processor = ListProcessor()

# 提取列表
markdown_text = """
# 任务列表
1. 完成报告
2. 发送邮件
3. 召开会议
"""

lists = processor.extract(markdown_text)

# 转换为 HTML
for lst in lists:
    html = processor.format(lst, format='html')
    print(html)
```

### 场景 3: 列表统计分析

```python
from ragflow_processing_api.list import ListExtractor

extractor = ListExtractor()

# 分析多个文档
documents = ['doc1.txt', 'doc2.txt', 'doc3.txt']
all_stats = []

for doc in documents:
    with open(doc, 'r', encoding='utf-8') as f:
        text = f.read()
    
    stats = extractor.count_lists(text)
    stats['filename'] = doc
    all_stats.append(stats)

# 输出统计
for stat in all_stats:
    print(f"\n文件: {stat['filename']}")
    print(f"总列表数: {stat['total']}")
    print(f"总项目数: {stat['total_items']}")
```

### 场景 4: 嵌套列表处理

```python
from ragflow_processing_api.list import ListExtractor, ListFormatter

extractor = ListExtractor()
formatter = ListFormatter()

text = """
目录:
1. 第一部分
   a. 章节1.1
   b. 章节1.2
2. 第二部分
   a. 章节2.1
   b. 章节2.2
"""

# 提取嵌套结构
nested = extractor.extract_nested_lists(text)

# 转换为 Markdown
for item in nested:
    md = formatter.format_nested_markdown(item)
    print(md)
```

### 场景 5: 批量文档列表提取

```python
from ragflow_processing_api.list import ListExtractor
import glob
import pandas as pd

extractor = ListExtractor()

# 处理所有文档
documents = glob.glob('*.txt')
all_lists = []

for doc in documents:
    with open(doc, 'r', encoding='utf-8') as f:
        text = f.read()
    
    lists = extractor.extract_lists(text)
    for lst in lists:
        for item in lst['items']:
            all_lists.append({
                'document': doc,
                'type': lst['type'],
                'item': item
            })

# 转换为 DataFrame
df = pd.DataFrame(all_lists)
df.to_csv('extracted_lists.csv', index=False)
```

## 高级用法

### 自定义列表模式

```python
from ragflow_processing_api.list import ListExtractor
import re

class CustomListExtractor(ListExtractor):
    def __init__(self):
        super().__init__()
        # 添加自定义模式
        custom_pattern = r'^\s*[√]\s+(.+)$'  # 勾选列表
        self.unordered_regex.append(re.compile(custom_pattern, re.MULTILINE))
```

### Markdown 专用提取器

```python
from ragflow_processing_api.list import MarkdownListExtractor

extractor = MarkdownListExtractor()

markdown = """
# 标题

- 列表项 1
- 列表项 2
  - 嵌套项 2.1
  - 嵌套项 2.2
- 列表项 3
"""

lists = extractor.extract_markdown_lists(markdown)
```

## 最佳实践

1. **文本预处理**: 清理文本中的特殊字符和格式
2. **编码处理**: 确保正确的 UTF-8 编码
3. **多语言支持**: 考虑不同语言的列表模式
4. **性能优化**: 大文本建议分段处理
5. **结果验证**: 检查提取结果的准确性

## 常见问题

**Q: 如何处理非标准的列表格式？**

A: 可以继承 `ListExtractor` 类并添加自定义的正则表达式模式。

**Q: 嵌套列表的层级识别不准确怎么办？**

A: 确保文本中的缩进一致，可以预处理文本统一缩进格式。

**Q: 如何提取任务列表（带复选框）？**

A: 添加自定义模式，如 `^\s*\[[ x]\]\s+(.+)$`。
