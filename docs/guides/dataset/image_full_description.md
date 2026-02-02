---
sidebar_position: 6
slug: /image_full_description
---

# 图片完整内容描述配置指南 / Image Full Description Configuration Guide

## 中文说明

### 问题描述

RAGFlow 默认的图片解析行为是使用 OCR 提取图片中的文字。如果你需要获取图片的完整内容描述（而不仅仅是文字提取），可以通过以下两种方式实现：

### 方案一：使用 Agent 数据流水线（推荐）

Agent 的数据流水线提供了更灵活的图片解析配置，可以通过 REST API 控制。

#### 1. 创建带有 Parser 组件的数据流水线

通过 REST API 创建或更新数据流水线时，在 Parser 组件的配置中为图片类型指定 VLM 模型：

```bash
curl --request POST \
  --url http://{address}/api/v1/pipelines \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "图片完整描述流水线",
    "dsl": {
      "components": {
        "Parser": {
          "setups": {
            "image": {
              "parse_method": "gpt-4o",
              "llm_id": "",
              "lang": "Chinese",
              "system_prompt": "请详细描述这张图片的内容，包括场景、物体、人物、颜色、布局等所有可见元素。",
              "output_format": "json"
            }
          }
        }
      }
    }
  }'
```

**关键配置项说明：**

- `parse_method`: 设置为 VLM 模型名称（如 `"gpt-4o"`, `"gpt-4-vision-preview"`, `"gemini-1.5-pro"` 等），而不是默认的 `"ocr"`
- `lang`: 设置语言，如 `"Chinese"` 或 `"English"`
- `system_prompt`: （可选）自定义提示词，指导模型如何描述图片
- `llm_id`: （可选）指定具体的模型 ID

#### 2. 创建数据集并关联流水线

```bash
curl --request POST \
  --url http://{address}/api/v1/datasets \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "图片数据集",
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "pipeline_id": "<PIPELINE_ID>",
    "parse_type": 1
  }'
```

**注意：** 使用流水线时，不要同时指定 `chunk_method` 或 `parser_config`。

#### 3. 上传图片文件

```bash
curl --request POST \
  --url http://{address}/api/v1/documents/upload \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --form 'file=@/path/to/image.jpg' \
  --form 'kb_id=<DATASET_ID>'
```

### 方案二：使用 Picture 块方法配置（适用于简单场景）

如果你使用的是内置的 `picture` 块方法，它有自动行为：

- 如果 OCR 提取的文本较短（<32个字符），会自动调用 VLM 模型生成完整描述
- 如果 OCR 文本较长，则只使用 OCR 结果

**创建数据集时指定 picture 块方法：**

```bash
curl --request POST \
  --url http://{address}/api/v1/datasets \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "图片数据集",
    "chunk_method": "picture",
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "parser_config": {
      "image_context_size": 0
    }
  }'
```

**配置项说明：**
- `image_context_size`: 设置图片上下文窗口大小（默认为 0）

**限制：** 此方法会自动判断是否使用 VLM，无法强制总是使用 VLM 进行完整描述。

### 方案三：更新现有文档的解析方式

如果你已经上传了文档，可以通过 `change_parser` API 更新其解析配置：

```bash
curl --request POST \
  --url http://{address}/api/v1/documents/change_parser \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "doc_id": "<DOCUMENT_ID>",
    "pipeline_id": "<PIPELINE_ID>",
    "parser_id": "parser"
  }'
```

### 支持的 VLM 模型

常见的 VLM（视觉语言模型）包括：

- OpenAI: `gpt-4o`, `gpt-4-turbo`, `gpt-4-vision-preview`
- Google: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro-vision`
- Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`
- 阿里: `qwen-vl-plus`, `qwen-vl-max`
- 其他开源模型（需要先在系统中配置）

**重要提示：** 确保你在 RAGFlow 的模型管理中已经配置了相应的 VLM 模型。

---

## English Documentation

### Problem Description

By default, RAGFlow uses OCR to extract text from images. If you need to get a complete description of image content (not just text extraction), you can achieve this through the following methods:

### Solution 1: Using Agent Ingestion Pipeline (Recommended)

