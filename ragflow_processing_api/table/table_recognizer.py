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
Table Structure Recognizer - Standalone API

This module provides table structure recognition capabilities extracted from RAGFlow's
deepdoc.vision.table_structure_recognizer module.
"""

import logging
import re
from collections import Counter
from typing import List, Dict, Any, Optional

import numpy as np


class TableStructureRecognizer:
    """
    Table Structure Recognizer
    
    This class provides methods for recognizing table structures in images,
    including detecting rows, columns, headers, and spanning cells.
    
    Example:
        >>> recognizer = TableStructureRecognizer()
        >>> # Assuming you have boxes from OCR or layout detection
        >>> html_table = recognizer.construct_table(boxes, html=True)
        >>> text_table = recognizer.construct_table(boxes, html=False)
    """
    
    labels = [
        "table",
        "table column",
        "table row",
        "table column header",
        "table projected row header",
        "table spanning cell",
    ]

    @staticmethod
    def is_caption(bx: Dict[str, Any]) -> bool:
        """
        Determine if a box is a table caption.
        
        Args:
            bx: Box dictionary with 'text' and optional 'layout_type' keys
            
        Returns:
            True if the box is identified as a caption, False otherwise
        """
        patt = [r"[图表]+[ 0-9:：]{2,}"]
        if any([re.match(p, bx["text"].strip()) for p in patt]) or bx.get("layout_type", "").find("caption") >= 0:
            return True
        return False

    @staticmethod
    def blockType(b: Dict[str, Any]) -> str:
        """
        Determine the type of a text block.
        
        Args:
            b: Block dictionary with 'text' key
            
        Returns:
            Block type code (Dt=Date, Nu=Number, Ca=Category, En=English, etc.)
        """
        patt = [
            ("^(20|19)[0-9]{2}[年/-][0-9]{1,2}[月/-][0-9]{1,2}日*$", "Dt"),
            (r"^(20|19)[0-9]{2}年$", "Dt"),
            (r"^(20|19)[0-9]{2}[年-][0-9]{1,2}月*$", "Dt"),
            ("^[0-9]{1,2}[月-][0-9]{1,2}日*$", "Dt"),
            (r"^第*[一二三四1-4]季度$", "Dt"),
            (r"^(20|19)[0-9]{2}年*[一二三四1-4]季度$", "Dt"),
            (r"^(20|19)[0-9]{2}[ABCDE]$", "Dt"),
            ("^[0-9.,+%/ -]+$", "Nu"),
            (r"^[0-9A-Z/\._~-]+$", "Ca"),
            (r"^[A-Z]*[a-z' -]+$", "En"),
            (r"^[0-9.,+-]+[0-9A-Za-z/$￥%<>（）()' -]+$", "NE"),
            (r"^.{1}$", "Sg"),
        ]
        for p, n in patt:
            if re.search(p, b["text"].strip()):
                return n
        
        # Simplified without RAG tokenizer dependency
        text = b["text"].strip()
        words = [w for w in text.split() if len(w) > 1]
        if len(words) > 3:
            if len(words) < 12:
                return "Tx"
            else:
                return "Lx"
        
        return "Ot"

    @staticmethod
    def construct_table(
        boxes: List[Dict[str, Any]], 
        is_english: bool = False, 
        html: bool = True,
        **kwargs
    ) -> Any:
        """
        Construct a table from detected boxes.
        
        Args:
            boxes: List of box dictionaries with text, position, and label information
            is_english: Whether the content is in English
            html: If True, return HTML format; if False, return descriptive text format
            **kwargs: Additional parameters
            
        Returns:
            HTML string if html=True, list of text strings if html=False
            
        Example:
            >>> boxes = [
            ...     {"text": "Header1", "x0": 0, "x1": 100, "top": 0, "bottom": 20, ...},
            ...     {"text": "Value1", "x0": 0, "x1": 100, "top": 20, "bottom": 40, ...},
            ... ]
            >>> html_table = TableStructureRecognizer.construct_table(boxes, html=True)
            >>> print(html_table)  # <table>...</table>
        """
        # Extract caption
        cap = ""
        i = 0
        while i < len(boxes):
            if TableStructureRecognizer.is_caption(boxes[i]):
                if is_english:
                    cap += " "
                cap += boxes[i]["text"]
                boxes.pop(i)
                i -= 1
            i += 1

        if not boxes:
            return []
        
        # Classify block types
        for b in boxes:
            b["btype"] = TableStructureRecognizer.blockType(b)
        
        max_type = Counter([b["btype"] for b in boxes]).items()
        max_type = max(max_type, key=lambda x: x[1])[0] if max_type else ""
        logging.debug("MAXTYPE: " + max_type)

        # Organize boxes into rows
        rowh = [b["R_bott"] - b["R_top"] for b in boxes if "R" in b]
        rowh = np.min(rowh) if rowh else 0
        boxes = TableStructureRecognizer._sort_R_firstly(boxes, rowh / 2)
        
        boxes[0]["rn"] = 0
        rows = [[boxes[0]]]
        btm = boxes[0]["bottom"]
        for b in boxes[1:]:
            b["rn"] = len(rows) - 1
            lst_r = rows[-1]
            if lst_r[-1].get("R", "") != b.get("R", "") or (
                b["top"] >= btm - 3 and lst_r[-1].get("R", "-1") != b.get("R", "-2")
            ):
                btm = b["bottom"]
                b["rn"] += 1
                rows.append([b])
                continue
            btm = (btm + b["bottom"]) / 2.0
            rows[-1].append(b)

        # Organize boxes into columns
        colwm = [b["C_right"] - b["C_left"] for b in boxes if "C" in b]
        colwm = np.min(colwm) if colwm else 0
        crosspage = len(set([b.get("page_number", 0) for b in boxes])) > 1
        if crosspage:
            boxes = TableStructureRecognizer._sort_X_firstly(boxes, colwm / 2)
        else:
            boxes = TableStructureRecognizer._sort_C_firstly(boxes, colwm / 2)
        
        boxes[0]["cn"] = 0
        cols = [[boxes[0]]]
        right = boxes[0]["x1"]
        for b in boxes[1:]:
            b["cn"] = len(cols) - 1
            lst_c = cols[-1]
            if (
                int(b.get("C", "1")) - int(lst_c[-1].get("C", "1")) == 1 
                and b.get("page_number", 0) == lst_c[-1].get("page_number", 0)
            ) or (b["x0"] >= right and lst_c[-1].get("C", "-1") != b.get("C", "-2")):
                right = b["x1"]
                b["cn"] += 1
                cols.append([b])
                continue
            right = (right + b["x1"]) / 2.0
            cols[-1].append(b)

        # Create table grid
        tbl = [[[] for _ in range(len(cols))] for _ in range(len(rows))]
        for b in boxes:
            tbl[b["rn"]][b["cn"]].append(b)

        # Identify header rows
        hdset = set([])
        for i in range(len(tbl)):
            cnt, h = 0, 0
            for j, arr in enumerate(tbl[i]):
                if not arr:
                    continue
                cnt += 1
                if max_type == "Nu" and arr[0]["btype"] == "Nu":
                    continue
                if any([a.get("H") for a in arr]) or (max_type == "Nu" and arr[0]["btype"] != "Nu"):
                    h += 1
            if cnt > 0 and h / cnt > 0.5:
                hdset.add(i)

        if html:
            return TableStructureRecognizer._html_table(
                cap, hdset, TableStructureRecognizer._cal_spans(boxes, rows, cols, tbl, True)
            )

        return TableStructureRecognizer._desc_table(
            cap, hdset, TableStructureRecognizer._cal_spans(boxes, rows, cols, tbl, False), is_english
        )

    @staticmethod
    def _sort_Y_firstly(boxes: List[Dict], y_tolerance: float = 0) -> List[Dict]:
        """Sort boxes by Y coordinate (top to bottom), then by X coordinate."""
        return sorted(boxes, key=lambda b: (b["top"] + y_tolerance, b["x0"]))

    @staticmethod
    def _sort_R_firstly(boxes: List[Dict], tolerance: float = 0) -> List[Dict]:
        """Sort boxes by row, then by X coordinate."""
        return sorted(boxes, key=lambda b: (b.get("R", b["top"] + tolerance), b["x0"]))

    @staticmethod
    def _sort_X_firstly(boxes: List[Dict], tolerance: float = 0) -> List[Dict]:
        """Sort boxes by X coordinate, then by Y coordinate."""
        return sorted(boxes, key=lambda b: (b["x0"] + tolerance, b["top"]))

    @staticmethod
    def _sort_C_firstly(boxes: List[Dict], tolerance: float = 0) -> List[Dict]:
        """Sort boxes by column, then by Y coordinate."""
        return sorted(boxes, key=lambda b: (b.get("C", b["x0"] + tolerance), b["top"]))

    @staticmethod
    def _html_table(cap: str, hdset: set, tbl: List[List]) -> str:
        """
        Construct HTML table from processed table data.
        
        Args:
            cap: Table caption
            hdset: Set of header row indices
            tbl: Table grid with processed cells
            
        Returns:
            HTML table string
        """
        html = "<table>"
        if cap:
            html += f"<caption>{cap}</caption>"
        
        for i in range(len(tbl)):
            row = "<tr>"
            txts = []
            for j, arr in enumerate(tbl[i]):
                if arr is None:
                    continue
                if not arr:
                    row += "<td></td>" if i not in hdset else "<th></th>"
                    continue
                
                txt = ""
                if arr:
                    h = min(np.min([c["bottom"] - c["top"] for c in arr]) / 2, 10)
                    txt = " ".join([c["text"] for c in TableStructureRecognizer._sort_Y_firstly(arr, h)])
                txts.append(txt)
                
                sp = ""
                if arr[0].get("colspan"):
                    sp = "colspan={}".format(arr[0]["colspan"])
                if arr[0].get("rowspan"):
                    sp += " rowspan={}".format(arr[0]["rowspan"])
                
                if i in hdset:
                    row += f"<th {sp} >" + txt + "</th>"
                else:
                    row += f"<td {sp} >" + txt + "</td>"

            if i in hdset:
                if all([t in hdset for t in txts]):
                    continue
                for t in txts:
                    hdset.add(t)

            if row != "<tr>":
                row += "</tr>"
            else:
                row = ""
            html += "\n" + row
        
        html += "\n</table>"
        return html

    @staticmethod
    def _desc_table(cap: str, hdr_rowno: set, tbl: List[List], is_english: bool) -> List[str]:
        """
        Construct descriptive text from processed table data.
        
        Args:
            cap: Table caption
            hdr_rowno: Set of header row numbers
            tbl: Table grid with processed cells
            is_english: Whether content is in English
            
        Returns:
            List of descriptive text strings
        """
        clmno = len(tbl[0])
        rowno = len(tbl)
        headers = {}
        lst_hdr = []
        de = "的" if not is_english else " for "
        
        # Build headers
        for r in sorted(list(hdr_rowno)):
            headers[r] = ["" for _ in range(clmno)]
            for i in range(clmno):
                if not tbl[r][i]:
                    continue
                txt = " ".join([a["text"].strip() for a in tbl[r][i]])
                headers[r][i] = txt
            
            if all([not t for t in headers[r]]):
                del headers[r]
                hdr_rowno.remove(r)
                continue
            
            for j in range(clmno):
                if headers[r][j]:
                    continue
                if j >= len(lst_hdr):
                    break
                headers[r][j] = lst_hdr[j]
            lst_hdr = headers[r]

        # Build row texts
        row_txt = []
        for i in range(rowno):
            if i in hdr_rowno:
                continue
            rtxt = []

            r = 0
            if len(headers.items()):
                _arr = [(i - r, r) for r, _ in headers.items() if r < i]
                if _arr:
                    _, r = min(_arr, key=lambda x: x[0])

            if r not in headers and clmno <= 2:
                for j in range(clmno):
                    if not tbl[i][j]:
                        continue
                    txt = "".join([a["text"].strip() for a in tbl[i][j]])
                    if txt:
                        rtxt.append(txt)
                if rtxt:
                    rtxt = "：".join(rtxt)
                    if row_txt and len(row_txt[-1]) + len(rtxt) < 64:
                        row_txt[-1] += "\n" + rtxt
                    else:
                        row_txt.append(rtxt)
                continue

            for j in range(clmno):
                if not tbl[i][j]:
                    continue
                txt = "".join([a["text"].strip() for a in tbl[i][j]])
                if not txt:
                    continue
                ctt = headers[r][j] if r in headers else ""
                if ctt:
                    ctt += "："
                ctt += txt
                if ctt:
                    rtxt.append(ctt)

            if rtxt:
                row_txt.append("; ".join(rtxt))

        if cap:
            if is_english:
                from_ = " in "
            else:
                from_ = "来自"
            row_txt = [t + f'\t——{from_}"{cap}"' for t in row_txt]
        
        return row_txt

    @staticmethod
    def _cal_spans(boxes: List[Dict], rows: List, cols: List, tbl: List[List], html: bool = True) -> List[List]:
        """
        Calculate rowspan and colspan for cells.
        
        Args:
            boxes: List of box dictionaries
            rows: List of rows
            cols: List of columns
            tbl: Table grid
            html: Whether generating for HTML
            
        Returns:
            Table grid with span information
        """
        clft = [np.mean([c.get("C_left", c["x0"]) for c in cln]) for cln in cols]
        crgt = [np.mean([c.get("C_right", c["x1"]) for c in cln]) for cln in cols]
        rtop = [np.mean([c.get("R_top", c["top"]) for c in row]) for row in rows]
        rbtm = [np.mean([c.get("R_btm", c["bottom"]) for c in row]) for row in rows]
        
        for b in boxes:
            if "SP" not in b:
                continue
            b["colspan"] = [b["cn"]]
            b["rowspan"] = [b["rn"]]
            
            # Calculate column span
            for j in range(0, len(clft)):
                if j == b["cn"]:
                    continue
                if clft[j] + (crgt[j] - clft[j]) / 2 < b.get("H_left", b["x0"]):
                    continue
                if crgt[j] - (crgt[j] - clft[j]) / 2 > b.get("H_right", b["x1"]):
                    continue
                b["colspan"].append(j)
            
            # Calculate row span
            for j in range(0, len(rtop)):
                if j == b["rn"]:
                    continue
                if rtop[j] + (rbtm[j] - rtop[j]) / 2 < b.get("H_top", b["top"]):
                    continue
                if rbtm[j] - (rbtm[j] - rtop[j]) / 2 > b.get("H_bott", b["bottom"]):
                    continue
                b["rowspan"].append(j)

        def join(arr):
            if not arr:
                return ""
            return "".join([t["text"] for t in arr])

        # Remove spanning cells
        for i in range(len(tbl)):
            for j, arr in enumerate(tbl[i]):
                if not arr:
                    continue
                if all(["rowspan" not in a and "colspan" not in a for a in arr]):
                    continue
                
                rowspan, colspan = [], []
                for a in arr:
                    if isinstance(a.get("rowspan", 0), list):
                        rowspan.extend(a["rowspan"])
                    if isinstance(a.get("colspan", 0), list):
                        colspan.extend(a["colspan"])
                
                rowspan, colspan = set(rowspan), set(colspan)
                if len(rowspan) < 2 and len(colspan) < 2:
                    for a in arr:
                        if "rowspan" in a:
                            del a["rowspan"]
                        if "colspan" in a:
                            del a["colspan"]
                    continue
                
                rowspan, colspan = sorted(rowspan), sorted(colspan)
                rowspan = list(range(rowspan[0], rowspan[-1] + 1))
                colspan = list(range(colspan[0], colspan[-1] + 1))
                
                assert i in rowspan, rowspan
                assert j in colspan, colspan
                
                arr = []
                for r in rowspan:
                    for c in colspan:
                        arr_txt = join(arr)
                        if tbl[r][c] and join(tbl[r][c]) != arr_txt:
                            arr.extend(tbl[r][c])
                        tbl[r][c] = None if html else arr
                
                for a in arr:
                    if len(rowspan) > 1:
                        a["rowspan"] = len(rowspan)
                    elif "rowspan" in a:
                        del a["rowspan"]
                    if len(colspan) > 1:
                        a["colspan"] = len(colspan)
                    elif "colspan" in a:
                        del a["colspan"]
                
                tbl[rowspan[0]][colspan[0]] = arr

        return tbl
