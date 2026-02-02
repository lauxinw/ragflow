#!/usr/bin/env python3
"""
Example: How to configure RAGFlow to generate complete image descriptions via REST API

This script demonstrates three approaches to get full image descriptions instead of just OCR text:
1. Using an ingestion pipeline with VLM-based image parsing
2. Using the picture chunk method (with automatic VLM fallback)
3. Updating existing documents to use VLM parsing

Prerequisites:
- RAGFlow server running
- API key configured
- VLM model (e.g., gpt-4o) configured in Model providers
"""

import requests
import json
import os
from typing import Optional

# Configuration
RAGFLOW_URL = os.environ.get("RAGFLOW_URL", "http://localhost:8086")
API_KEY = os.environ.get("RAGFLOW_API_KEY", "your-api-key-here")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def create_ingestion_pipeline_with_vlm(
    pipeline_name: str = "Image Description Pipeline",
    vlm_model: str = "gpt-4o",
    language: str = "English",
    system_prompt: Optional[str] = None
) -> str:
    """
    Create an ingestion pipeline that uses VLM for complete image descriptions.
    
    Args:
        pipeline_name: Name for the pipeline
        vlm_model: VLM model name (e.g., "gpt-4o", "gemini-1.5-pro")
        language: Language for image description
        system_prompt: Optional custom prompt for VLM
    
    Returns:
        Pipeline ID
    """
    if system_prompt is None:
        system_prompt = (
            "Please provide a detailed description of this image, "
            "including the scene, objects, people, colors, layout, "
            "and all visible elements."
        )
    
    pipeline_data = {
        "name": pipeline_name,
        "dsl": {
            "components": {
                "Parser": {
                    "setups": {
                        "image": {
                            "parse_method": vlm_model,
                            "llm_id": "",
                            "lang": language,
                            "system_prompt": system_prompt,
                            "output_format": "json"
                        }
                    }
                }
            }
        }
    }
    
    response = requests.post(
        f"{RAGFLOW_URL}/api/v1/pipelines",
        headers=HEADERS,
        json=pipeline_data
    )
    
    if response.status_code == 200:
        result = response.json()
        pipeline_id = result["data"]["id"]
        print(f"✓ Created pipeline: {pipeline_name} (ID: {pipeline_id})")
        return pipeline_id
    else:
        raise Exception(f"Failed to create pipeline: {response.text}")


def create_dataset_with_pipeline(
    dataset_name: str,
    pipeline_id: str,
    embedding_model: str = "BAAI/bge-large-zh-v1.5"
) -> str:
    """
    Create a dataset that uses the ingestion pipeline with VLM image parsing.
    
    Args:
        dataset_name: Name for the dataset
        pipeline_id: ID of the ingestion pipeline
        embedding_model: Embedding model to use
    
    Returns:
        Dataset ID
    """
    dataset_data = {
        "name": dataset_name,
        "embedding_model": embedding_model,
        "pipeline_id": pipeline_id,
        "parse_type": 1  # Number of parsers in the Parser component
    }
    
    response = requests.post(
        f"{RAGFLOW_URL}/api/v1/datasets",
        headers=HEADERS,
        json=dataset_data
    )
    
    if response.status_code == 200:
        result = response.json()
        dataset_id = result["data"]["id"]
        print(f"✓ Created dataset: {dataset_name} (ID: {dataset_id})")
        return dataset_id
    else:
        raise Exception(f"Failed to create dataset: {response.text}")


def create_dataset_with_picture_method(
    dataset_name: str,
    embedding_model: str = "BAAI/bge-large-zh-v1.5",
    image_context_size: int = 0
) -> str:
    """
    Create a dataset using the 'picture' chunk method.
    
    Note: This method automatically uses VLM only when OCR text is short (<32 chars).
    For full control, use create_dataset_with_pipeline instead.
    
    Args:
        dataset_name: Name for the dataset
        embedding_model: Embedding model to use
        image_context_size: Context window size around images
    
    Returns:
        Dataset ID
    """
    dataset_data = {
        "name": dataset_name,
        "chunk_method": "picture",
        "embedding_model": embedding_model,
        "parser_config": {
            "image_context_size": image_context_size
        }
    }
    
    response = requests.post(
        f"{RAGFLOW_URL}/api/v1/datasets",
        headers=HEADERS,
        json=dataset_data
    )
    
    if response.status_code == 200:
        result = response.json()
        dataset_id = result["data"]["id"]
        print(f"✓ Created dataset: {dataset_name} (ID: {dataset_id})")
        print("  Note: This dataset will automatically use VLM for images with short OCR text")
        return dataset_id
    else:
        raise Exception(f"Failed to create dataset: {response.text}")


