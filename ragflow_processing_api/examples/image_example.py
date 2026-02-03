#!/usr/bin/env python3
#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""
Image Processing Example

This script demonstrates how to use the RAGFlow Image Processing API.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragflow_processing_api import ImageProcessor
import numpy as np
from PIL import Image


def example_ocr_processing():
    """Example: OCR processing."""
    print("=" * 60)
    print("Example 1: OCR Processing")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Create a sample image with text
    print("\nCreating sample image...")
    img = Image.new('RGB', (400, 100), color='white')
    
    # Note: In real usage, you would load an actual image
    # img = Image.open("document.jpg")
    
    print("Processing image with OCR...")
    result = processor.ocr(img, return_boxes=False)
    print(f"Extracted text: {result}")
    
    print("\nNote: This is a placeholder. For actual OCR functionality,")
    print("integrate with RAGFlow's OCR models or use PaddleOCR/Tesseract.")
    
    print("\n" + "=" * 60)


def example_image_description():
    """Example: Image description."""
    print("=" * 60)
    print("Example 2: Image Description")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Create a sample image
    print("\nCreating sample image...")
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # Describe the image
    print("Generating image description...")
    description = processor.describe(img)
    print(f"Description: {description}")
    
    # Describe with context
    print("\nGenerating description with context...")
    description = processor.describe(
        img,
        context={
            "above": "Sales data for Q4",
            "below": "Total revenue increased by 25%"
        }
    )
    print(f"Description with context: {description}")
    
    print("\nNote: This is a placeholder. For actual image description,")
    print("integrate with vision-language models like CLIP, BLIP, or LLaVA.")
    
    print("\n" + "=" * 60)


def example_batch_processing():
    """Example: Batch image processing."""
    print("=" * 60)
    print("Example 3: Batch Image Processing")
    print("=" * 60)
    
    processor = ImageProcessor()
    
    # Create sample images
    print("\nCreating sample images...")
    images = [
        Image.new('RGB', (200, 200), color='red'),
        Image.new('RGB', (200, 200), color='green'),
        Image.new('RGB', (200, 200), color='blue'),
    ]
    
    # Process batch
    print(f"Processing {len(images)} images...")
    results = processor.ocr_processor.process_batch(images, return_boxes=False)
    
    for i, result in enumerate(results):
        print(f"Image {i+1}: {result}")
    
    print("\n" + "=" * 60)


def main():
    """Run all examples."""
    print("\nRAGFlow Image Processing API - Examples\n")
    
    try:
        example_ocr_processing()
        print("\n")
        example_image_description()
        print("\n")
        example_batch_processing()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nExamples completed!")


if __name__ == "__main__":
    main()
