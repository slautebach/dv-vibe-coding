"""
North52 Formula Parser and Analyzer

Analyzes North52 Decision Suite formula code to extract:
- Functions used and their call counts
- Variables defined and used
- Decision tables
- FetchXML references
- Complexity indicators
- Formula metadata

Usage:
    from analyze_formula import North52FormulaParser
    
    parser = North52FormulaParser(formula_code_string)
    result = parser.parse()
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from north52_functions import NORTH52_FUNCTIONS


class North52FormulaParser:
    """Parser for analyzing North52 formula code."""
    
    def __init__(self, formula_code: str, formula_name: str = "Unknown"):
        """
        Initialize the parser with formula code.
        
        Args:
            formula_code: The North52 formula code to analyze
            formula_name: Name of the formula (for context)
        """
        self.formula_content = formula_code  # Keep original name for compatibility
        self.formula_code = formula_code
        self.formula_name = formula_name
        self.metadata = {}
        self.functions = {}
        self.variables = set()
        self.decision_tables = []
        self.fetchxml_refs = set()
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the formula and extract all analysis information.
        
        Returns:
            Dict containing:
                - metadata: Spreadsheet metadata from JSON comments
                - functions: Dict with function name as key and count as value
                - variables: List of variable names
                - decision_tables: List of decision table data
                - fetchxml_refs: List of FetchXML reference names
        """
        # Extract metadata from embedded JSON
        self._extract_metadata()
        
        # Extract functions first (needed for other analysis)
        self._extract_functions()
        
        # Extract variables
        self._extract_variables()
        
        # Parse decision tables
        self._extract_decision_tables()
        
        # Extract FetchXML references
        self._extract_fetchxml_refs()
        
        # Return functions as simple dict (name: count)
        return {
            'metadata': self.metadata,
            'functions': self.functions,  # Simple dict with name: count
            'variables': sorted(list(self.variables)),
            'decision_tables': self.decision_tables,
            'fetchxml_refs': sorted(list(self.fetchxml_refs))
        }
    
    def _extract_metadata(self):
        """Extract spreadsheet metadata from JSON comment."""
        # Find JSON metadata block (usually at end of file in /* */ comment)
        json_match = re.search(r'/\*({.*})\*/', self.formula_content, re.DOTALL)
        if json_match:
            try:
                metadata = json.loads(json_match.group(1))
                self.metadata = {
                    'version': metadata.get('version', 'Unknown'),
                    'sheet_count': metadata.get('sheetCount', 0),
                    'sheets': {}
                }
                
                # Extract sheet information
                if 'sheets' in metadata:
                    for sheet_name, sheet_data in metadata['sheets'].items():
                        self.metadata['sheets'][sheet_name] = {
                            'name': sheet_data.get('name', sheet_name),
                            'tag': sheet_data.get('tag', ''),
                            'visible': sheet_data.get('visible', True),
                            'rows': sheet_data.get('rowCount', 0),
                            'columns': sheet_data.get('columnCount', 0)
                        }
            except json.JSONDecodeError:
                self.metadata = {'error': 'Failed to parse metadata JSON'}
    
    def _extract_functions(self):
        """Extract all North52 functions and count their usage."""
        # Get all known North52 function names
        known_functions = list(NORTH52_FUNCTIONS.keys())
        
        # Sort by length (longest first) to avoid matching partial names
        known_functions.sort(key=len, reverse=True)
        
        # Count each function's usage
        for func_name in known_functions:
            # Use word boundary to match complete function names
            # Look for function calls: FunctionName(...) 
            pattern = rf'\b{re.escape(func_name)}\s*\('
            matches = re.findall(pattern, self.formula_code, re.IGNORECASE)
            
            if matches:
                # Store with exact case from NORTH52_FUNCTIONS
                self.functions[func_name] = len(matches)
    
    def _extract_variables(self):
        """Extract all variable names from SetVar and other variable operations."""
        # Pattern for SetVar function: SetVar('varname', value)
        setvar_pattern = r"[Ss]etVar\s*\(\s*['\"]([^'\"]+)['\"]"
        setvar_matches = re.findall(setvar_pattern, self.formula_content)
        for var in setvar_matches:
            self.variables.add(var)
        
        # Pattern for GetVar function: GetVar('varname')
        getvar_pattern = r"[Gg]etVar\s*\(\s*['\"]([^'\"]+)['\"]"
        getvar_matches = re.findall(getvar_pattern, self.formula_content)
        for var in getvar_matches:
            self.variables.add(var)
        
        # Pattern for variable references in decision tables: [varname]
        bracket_pattern = r'\[([a-zA-Z_][a-zA-Z0-9_]*)\]'
        bracket_matches = re.findall(bracket_pattern, self.formula_content)
        for var in bracket_matches:
            self.variables.add(var)
    
    def _extract_decision_tables(self):
        """Extract decision table information from the formula."""
        # Pattern 1: Explicit DecisionTable function calls
        # DecisionTable(..., 'tag')
        table_pattern = r'DecisionTable\s*\((.*?),\s*[\'"]([^\'"\s]+)[\'"][\)\s]*(?:\s*,|\))'
        
        tables = re.finditer(table_pattern, self.formula_content, re.DOTALL)
        
        for idx, table_match in enumerate(tables):
            table_content = table_match.group(1)
            table_tag = table_match.group(2)
            
            # Parse tag (format: 'true|false|update|TableName')
            tag_parts = table_tag.split('|')
            table_name = tag_parts[-1] if len(tag_parts) > 0 else f"Table{idx+1}"
            
            # Extract operations within the table
            operations = self._extract_operations(table_content)
            
            self.decision_tables.append({
                'name': table_name,
                'tag': table_tag,
                'type': 'explicit',
                'operations': operations,
                'content_preview': table_content[:200] + '...' if len(table_content) > 200 else table_content
            })
        
        # Pattern 2: If-Then-Else chains (implicit decision tables)
        # Count nested If statements as potential decision table logic
        if_count = len(self.functions.get('If', 0)) if 'If' in self.functions else 0
        if if_count == 0:
            # Fallback: search manually
            if_pattern = r'\bIf\s*\('
            if_count = len(re.findall(if_pattern, self.formula_content, re.IGNORECASE))
        
        # If there are multiple If statements and no explicit tables, consider it decision logic
        if if_count >= 3 and not self.decision_tables:
            self.decision_tables.append({
                'name': 'Implicit If-Then-Else Logic',
                'tag': '',
                'type': 'implicit',
                'if_count': if_count,
                'operations': []
            })
    
    def _extract_operations(self, content: str) -> List[str]:
        """Extract high-level operations from decision table content."""
        operations = []
        
        # Look for SetVar, IfTrue, SmartFlow, etc.
        operation_patterns = [
            (r'SetVar\s*\([\'"]([^\'\"]+)[\'"]', 'SetVar'),
            (r'IfTrue\s*\(', 'IfTrue'),
            (r'SmartFlow\s*\(', 'SmartFlow'),
            (r'ForEachRecord\s*\(', 'ForEachRecord'),
            (r'UpdateRecord\s*\(', 'UpdateRecord'),
            (r'SetClientSideField\s*\(', 'SetClientSideField'),
            (r'FormSave\s*\(', 'FormSave'),
            (r'MultipleClientSide\s*\(', 'MultipleClientSide')
        ]
        
        for pattern, op_name in operation_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                if op_name == 'SetVar':
                    operations.append(f"SetVar('{match.group(1)}')")
                else:
                    operations.append(op_name)
        
        return operations
    
    def _extract_fetchxml_refs(self):
        """Extract FetchXML query references from FindRecordsFD/FindValueFD calls."""
        # Pattern for FindRecordsFD and FindValueFD functions
        fd_pattern = r'Find(?:Records|Value)FD\s*\(\s*[\'"]([^\'"]+)[\'"]'
        fd_matches = re.findall(fd_pattern, self.formula_content, re.IGNORECASE)
        for ref in fd_matches:
            self.fetchxml_refs.add(ref)
        
        # Pattern for ExecuteFetchXML function
        fetch_pattern = r'ExecuteFetchXML\s*\('
        if re.search(fetch_pattern, self.formula_content, re.IGNORECASE):
            self.fetchxml_refs.add('Inline FetchXML')
        
        # Pattern for FindRecords function (may use inline or referenced queries)
        findrecords_pattern = r'FindRecords\s*\('
        findrecords_matches = re.findall(findrecords_pattern, self.formula_content, re.IGNORECASE)
        if findrecords_matches:
            # Add generic marker for FindRecords usage
            for i in range(len(findrecords_matches)):
                ref_name = f'FindRecords_{i+1}'
                if ref_name not in self.fetchxml_refs:
                    self.fetchxml_refs.add(ref_name)
    
    def generate_summary(self) -> str:
        """Generate a human-readable summary of the formula."""
        lines = []
        lines.append("=" * 80)
        lines.append("NORTH52 FORMULA ANALYSIS")
        lines.append("=" * 80)
        lines.append(f"Formula: {self.formula_name}")
        lines.append("")
        
        # Metadata
        if self.metadata:
            lines.append("METADATA:")
            lines.append(f"  Version: {self.metadata.get('version', 'Unknown')}")
            lines.append(f"  Sheets: {self.metadata.get('sheet_count', 0)}")
            for sheet_name, sheet_info in self.metadata.get('sheets', {}).items():
                visible = "Visible" if sheet_info.get('visible', True) else "Hidden"
                lines.append(f"    - {sheet_name} ({visible}): {sheet_info.get('rows', 0)}x{sheet_info.get('columns', 0)}")
                if sheet_info.get('tag'):
                    lines.append(f"      Tag: {sheet_info['tag']}")
            lines.append("")
        
        # Decision Tables
        lines.append(f"DECISION TABLES: {len(self.decision_tables)}")
        for idx, table in enumerate(self.decision_tables, 1):
            lines.append(f"  {idx}. {table['name']}")
            if table.get('tag'):
                lines.append(f"     Tag: {table['tag']}")
            if table.get('operations'):
                lines.append(f"     Operations: {len(table['operations'])}")
                for op in table['operations'][:5]:  # Show first 5
                    lines.append(f"       - {op}")
                if len(table['operations']) > 5:
                    lines.append(f"       ... and {len(table['operations']) - 5} more")
        lines.append("")
        
        # Variables
        lines.append(f"VARIABLES: {len(self.variables)}")
        if self.variables:
            for var in sorted(self.variables):
                lines.append(f"  - {var}")
        lines.append("")
        
        # Functions
        function_list = [
            {'name': name, 'count': count}
            for name, count in sorted(self.functions.items(), key=lambda x: x[1], reverse=True)
        ]
        lines.append(f"FUNCTIONS USED: {len(function_list)}")
        for func in function_list[:15]:  # Top 15
            lines.append(f"  - {func['name']}: {func['count']} occurrences")
        if len(function_list) > 15:
            lines.append(f"  ... and {len(function_list) - 15} more")
        lines.append("")
        
        # FetchXML References
        lines.append(f"FETCHXML QUERIES: {len(self.fetchxml_refs)}")
        for fetch_ref in sorted(self.fetchxml_refs):
            lines.append(f"  - {fetch_ref}")
        lines.append("")
        
        lines.append("=" * 80)
        
        return "\n".join(lines)


