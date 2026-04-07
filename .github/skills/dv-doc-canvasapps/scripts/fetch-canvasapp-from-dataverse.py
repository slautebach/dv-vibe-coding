#!/usr/bin/env python3
"""
Fetch canvas app metadata directly from Dataverse.

This script retrieves the latest matching canvas app and writes files for analysis:

- <AppName>.meta.xml               (normalized metadata for the canvas app skill)
- <AppName>.dataverse.json         (raw Dataverse record for traceability)

By default, output is written to:
/all  .staging/canvas-apps/<AppName>/source/

Usage examples:
    # List configured environments
    python fetch-canvasapp-from-dataverse.py --list-environments

    # Fetch by canvas app ID
    python fetch-canvasapp-from-dataverse.py --environment dev \
        --app-id e7274ede-a366-4cd5-8728-e909c7aeb04a

    # Fetch by exact name
    python fetch-canvasapp-from-dataverse.py --environment dev \
        --name mnp_emaildialog_8c1d7

    # Fetch by partial name
    python fetch-canvasapp-from-dataverse.py --environment dev \
        --name-contains emaildialog
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


def _v(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _normalize_guid(value: str) -> str:
    return value.strip().strip("{}").lower()


def _sanitize_name(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "-", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "CanvasApp"


class DataverseCanvasAppFetcher:
    """Fetch canvas app metadata from Dataverse."""

    COLUMNS = [
        "canvasappid",
        "name",
        "displayname",
        "appversion",
        "status",
        "createdbyclientversion",
        "minclientversion",
        "tags",
        "description",
        "connectionreferences",
        "cdsdependencies",
        "authorizationreferences",
        "databasereferences",
        "appcomponents",
        "appcomponentdependencies",
        "backgroundimageuri",
        "documenturi",
        "introducedversion",
        "modifiedon",
        "versionnumber",
    ]

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_fetchxml(
        self,
        app_id: Optional[str] = None,
        name: Optional[str] = None,
        name_contains: Optional[str] = None,
        top: int = 25,
    ) -> str:
        attributes = "".join(f'<attribute name="{c}" />' for c in self.COLUMNS)
        clauses: List[str] = []

        if app_id:
            clauses.append(
                f'<condition attribute="canvasappid" operator="eq" value="{_normalize_guid(app_id)}" />'
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
  <entity name="canvasapp">
    {attributes}
    {filter_xml}
    <order attribute="modifiedon" descending="true" />
    <order attribute="versionnumber" descending="true" />
  </entity>
</fetch>
"""

    def query_latest(
        self,
        app_id: Optional[str] = None,
        name: Optional[str] = None,
        name_contains: Optional[str] = None,
    ) -> Dict[str, Any]:
        fetch_xml = self._build_fetchxml(app_id=app_id, name=name, name_contains=name_contains)
        result = self.client.get_records_with_fetchxml("canvasapps", fetch_xml)
        matches = result.get("value", [])
        if not matches:
            raise ValueError("No matching canvas apps were found.")
        return {"latest": matches[0], "matches": matches}


def _meta_field_xml_name(key: str) -> str:
    return "".join(part.capitalize() for part in key.split("_"))


def _build_meta_xml(record: Dict[str, Any]) -> str:
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root = ET.Element("CanvasApp", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})

    ordered_fields = [
        "name",
        "appversion",
        "status",
        "createdbyclientversion",
        "minclientversion",
        "tags",
        "displayname",
        "description",
        "authorizationreferences",
        "connectionreferences",
        "databasereferences",
        "appcomponents",
        "appcomponentdependencies",
        "introducedversion",
        "cdsdependencies",
        "backgroundimageuri",
        "documenturi",
    ]

    for field in ordered_fields:
        el = ET.SubElement(root, _meta_field_xml_name(field))
        value = _v(record.get(field))
        if field in {
            "authorizationreferences",
            "connectionreferences",
            "databasereferences",
            "appcomponents",
            "appcomponentdependencies",
            "cdsdependencies",
            "tags",
        } and value == "":
            value = "[]"
        el.text = value

    gallery_item = ET.SubElement(root, "GalleryItemId")
    gallery_item.set("{http://www.w3.org/2001/XMLSchema-instance}nil", "true")
    gallery_item.text = ""

    xml_bytes = ET.tostring(root, encoding="utf-8")
    return '<?xml version="1.0" encoding="utf-8"?>\n' + xml_bytes.decode("utf-8")


def _write_outputs(record: Dict[str, Any], output_dir: Optional[Path] = None) -> Dict[str, Path]:
    app_name = _sanitize_name(_v(record.get("name"), "CanvasApp"))
    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "canvas-apps" / app_name / "source"

    output_dir.mkdir(parents=True, exist_ok=True)

    meta_path = output_dir / f"{app_name}.meta.xml"
    raw_path = output_dir / f"{app_name}.dataverse.json"
    meta_path.write_text(_build_meta_xml(record), encoding="utf-8")
    raw_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"meta_xml": meta_path, "raw_json": raw_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch latest canvas app metadata from Dataverse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--environment", "-e", default="dev", help="Accepted for backward compatibility; configuration is loaded from .env")
    parser.add_argument("--list-environments", action="store_true", help="List available environments and exit")
    parser.add_argument("--app-id", help="Canvas app GUID (exact match)")
    parser.add_argument("--name", help="Canvas app name (exact match)")
    parser.add_argument("--name-contains", help="Canvas app name contains text")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output folder for generated files (default: .staging/canvas-apps/<AppName>/source/)")
    parser.add_argument("--client-id", help="Application (client) ID (overrides config if supplied)")
    parser.add_argument("--client-secret", help="Client secret (or set DATAVERSE_CLIENT_SECRET)")
    parser.add_argument("--clear-auth", action="store_true", help="Clear cached interactive auth records and exit")
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

    provided_lookup = [bool(args.app_id), bool(args.name), bool(args.name_contains)]
    if sum(provided_lookup) != 1:
        print("Error: Provide exactly one lookup option: --app-id, --name, or --name-contains.", file=sys.stderr)
        return 1

    try:
        config = load_dataverse_config(args.environment)
    except ConfigurationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    environment_url = config["environment_url"]
    tenant_id = config["tenant_id"]
    client_id = args.client_id or config.get("app_id")
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
        client.connect(app_id=client_id, client_secret=client_secret, tenant_id=tenant_id)

        fetcher = DataverseCanvasAppFetcher(client)
        result = fetcher.query_latest(app_id=args.app_id, name=args.name, name_contains=args.name_contains)
        latest = result["latest"]
        matches = result["matches"]
        paths = _write_outputs(latest, args.output_dir)

        print("Canvas app fetched successfully.")
        print(f"  Name:      {latest.get('name', '<unknown>')}")
        print(f"  ID:        {latest.get('canvasappid', '<unknown>')}")
        print(f"  Modified:  {latest.get('modifiedon', '<unknown>')}")
        print(f"  Matches:   {len(matches)} (latest selected)")
        print(f"  Meta XML:  {paths['meta_xml']}")
        print(f"  Raw JSON:  {paths['raw_json']}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
