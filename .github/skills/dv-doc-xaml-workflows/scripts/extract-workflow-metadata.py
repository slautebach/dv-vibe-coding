#!/usr/bin/env python3
"""
Extract metadata from Dynamics 365 classic XAML workflow files.

Parses the paired .xaml and .xaml.data.xml files and generates a metadata.json
file containing workflow properties, trigger info, step statistics, and complexity.

Usage:
    python extract-workflow-metadata.py <xaml-path> [output-dir]

Arguments:
    xaml-path:  Path to the .xaml workflow file
    output-dir: Optional output directory (defaults to wiki/Technical-Reference/classic-workflows/<WorkflowName>/)

Example:
    python extract-workflow-metadata.py <Solutions>/<SolutionName>/Workflows/SIS-CloseCase-E9581E0B.xaml
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET


# Category codes
CATEGORY_NAMES = {
    "0": "Workflow",
    "1": "Dialog",
    "2": "Business Rule",
    "3": "Action",
    "4": "Business Process Flow",
    "6": "Flow",
    "9": "Modern Flow",
}

# Mode codes
MODE_NAMES = {
    "0": "Background (Asynchronous)",
    "1": "Real-time (Synchronous)",
}

# Scope codes
SCOPE_NAMES = {
    "1": "User",
    "2": "Business Unit",
    "3": "Parent: Child Business Units",
    "4": "Organization",
}


def extract_workflow_name(file_path: str) -> str:
    """Extract workflow name from filename by removing GUID suffix."""
    filename = Path(file_path).stem  # Removes .xaml extension

    # Remove GUID pattern: 8-4-4-4-12 hexadecimal at end
    parts = filename.split('-')
    if len(parts) >= 5:
        guid_parts = parts[-5:]
        if (len(guid_parts[0]) == 8 and len(guid_parts[1]) == 4 and
                len(guid_parts[2]) == 4 and len(guid_parts[3]) == 4 and
                len(guid_parts[4]) == 12):
            return '-'.join(parts[:-5])

    return filename


def parse_data_xml(data_xml_path: str) -> Dict[str, Any]:
    """Parse the .xaml.data.xml metadata file."""
    tree = ET.parse(data_xml_path)
    root = tree.getroot()

    def get_text(tag: str, default: str = "") -> str:
        el = root.find(tag)
        return el.text.strip() if el is not None and el.text else default

    category_code = get_text("Category", "0")
    mode_code = get_text("Mode", "0")
    scope_code = get_text("Scope", "4")

    # Build trigger description
    trigger_parts = []
    on_demand = get_text("OnDemand", "0") == "1"
    trigger_on_create = get_text("TriggerOnCreate", "0") == "1"
    trigger_on_delete = get_text("TriggerOnDelete", "0") == "1"
    trigger_fields_raw = get_text("TriggerOnUpdateAttributeList", "")
    trigger_fields = [f.strip() for f in trigger_fields_raw.split(",") if f.strip()]

    if trigger_on_create:
        trigger_parts.append("Record Created")
    if trigger_on_delete:
        trigger_parts.append("Record Deleted")
    if trigger_fields:
        trigger_parts.append(f"Field Updated ({', '.join(trigger_fields)})")
    if on_demand and not trigger_parts:
        trigger_parts.append("On Demand / Manual")
    if not trigger_parts:
        trigger_parts.append("Unknown")

    workflow_id = root.get("WorkflowId", "").strip("{}")
    workflow_name = root.get("Name", "")

    return {
        "workflowId": workflow_id,
        "name": workflow_name,
        "category": CATEGORY_NAMES.get(category_code, f"Unknown ({category_code})"),
        "categoryCode": int(category_code),
        "mode": MODE_NAMES.get(mode_code, f"Unknown ({mode_code})"),
        "modeCode": int(mode_code),
        "scope": SCOPE_NAMES.get(scope_code, f"Unknown ({scope_code})"),
        "primaryEntity": get_text("PrimaryEntity", "Unknown"),
        "isSubprocess": get_text("Subprocess", "0") == "1",
        "isActive": get_text("StateCode", "0") == "1",
        "runAs": "Calling User" if get_text("RunAs", "1") == "0" else "Owner",
        "isTransacted": get_text("IsTransacted", "0") == "1",
        "trigger": {
            "onDemand": on_demand,
            "onCreate": trigger_on_create,
            "onDelete": trigger_on_delete,
            "onUpdateFields": trigger_fields,
            "description": " / ".join(trigger_parts),
        },
        "introducedVersion": get_text("IntroducedVersion", ""),
    }


def parse_xaml_steps(xaml_path: str) -> Dict[str, Any]:
    """Parse the XAML workflow file to extract step statistics."""
    tree = ET.parse(xaml_path)
    root = tree.getroot()

    # Namespace mappings
    ns = {
        "mxswa": "clr-namespace:Microsoft.Xrm.Sdk.Workflow.Activities;assembly=Microsoft.Xrm.Sdk.Workflow, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
        "x": "http://schemas.microsoft.com/winfx/2006/xaml",
    }

    stats = {
        "conditions": 0,
        "updates": 0,
        "creates": 0,
        "sends": 0,
        "assigns": 0,
        "customActivities": 0,
        "totalSteps": 0,
        "nestingDepth": 0,
        "namedSteps": [],
    }

    def walk(element: ET.Element, depth: int = 0):
        stats["nestingDepth"] = max(stats["nestingDepth"], depth)

        display_name = element.get("DisplayName", "")
        aqn = element.get("AssemblyQualifiedName", "")

        if display_name:
            stats["totalSteps"] += 1
            if display_name not in stats["namedSteps"]:
                stats["namedSteps"].append(display_name)

        # Classify step type from AssemblyQualifiedName or DisplayName
        if "ConditionSequence" in aqn or display_name.lower().startswith("conditionstep"):
            stats["conditions"] += 1
        elif "UpdateEntity" in aqn or "SetEntityProperty" in aqn.split(".")[-1]:
            stats["updates"] += 1
        elif "CreateEntity" in aqn:
            stats["creates"] += 1
        elif "SendEmail" in aqn:
            stats["sends"] += 1
        elif "AssignEntity" in aqn:
            stats["assigns"] += 1
        elif aqn and "Microsoft.Crm.Workflow" not in aqn and "Microsoft.Xrm" not in aqn:
            stats["customActivities"] += 1

        for child in element:
            walk(child, depth + 1)

    walk(root)

    # Remove duplicate/boilerplate step names
    boilerplate = {"EvaluateExpression", "EvaluateCondition", "GetEntityProperty", "SetEntityProperty"}
    stats["namedSteps"] = [s for s in stats["namedSteps"] if s not in boilerplate][:20]

    return stats


def calculate_complexity(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate workflow complexity rating."""
    total = stats["totalSteps"]
    depth = stats["nestingDepth"]
    conditions = stats["conditions"]
    custom = stats["customActivities"]

    factors = []

    if total > 50 or depth > 6:
        rating = "Very Complex"
    elif total > 25 or depth > 4:
        rating = "Complex"
    elif total > 10 or depth > 3:
        rating = "Medium"
    else:
        rating = "Simple"

    if depth > 4:
        factors.append(f"Deep nesting ({depth} levels)")
    if conditions > 5:
        factors.append(f"Many conditions ({conditions})")
    elif conditions > 2:
        factors.append(f"Multiple conditions ({conditions})")
    if custom > 0:
        factors.append(f"Custom plugin activities ({custom})")
    if stats["creates"] > 2:
        factors.append(f"Multiple record creates ({stats['creates']})")
    if stats["sends"] > 0:
        factors.append(f"Email notifications ({stats['sends']})")
    if not factors:
        factors.append("Simple sequential steps")

    return {"rating": rating, "factors": factors}