The Agent ingestion pipeline provides more flexible image parsing configuration that can be controlled via REST API.

#### 1. Create an Ingestion Pipeline with Parser Component

When creating or updating an ingestion pipeline via REST API, specify a VLM model for image type in the Parser component configuration:

```bash
curl --request POST \
  --url http://{address}/api/v1/pipelines \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "Image Full Description Pipeline",
    "dsl": {
      "components": {
        "Parser": {
          "setups": {
            "image": {
              "parse_method": "gpt-4o",
              "llm_id": "",
              "lang": "English",
              "system_prompt": "Please provide a detailed description of this image, including the scene, objects, people, colors, layout, and all visible elements.",
              "output_format": "json"
            }
          }
        }
      }
    }
  }'
```

**Key Configuration Parameters:**

- `parse_method`: Set to a VLM model name (e.g., `"gpt-4o"`, `"gpt-4-vision-preview"`, `"gemini-1.5-pro"`) instead of the default `"ocr"`
- `lang`: Set language, e.g., `"Chinese"` or `"English"`
- `system_prompt`: (Optional) Custom prompt to guide how the model describes the image
- `llm_id`: (Optional) Specify a specific model ID

#### 2. Create Dataset and Associate Pipeline

```bash
curl --request POST \
  --url http://{address}/api/v1/datasets \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "Image Dataset",
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "pipeline_id": "<PIPELINE_ID>",
    "parse_type": 1
  }'
```

**Note:** When using a pipeline, do not specify `chunk_method` or `parser_config` at the same time.

#### 3. Upload Image Files

```bash
curl --request POST \
  --url http://{address}/api/v1/documents/upload \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --form 'file=@/path/to/image.jpg' \
  --form 'kb_id=<DATASET_ID>'
```

### Solution 2: Using Picture Chunk Method (For Simple Scenarios)

If you're using the built-in `picture` chunk method, it has automatic behavior:

- If OCR-extracted text is short (<32 characters), it automatically calls the VLM model for a complete description
- If OCR text is long, it uses only the OCR result

**Create a dataset with picture chunk method:**

```bash
curl --request POST \
  --url http://{address}/api/v1/datasets \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "name": "Image Dataset",
    "chunk_method": "picture",
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "parser_config": {
      "image_context_size": 0
    }
  }'
```

**Configuration Parameters:**
- `image_context_size`: Set image context window size (default is 0)

**Limitation:** This method automatically determines whether to use VLM and cannot force always using VLM for complete descriptions.

### Solution 3: Update Existing Document Parsing Method

If you've already uploaded documents, you can update their parsing configuration via the `change_parser` API:

```bash
curl --request POST \
  --url http://{address}/api/v1/documents/change_parser \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <YOUR_API_KEY>' \
  --data '{
    "doc_id": "<DOCUMENT_ID>",
    "pipeline_id": "<PIPELINE_ID>",
    "parser_id": "parser"
  }'
```

### Supported VLM Models

Common VLM (Vision Language Models) include:

- OpenAI: `gpt-4o`, `gpt-4-turbo`, `gpt-4-vision-preview`
- Google: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro-vision`
- Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`
- Alibaba: `qwen-vl-plus`, `qwen-vl-max`
- Other open-source models (must be configured in the system first)

**Important:** Make sure you have configured the corresponding VLM model in RAGFlow's model management.

## Practical Example

For a complete working example with Python code, see [image_description_api_example.py](/docs/examples/image_description_api_example.py) which demonstrates all three approaches with step-by-step API calls.

---

## Code References

For developers interested in the implementation details:

- Image parser configuration: `rag/flow/parser/parser.py` (lines 121-128, 630-647)
- Picture chunk method: `rag/app/picture.py` (lines 36-92)
- Parser component in agent pipeline: `agent/component/parser.py`
- Frontend image form: `web/src/pages/agent/form/parser-form/image-form-fields.tsx`

## See Also

- [Configure Knowledge Base](/docs/guides/dataset/configure_knowledge_base)
- [Agent Ingestion Pipeline Quickstart](/docs/guides/agent/agent_quickstarts/ingestion_pipeline_quickstart)
- [HTTP API Reference](/docs/references/http_api_reference)