def upload_image(dataset_id: str, image_path: str) -> str:
    """
    Upload an image file to a dataset.
    
    Args:
        dataset_id: Target dataset ID
        image_path: Path to the image file
    
    Returns:
        Document ID
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'kb_id': dataset_id}
        
        # Note: For file upload, we don't use JSON content-type
        headers = {"Authorization": f"Bearer {API_KEY}"}
        
        response = requests.post(
            f"{RAGFLOW_URL}/api/v1/documents/upload",
            headers=headers,
            files=files,
            data=data
        )
    
    if response.status_code == 200:
        result = response.json()
        doc_id = result["data"][0]["id"]
        print(f"✓ Uploaded image: {image_path} (Doc ID: {doc_id})")
        return doc_id
    else:
        raise Exception(f"Failed to upload image: {response.text}")


def update_document_parser(doc_id: str, pipeline_id: str):
    """
    Update an existing document to use a different parsing pipeline.
    
    Args:
        doc_id: Document ID to update
        pipeline_id: New pipeline ID to use
    """
    update_data = {
        "doc_id": doc_id,
        "pipeline_id": pipeline_id,
        "parser_id": "parser"
    }
    
    response = requests.post(
        f"{RAGFLOW_URL}/api/v1/documents/change_parser",
        headers=HEADERS,
        json=update_data
    )
    
    if response.status_code == 200:
        print(f"✓ Updated document {doc_id} to use pipeline {pipeline_id}")
    else:
        raise Exception(f"Failed to update document parser: {response.text}")


def trigger_document_parsing(doc_id: str):
    """
    Trigger parsing for a document.
    
    Args:
        doc_id: Document ID to parse
    """
    parse_data = {
        "doc_ids": [doc_id]
    }
    
    response = requests.post(
        f"{RAGFLOW_URL}/api/v1/documents/run",
        headers=HEADERS,
        json=parse_data
    )
    
    if response.status_code == 200:
        print(f"✓ Triggered parsing for document {doc_id}")
    else:
        raise Exception(f"Failed to trigger parsing: {response.text}")


def main():
    """
    Demonstration of three approaches to get full image descriptions.
    """
    print("=" * 60)
    print("RAGFlow Image Description API Examples")
    print("=" * 60)
    
    # Approach 1: Using ingestion pipeline with VLM (Recommended)
    print("\n[Approach 1] Using Ingestion Pipeline with VLM")
    print("-" * 60)
    try:
        pipeline_id = create_ingestion_pipeline_with_vlm(
            pipeline_name="Complete Image Description Pipeline",
            vlm_model="gpt-4o",
            language="English",
            system_prompt=(
                "Describe this image in detail. Include information about "
                "the scene, main subjects, their activities, colors, mood, "
                "and any text visible in the image."
            )
        )
        
        dataset_id = create_dataset_with_pipeline(
            dataset_name="Images with Full Descriptions",
            pipeline_id=pipeline_id
        )
        
        print("\nNow you can upload images to this dataset via:")
        print(f"  - Web UI: Upload to dataset '{dataset_id}'")
        print(f"  - API: upload_image('{dataset_id}', 'path/to/image.jpg')")
        
    except Exception as e:
        print(f"✗ Error in Approach 1: {e}")
    
    # Approach 2: Using picture chunk method
    print("\n[Approach 2] Using Picture Chunk Method")
    print("-" * 60)
    print("Note: This method auto-determines whether to use VLM")
    try:
        dataset_id = create_dataset_with_picture_method(
            dataset_name="Images with Picture Method",
            image_context_size=0
        )
        
        print("\nImages uploaded to this dataset will:")
        print("  - Use OCR if text is long (>32 chars)")
        print("  - Use VLM if OCR text is short (<32 chars)")
        
    except Exception as e:
        print(f"✗ Error in Approach 2: {e}")
    
    # Approach 3 example (commented out as it requires existing docs)
    print("\n[Approach 3] Updating Existing Documents")
    print("-" * 60)
    print("To update an existing document to use VLM parsing:")
    print("  update_document_parser(doc_id='<DOC_ID>', pipeline_id='<PIPELINE_ID>')")
    print("  trigger_document_parsing(doc_id='<DOC_ID>')")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Check if API key is configured
    if API_KEY == "your-api-key-here":
        print("⚠️  Please set RAGFLOW_API_KEY environment variable")
        print("   Example: export RAGFLOW_API_KEY='your-actual-api-key'")
        print("\nYou can also set RAGFLOW_URL if not using default:")
        print("   Example: export RAGFLOW_URL='http://your-server:8086'")
        print("\nTo get your API key:")
        print("   1. Log in to RAGFlow")
        print("   2. Go to Settings > API Keys")
        print("   3. Create or copy an API key")
        exit(1)
    
    main()
