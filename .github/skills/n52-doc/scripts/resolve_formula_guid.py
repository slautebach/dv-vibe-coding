"""
Resolve North52 Formula GUIDs from Unpacked D365 Solution WebResources

North52 formulas are stored in Dataverse as `north52_formula` records. When a
solution is unpacked, each formula is stored as a WebResource under:

    <Solution>/WebResources/north52_/formula/<entity>/<shortcode>/

Each shortcode folder contains two types of files:
  - f.<guid>.data.xml   — the formula record (DisplayName = formula GUID)
  - fd.<guid>.data.xml  — formula detail/fetch query records

This module scans all solution directories in D365Solution/ to build a map of
    (entity, shortcode) -> north52_formulaid (GUID)

Usage (as a module):
    from resolve_formula_guid import build_formula_guid_map, resolve_guid

    guid_map = build_formula_guid_map(workspace_root)
    guid = resolve_guid(guid_map, 'account', 'cTk')

Usage (standalone — list all resolved GUIDs):
    python resolve_formula_guid.py [--workspace <path>]
    python resolve_formula_guid.py --entity account --shortcode cTk
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple


# Regex patterns for .data.xml parsing
_DISPLAY_NAME_RE = re.compile(r'<DisplayName>([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})</DisplayName>', re.IGNORECASE)
_DESC_FORMULA_RE = re.compile(r'<Description>North52Formula:\s*', re.IGNORECASE)

# GUID map type alias
GuidMap = Dict[Tuple[str, str], str]  # (entity, shortcode) -> guid


def build_formula_guid_map(workspace_root: Path) -> GuidMap:
    """
    Scan all D365 solution WebResources and build a map of
    (entity, shortcode) -> north52_formulaid.

    Searches every solution directory under <workspace_root>/D365Solution/ for:
        WebResources/north52_/formula/<entity>/<shortcode>/f.*.data.xml

    Args:
        workspace_root: Repository root path.

    Returns:
        Dict mapping (entity, shortcode) tuples to formula GUIDs (lowercase).
    """
    guid_map: GuidMap = {}
    d365_root = workspace_root / 'D365Solution'

    if not d365_root.is_dir():
        return guid_map

    for solution_dir in d365_root.iterdir():
        if not solution_dir.is_dir():
            continue

        wr_base = solution_dir / 'WebResources' / 'north52_' / 'formula'
        if not wr_base.is_dir():
            continue

        for entity_dir in wr_base.iterdir():
            if not entity_dir.is_dir():
                continue
            entity = entity_dir.name

            for sc_dir in entity_dir.iterdir():
                if not sc_dir.is_dir():
                    continue
                shortcode = sc_dir.name

                # Skip if already resolved (first solution wins; later ones
                # are likely managed copies of the same record)
                if (entity, shortcode) in guid_map:
                    continue

                guid = _extract_formula_guid(sc_dir)
                if guid:
                    guid_map[(entity, shortcode)] = guid

    return guid_map


def resolve_guid(guid_map: GuidMap, entity: str, shortcode: str) -> Optional[str]:
    """
    Look up the formula GUID for a given entity/shortcode pair.

    Args:
        guid_map: Map built by build_formula_guid_map().
        entity:   Entity logical name (e.g. 'account').
        shortcode: Formula shortcode (e.g. 'cTk').

    Returns:
        GUID string (lowercase) or None if not found.
    """
    return guid_map.get((entity, shortcode))


def _extract_formula_guid(sc_dir: Path) -> Optional[str]:
    """
    Extract the formula GUID from the f.*.data.xml file in a shortcode folder.

    The formula file is distinguished from formula-detail files by:
    - Filename starts with 'f.' (not 'fd.')
    - <Description> contains 'North52Formula:'
    - <DisplayName> contains a valid GUID

    Returns:
        GUID string (lowercase) or None.
    """
    for fname in os.listdir(sc_dir):
        if not fname.endswith('.data.xml'):
            continue
        if fname.startswith('fd.'):
            continue  # formula detail — skip

        file_path = sc_dir / fname
        try:
            content = file_path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue

        # Must be a formula record (not a web resource of another type)
        if not _DESC_FORMULA_RE.search(content):
            continue

        m = _DISPLAY_NAME_RE.search(content)
        if m:
            return m.group(1).lower()

    return None


def get_workspace_root(script_path: Path) -> Path:
    """Navigate up from scripts/ to the workspace root."""
    # scripts/ -> n52-doc/ -> skills/ -> .github/ -> root
    return script_path.parent.parent.parent.parent.parent.resolve()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description='Resolve North52 formula GUIDs from unpacked D365 solution WebResources.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--workspace', help='Path to workspace root (auto-detected if omitted)')
    parser.add_argument('--entity', help='Filter by entity name')
    parser.add_argument('--shortcode', help='Filter by shortcode')
    args = parser.parse_args()

    workspace_root = Path(args.workspace).resolve() if args.workspace else get_workspace_root(Path(__file__).resolve())

    print(f'Workspace: {workspace_root}')
    guid_map = build_formula_guid_map(workspace_root)
    print(f'Found {len(guid_map)} formula GUIDs\n')

    if args.entity and args.shortcode:
        guid = resolve_guid(guid_map, args.entity, args.shortcode)
        if guid:
            print(f'{args.entity}/{args.shortcode} -> {guid}')
        else:
            print(f'{args.entity}/{args.shortcode} -> NOT FOUND')
        return 0 if guid else 1

    # Print all (optionally filtered)
    for (entity, sc), guid in sorted(guid_map.items()):
        if args.entity and entity != args.entity:
            continue
        print(f'{entity}/{sc}: {guid}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
