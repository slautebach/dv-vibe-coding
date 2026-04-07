#!/usr/bin/env python3
"""
Fetch classic Dataverse workflow XAML directly from an environment.

This script retrieves the latest matching classic workflow definition from Dataverse
and writes two files that align with unpacked solution conventions:

- <WorkflowName>-<GUID>.xaml
- <WorkflowName>-<GUID>.xaml.data.xml

By default, output is written to:
  .staging/classic-workflows/<WorkflowName>-<GUID>/

Environment configuration is loaded from the .env file at the repository root using the shared
config_loader.py script.

Usage examples:
    # List configured environments
    python fetch-workflow-from-dataverse.py --list-environments

    # Fetch latest by workflow ID
    python fetch-workflow-from-dataverse.py --environment dev \
        --workflow-id E9581E0B-F5C7-49CD-81B7-7EAF5D668B3A

    # Fetch latest by exact name
    python fetch-workflow-from-dataverse.py --environment dev \
        --name "SIS - Close Case"

    # Fetch latest by partial name match
    python fetch-workflow-from-dataverse.py --environment dev \
        --name-contains "Close Case"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional


# Add shared scripts directory to path for config_loader and dataverse_sdk_client
_SHARED_SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "scripts"
_REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
if str(_SHARED_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_SCRIPTS_DIR))

from config_loader import ConfigurationError, list_environments, load_dataverse_config

DATAVERSE_AVAILABLE = False
IMPORT_ERROR = ""

try:
    from dataverse_sdk_client import DataverseClient

    DATAVERSE_AVAILABLE = True
except ImportError as e:
    IMPORT_ERROR = str(e)


def _normalize_guid(value: str) -> str:
    return value.strip().strip("{}").lower()


def _sanitize_filename(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "-", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "Workflow"


def _xml_value(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


class WorkflowDataverseFetcher:
    """Fetch classic workflow definitions from Dataverse."""

    WORKFLOW_COLUMNS = [
        "workflowid",
        "name",
        "uniquename",
        "category",
        "mode",
        "scope",
        "ondemand",
        "triggeroncreate",
        "triggerondelete",
        "triggeronupdateattributelist",
        "primaryentity",
        "subprocess",
        "statecode",
        "runas",
        "istransacted",
        "introducedversion",
        "xaml",
        "modifiedon",
        "versionnumber",
    ]

    # 0=Workflow, 1=Dialog, 3=Action, 4=BPF; exclude modern flow categories.
    CLASSIC_CATEGORIES = ["0", "1", "3", "4"]

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_fetchxml(
        self,
        workflow_id: Optional[str] = None,
        name: Optional[str] = None,
        name_contains: Optional[str] = None,
        state_filter: str = "all",
        top: int = 25,
    ) -> str:
        attributes = "".join(f'<attribute name="{c}" />' for c in self.WORKFLOW_COLUMNS)

        clauses: List[str] = [
            "<filter type=\"or\">"
            + "".join(
                f'<condition attribute="category" operator="eq" value="{c}" />'
                for c in self.CLASSIC_CATEGORIES
            )
            + "</filter>"
        ]

        if state_filter == "active":
            clauses.append('<condition attribute="statecode" operator="eq" value="1" />')
        elif state_filter == "draft":
            clauses.append('<condition attribute="statecode" operator="eq" value="0" />')

        if workflow_id:
            clauses.append(
                f'<condition attribute="workflowid" operator="eq" value="{_normalize_guid(workflow_id)}" />'
            )
        elif name:
            safe_name = name.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="eq" value="{safe_name}" />')
        elif name_contains:
            safe_name = name_contains.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="like" value="%{safe_name}%" />')

        filter_xml = "<filter type=\"and\">" + "".join(clauses) + "</filter>"

        # Prefer newest modified records and then latest version number.
        return f"""
<fetch top="{top}">
  <entity name="workflow">
    {attributes}
    {filter_xml}
    <order attribute="modifiedon" descending="true" />
    <order attribute="versionnumber" descending="true" />
  </entity>
