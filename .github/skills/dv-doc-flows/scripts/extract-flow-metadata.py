#!/usr/bin/env python3
"""
Extract metadata from Power Automate cloud flow JSON files.

This script parses a Power Automate flow JSON file and generates a metadata.json
file containing source file reference, flow statistics, complexity rating, and
other metadata to help AI with evaluation.

Usage:
    python extract-flow-metadata.py <flow-json-path> [output-dir]

Arguments:
    flow-json-path: Path to the flow JSON file
    output-dir: Optional output directory for metadata.json (defaults to wiki/Technical-Reference/cloud-flows/<FlowName>/)

Example:
    python extract-flow-metadata.py **/IncomeAssistancePowerAutomate/Workflows/AutomatedEmailAudit-*.json
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


# Connector ID to display name mapping
CONNECTOR_MAPPINGS = {
    "shared_commondataserviceforapps": "Microsoft Dataverse",
    "shared_commondataservice": "Microsoft Dataverse",
    "shared_office365": "Office 365 Outlook",
    "shared_sharepointonline": "SharePoint",
    "shared_teams": "Microsoft Teams",
    "shared_approvals": "Approvals",
    "shared_onedriveforbusiness": "OneDrive for Business",
    "shared_word": "Word Online",
    "shared_excel": "Excel Online",
    "shared_powerbi": "Power BI",
    "shared_sql": "SQL Server",
    "shared_azureblob": "Azure Blob Storage",
    "shared_azurequeues": "Azure Queue Storage",
    "shared_azuretables": "Azure Table Storage",
    "shared_servicebus": "Azure Service Bus",
    "shared_keyvault": "Azure Key Vault",
    "shared_sendgrid": "SendGrid",
    "shared_twilio": "Twilio",
    "shared_twitter": "Twitter",
    "shared_facebook": "Facebook",
    "shared_slack": "Slack",
    "shared_outlook": "Outlook.com",
    "shared_gmail": "Gmail",
    "shared_googledrive": "Google Drive",
    "shared_dropbox": "Dropbox",
    "shared_box": "Box",
}


def extract_flow_name(file_path: str) -> str:
    """Extract flow name from filename by removing GUID suffix."""
    filename = Path(file_path).stem  # Get filename without extension
    
    # Remove GUID pattern (8-4-4-4-12 hexadecimal)
    # Pattern: FlowName-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    parts = filename.split('-')
    
    # If we have a GUID pattern at the end (5 parts after last meaningful hyphen)
    if len(parts) >= 5:
        # Check if last 5 parts look like a GUID
        guid_parts = parts[-5:]
        if (len(guid_parts[0]) == 8 and len(guid_parts[1]) == 4 and 
            len(guid_parts[2]) == 4 and len(guid_parts[3]) == 4 and 
            len(guid_parts[4]) == 12):
            # Remove the GUID parts
            return '-'.join(parts[:-5])
    
    return filename


def count_actions_recursive(actions: Dict[str, Any], depth: int = 1) -> tuple[int, int, int, int]:
    """
    Recursively count actions, conditions, loops, and calculate max nesting depth.
    
    Returns: (total_actions, conditions, loops, max_depth)
    """
    if not actions:
        return 0, 0, 0, depth - 1
    
    total_actions = len(actions)
    conditions = 0
    loops = 0
    max_depth = depth
    
    for action_name, action in actions.items():
        action_type = action.get('type', '')
        
        # Count conditions
        if action_type in ['If', 'Switch']:
            conditions += 1
            
            # Recurse into condition branches
            if action_type == 'If':
                if 'actions' in action:
                    sub_actions, sub_cond, sub_loops, sub_depth = count_actions_recursive(
                        action['actions'], depth + 1
                    )
                    total_actions += sub_actions
                    conditions += sub_cond
                    loops += sub_loops
                    max_depth = max(max_depth, sub_depth)
                
                if 'else' in action and 'actions' in action['else']:
                    sub_actions, sub_cond, sub_loops, sub_depth = count_actions_recursive(
                        action['else']['actions'], depth + 1
                    )
                    total_actions += sub_actions
                    conditions += sub_cond
                    loops += sub_loops
                    max_depth = max(max_depth, sub_depth)
            
            elif action_type == 'Switch':
                if 'cases' in action:
                    for case_name, case in action['cases'].items():
                        if 'actions' in case:
                            sub_actions, sub_cond, sub_loops, sub_depth = count_actions_recursive(
                                case['actions'], depth + 1
                            )
                            total_actions += sub_actions
                            conditions += sub_cond
                            loops += sub_loops
                            max_depth = max(max_depth, sub_depth)
                
                if 'default' in action and 'actions' in action['default']:
                    sub_actions, sub_cond, sub_loops, sub_depth = count_actions_recursive(
                        action['default']['actions'], depth + 1
                    )
                    total_actions += sub_actions
                    conditions += sub_cond
                    loops += sub_loops
                    max_depth = max(max_depth, sub_depth)
        
        # Count loops
        elif action_type in ['Foreach', 'Until']:
            loops += 1
            
            # Recurse into loop actions
            if 'actions' in action:
                sub_actions, sub_cond, sub_loops, sub_depth = count_actions_recursive(
                    action['actions'], depth + 1
                )
                total_actions += sub_actions
                conditions += sub_cond
                loops += sub_loops
                max_depth = max(max_depth, sub_depth)
    
    return total_actions, conditions, loops, max_depth


def analyze_trigger(triggers: Dict[str, Any]) -> Dict[str, str]:
    """Extract trigger information."""
    if not triggers:
        return {"type": "Unknown", "details": "No trigger found"}
    
    # Get the first trigger (flows typically have one trigger)
    trigger_name, trigger = next(iter(triggers.items()))
    trigger_type = trigger.get('type', 'Unknown')
    
    # Generate human-readable details based on trigger type
    details = "Unknown trigger configuration"
    
    if trigger_type == 'Recurrence':
        recurrence = trigger.get('recurrence', {})
        frequency = recurrence.get('frequency', '')
        interval = recurrence.get('interval', 1)
        
        if frequency == 'Minute':
            details = f"Runs every {interval} minute{'s' if interval > 1 else ''}"
        elif frequency == 'Hour':
            details = f"Runs every {interval} hour{'s' if interval > 1 else ''}"
        elif frequency == 'Day':
            details = f"Runs daily" if interval == 1 else f"Runs every {interval} days"
        elif frequency == 'Week':
            details = f"Runs weekly" if interval == 1 else f"Runs every {interval} weeks"
        elif frequency == 'Month':
            details = f"Runs monthly" if interval == 1 else f"Runs every {interval} months"
        else:
            details = f"Runs on schedule: {frequency}"
    
    elif trigger_type == 'ApiConnection':
        operation_id = trigger.get('inputs', {}).get('host', {}).get('operationId', '')
        
        if 'GetOnNewItems' in operation_id or 'GetOnUpdatedItems' in operation_id:
            details = "When a record is created or updated in Dataverse"
        elif 'GetOnNewOrModifiedItems' in operation_id:
            details = "When an item is created or modified"
        else:
            details = f"API Connection trigger: {operation_id or 'Unknown operation'}"
    
    elif trigger_type == 'Request':
        details = "HTTP request trigger (manual or webhook)"
    
    elif trigger_type == 'manual':
        details = "Manually triggered by user"
    
    return {
        "type": trigger_type,
        "details": details
    }


def calculate_complexity(total_actions: int, nesting_depth: int, 
                        total_loops: int, total_conditions: int,
                        connection_count: int) -> Dict[str, Any]:
    """Calculate complexity rating and contributing factors."""
    factors = []
    
    # Determine rating
    if total_actions > 30 or nesting_depth > 4:
        rating = "Very Complex"
    elif total_actions > 15 or nesting_depth == 4:
        rating = "Complex"
    elif total_actions > 5 or nesting_depth == 3:
        rating = "Medium"
    else:
        rating = "Simple"
    
    # Identify complexity factors
    if nesting_depth > 4:
        factors.append(f"Very deep nesting ({nesting_depth} levels)")
    elif nesting_depth == 4:
        factors.append(f"Deep nesting (4 levels)")
    elif nesting_depth == 3:
        factors.append("Moderate nesting (3 levels)")
    
    if total_actions > 30:
        factors.append(f"High action count ({total_actions} actions)")
    elif total_actions > 15:
        factors.append(f"Many actions ({total_actions} actions)")
    
    if total_loops > 2:
        factors.append("Multiple nested loops" if nesting_depth > 2 else f"Multiple loops ({total_loops})")
    elif total_loops > 0:
        factors.append("Contains loops")
    
    if total_conditions > 3:
        factors.append(f"Complex conditions ({total_conditions} conditional branches)")
    elif total_conditions > 1:
        factors.append("Multiple conditions")
    
    if connection_count > 3:
        factors.append(f"Multiple connection dependencies ({connection_count} connectors)")
    elif connection_count > 1:
        factors.append("Multiple connectors")
    
    if not factors:
        factors.append("Simple linear flow")
    
    return {
        "rating": rating,
        "factors": factors
    }


def extract_connectors(connection_references: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract connector information from connection references."""
    connectors = []
    
    for conn_id, conn_info in connection_references.items():
        # Try to get display name from connector mapping
        display_name = CONNECTOR_MAPPINGS.get(conn_id)
        
        # If not in mapping, try to extract from connection info
        if not display_name:
            # Try to get from connection reference
            if isinstance(conn_info, dict):
                api_id = conn_info.get('api', {}).get('name', '') if isinstance(conn_info.get('api'), dict) else ''
                display_name = CONNECTOR_MAPPINGS.get(api_id)
                
                # Last resort: use connection ID with formatting
                if not display_name:
                    display_name = conn_id.replace('shared_', '').replace('_', ' ').title()
        
        connectors.append({
            "id": conn_id,
            "displayName": display_name
        })
    
    return connectors


