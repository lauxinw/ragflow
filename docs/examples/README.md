# RAGFlow API Examples

This directory contains practical examples demonstrating how to use RAGFlow's REST API for various tasks.

## Available Examples

### Image Description API Example

**File:** `image_description_api_example.py`

Demonstrates how to configure RAGFlow to generate complete image descriptions (instead of just OCR text extraction) via REST API.

**What it covers:**
- Creating an ingestion pipeline with VLM-based image parsing
- Creating datasets with different parsing methods
- Uploading images to datasets
- Updating existing documents to use VLM parsing

**Prerequisites:**
- RAGFlow server running
- API key (get from Settings > API Keys in RAGFlow UI)
- VLM model configured in Model providers (e.g., gpt-4o, gemini-1.5-pro)

**Usage:**
```bash
# Set environment variables
export RAGFLOW_API_KEY='your-api-key-here'
export RAGFLOW_URL='http://localhost:8086'  # Optional, defaults to localhost

# Run the example
python3 image_description_api_example.py
```

**Related Documentation:**
- [Image Full Description Guide](/docs/guides/dataset/image_full_description)
- [HTTP API Reference](/docs/references/http_api_reference)
- [Ingestion Pipeline Quickstart](/docs/guides/agent/agent_quickstarts/ingestion_pipeline_quickstart)

## Contributing

If you have created useful examples that others might benefit from, please consider contributing them to this directory:

1. Create a well-documented Python script
2. Include prerequisites and usage instructions
3. Test the example with the latest RAGFlow version
4. Submit a pull request

## Support

For questions or issues with these examples:
- Check the [RAGFlow Documentation](https://ragflow.io/docs)
- Visit the [RAGFlow GitHub Discussions](https://github.com/infiniflow/ragflow/discussions)
- Join the [RAGFlow Discord Community](https://discord.gg/ragflow)