</fetch>
"""

    def query_latest(
        self,
        workflow_id: Optional[str] = None,
        name: Optional[str] = None,
        name_contains: Optional[str] = None,
        state_filter: str = "all",
    ) -> Dict[str, Any]:
        fetch_xml = self._build_fetchxml(
            workflow_id=workflow_id,
            name=name,
            name_contains=name_contains,
            state_filter=state_filter,
        )
        result = self.client.get_records_with_fetchxml("workflows", fetch_xml)
        matches = result.get("value", [])
        if not matches:
            raise ValueError("No matching classic workflows were found.")

        latest = matches[0]
        if not latest.get("xaml"):
            raise ValueError(
                "Matching workflow found, but XAML payload is empty. "
                "Ensure this is a classic XAML workflow."
            )

        return {"latest": latest, "matches": matches}


def _write_data_xml(record: Dict[str, Any], output_path: Path) -> None:
    workflow_id = _xml_value(record.get("workflowid")).strip("{}")
    name = _xml_value(record.get("name"))

    root = ET.Element(
        "Workflow",
        {
            "Name": name,
            "WorkflowId": "{" + workflow_id + "}" if workflow_id else "",
        },
    )

    fields = {
        "Category": _xml_value(record.get("category"), "0"),
        "Mode": _xml_value(record.get("mode"), "0"),
        "Scope": _xml_value(record.get("scope"), "4"),
        "OnDemand": _xml_value(record.get("ondemand"), "0"),
        "TriggerOnCreate": _xml_value(record.get("triggeroncreate"), "0"),
        "TriggerOnDelete": _xml_value(record.get("triggerondelete"), "0"),
        "TriggerOnUpdateAttributeList": _xml_value(record.get("triggeronupdateattributelist"), ""),
        "PrimaryEntity": _xml_value(record.get("primaryentity"), ""),
        "Subprocess": _xml_value(record.get("subprocess"), "0"),
        "StateCode": _xml_value(record.get("statecode"), "0"),
        "RunAs": _xml_value(record.get("runas"), "1"),
        "IsTransacted": _xml_value(record.get("istransacted"), "0"),
        "IntroducedVersion": _xml_value(record.get("introducedversion"), ""),
    }

    for key, value in fields.items():
        el = ET.SubElement(root, key)
        el.text = value

    xml_bytes = ET.tostring(root, encoding="utf-8")
    output_path.write_bytes(b'<?xml version="1.0" encoding="utf-8"?>\n' + xml_bytes)


def _write_outputs(record: Dict[str, Any], output_dir: Optional[Path] = None) -> Dict[str, Path]:
    workflow_id = _normalize_guid(_xml_value(record.get("workflowid")))
    name = _sanitize_filename(_xml_value(record.get("name"), "Workflow"))
    base_name = f"{name}-{workflow_id.upper()}" if workflow_id else name

    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "classic-workflows" / base_name

    output_dir.mkdir(parents=True, exist_ok=True)
    xaml_path = output_dir / f"{base_name}.xaml"
    data_xml_path = output_dir / f"{base_name}.xaml.data.xml"
    raw_json_path = output_dir / f"{base_name}.dataverse.json"

    xaml_text = _xml_value(record.get("xaml"))
    xaml_path.write_text(xaml_text, encoding="utf-8")
    _write_data_xml(record, data_xml_path)
    raw_json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"xaml": xaml_path, "data_xml": data_xml_path, "raw_json": raw_json_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch latest classic workflow XAML from Dataverse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--environment",
        "-e",
        default="dev",
        help="Accepted for backward compatibility; configuration is loaded from .env",
    )
    parser.add_argument(
        "--list-environments",
        action="store_true",
        help="List available environment names from config and exit",
    )

    parser.add_argument("--workflow-id", help="Workflow GUID (exact match)")
    parser.add_argument("--name", help="Workflow name (exact match)")
    parser.add_argument("--name-contains", help="Workflow name contains text")
    parser.add_argument(
        "--state",
        choices=["all", "active", "draft"],
        default="all",
        help="Filter by workflow state before selecting latest (default: all)",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder for generated files (default: .staging/classic-workflows/<WorkflowName>-<GUID>/)",
    )

    parser.add_argument(
        "--app-id",
        help="Application (client) ID (overrides config if supplied)",
    )
    parser.add_argument(
        "--client-secret",
        help="Client secret (or set DATAVERSE_CLIENT_SECRET)",
    )
    parser.add_argument(
        "--clear-auth",
        action="store_true",
        help="Clear cached interactive auth records and exit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_environments:
        try:
            print(", ".join(list_environments()))
            return 0
        except ConfigurationError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if not DATAVERSE_AVAILABLE:
        print("Error: Dataverse client dependencies are not available.", file=sys.stderr)
        print(f"Import error: {IMPORT_ERROR}", file=sys.stderr)
        print(
            "Install dependencies: pip install azure-identity requests PowerPlatform-Dataverse-Client",
            file=sys.stderr,
        )
        return 1

    provided_lookup = [bool(args.workflow_id), bool(args.name), bool(args.name_contains)]
    if sum(provided_lookup) != 1:
        print(
            "Error: Provide exactly one lookup option: --workflow-id, --name, or --name-contains.",
            file=sys.stderr,
        )
        return 1

    try:
        config = load_dataverse_config(args.environment)
    except ConfigurationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    environment_url = config["environment_url"]
    tenant_id = config["tenant_id"]
    app_id = args.app_id or config.get("app_id")
    client_secret = args.client_secret or os.environ.get("DATAVERSE_CLIENT_SECRET")

    if args.clear_auth:
        auth_dir = Path.home() / ".dataverse"
        if auth_dir.exists():
            for auth_file in auth_dir.glob("auth_record_*.json"):
                auth_file.unlink()
                print(f"Cleared cached auth: {auth_file}")
        else:
            print("No cached authentication records found.")
        return 0

    try:
        client = DataverseClient(environment_url)
        client.connect(app_id=app_id, client_secret=client_secret, tenant_id=tenant_id)

        fetcher = WorkflowDataverseFetcher(client)
        response = fetcher.query_latest(
            workflow_id=args.workflow_id,
            name=args.name,
            name_contains=args.name_contains,
            state_filter=args.state,
        )

        latest = response["latest"]
        matches = response["matches"]
        paths = _write_outputs(latest, args.output_dir)

        print("Workflow fetched successfully.")
        print(f"  Name:      {latest.get('name', '<unknown>')}")
        print(f"  ID:        {latest.get('workflowid', '<unknown>')}")
        print(f"  Modified:  {latest.get('modifiedon', '<unknown>')}")
        print(f"  Matches:   {len(matches)} (latest selected)")
        print(f"  XAML:      {paths['xaml']}")
        print(f"  Data XML:  {paths['data_xml']}")
        print(f"  Raw JSON:  {paths['raw_json']}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
