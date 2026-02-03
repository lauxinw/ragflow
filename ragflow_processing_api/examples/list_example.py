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
List Processing Example

This script demonstrates how to use the RAGFlow List Processing API.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragflow_processing_api import ListProcessor


def example_ordered_list():
    """Example: Extract and format ordered list."""
    print("=" * 60)
    print("Example 1: Ordered List Processing")
    print("=" * 60)
    
    processor = ListProcessor()
    
    text = """
    Here are the steps:
    1. First, prepare the data
    2. Then, clean the data
    3. Next, analyze the data
    4. Finally, visualize the results
    """
    
    print("Input text:")
    print(text)
    
    # Extract lists
    lists = processor.extract(text)
    print(f"\nExtracted {len(lists)} list(s):")
    for i, lst in enumerate(lists):
        print(f"\nList {i+1}:")
        print(f"  Type: {lst['type']}")
        print(f"  Items: {lst['items']}")
    
    # Format as HTML
    if lists:
        html = processor.format(lists[0], format='html')
        print("\nHTML format:")
        print(html)
        
        # Format as Markdown
        markdown = processor.format(lists[0], format='markdown')
        print("\nMarkdown format:")
        print(markdown)
    
    print("\n" + "=" * 60)


def example_unordered_list():
    """Example: Extract and format unordered list."""
    print("=" * 60)
    print("Example 2: Unordered List Processing")
    print("=" * 60)
    
    processor = ListProcessor()
    
    text = """
    Features include:
    - Easy to use
    - Fast processing
    - High accuracy
    - Multiple formats supported
    """
    
    print("Input text:")
    print(text)
    
    # Extract lists
    lists = processor.extract(text)
    print(f"\nExtracted {len(lists)} list(s):")
    for i, lst in enumerate(lists):
        print(f"\nList {i+1}:")
        print(f"  Type: {lst['type']}")
        print(f"  Items: {lst['items']}")
    
    # Format as HTML
    if lists:
        html = processor.format(lists[0], format='html')
        print("\nHTML format:")
        print(html)
    
    print("\n" + "=" * 60)


def example_nested_list():
    """Example: Extract nested lists."""
    print("=" * 60)
    print("Example 3: Nested List Processing")
    print("=" * 60)
    
    processor = ListProcessor()
    
    text = """
    Main topics:
    1. Introduction
       - Background
       - Motivation
    2. Methods
       - Data collection
       - Analysis
    3. Results
    """
    
    print("Input text:")
    print(text)
    
    # Extract nested lists
    nested_lists = processor.extractor.extract_nested_lists(text)
    print(f"\nExtracted nested structure:")
    
    def print_nested(items, indent=0):
        for item in items:
            prefix = "  " * indent
            print(f"{prefix}- {item.get('content', 'Root')}")
            if item.get('children'):
                print_nested(item['children'], indent + 1)
    
    print_nested(nested_lists)
    
    # Format nested list as Markdown
    if nested_lists:
        print("\nMarkdown format:")
        for item in nested_lists:
            markdown = processor.formatter.format_nested_markdown(item)
            print(markdown)
    
    print("\n" + "=" * 60)


def example_list_statistics():
    """Example: Get list statistics."""
    print("=" * 60)
    print("Example 4: List Statistics")
    print("=" * 60)
    
    processor = ListProcessor()
    
    text = """
    Ordered list:
    1. Item one
    2. Item two
    3. Item three
    
    Unordered list:
    - Point A
    - Point B
    - Point C
    - Point D
    """
    
    print("Input text:")
    print(text)
    
    # Get statistics
    stats = processor.extractor.count_lists(text)
    print("\nList statistics:")
    print(f"  Total lists: {stats['total']}")
    print(f"  Ordered lists: {stats['ordered']}")
    print(f"  Unordered lists: {stats['unordered']}")
    print(f"  Total items: {stats['total_items']}")
    
    # Check if text contains lists
    has_lists = processor.extractor.is_list_content(text)
    print(f"\nContains lists: {has_lists}")
    
    print("\n" + "=" * 60)


def main():
    """Run all examples."""
    print("\nRAGFlow List Processing API - Examples\n")
    
    try:
        example_ordered_list()
        print("\n")
        example_unordered_list()
        print("\n")
        example_nested_list()
        print("\n")
        example_list_statistics()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nExamples completed!")


if __name__ == "__main__":
    main()