def extract_metadata(flow_json_path: str) -> Dict[str, Any]:
    """Extract metadata from a flow JSON file."""
    
    # Read and parse JSON
    with open(flow_json_path, 'r', encoding='utf-8') as f:
        flow_data = json.load(f)
    
    # Get file info
    file_stat = os.stat(flow_json_path)
    file_size = file_stat.st_size
    file_modified = datetime.fromtimestamp(file_stat.st_mtime).isoformat() + 'Z'
    
    # Extract flow name from filename
    flow_name = extract_flow_name(flow_json_path)
    
    # Get display name from JSON
    properties = flow_data.get('properties', {})
    display_name = properties.get('displayName', flow_name)
    
    # Get definition
    definition = properties.get('definition', {})
    triggers = definition.get('triggers', {})
    actions = definition.get('actions', {})
    
    # Analyze trigger
    trigger_info = analyze_trigger(triggers)
    
    # Count actions and calculate complexity
    total_actions, total_conditions, total_loops, nesting_depth = count_actions_recursive(actions)
    
    # Get connection references
    connection_references = properties.get('connectionReferences', {})
    connection_ref_list = list(connection_references.keys())
    
    # Extract connectors
    connectors = extract_connectors(connection_references)
    
    # Calculate complexity
    complexity = calculate_complexity(
        total_actions, nesting_depth, total_loops, 
        total_conditions, len(connection_references)
    )
    
    # Build metadata
    metadata = {
        "flowName": flow_name,
        "sourceFile": flow_json_path,
        "displayName": display_name,
        "analysisDate": datetime.now().astimezone().replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        "trigger": trigger_info,
        "statistics": {
            "totalActions": total_actions,
            "totalConditions": total_conditions,
            "totalLoops": total_loops,
            "nestingDepth": nesting_depth,
            "connectionReferences": connection_ref_list
        },
        "complexity": complexity,
        "connectors": connectors,
        "fileInfo": {
            "sizeBytes": file_size,
            "lastModified": file_modified
        }
    }
    
    return metadata


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ['--help', '-h', 'help']:
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    flow_json_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(flow_json_path):
        print(f"Error: File not found: {flow_json_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Extract metadata
        print(f"Extracting metadata from: {flow_json_path}")
        metadata = extract_metadata(flow_json_path)
        
        # Determine output directory
        if len(sys.argv) >= 3:
            output_dir = sys.argv[2]
        else:
            # Default: wiki/Technical-Reference/cloud-flows/<FlowName>/
            flow_name = metadata['flowName']
            output_dir = f"wiki/Technical-Reference/cloud-flows/{flow_name}"
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Write metadata.json
        output_path = os.path.join(output_dir, 'metadata.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Metadata extracted successfully")
        print(f"  Output: {output_path}")
        print(f"  Flow: {metadata['displayName']}")
        print(f"  Complexity: {metadata['complexity']['rating']}")
        print(f"  Actions: {metadata['statistics']['totalActions']}")
        print(f"  Connectors: {len(metadata['connectors'])}")
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
