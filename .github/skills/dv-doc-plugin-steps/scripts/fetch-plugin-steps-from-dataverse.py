#!/usr/bin/env python3
"""
Fetch plugin assemblies and registered SDK message processing steps from Dataverse.

This script retrieves plugin step registrations via a single joined FetchXML query
that spans sdkmessageprocessingstep, plugintype, pluginassembly, sdkmessage, and
sdkmessagefilter. Results are grouped by assembly name and written per assembly.

Output JSON structure per assembly:
  {
    "assembly": "MNP.IA.Plugins",
    "steps": [
      {
        "sdkmessageprocessingstepid": "...",
        "name": "...",
        "description": "...",
        "stage": 20,
        "mode": 0,
        "rank": 1,
        "statecode": 0,
        "filteringattributes": "...",
        "configuration": "...",
        "supporteddeployment": 0,
        "modifiedon": "...",
        "plugintype_typename": "MNP.IA.Plugins.SomePlugin",
        "plugintype_name": "SomePlugin",
        "plugintype_description": "...",
        "message_name": "Update",
        "primary_entity": "contact"
      }
    ]
  }

Files written to .staging/plugin-steps/<AssemblyName>/:
  <AssemblyName>.plugin-steps.json  — grouped assembly + steps
  <AssemblyName>.dataverse.json     — raw FetchXML records for traceability

Usage examples:
    # List configured environments
    python fetch-plugin-steps-from-dataverse.py --list-environments

    # Fetch steps for a specific assembly (name contains)
    python fetch-plugin-steps-from-dataverse.py --environment dev --assembly "MNP.IA.Plugins"

    # Fetch steps registered on a specific entity
    python fetch-plugin-steps-from-dataverse.py --environment dev --entity contact

    # Fetch all custom plugin steps
    python fetch-plugin-steps-from-dataverse.py --environment dev --all
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
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
    return cleaned or "PluginAssembly"


def _v(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


class DataversePluginStepFetcher:
    """Fetch plugin step registrations from Dataverse via joined FetchXML."""

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_fetchxml(
        self,
        assembly_contains: Optional[str] = None,
        entity_name: Optional[str] = None,
        fetch_all: bool = False,
        top: int = 500,
    ) -> str:
        assembly_filter = ""
        if assembly_contains:
            safe = assembly_contains.replace('"', "&quot;")
            assembly_filter = f'<condition attribute="name" operator="like" value="%{safe}%" />'
        elif fetch_all:
            # Exclude system plugins by requiring customizationlevel > 0
            assembly_filter = '<condition attribute="customizationlevel" operator="gt" value="0" />'

        entity_filter = ""
        if entity_name:
            safe = entity_name.replace('"', "&quot;")
            entity_filter = f'<condition attribute="primaryobjecttypecode" operator="eq" value="{safe}" />'

        return f"""
<fetch top="{top}">
  <entity name="sdkmessageprocessingstep">
    <attribute name="sdkmessageprocessingstepid"/>
    <attribute name="name"/>
    <attribute name="description"/>
    <attribute name="stage"/>
    <attribute name="mode"/>
    <attribute name="rank"/>
    <attribute name="statecode"/>
    <attribute name="filteringattributes"/>
    <attribute name="configuration"/>
    <attribute name="supporteddeployment"/>
    <attribute name="modifiedon"/>
    <link-entity name="plugintype" from="plugintypeid" to="plugintypeid" alias="pt">
      <attribute name="typename"/>
      <attribute name="name"/>
      <attribute name="description"/>
      <link-entity name="pluginassembly" from="pluginassemblyid" to="pluginassemblyid" alias="pa">
        <attribute name="name"/>
        <attribute name="version"/>
        <attribute name="isolationmode"/>
        {assembly_filter}
      </link-entity>
    </link-entity>
    <link-entity name="sdkmessage" from="sdkmessageid" to="sdkmessageid" alias="msg">
      <attribute name="name"/>
    </link-entity>
    <link-entity name="sdkmessagefilter" from="sdkmessagefilterid" to="sdkmessagefilterid" link-type="outer" alias="flt">
      <attribute name="primaryobjecttypecode"/>
      {entity_filter}
    </link-entity>
  </entity>
