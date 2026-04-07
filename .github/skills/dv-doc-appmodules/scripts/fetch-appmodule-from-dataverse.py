#!/usr/bin/env python3
"""
Fetch model-driven app module and sitemap directly from Dataverse.

This script retrieves the latest matching app module definition and its associated
sitemap from Dataverse and writes files for downstream analysis:

- <AppUniqueName>.appmodule.json  — merged {"appmodule": {...}, "sitemap": {...}}
- <AppUniqueName>.dataverse.json  — raw Dataverse records for traceability

By default, output is written to:
  .staging/app-modules/<AppUniqueName>/

Output JSON structure:
  {
    "appmodule": {
      "appmoduleid": "...",
      "uniquename": "...",
      "name": "...",
      "description": "...",
      "isdefault": false,
      "formfactor": 2,
      "clienttype": 4,
      "appmoduleversion": "1.0.0.0",
      "statecode": 0,
      "modifiedon": "..."
    },
    "sitemap": {
      "sitemapid": "...",
      "sitemapname": "...",
      "uniquename": "...",
      "sitemapxml": "<SiteMap>...</SiteMap>",
      "isdefault": false,
      "modifiedon": "..."
    }
  }

Usage examples:
    # List configured environments
    python fetch-appmodule-from-dataverse.py --list-environments

    # Fetch by display name
    python fetch-appmodule-from-dataverse.py --environment dev --name "SIS App"

    # Fetch by unique name
    python fetch-appmodule-from-dataverse.py --environment dev --unique-name mnp_sisapp

    # Fetch by app module GUID
    python fetch-appmodule-from-dataverse.py --environment dev \
        --app-id-guid 3a7c1e2d-5f4b-4e6a-9c8d-1b2e3f4a5b6c

    # Fetch all app modules
    python fetch-appmodule-from-dataverse.py --environment dev --all
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
    return cleaned or "AppModule"


def _v(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


class DataverseAppModuleFetcher:
    """Fetch app module and sitemap definitions from Dataverse."""

    APPMODULE_COLUMNS = [
        "appmoduleid",
        "uniquename",
        "name",
        "description",
        "isdefault",
        "formfactor",
        "clienttype",
        "appmoduleversion",
        "statecode",
        "modifiedon",
    ]

    SITEMAP_COLUMNS = [
        "sitemapid",
        "sitemapname",
        "uniquename",
        "sitemapxml",
        "isdefault",
        "modifiedon",
    ]

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_appmodule_fetchxml(
        self,
        app_id_guid: Optional[str] = None,
        name: Optional[str] = None,
        unique_name: Optional[str] = None,
        fetch_all: bool = False,
        top: int = 50,
    ) -> str:
        attributes = "".join(f'<attribute name="{c}" />' for c in self.APPMODULE_COLUMNS)
        clauses: List[str] = []

        if app_id_guid:
            clauses.append(
                f'<condition attribute="appmoduleid" operator="eq" value="{_normalize_guid(app_id_guid)}" />'
            )
        elif unique_name:
            safe = unique_name.replace('"', "&quot;")
            clauses.append(f'<condition attribute="uniquename" operator="eq" value="{safe}" />')
        elif name:
            safe = name.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="eq" value="{safe}" />')

        filter_xml = ""
        if clauses:
            filter_xml = "<filter type=\"and\">" + "".join(clauses) + "</filter>"

        return f"""
<fetch top="{top}">
  <entity name="appmodule">
    {attributes}
    {filter_xml}
    <order attribute="name" descending="false" />
  </entity>
</fetch>
"""

    def _build_sitemap_fetchxml(self, sitemap_id: str) -> str:
        attributes = "".join(f'<attribute name="{c}" />' for c in self.SITEMAP_COLUMNS)
        safe_id = _normalize_guid(sitemap_id)
        return f"""
<fetch top="1">
  <entity name="sitemap">
    {attributes}
    <filter type="and">
      <condition attribute="sitemapid" operator="eq" value="{safe_id}" />
    </filter>
  </entity>
