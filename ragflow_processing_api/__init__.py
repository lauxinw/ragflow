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
RAGFlow Processing API

A standalone API extracted from RAGFlow for processing tables, images, and lists.

This package provides independent Python APIs for:
- Table processing (structure recognition, Excel parsing)
- Image processing (OCR, image analysis)
- List processing (extraction, formatting)

Example:
    >>> from ragflow_processing_api import TableProcessor, ImageProcessor, ListProcessor
    >>> 
    >>> # Process tables
    >>> table_processor = TableProcessor()
    >>> tables = table_processor.process_excel("data.xlsx")
    >>> 
    >>> # Process images
    >>> image_processor = ImageProcessor()
    >>> text = image_processor.ocr("document.jpg")
    >>> 
    >>> # Process lists
    >>> list_processor = ListProcessor()
    >>> lists = list_processor.extract_lists(text)
"""

from .table import TableStructureRecognizer, ExcelTableProcessor
from .image import OCRProcessor, ImageAnalyzer
from .list import ListExtractor, ListFormatter

__version__ = "1.0.0"

__all__ = [
    # Table processing
    'TableStructureRecognizer',
    'ExcelTableProcessor',
    'TableProcessor',
    
    # Image processing
    'OCRProcessor',
    'ImageAnalyzer',
    'ImageProcessor',
    
    # List processing
    'ListExtractor',
    'ListFormatter',
    'ListProcessor',
]


class TableProcessor:
    """
    Unified interface for table processing.
    
    Example:
        >>> processor = TableProcessor()
        >>> # Process Excel file
        >>> tables = processor.process_excel("data.xlsx")
        >>> # Construct table from boxes
        >>> html_table = processor.construct_table(boxes, html=True)
    """
    
    def __init__(self):
        """Initialize Table Processor."""
        self.recognizer = TableStructureRecognizer()
        self.excel_processor = ExcelTableProcessor()
    
    def process_excel(self, file_path, **kwargs):
        """Process an Excel file and extract tables."""
        return self.excel_processor.process_file(file_path, **kwargs)
    
    def construct_table(self, boxes, **kwargs):
        """Construct a table from detected boxes."""
        return self.recognizer.construct_table(boxes, **kwargs)


class ImageProcessor:
    """
    Unified interface for image processing.
    
    Example:
        >>> processor = ImageProcessor()
        >>> # Perform OCR
        >>> text = processor.ocr("document.jpg")
        >>> # Describe image
        >>> description = processor.describe("chart.png")
    """
    
    def __init__(self, model_dir=None):
        """Initialize Image Processor."""
        self.ocr_processor = OCRProcessor(model_dir=model_dir)
        self.analyzer = ImageAnalyzer()
    
    def ocr(self, image, return_boxes=False):
        """Perform OCR on an image."""
        return self.ocr_processor.process_image(image, return_boxes=return_boxes)
    
    def describe(self, image, **kwargs):
        """Generate a description of an image."""
        return self.analyzer.describe_image(image, **kwargs)


class ListProcessor:
    """
    Unified interface for list processing.
    
    Example:
        >>> processor = ListProcessor()
        >>> # Extract lists from text
        >>> lists = processor.extract(text)
        >>> # Format lists
        >>> html = processor.format(lists, format='html')
    """
    
    def __init__(self):
        """Initialize List Processor."""
        self.extractor = ListExtractor()
        self.formatter = ListFormatter()
    
    def extract(self, text):
        """Extract lists from text."""
        return self.extractor.extract_lists(text)
    
    def format(self, list_dict, format='html'):
        """Format a list in the specified format."""
        return self.formatter.format_from_dict(list_dict, format=format)
