#!/usr/bin/env python3
"""
Fetch Power Automate cloud flow JSON directly from Dataverse.

This script retrieves the latest matching cloud flow definition from Dataverse and
writes files aligned with unpacked solution conventions:

- <FlowName>-<GUID>.json
- <FlowName>-<GUID>.dataverse.json (raw Dataverse record for traceability)

By default, output is written to:
  .staging/cloud-flows/<FlowName>/

Usage examples:
    # List configured environments
    python fetch-flow-from-dataverse.py --list-environments

    # Fetch latest by flow ID
    python fetch-flow-from-dataverse.py --environment dev \
        --flow-id FF7B08CD-132F-EF11-8E4F-6045BD5D6396

    # Fetch latest by exact name
    python fetch-flow-from-dataverse.py --environment dev \
        --name "UpdateInvoiceDetails"

    # Fetch latest by partial name
    python fetch-flow-from-dataverse.py --environment dev \
        --name-contains "UpdateInvoice"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
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
    return cleaned or "CloudFlow"


def _v(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


class DataverseCloudFlowFetcher:
    """Fetch cloud flow definitions from Dataverse workflow table."""

    WORKFLOW_COLUMNS = [
        "workflowid",
        "name",
        "uniquename",
        "category",
        "statecode",
        "ondemand",
        "modifiedon",
        "versionnumber",
        "clientdata",
    ]

    # Cloud flow categories observed in Dataverse workflow table.
    CLOUD_FLOW_CATEGORIES = ["5", "6", "9"]

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_fetchxml(
        self,
        flow_id: Optional[str] = None,
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
                for c in self.CLOUD_FLOW_CATEGORIES
            )
            + "</filter>"
        ]

        if state_filter == "active":
            clauses.append('<condition attribute="statecode" operator="eq" value="1" />')
        elif state_filter == "draft":
            clauses.append('<condition attribute="statecode" operator="eq" value="0" />')

        if flow_id:
            clauses.append(
                f'<condition attribute="workflowid" operator="eq" value="{_normalize_guid(flow_id)}" />'
            )
        elif name:
            safe_name = name.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="eq" value="{safe_name}" />')
        elif name_contains:
            safe_name = name_contains.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="like" value="%{safe_name}%" />')

        filter_xml = "<filter type=\"and\">" + "".join(clauses) + "</filter>"

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
        flow_id: Optional[str] = None,
        name: Optional[str] = None,
        name_contains: Optional[str] = None,
        state_filter: str = "all",
    ) -> Dict[str, Any]:
        fetch_xml = self._build_fetchxml(
            flow_id=flow_id,
            name=name,
            name_contains=name_contains,
            state_filter=state_filter,
        )
        result = self.client.get_records_with_fetchxml("workflows", fetch_xml)
        matches = result.get("value", [])
        if not matches:
            raise ValueError("No matching cloud flows were found.")

        latest = matches[0]
        if not latest.get("clientdata"):
            raise ValueError(
                "Matching flow found, but 'clientdata' is empty. "
                "This record may not contain a cloud flow definition."
            )

        return {"latest": latest, "matches": matches}


def _normalize_flow_payload(clientdata: str, fallback_name: str) -> Dict[str, Any]:
    payload: Any = json.loads(clientdata)

    # Most unpacked flow files use a top-level "properties" object.
    if isinstance(payload, dict) and "properties" in payload and isinstance(payload["properties"], dict):
        payload["properties"].setdefault("displayName", fallback_name)
        return payload

    # Defensive fallback for alternate shapes.
    if isinstance(payload, dict):
        wrapped = {"properties": payload}
        wrapped["properties"].setdefault("displayName", fallback_name)
        return wrapped

    raise ValueError("Cloud flow clientdata JSON is not an object.")


def _write_outputs(record: Dict[str, Any], output_dir: Optional[Path] = None) -> Dict[str, Path]:
    flow_id = _normalize_guid(_v(record.get("workflowid")))
    flow_name = _sanitize_filename(_v(record.get("name"), "CloudFlow"))
    base_name = f"{flow_name}-{flow_id.upper()}" if flow_id else flow_name

    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "cloud-flows" / flow_name

    output_dir.mkdir(parents=True, exist_ok=True)
    flow_json_path = output_dir / f"{base_name}.json"
    raw_json_path = output_dir / f"{base_name}.dataverse.json"

    normalized_payload = _normalize_flow_payload(_v(record.get("clientdata")), _v(record.get("name"), flow_name))
    flow_json_path.write_text(json.dumps(normalized_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    raw_json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"flow_json": flow_json_path, "raw_json": raw_json_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch latest cloud flow JSON from Dataverse",
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

    parser.add_argument("--flow-id", help="Flow workflow GUID (exact match)")
    parser.add_argument("--name", help="Flow name (exact match)")
    parser.add_argument("--name-contains", help="Flow name contains text")
    parser.add_argument(
        "--state",
        choices=["all", "active", "draft"],
        default="all",
        help="Filter by flow state before selecting latest (default: all)",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder for generated files (default: .staging/cloud-flows/<FlowName>/)",
    )

    parser.add_argument("--app-id", help="Application (client) ID (overrides config if supplied)")
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
            "Install dependencies: pip install azure-identity requests PowerPlatform-Dataverse-Client",
            file=sys.stderr,
        )
        return 1

    provided_lookup = [bool(args.flow_id), bool(args.name), bool(args.name_contains)]
    if sum(provided_lookup) != 1:
        print(
            "Error: Provide exactly one lookup option: --flow-id, --name, or --name-contains.",
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

        fetcher = DataverseCloudFlowFetcher(client)
        response = fetcher.query_latest(
            flow_id=args.flow_id,
            name=args.name,
            name_contains=args.name_contains,
            state_filter=args.state,
        )

        latest = response["latest"]
        matches = response["matches"]
        paths = _write_outputs(latest, args.output_dir)

        print("Cloud flow fetched successfully.")
        print(f"  Name:      {latest.get('name', '<unknown>')}")
        print(f"  ID:        {latest.get('workflowid', '<unknown>')}")
        print(f"  Category:  {latest.get('category', '<unknown>')}")
        print(f"  Modified:  {latest.get('modifiedon', '<unknown>')}")
        print(f"  Matches:   {len(matches)} (latest selected)")
        print(f"  Flow JSON: {paths['flow_json']}")
        print(f"  Raw JSON:  {paths['raw_json']}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
