# 图片完整内容描述方案总结 / Image Full Description Solution Summary

## 问题 / Problem

用户问题：现有的图片解析只是简单提取图片中的文字，我需要完整描述图片的内容，我使用REST API怎么控制这个行为？

User's question: The current image parsing only extracts text from images. I need complete descriptions of image content. How can I control this behavior using REST API?

## 解决方案 / Solution

### 方法一：使用Agent数据流水线（推荐）/ Method 1: Using Agent Ingestion Pipeline (Recommended)

这是最灵活和可控的方法。通过创建一个自定义的数据流水线，在Parser组件中配置图片解析使用VLM（视觉语言模型）而不是OCR。

This is the most flexible and controllable method. Create a custom ingestion pipeline and configure the Parser component to use VLM (Vision Language Model) instead of OCR for image parsing.

**核心配置 / Key Configuration:**

```json
{
  "image": {
    "parse_method": "gpt-4o",  // 设置为VLM模型名称 / Set to VLM model name
    "lang": "Chinese",         // 语言 / Language
    "system_prompt": "请详细描述这张图片...",  // 自定义提示词 / Custom prompt
    "output_format": "json"
  }
}
```

**API调用流程 / API Call Flow:**

1. 创建带有VLM配置的Pipeline / Create pipeline with VLM config
   ```bash
   POST /api/v1/pipelines
   ```

2. 创建Dataset并关联Pipeline / Create dataset with pipeline
   ```bash
   POST /api/v1/datasets
   Body: {"pipeline_id": "<ID>", "parse_type": 1}
   ```

3. 上传图片 / Upload images
   ```bash
   POST /api/v1/documents/upload
   ```

### 方法二：使用Picture块方法 / Method 2: Using Picture Chunk Method

使用内置的`picture`块方法，它会自动判断是否使用VLM：
- OCR 文本短（<32字符）→ 自动调用VLM生成完整描述
- OCR 文本长（≥32字符）→ 只使用OCR结果

Built-in `picture` chunk method automatically determines whether to use VLM:
- Short OCR text (<32 chars) → Auto-call VLM for full description
- Long OCR text (≥32 chars) → Use OCR result only

**API调用 / API Call:**

```bash
POST /api/v1/datasets
Body: {
  "name": "图片数据集",
  "chunk_method": "picture",
  "parser_config": {"image_context_size": 0}
}
```

**限制 / Limitation:** 无法强制总是使用VLM / Cannot force always using VLM

### 方法三：更新现有文档 / Method 3: Update Existing Documents

如果已经上传了文档，可以更新其解析方式：

If you've already uploaded documents, you can update their parsing method:

```bash
POST /api/v1/documents/change_parser
Body: {
  "doc_id": "<DOC_ID>",
  "pipeline_id": "<PIPELINE_ID>",
  "parser_id": "parser"
}
```

## 支持的VLM模型 / Supported VLM Models

- OpenAI: `gpt-4o`, `gpt-4-turbo`, `gpt-4-vision-preview`
- Google: `gemini-1.5-pro`, `gemini-1.5-flash`
- Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`
- 阿里: `qwen-vl-plus`, `qwen-vl-max`
- 其他在系统中配置的模型 / Other models configured in the system

**重要 / Important:** 必须先在RAGFlow的模型管理中配置VLM模型 / Must configure VLM models in RAGFlow's model management first

## 文档位置 / Documentation Location

### 新增文档 / New Documentation

1. **完整指南 / Complete Guide:**
   - `docs/guides/dataset/image_full_description.md`
   - 包含中英文详细说明、API示例、配置选项
   - Contains bilingual detailed instructions, API examples, configuration options

2. **Python示例代码 / Python Example Code:**
   - `docs/examples/image_description_api_example.py`
   - 可直接运行的完整示例
   - Ready-to-run complete example

3. **示例目录说明 / Examples Directory:**
   - `docs/examples/README.md`
   - 如何使用示例代码
   - How to use example code

### 更新的文档 / Updated Documentation

1. **HTTP API参考 / HTTP API Reference:**
   - `docs/references/http_api_reference.md`
   - 添加了picture块方法的parser_config详细说明
   - Added detailed parser_config for picture chunk method

2. **数据流水线快速开始 / Ingestion Pipeline Quickstart:**
   - `docs/guides/agent/agent_quickstarts/ingestion_pipeline_quickstart.md`
   - 增强了图片解析配置说明
   - Enhanced image parsing configuration instructions

3. **Parser组件参考 / Parser Component Reference:**
   - `docs/guides/agent/agent_component_reference/parser.md`
   - 扩展了图片解析器的详细说明
   - Expanded image parser detailed instructions

## 代码实现位置 / Code Implementation Location

- **图片解析器配置**: `rag/flow/parser/parser.py` (lines 121-128, 630-647)
- **Picture块方法**: `rag/app/picture.py` (lines 36-92)
- **前端图片表单**: `web/src/pages/agent/form/parser-form/image-form-fields.tsx`

## 快速开始 / Quick Start

### 方式1：使用文档 / Option 1: Use Documentation

查看完整指南：
See complete guide:
```
docs/guides/dataset/image_full_description.md
```

### 方式2：使用示例代码 / Option 2: Use Example Code

```bash
# 设置环境变量 / Set environment variables
export RAGFLOW_API_KEY='your-api-key'
export RAGFLOW_URL='http://localhost:8086'

# 运行示例 / Run example
python3 docs/examples/image_description_api_example.py
```

### 方式3：直接使用cURL / Option 3: Direct cURL

参考文档中的cURL示例，直接调用API。
Refer to cURL examples in documentation for direct API calls.

## 总结 / Summary

问题已完全解决！用户现在可以通过三种方式控制图片解析行为：

Problem fully solved! User can now control image parsing behavior through three methods:

1. ✅ **推荐**: 使用Agent数据流水线，完全控制VLM配置
2. ✅ 使用Picture块方法，自动智能判断
3. ✅ 更新已有文档的解析方式

所有方法都有完整的文档、API示例和Python代码示例。

All methods have complete documentation, API examples, and Python code examples.
