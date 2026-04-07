"""
Shared metadata building functions for North52 formula analysis.

This module provides a single source of truth for building the v2.0 metadata schema
used by fetch_north52_from_dataverse.py and other analysis scripts.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union


METADATA_VERSION = "2.0"


def build_metadata_v2(
    formula_name: str,
    entity: str,
    shortcode: str,
    formula_type: str,
    event: str,
    category: str,
    mode: str,
    stage: str,
    variables: List[str],
    functions: Union[List[Dict[str, Any]], Dict[str, int]],
    queries: List[Dict[str, str]],
    complexity_indicators: Dict[str, Any],
    formula_path: Path,
    n52f_filename: str,
    workspace_root: Path,
    source_entity: Optional[str] = None,
    decision_tables: Optional[Union[List[Any], int]] = None,
    last_formula_modified: Optional[str] = None,
    yml_file: str = "",
    formula_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Build v2.0 metadata schema for North52 formula analysis.
    
    Args:
        formula_name: Name of the formula
        entity: Entity name (e.g., 'contact', 'account')
        shortcode: Formula shortcode (e.g., '0rC')
        formula_type: Type of formula (e.g., 'Calculation', 'Process Genie')
        event: Trigger event (e.g., 'Create', 'Update')
        category: Formula category
        mode: Execution mode (e.g., 'Server Side')
        stage: Pipeline stage (e.g., 'Pre Operation')
        variables: List of variable names used in formula
        functions: Either a list of dicts with 'name' and 'count' keys, or a dict mapping names to counts
        queries: List of FetchXML query dicts with 'name' key
        complexity_indicators: Dict with has_loops, max_nesting_level, uses_client_side, uses_server_side
        formula_path: Path to the formula folder
        n52f_filename: Name of the .n52f file
        workspace_root: Root of the workspace
        source_entity: Override source entity (defaults to entity parameter)
        decision_tables: List of decision table data, count, or None (optional)
        last_formula_modified: ISO timestamp of last modification (defaults to now)
        yml_file: Name of yml file (optional, defaults to empty string)
    
    Returns:
        Complete metadata dictionary conforming to v2.0 schema
    """
    # Calculate relative path if possible
    try:
        relative_formula_path = str(formula_path.relative_to(workspace_root))
    except (ValueError, AttributeError):
        relative_formula_path = str(formula_path)
    
    # Handle functions in both formats (list of dicts or dict)
    if isinstance(functions, list):
        # Convert list of dicts [{'name': 'If', 'count': 5}, ...] to dict {'If': 5, ...}
        functions_dict = {func['name']: func['count'] for func in functions}
        function_count = len(functions)
        total_function_calls = sum(func['count'] for func in functions)
    else:
        # Already a dict {'If': 5, 'SetVar': 3, ...}
        functions_dict = functions
        function_count = len(functions)
        total_function_calls = sum(functions.values())
    
    # Calculate variable stats
    variable_count = len(variables)
    
    # Handle decision tables
    if decision_tables is None:
        decision_tables_count = 0
    elif isinstance(decision_tables, list):
        decision_tables_count = len(decision_tables)
    else:
        decision_tables_count = decision_tables  # Already a count
    
    # Use current timestamp if not provided
    if last_formula_modified is None:
        last_formula_modified = datetime.now().isoformat()
    
    # Build complete metadata structure
    metadata = {
        "metadata_version": METADATA_VERSION,
        "generated": datetime.now().isoformat(),
        "source_files": {
            "formula_path": relative_formula_path,
            "n52f_file": n52f_filename,
            "yml_file": yml_file,
            "fetch_xml_files": [q['name'] for q in queries]
        },
        "formula": {
            "name": formula_name,
            "source_entity": source_entity if source_entity else entity,
            "shortcode": shortcode,
            "formula_type": formula_type,
            "event": event,
            "category": category,
            "mode": mode,
            "stage": stage,
            "formula_id": formula_id
        },
        "analysis": {
            "decision_tables": decision_tables_count,
            "variables": variables,
            "variable_count": variable_count,
            "functions": functions_dict,
            "function_count": function_count,
            "total_function_calls": total_function_calls,
            "fetch_count": len(queries),
            "fetch_files": [q['name'] for q in queries],
            "complexity_indicators": complexity_indicators
        },
        "ai_documentation": {
            "description_generated": None,
            "codereview_generated": None,
            "last_formula_modified": last_formula_modified
        }
    }
    
    return metadata


def get_name_or_value(field: Any, default: str = 'Unknown') -> str:
    """
    Extract name from field that may be a dict with 'Name' key or a simple value.
    
    Many North52 metadata fields can be either:
    - A dict like {'Name': 'Create', 'Value': 'create'}
    - A simple string like 'Create'
    
    Args:
        field: Field value (dict or string)
        default: Default value if field is None or empty
    
    Returns:
        Extracted name or default value
    """
    if isinstance(field, dict):
        return field.get('Name', default)
    return field if field else default


def extract_metadata_fields(metadata_dict: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract common metadata fields from parsed North52 metadata.
    
    Handles both dict-based fields (with 'Name' key) and simple string fields.
    
    Args:
        metadata_dict: Parsed metadata from Dataverse or analysis scripts
    
    Returns:
        Dict with extracted fields: formula_type, event, mode, stage, category, 
        source_entity, name, shortcode
    """
    return {
        'formula_type': get_name_or_value(metadata_dict.get('Formula Type'), 'Unknown'),
        'event': get_name_or_value(metadata_dict.get('Event'), 'Unknown'),
        'mode': get_name_or_value(metadata_dict.get('Mode'), ''),
        'stage': get_name_or_value(metadata_dict.get('Stage'), ''),
        'category': metadata_dict.get('Category', ''),
        'source_entity': metadata_dict.get('Source Entity Name', ''),
        'name': metadata_dict.get('Name', 'Unknown'),
        'shortcode': metadata_dict.get('ShortCode', '')
    }
