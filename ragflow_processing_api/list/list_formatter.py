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
List Formatter - Standalone API

This module provides list formatting capabilities.
"""

from typing import List, Dict, Any, Optional


class ListFormatter:
    """
    List Formatter
    
    This class provides methods for formatting lists in various output formats.
    
    Example:
        >>> formatter = ListFormatter()
        >>> items = ['First', 'Second', 'Third']
        >>> html = formatter.format_as_html(items, ordered=True)
        >>> markdown = formatter.format_as_markdown(items, ordered=True)
    """

    def format_as_html(
        self,
        items: List[str],
        ordered: bool = False,
        nested: bool = False
    ) -> str:
        """
        Format list items as HTML.
        
        Args:
            items: List of item strings
            ordered: If True, create ordered list (<ol>); otherwise unordered (<ul>)
            nested: If True, items may contain nested lists
            
        Returns:
            HTML string
            
        Example:
            >>> formatter = ListFormatter()
            >>> html = formatter.format_as_html(['Item 1', 'Item 2'], ordered=True)
            >>> print(html)
            <ol>
            <li>Item 1</li>
            <li>Item 2</li>
            </ol>
        """
        tag = 'ol' if ordered else 'ul'
        html = f'<{tag}>\n'
        
        for item in items:
            html += f'<li>{item}</li>\n'
        
        html += f'</{tag}>'
        return html

    def format_as_markdown(
        self,
        items: List[str],
        ordered: bool = False,
        start_number: int = 1
    ) -> str:
        """
        Format list items as Markdown.
        
        Args:
            items: List of item strings
            ordered: If True, create numbered list; otherwise bullet list
            start_number: Starting number for ordered lists
            
        Returns:
            Markdown string
            
        Example:
            >>> formatter = ListFormatter()
            >>> md = formatter.format_as_markdown(['Item 1', 'Item 2'], ordered=True)
            >>> print(md)
            1. Item 1
            2. Item 2
        """
        lines = []
        for i, item in enumerate(items):
            if ordered:
                lines.append(f'{start_number + i}. {item}')
            else:
                lines.append(f'- {item}')
        
        return '\n'.join(lines)

    def format_as_text(
        self,
        items: List[str],
        indent: str = '  ',
        bullet: str = '•'
    ) -> str:
        """
        Format list items as plain text.
        
        Args:
            items: List of item strings
            indent: Indentation string
            bullet: Bullet character for unordered lists
            
        Returns:
            Plain text string
        """
        lines = []
        for item in items:
            lines.append(f'{indent}{bullet} {item}')
        
        return '\n'.join(lines)

    def format_nested_html(self, nested_list: Dict[str, Any]) -> str:
        """
        Format nested list structure as HTML.
        
        Args:
            nested_list: Dictionary with 'type', 'content', and 'children' keys
            
        Returns:
            HTML string
        """
        list_type = nested_list.get('type', 'unordered')
        tag = 'ol' if list_type == 'ordered' else 'ul'
        
        html = f'<{tag}>\n'
        
        if 'content' in nested_list:
            html += f'<li>{nested_list["content"]}'
            if nested_list.get('children'):
                html += '\n'
                for child in nested_list['children']:
                    html += self.format_nested_html(child)
            html += '</li>\n'
        elif 'children' in nested_list:
            for child in nested_list['children']:
                html += self.format_nested_html(child)
        
        html += f'</{tag}>'
        return html

    def format_nested_markdown(
        self,
        nested_list: Dict[str, Any],
        level: int = 0,
        indent: str = '  '
    ) -> str:
        """
        Format nested list structure as Markdown.
        
        Args:
            nested_list: Dictionary with 'type', 'content', and 'children' keys
            level: Current nesting level
            indent: Indentation string per level
            
        Returns:
            Markdown string
        """
        lines = []
        list_type = nested_list.get('type', 'unordered')
        prefix = indent * level
        
        if 'content' in nested_list:
            marker = nested_list.get('marker', '1') if list_type == 'ordered' else '-'
            if list_type == 'ordered':
                marker = f'{marker}.'
            lines.append(f'{prefix}{marker} {nested_list["content"]}')
            
            if nested_list.get('children'):
                for child in nested_list['children']:
                    child_text = self.format_nested_markdown(child, level + 1, indent)
                    lines.append(child_text)
        
        elif 'children' in nested_list:
            for child in nested_list['children']:
                child_text = self.format_nested_markdown(child, level, indent)
                lines.append(child_text)
        
        return '\n'.join(lines)

    def format_from_dict(self, list_dict: Dict[str, Any], format: str = 'html') -> str:
        """
        Format a list dictionary in the specified format.
        
        Args:
            list_dict: Dictionary with 'type' and 'items' keys
            format: Output format ('html', 'markdown', or 'text')
            
        Returns:
            Formatted string
        """
        list_type = list_dict.get('type', 'unordered')
        items = list_dict.get('items', [])
        ordered = list_type == 'ordered'
        
        if format == 'html':
            return self.format_as_html(items, ordered=ordered)
        elif format == 'markdown':
            return self.format_as_markdown(items, ordered=ordered)
        elif format == 'text':
            return self.format_as_text(items)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def convert_to_json(self, list_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert list structure to JSON-serializable format.
        
        Args:
            list_dict: List dictionary
            
        Returns:
            JSON-serializable dictionary
        """
        return {
            'type': list_dict.get('type', 'unordered'),
            'items': list_dict.get('items', []),
            'count': len(list_dict.get('items', [])),
            'markers': list_dict.get('markers', [])
        }