</fetch>
"""

    def query_appmodules(
        self,
        app_id_guid: Optional[str] = None,
        name: Optional[str] = None,
        unique_name: Optional[str] = None,
        fetch_all: bool = False,
    ) -> List[Dict[str, Any]]:
        fetch_xml = self._build_appmodule_fetchxml(
            app_id_guid=app_id_guid,
            name=name,
            unique_name=unique_name,
            fetch_all=fetch_all,
        )
        result = self.client.get_records_with_fetchxml("appmodules", fetch_xml)
        matches = result.get("value", [])
        if not matches:
            raise ValueError("No matching app modules were found.")
        return matches

    def query_sitemap(self, sitemap_id: str) -> Optional[Dict[str, Any]]:
        fetch_xml = self._build_sitemap_fetchxml(sitemap_id)
        result = self.client.get_records_with_fetchxml("sitemaps", fetch_xml)
        records = result.get("value", [])
        return records[0] if records else None


def _write_outputs(
    appmodule: Dict[str, Any],
    sitemap: Optional[Dict[str, Any]],
    output_dir: Optional[Path] = None,
) -> Dict[str, Path]:
    unique_name = _sanitize_filename(
        _v(appmodule.get("uniquename")) or _v(appmodule.get("name"), "AppModule")
    )

    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "app-modules" / unique_name

    output_dir.mkdir(parents=True, exist_ok=True)

    merged = {"appmodule": appmodule, "sitemap": sitemap or {}}
    merged_path = output_dir / f"{unique_name}.appmodule.json"
    merged_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    raw = {"appmodule": appmodule, "sitemap": sitemap or {}}
    raw_path = output_dir / f"{unique_name}.dataverse.json"
    raw_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"appmodule_json": merged_path, "raw_json": raw_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch app module and sitemap from Dataverse",
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
    lookup.add_argument("--name", help="App module display name (exact match)")
    lookup.add_argument("--unique-name", help="App module unique name (exact match)")
    lookup.add_argument("--app-id-guid", help="App module GUID (exact match)")
    lookup.add_argument("--all", action="store_true", help="Fetch all app modules")

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder for generated files (default: .staging/app-modules/<AppUniqueName>/)",
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

    if not any([args.name, args.unique_name, args.app_id_guid, args.all]):
        print(
            "Error: Provide one lookup option: --name, --unique-name, --app-id-guid, or --all.",
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

        fetcher = DataverseAppModuleFetcher(client)
        appmodules = fetcher.query_appmodules(
            app_id_guid=args.app_id_guid,
            name=args.name,
            unique_name=args.unique_name,
            fetch_all=args.all,
        )

        processed = 0
        for appmodule in appmodules:
            sitemap: Optional[Dict[str, Any]] = None
            sitemap_id = appmodule.get("_sitemapid_value")
            if sitemap_id:
                sitemap = fetcher.query_sitemap(sitemap_id)

            out_dir = args.output_dir
            paths = _write_outputs(appmodule, sitemap, out_dir)

            unique_name = _v(appmodule.get("uniquename")) or _v(appmodule.get("name"), "<unknown>")
            print(f"App module fetched: {unique_name}")
            print(f"  Name:         {appmodule.get('name', '<unknown>')}")
            print(f"  Unique Name:  {appmodule.get('uniquename', '<unknown>')}")
            print(f"  ID:           {appmodule.get('appmoduleid', '<unknown>')}")
            print(f"  Modified:     {appmodule.get('modifiedon', '<unknown>')}")
            sitemap_label = sitemap.get("sitemapname", "<unknown>") if sitemap else "<none>"
            print(f"  Sitemap:      {sitemap_label}")
            print(f"  Output JSON:  {paths['appmodule_json']}")
            print(f"  Raw JSON:     {paths['raw_json']}")
            processed += 1

        print(f"\nDone. {processed} app module(s) written.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