def extract_metadata(xaml_path: str) -> Dict[str, Any]:
    """Extract full metadata from a XAML workflow file pair."""
    data_xml_path = xaml_path + ".data.xml"

    if not os.path.exists(data_xml_path):
        raise FileNotFoundError(f"Metadata file not found: {data_xml_path}")

    file_stat = os.stat(xaml_path)
    file_size = file_stat.st_size
    file_modified = datetime.fromtimestamp(file_stat.st_mtime).isoformat() + "Z"

    workflow_name = extract_workflow_name(xaml_path)
    data = parse_data_xml(data_xml_path)
    xaml_stats = parse_xaml_steps(xaml_path)
    complexity = calculate_complexity(xaml_stats)

    return {
        "workflowName": workflow_name,
        "displayName": data["name"] or workflow_name,
        "workflowId": data["workflowId"],
        "sourceFile": xaml_path,
        "metadataFile": data_xml_path,
        "analysisDate": datetime.now().astimezone().replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "category": data["category"],
        "mode": data["mode"],
        "scope": data["scope"],
        "primaryEntity": data["primaryEntity"],
        "isActive": data["isActive"],
        "isSubprocess": data["isSubprocess"],
        "runAs": data["runAs"],
        "isTransacted": data["isTransacted"],
        "introducedVersion": data["introducedVersion"],
        "trigger": data["trigger"],
        "statistics": {
            "totalSteps": xaml_stats["totalSteps"],
            "conditions": xaml_stats["conditions"],
            "updates": xaml_stats["updates"],
            "creates": xaml_stats["creates"],
            "emailsSent": xaml_stats["sends"],
            "assigns": xaml_stats["assigns"],
            "customActivities": xaml_stats["customActivities"],
            "nestingDepth": xaml_stats["nestingDepth"],
            "namedSteps": xaml_stats["namedSteps"],
        },
        "complexity": complexity,
        "fileInfo": {
            "sizeBytes": file_size,
            "lastModified": file_modified,
        },
    }


def main():
    """Main entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h", "help"]:
        print(__doc__)
        sys.exit(0 if len(sys.argv) > 1 else 1)

    xaml_path = sys.argv[1]

    if not os.path.exists(xaml_path):
        print(f"Error: File not found: {xaml_path}", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Extracting metadata from: {xaml_path}")
        metadata = extract_metadata(xaml_path)

        if len(sys.argv) >= 3:
            output_dir = sys.argv[2]
        else:
            output_dir = f"wiki/Technical-Reference/classic-workflows/{metadata['workflowName']}"

        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "metadata.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Metadata extracted successfully")
        print(f"  Output:     {output_path}")
        print(f"  Workflow:   {metadata['displayName']}")
        print(f"  Entity:     {metadata['primaryEntity']}")
        print(f"  Trigger:    {metadata['trigger']['description']}")
        print(f"  Mode:       {metadata['mode']}")
        print(f"  Complexity: {metadata['complexity']['rating']}")
        print(f"  Steps:      {metadata['statistics']['totalSteps']}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Error: Invalid XML: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