def analyze_formula(formula_code: str, formula_name: str = "Unknown") -> Dict[str, Any]:
    """
    Convenience function to analyze a formula without creating a parser object.
    
    Args:
        formula_code: The North52 formula code to analyze
        formula_name: Name of the formula (for context)
        
    Returns:
        Dict containing analysis results
    """
    parser = North52FormulaParser(formula_code, formula_name)
    return parser.parse()


def main():
    """Command-line interface for formula parser."""
    if len(sys.argv) < 2:
        print("Usage: python analyze_formula.py <formula-folder-path>")
        print("\nExample:")
        print("  python analyze_formula.py c:/path/to/wiki/Technical-Reference/North52/invoice/2WE")
        print("\nThis will analyze the .n52 file and display the results.")
        print("Full analysis is saved in analysis_metadata.json by fetch_north52_from_dataverse.py")
        sys.exit(1)
    
    folder_path = Path(sys.argv[1])
    
    if not folder_path.exists():
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    print("\nAnalyzing North52 formula file...")
    
    # Read .n52 file
    n52_files = list(folder_path.glob('*.n52'))
    if not n52_files:
        print("Error: No .n52 file found in folder")
        print("Use fetch_north52_from_dataverse.py to retrieve formulas from Dataverse")
        sys.exit(1)
    
    formula_file = n52_files[0]
    formula_code = formula_file.read_text(encoding='utf-8')
    formula_name = formula_file.stem
    
    # Analyze formula
    parser = North52FormulaParser(formula_code, formula_name)
    analysis = parser.parse()
    
    # Print summary
    print(parser.generate_summary())


if __name__ == '__main__':
    main()
