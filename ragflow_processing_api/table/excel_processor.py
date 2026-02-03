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
Excel Table Processor - Standalone API

This module provides Excel table processing capabilities extracted from RAGFlow.
"""

import logging
from io import BytesIO
from typing import List, Dict, Any, Optional, Union, Callable

import pandas as pd
from openpyxl import load_workbook


class ExcelTableProcessor:
    """
    Excel Table Processor
    
    This class provides methods for processing Excel files, including:
    - Reading Excel sheets
    - Extracting table headers
    - Parsing table data
    - Handling merged cells
    
    Example:
        >>> processor = ExcelTableProcessor()
        >>> tables = processor.process_file("data.xlsx")
        >>> for table in tables:
        ...     print(table["sheet_name"])
        ...     print(table["dataframe"].head())
    """

    @staticmethod
    def load_excel(file_path_or_binary: Union[str, BytesIO]):
        """
        Load Excel workbook from file path or binary data.
        
        Args:
            file_path_or_binary: File path string or BytesIO object
            
        Returns:
            openpyxl Workbook object
        """
        return load_workbook(file_path_or_binary, data_only=True)

    @staticmethod
    def parse_headers(worksheet, rows: List, max_header_rows: int = 3) -> tuple:
        """
        Parse table headers from worksheet rows.
        
        Args:
            worksheet: openpyxl worksheet object
            rows: List of row tuples
            max_header_rows: Maximum number of rows to check for headers
            
        Returns:
            Tuple of (headers list, number of header rows)
        """
        headers = []
        header_rows = 0
        
        # Try to identify header rows
        for row_idx in range(min(max_header_rows, len(rows))):
            row = rows[row_idx]
            row_values = [cell.value for cell in row]
            
            # Check if row contains header-like content
            non_empty = [v for v in row_values if v is not None and str(v).strip()]
            if len(non_empty) > 0:
                if not headers:
                    headers = [str(v) if v is not None else f"Column{i}" for i, v in enumerate(row_values)]
                    header_rows = row_idx + 1
                    break
        
        if not headers:
            # Default headers if none found
            if rows:
                headers = [f"Column{i}" for i in range(len(rows[0]))]
            header_rows = 0
        
        return headers, header_rows

    @staticmethod
    def extract_row_data(worksheet, row, row_idx: int, num_columns: int) -> Optional[List]:
        """
        Extract data from a single row.
        
        Args:
            worksheet: openpyxl worksheet object
            row: Row tuple
            row_idx: Row index (0-based)
            num_columns: Expected number of columns
            
        Returns:
            List of cell values or None if row is invalid
        """
        try:
            row_data = []
            for i, cell in enumerate(row[:num_columns]):
                value = cell.value
                if value is None:
                    row_data.append("")
                else:
                    row_data.append(str(value))
            return row_data
        except Exception as e:
            logging.warning(f"Error extracting row {row_idx}: {e}")
            return None

    @staticmethod
    def is_empty_row(row_data: List) -> bool:
        """
        Check if a row is empty.
        
        Args:
            row_data: List of cell values
            
        Returns:
            True if row is empty, False otherwise
        """
        return all(not str(v).strip() for v in row_data)

    def process_file(
        self,
        file_path_or_binary: Union[str, BytesIO],
        from_page: int = 0,
        to_page: int = 10000000000,
        callback: Optional[Callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Process an Excel file and extract all tables.
        
        Args:
            file_path_or_binary: File path string or BytesIO object
            from_page: Start processing from this row (0-based)
            to_page: Stop processing at this row (exclusive)
            callback: Optional callback function for progress updates
            
        Returns:
            List of dictionaries containing sheet information and DataFrames
            
        Example:
            >>> processor = ExcelTableProcessor()
            >>> results = processor.process_file("data.xlsx")
            >>> for result in results:
            ...     print(f"Sheet: {result['sheet_name']}")
            ...     print(result['dataframe'])
        """
        wb = self.load_excel(file_path_or_binary)
        results = []
        
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            
            try:
                rows = list(ws.rows)
            except Exception as e:
                logging.warning(f"Skip sheet '{sheet_name}' due to rows access error: {e}")
                continue
            
            if not rows:
                continue
            
            # Parse headers
            headers, header_rows = self.parse_headers(ws, rows)
            if not headers:
                continue
            
            # Extract data
            data = []
            for i, r in enumerate(rows[header_rows:]):
                row_num = header_rows + i
                if row_num < from_page:
                    continue
                if row_num >= to_page:
                    break
                
                row_data = self.extract_row_data(ws, r, row_num, len(headers))
                if row_data is None:
                    continue
                if self.is_empty_row(row_data):
                    continue
                
                data.append(row_data)
            
            if len(data) == 0:
                continue
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=headers)
            
            results.append({
                "sheet_name": sheet_name,
                "dataframe": df,
                "headers": headers,
                "header_rows": header_rows,
                "num_rows": len(data)
            })
            
            if callback:
                callback(f"Processed sheet: {sheet_name} with {len(data)} rows")
        
        return results

    def process_file_to_dict(
        self,
        file_path_or_binary: Union[str, BytesIO],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Process an Excel file and return results as list of dictionaries.
        
        Args:
            file_path_or_binary: File path string or BytesIO object
            **kwargs: Additional arguments passed to process_file
            
        Returns:
            List of dictionaries where each dict represents a row
        """
        results = self.process_file(file_path_or_binary, **kwargs)
        
        output = []
        for result in results:
            df = result["dataframe"]
            sheet_name = result["sheet_name"]
            
            for idx, row in df.iterrows():
                row_dict = row.to_dict()
                row_dict["_sheet_name"] = sheet_name
                row_dict["_row_index"] = idx
                output.append(row_dict)
        
        return output
