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
Table Processing Example

This script demonstrates how to use the RAGFlow Table Processing API.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ragflow_processing_api import TableProcessor


def example_excel_processing():
    """Example: Process an Excel file."""
    print("=" * 60)
    print("Example 1: Excel File Processing")
    print("=" * 60)
    
    processor = TableProcessor()
    
    # Note: Replace with actual Excel file path
    excel_file = "sample_data.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"Sample file '{excel_file}' not found. Creating sample data...")
        # Create a sample Excel file
        import pandas as pd
        df = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Paris']
        })
        df.to_excel(excel_file, index=False)
        print(f"Created sample file: {excel_file}")
    
    # Process the Excel file
    print(f"\nProcessing: {excel_file}")
    tables = processor.process_excel(excel_file)
    
    for table in tables:
        print(f"\nSheet: {table['sheet_name']}")
        print(f"Headers: {table['headers']}")
        print(f"Number of rows: {table['num_rows']}")
        print("\nData preview:")
        print(table['dataframe'].head())
    
    print("\n" + "=" * 60)


def example_table_construction():
    """Example: Construct table from boxes."""
    print("=" * 60)
    print("Example 2: Table Construction from Boxes")
    print("=" * 60)
    
    processor = TableProcessor()
    
    # Simulate OCR boxes (in real usage, these would come from OCR/layout detection)
    boxes = [
        # Header row
        {"text": "Name", "x0": 0, "x1": 100, "top": 0, "bottom": 20, "rn": 0, "cn": 0, "R": "0", "C": "0", "H": True},
        {"text": "Age", "x0": 100, "x1": 200, "top": 0, "bottom": 20, "rn": 0, "cn": 1, "R": "0", "C": "1", "H": True},
        {"text": "City", "x0": 200, "x1": 300, "top": 0, "bottom": 20, "rn": 0, "cn": 2, "R": "0", "C": "2", "H": True},
        # Data rows
        {"text": "Alice", "x0": 0, "x1": 100, "top": 20, "bottom": 40, "rn": 1, "cn": 0, "R": "1", "C": "0"},
        {"text": "25", "x0": 100, "x1": 200, "top": 20, "bottom": 40, "rn": 1, "cn": 1, "R": "1", "C": "1"},
        {"text": "New York", "x0": 200, "x1": 300, "top": 20, "bottom": 40, "rn": 1, "cn": 2, "R": "1", "C": "2"},
    ]
    
    # Construct HTML table
    print("\nConstructing HTML table from boxes...")
    html_table = processor.construct_table(boxes, html=True)
    print("\nHTML Output:")
    print(html_table)
    
    # Construct descriptive text table
    print("\nConstructing descriptive text table from boxes...")
    text_table = processor.construct_table(boxes, html=False)
    print("\nText Output:")
    for row in text_table:
        print(row)
    
    print("\n" + "=" * 60)


def main():
    """Run all examples."""
    print("\nRAGFlow Table Processing API - Examples\n")
    
    try:
        example_excel_processing()
        print("\n")
        example_table_construction()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nExamples completed!")


if __name__ == "__main__":
    main()
