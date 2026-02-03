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
List Extractor - Standalone API

This module provides list extraction capabilities from various document formats.
"""

import re
from typing import List, Dict, Any, Optional, Tuple


class ListExtractor:
    """
    List Extractor
    
    This class provides methods for detecting and extracting lists from text and documents.
    
    Features:
    - Detect ordered lists (numbered, lettered)
    - Detect unordered lists (bullets)
    - Extract nested lists
    - Preserve list structure and hierarchy
    
    Example:
        >>> extractor = ListExtractor()
        >>> text = '''
        ... 1. First item
        ... 2. Second item
        ...    - Sub item A
        ...    - Sub item B
        ... 3. Third item
        ... '''
        >>> lists = extractor.extract_lists(text)
        >>> for lst in lists:
        ...     print(lst['type'], lst['items'])
    """

    # Common list patterns
    ORDERED_PATTERNS = [
        r'^\s*(\d+)[\.\)]\s+(.+)$',  # 1. or 1)
        r'^\s*([a-zA-Z])[\.\)]\s+(.+)$',  # a. or a)
        r'^\s*([ivxIVX]+)[\.\)]\s+(.+)$',  # i. or I.
    ]
    
    UNORDERED_PATTERNS = [
        r'^\s*[-•*+]\s+(.+)$',  # -, •, *, +
        r'^\s*[◦◘○●]\s+(.+)$',  # circle bullets
    ]

    def __init__(self):
        """Initialize List Extractor."""
        self.ordered_regex = [re.compile(p, re.MULTILINE) for p in self.ORDERED_PATTERNS]
        self.unordered_regex = [re.compile(p, re.MULTILINE) for p in self.UNORDERED_PATTERNS]

    def extract_lists(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract all lists from text.
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries containing list information
            
        Example:
            >>> extractor = ListExtractor()
            >>> text = "1. First\\n2. Second\\n3. Third"
            >>> lists = extractor.extract_lists(text)
            >>> print(lists[0]['items'])
            ['First', 'Second', 'Third']
        """
        lines = text.split('\n')
        lists = []
        current_list = None
        
        for line in lines:
            # Check for ordered list
            is_ordered, marker, content = self._check_ordered(line)
            if is_ordered:
                if current_list is None or current_list['type'] != 'ordered':
                    if current_list:
                        lists.append(current_list)
                    current_list = {
                        'type': 'ordered',
                        'items': [],
                        'markers': [],
                        'indentation': self._get_indentation(line)
                    }
                current_list['items'].append(content)
                current_list['markers'].append(marker)
                continue
            
            # Check for unordered list
            is_unordered, content = self._check_unordered(line)
            if is_unordered:
                if current_list is None or current_list['type'] != 'unordered':
                    if current_list:
                        lists.append(current_list)
                    current_list = {
                        'type': 'unordered',
                        'items': [],
                        'indentation': self._get_indentation(line)
                    }
                current_list['items'].append(content)
                continue
            
            # Not a list item - close current list if exists
            if current_list and line.strip():
                lists.append(current_list)
                current_list = None
        
        # Don't forget the last list
        if current_list:
            lists.append(current_list)
        
        return lists

    def _check_ordered(self, line: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if line is an ordered list item.
        
        Returns:
            Tuple of (is_ordered, marker, content)
        """
        for regex in self.ordered_regex:
            match = regex.match(line)
            if match:
                if len(match.groups()) == 2:
                    marker, content = match.groups()
                    return True, marker, content.strip()
        return False, None, None

    def _check_unordered(self, line: str) -> Tuple[bool, Optional[str]]:
        """
        Check if line is an unordered list item.
        
        Returns:
            Tuple of (is_unordered, content)
        """
        for regex in self.unordered_regex:
            match = regex.match(line)
            if match:
                content = match.group(1)
                return True, content.strip()
        return False, None

    def _get_indentation(self, line: str) -> int:
        """Get indentation level of a line."""
        return len(line) - len(line.lstrip())

    def extract_nested_lists(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract nested lists with hierarchy information.
        
        Args:
            text: Input text
            
        Returns:
            List of dictionaries with nested structure
        """
        lines = text.split('\n')
        root = {'children': [], 'level': -1}
        stack = [root]
        
        for line in lines:
            if not line.strip():
                continue
            
            indent = self._get_indentation(line)
            
            # Check if it's a list item
            is_ordered, marker, o_content = self._check_ordered(line)
            is_unordered, u_content = self._check_unordered(line)
            
            if is_ordered or is_unordered:
                item = {
                    'type': 'ordered' if is_ordered else 'unordered',
                    'content': o_content if is_ordered else u_content,
                    'marker': marker if is_ordered else None,
                    'level': indent,
                    'children': []
                }
                
                # Find parent based on indentation
                while len(stack) > 1 and stack[-1]['level'] >= indent:
                    stack.pop()
                
                stack[-1]['children'].append(item)
                stack.append(item)
        
        return root['children']

    def count_lists(self, text: str) -> Dict[str, int]:
        """
        Count lists in text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with counts of different list types
        """
        lists = self.extract_lists(text)
        
        return {
            'total': len(lists),
            'ordered': sum(1 for lst in lists if lst['type'] == 'ordered'),
            'unordered': sum(1 for lst in lists if lst['type'] == 'unordered'),
            'total_items': sum(len(lst['items']) for lst in lists)
        }

    def extract_list_items_only(self, text: str) -> List[str]:
        """
        Extract just the list items as a flat list.
        
        Args:
            text: Input text
            
        Returns:
            List of item contents
        """
        lists = self.extract_lists(text)
        items = []
        for lst in lists:
            items.extend(lst['items'])
        return items

    def is_list_content(self, text: str) -> bool:
        """
        Check if text contains list content.
        
        Args:
            text: Input text
            
        Returns:
            True if text contains lists, False otherwise
        """
        lists = self.extract_lists(text)
        return len(lists) > 0


class MarkdownListExtractor(ListExtractor):
    """
    Specialized extractor for Markdown-formatted lists.
    """
    
    def __init__(self):
        """Initialize Markdown List Extractor."""
        super().__init__()
        # Add markdown-specific patterns
        self.markdown_ordered = re.compile(r'^\s*(\d+)\.\s+(.+)$', re.MULTILINE)
        self.markdown_unordered = re.compile(r'^\s*[-*+]\s+(.+)$', re.MULTILINE)

    def extract_markdown_lists(self, markdown_text: str) -> List[Dict[str, Any]]:
        """
        Extract lists specifically from Markdown text.
        
        Args:
            markdown_text: Markdown formatted text
            
        Returns:
            List of dictionaries containing list information
        """
        return self.extract_lists(markdown_text)
