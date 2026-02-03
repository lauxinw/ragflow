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
OCR Processor - Standalone API

This module provides OCR (Optical Character Recognition) capabilities extracted from RAGFlow's
deepdoc.vision.ocr module.

Note: This is a simplified wrapper. For full functionality, you need to integrate with
RAGFlow's OCR models (detection and recognition models).
"""

import io
import logging
from typing import List, Tuple, Dict, Any, Optional, Union

import numpy as np
from PIL import Image


class OCRProcessor:
    """
    OCR Processor
    
    This class provides OCR functionality for extracting text from images.
    
    Features:
    - Text detection (locating text regions in images)
    - Text recognition (converting text regions to text)
    - Batch processing
    - Confidence scoring
    
    Example:
        >>> ocr = OCRProcessor()
        >>> image = Image.open("document.jpg")
        >>> results = ocr.process_image(image)
        >>> for bbox, (text, confidence) in results:
        ...     print(f"Text: {text}, Confidence: {confidence}")
    
    Note:
        This is a simplified interface. For production use, integrate with
        RAGFlow's pre-trained OCR models or other OCR engines like PaddleOCR,
        Tesseract, or cloud OCR APIs.
    """

    def __init__(self, model_dir: Optional[str] = None, device_id: Optional[int] = None):
        """
        Initialize OCR Processor.
        
        Args:
            model_dir: Path to OCR model directory (optional)
            device_id: GPU device ID (optional, uses CPU if None)
        """
        self.model_dir = model_dir
        self.device_id = device_id
        self.drop_score = 0.5  # Minimum confidence threshold
        
        logging.info("OCRProcessor initialized")
        logging.warning(
            "This is a simplified OCR interface. For full functionality, "
            "integrate with RAGFlow's OCR models or other OCR engines."
        )

    def detect_text(self, image: Union[np.ndarray, Image.Image]) -> List[np.ndarray]:
        """
        Detect text regions in an image.
        
        Args:
            image: Input image as numpy array or PIL Image
            
        Returns:
            List of bounding boxes (each box is a 4x2 numpy array with corner coordinates)
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # This is a placeholder. In production, this would call the actual detection model
        logging.warning("Text detection is not implemented. Please integrate with an OCR engine.")
        return []

    def recognize_text(
        self, 
        image: Union[np.ndarray, Image.Image], 
        boxes: List[np.ndarray]
    ) -> List[Tuple[str, float]]:
        """
        Recognize text from detected regions.
        
        Args:
            image: Input image as numpy array or PIL Image
            boxes: List of bounding boxes from text detection
            
        Returns:
            List of (text, confidence) tuples
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # This is a placeholder. In production, this would call the actual recognition model
        logging.warning("Text recognition is not implemented. Please integrate with an OCR engine.")
        return [("", 0.0) for _ in boxes]

    def process_image(
        self, 
        image: Union[np.ndarray, Image.Image, str, bytes],
        return_boxes: bool = True
    ) -> Union[List[Tuple[np.ndarray, Tuple[str, float]]], str]:
        """
        Process an image and extract text.
        
        Args:
            image: Input image (numpy array, PIL Image, file path, or binary data)
            return_boxes: If True, return boxes with text; if False, return only text
            
        Returns:
            If return_boxes=True: List of (bbox, (text, confidence)) tuples
            If return_boxes=False: Concatenated text string
            
        Example:
            >>> ocr = OCRProcessor()
            >>> # With boxes
            >>> results = ocr.process_image("document.jpg", return_boxes=True)
            >>> # Without boxes (text only)
            >>> text = ocr.process_image("document.jpg", return_boxes=False)
        """
        # Load image if needed
        if isinstance(image, str):
            # File path
            image = Image.open(image)
        elif isinstance(image, bytes):
            # Binary data
            image = Image.open(io.BytesIO(image))
        
        # Convert to RGB if needed
        if isinstance(image, Image.Image):
            if image.mode != 'RGB':
                image = image.convert('RGB')
        
        # Detect text regions
        boxes = self.detect_text(image)
        
        if not boxes:
            if return_boxes:
                return []
            return ""
        
        # Recognize text
        results = self.recognize_text(image, boxes)
        
        # Filter by confidence
        filtered_results = [
            (box, (text, score)) 
            for box, (text, score) in zip(boxes, results)
            if score >= self.drop_score
        ]
        
        if return_boxes:
            return filtered_results
        else:
            # Return text only
            return "\n".join([text for _, (text, _) in filtered_results])

    def process_batch(
        self,
        images: List[Union[np.ndarray, Image.Image, str, bytes]],
        return_boxes: bool = True
    ) -> List:
        """
        Process multiple images in batch.
        
        Args:
            images: List of images
            return_boxes: If True, return boxes with text; if False, return only text
            
        Returns:
            List of results, one for each image
        """
        results = []
        for image in images:
            result = self.process_image(image, return_boxes=return_boxes)
            results.append(result)
        return results

    def process_image_region(
        self,
        image: Union[np.ndarray, Image.Image],
        region: Tuple[int, int, int, int]
    ) -> str:
        """
        Process a specific region of an image.
        
        Args:
            image: Input image
            region: Region as (x0, y0, x1, y1) tuple
            
        Returns:
            Extracted text from the region
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        x0, y0, x1, y1 = region
        cropped = image[y0:y1, x0:x1]
        
        return self.process_image(cropped, return_boxes=False)


class OCRResult:
    """
    Container for OCR results with helper methods.
    """
    
    def __init__(self, results: List[Tuple[np.ndarray, Tuple[str, float]]]):
        """
        Initialize OCR result.
        
        Args:
            results: List of (bbox, (text, confidence)) tuples
        """
        self.results = results
    
    def get_text(self, separator: str = "\n") -> str:
        """
        Get all text concatenated.
        
        Args:
            separator: String to join text lines
            
        Returns:
            Concatenated text
        """
        return separator.join([text for _, (text, _) in self.results])
    
    def get_boxes(self) -> List[np.ndarray]:
        """Get all bounding boxes."""
        return [box for box, _ in self.results]
    
    def get_confidences(self) -> List[float]:
        """Get all confidence scores."""
        return [score for _, (_, score) in self.results]
    
    def filter_by_confidence(self, threshold: float) -> 'OCRResult':
        """
        Filter results by confidence threshold.
        
        Args:
            threshold: Minimum confidence score
            
        Returns:
            New OCRResult with filtered results
        """
        filtered = [
            (box, (text, score))
            for box, (text, score) in self.results
            if score >= threshold
        ]
        return OCRResult(filtered)
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """
        Convert results to list of dictionaries.
        
        Returns:
            List of dicts with 'bbox', 'text', and 'confidence' keys
        """
        return [
            {
                'bbox': box.tolist(),
                'text': text,
                'confidence': score
            }
            for box, (text, score) in self.results
        ]
