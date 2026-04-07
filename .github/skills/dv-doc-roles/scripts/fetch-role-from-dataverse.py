#!/usr/bin/env python3
"""
Fetch security role metadata and privileges directly from Dataverse.

This script retrieves role definitions and their associated privileges using a
two-query approach: first fetching role records, then fetching roleprivileges
for each role joined to the privilege table.

Output JSON structure:
  {
    "role": {
      "roleid": "...",
      "name": "...",
      "description": "...",
      "businessunitid": "...",
      "modifiedon": "...",
      "ismanaged": false
    },
    "privileges": [
      {
        "privilegedepthmask": 8,
        "privilege_name": "prvReadContact",
        "privilege_accessright": 1
      }
    ]
  }

Files written to .staging/roles/<RoleName>/:
  <RoleName>.role.json      — merged role metadata + privileges
  <RoleName>.dataverse.json — raw Dataverse records for traceability

Usage examples:
    # List configured environments
    python fetch-role-from-dataverse.py --list-environments

    # Fetch a single role by name
    python fetch-role-from-dataverse.py --environment dev --name "SIS Worker"

    # Fetch a role by GUID
    python fetch-role-from-dataverse.py --environment dev \
        --role-id 5f3a1e2d-4b6c-4e8a-9d0e-1f2a3b4c5d6e

    # Fetch all roles in the current business unit
    python fetch-role-from-dataverse.py --environment dev --all
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
    return cleaned or "Role"


def _v(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


class DataverseRoleFetcher:
    """Fetch security role definitions and privileges from Dataverse."""

    ROLE_COLUMNS = [
        "roleid",
        "name",
        "description",
        "_businessunitid_value",
        "modifiedon",
        "ismanaged",
        "isinherited",
    ]

    def __init__(self, client: DataverseClient):
        self.client = client

    def _build_role_fetchxml(
        self,
        role_id: Optional[str] = None,
        name: Optional[str] = None,
        fetch_all: bool = False,
        top: int = 200,
    ) -> str:
        attributes = "".join(f'<attribute name="{c}" />' for c in self.ROLE_COLUMNS)
        clauses: List[str] = [
            # Exclude roles not attached to a business unit (system-only records)
            '<condition attribute="businessunitid" operator="not-null"/>'
        ]

        if role_id:
            clauses.append(
                f'<condition attribute="roleid" operator="eq" value="{_normalize_guid(role_id)}" />'
            )
        elif name:
            safe = name.replace('"', "&quot;")
            clauses.append(f'<condition attribute="name" operator="eq" value="{safe}" />')

        filter_xml = "<filter type=\"and\">" + "".join(clauses) + "</filter>"

        return f"""
<fetch top="{top}">
  <entity name="role">
    {attributes}
    {filter_xml}
    <order attribute="name" descending="false" />
  </entity>
</fetch>
"""

    def _build_privileges_fetchxml(self, role_id: str, top: int = 2000) -> str:
        safe_id = _normalize_guid(role_id)
        return f"""
<fetch top="{top}">
  <entity name="roleprivileges">
    <attribute name="privilegedepthmask"/>
    <filter>
      <condition attribute="roleid" operator="eq" value="{safe_id}"/>
    </filter>
    <link-entity name="privilege" from="privilegeid" to="privilegeid" alias="p">
      <attribute name="name"/>
      <attribute name="accessright"/>
    </link-entity>
  </entity>
</fetch>
"""

    def query_roles(
        self,
        role_id: Optional[str] = None,
        name: Optional[str] = None,
        fetch_all: bool = False,
    ) -> List[Dict[str, Any]]:
        fetch_xml = self._build_role_fetchxml(
            role_id=role_id,
            name=name,
            fetch_all=fetch_all,
        )
        result = self.client.get_records_with_fetchxml("roles", fetch_xml)
        matches = result.get("value", [])
        if not matches:
            raise ValueError("No matching roles were found.")
        return matches

    def query_privileges(self, role_id: str) -> List[Dict[str, Any]]:
        fetch_xml = self._build_privileges_fetchxml(role_id)
        result = self.client.get_records_with_fetchxml("roleprivileges", fetch_xml)
        raw_privileges = result.get("value", [])

        privileges: List[Dict[str, Any]] = []
        for rec in raw_privileges:
            flat: Dict[str, Any] = {}
            for key, val in rec.items():
                clean_key = re.sub(r"@.*", "", key)
                flat[clean_key] = val
            privileges.append(
                {
                    "privilegedepthmask": flat.get("privilegedepthmask"),
                    "privilege_name": flat.get("p.name"),
                    "privilege_accessright": flat.get("p.accessright"),
                }
            )
        return privileges


def _write_outputs(
    role: Dict[str, Any],
    privileges: List[Dict[str, Any]],
    raw_role: Dict[str, Any],
    raw_privileges: List[Dict[str, Any]],
    output_dir: Optional[Path] = None,
) -> Dict[str, Path]:
    role_name = _sanitize_filename(_v(role.get("name"), "Role"))

    if output_dir is None:
        output_dir = _REPO_ROOT / ".staging" / "roles" / role_name

    output_dir.mkdir(parents=True, exist_ok=True)

    merged = {"role": role, "privileges": privileges}
    role_path = output_dir / f"{role_name}.role.json"
    role_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    raw = {"role": raw_role, "privileges": raw_privileges}
    raw_path = output_dir / f"{role_name}.dataverse.json"
    raw_path.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"role_json": role_path, "raw_json": raw_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch security role metadata and privileges from Dataverse",
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
    lookup.add_argument("--name", help="Role name (exact match)")
    lookup.add_argument("--role-id", help="Role GUID (exact match)")
    lookup.add_argument("--all", action="store_true", help="Fetch all roles in the current business unit")

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output folder override (default: .staging/roles/<RoleName>/)",
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

    if not any([args.name, args.role_id, args.all]):
        print(
            "Error: Provide one lookup option: --name, --role-id, or --all.",
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

        fetcher = DataverseRoleFetcher(client)
        roles = fetcher.query_roles(
            role_id=args.role_id,
            name=args.name,
            fetch_all=args.all,
        )

        processed = 0
        for role in roles:
            role_id = _v(role.get("roleid"))
            raw_privileges: List[Dict[str, Any]] = []
            privileges: List[Dict[str, Any]] = []
            if role_id:
                raw_privileges = fetcher.query_privileges(role_id)
                privileges = raw_privileges  # already normalized in query_privileges

            paths = _write_outputs(role, privileges, role, raw_privileges, args.output_dir)

            print(f"Role fetched: {role.get('name', '<unknown>')}")
            print(f"  ID:         {role.get('roleid', '<unknown>')}")
            print(f"  Modified:   {role.get('modifiedon', '<unknown>')}")
            print(f"  Privileges: {len(privileges)}")
            print(f"  Role JSON:  {paths['role_json']}")
            print(f"  Raw JSON:   {paths['raw_json']}")
            processed += 1

        print(f"\nDone. {processed} role(s) written.")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