</fetch>
"""

    def query_steps(
        self,
        assembly_contains: Optional[str] = None,
        entity_name: Optional[str] = None,
        fetch_all: bool = False,
    ) -> List[Dict[str, Any]]:
        fetch_xml = self._build_fetchxml(
            assembly_contains=assembly_contains,
            entity_name=entity_name,
            fetch_all=fetch_all,
        )
        result = self.client.get_records_with_fetchxml("sdkmessageprocessingsteps", fetch_xml)
        records = result.get("value", [])
        if not records:
            raise ValueError("No matching plugin steps were found.")
        return records


def _flatten_aliased_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    """Promote OData aliased fields (e.g. 'pa.name@OData.Community...') to clean keys."""
    flat: Dict[str, Any] = {}
    for key, val in record.items():
        # Strip OData annotation suffixes
        clean_key = re.sub(r"@.*", "", key)
        flat[clean_key] = val
    return flat


def _group_by_assembly(records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group flattened step records by assembly name."""
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in records:
        flat = _flatten_aliased_fields(record)
        assembly_name = _v(flat.get("pa.name"), "Unknown")
        step = {
            "sdkmessageprocessingstepid": flat.get("sdkmessageprocessingstepid"),
            "name": flat.get("name"),
            "description": flat.get("description"),
            "stage": flat.get("stage"),
            "mode": flat.get("mode"),
            "rank": flat.get("rank"),
            "statecode": flat.get("statecode"),
            "filteringattributes": flat.get("filteringattributes"),
            "configuration": flat.get("configuration"),
            "supporteddeployment": flat.get("supporteddeployment"),
            "modifiedon": flat.get("modifiedon"),
            "plugintype_typename": flat.get("pt.typename"),
            "plugintype_name": flat.get("pt.name"),
            "plugintype_description": flat.get("pt.description"),
            "assembly_name": assembly_name,
            "assembly_version": flat.get("pa.version"),
            "assembly_isolationmode": flat.get("pa.isolationmode"),
            "message_name": flat.get("msg.name"),
            "primary_entity": flat.get("flt.primaryobjecttypecode"),
        }
        groups[assembly_name].append(step)
    return dict(groups)


def _write_outputs(
    assembly_name: str,
    steps: List[Dict[str, Any]],
    raw_records: List[Dict[str, Any]],
    output_dir: Optional[Path] = None,
) -> Dict[str, Path]:
    safe_name = _sanitize_filename(assembly_name)

    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "plugin-steps" / safe_name

    output_dir.mkdir(parents=True, exist_ok=True)

    steps_payload = {"assembly": assembly_name, "steps": steps}
    steps_path = output_dir / f"{safe_name}.plugin-steps.json"
    steps_path.write_text(json.dumps(steps_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    raw_path = output_dir / f"{safe_name}.dataverse.json"
    raw_path.write_text(json.dumps(raw_records, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"steps_json": steps_path, "raw_json": raw_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch plugin assemblies and SDK message processing steps from Dataverse",
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

    lookup = parser.add_mutually_exclusive_group()
    lookup.add_argument("--assembly", help="Filter by assembly name (contains match)")
    lookup.add_argument("--entity", help="Filter by primary entity logical name (exact match)")
    lookup.add_argument("--all", action="store_true", help="Fetch all custom plugin steps")

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder override (default: .staging/plugin-steps/<AssemblyName>/)",
    )

    parser.add_argument("--app-id", help="Application (client) ID for auth (overrides config)")
    parser.add_argument("--client-secret", help="Client secret (or set DATAVERSE_CLIENT_SECRET)")
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
            "Install dependencies: pip install azure-identity requests",
            file=sys.stderr,
        )
        return 1

    if not any([args.assembly, args.entity, args.all]):
        print(
            "Error: Provide one lookup option: --assembly, --entity, or --all.",
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

        fetcher = DataversePluginStepFetcher(client)
        raw_records = fetcher.query_steps(
            assembly_contains=args.assembly,
            entity_name=args.entity,
            fetch_all=args.all,
        )

        grouped = _group_by_assembly(raw_records)
        print(f"Found {len(raw_records)} step(s) across {len(grouped)} assembly(ies).")

        for assembly_name, steps in grouped.items():
            paths = _write_outputs(assembly_name, steps, raw_records, args.output_dir)
            print(f"\nAssembly: {assembly_name}")
            print(f"  Steps:       {len(steps)}")
            print(f"  Steps JSON:  {paths['steps_json']}")
            print(f"  Raw JSON:    {paths['raw_json']}")

        print(f"\nDone. {len(grouped)} assembly file(s) written.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
