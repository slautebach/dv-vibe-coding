#!/usr/bin/env python3
"""
Search a Dynamics 365 solution for Power Automate cloud flow JSON files.

Scans unpacked solution folders under **/ for cloud flow JSON files,
extracts key metadata from each, and outputs a summary table. Optionally runs
extract-flow-metadata.py on each discovered flow.

Usage:
    python find-solution-flows.py [solution-name] [options]

Arguments:
    solution-name: Optional name of a specific solution folder to search.
                   If omitted, searches all solution folders under **/.

Options:
    --root <path>     Root path containing **/ (default: current working directory)
    --extract         Run extract-flow-metadata.py on each discovered flow
    --json            Output results as JSON instead of a table
    --filter <text>   Filter flows by name (case-insensitive substring match)
    --solution <name> Filter by solution name (same as positional argument)
    -h, --help        Show this help message

Examples:
    # List all flows across all solutions
    python find-solution-flows.py

    # List flows in a specific solution
    python find-solution-flows.py IncomeAssistancePowerAutomate

    # Search from a different root directory
    python find-solution-flows.py --root C:/dev/myproject

    # Filter flows by name
    python find-solution-flows.py --filter "CreateTask"

    # Extract metadata for all found flows
    python find-solution-flows.py IncomeAssistancePowerAutomate --extract

    # Output as JSON for scripting
    python find-solution-flows.py --json
"""

import json
import sys
import os
import re
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional


def extract_flow_name(file_path: str) -> str:
    """Extract flow name from filename by removing GUID suffix."""
    filename = Path(file_path).stem
    parts = filename.split('-')
    if len(parts) >= 5:
        guid_parts = parts[-5:]
        if (len(guid_parts[0]) == 8 and len(guid_parts[1]) == 4 and
                len(guid_parts[2]) == 4 and len(guid_parts[3]) == 4 and
                len(guid_parts[4]) == 12):
            return '-'.join(parts[:-5])
    return filename


def is_cloud_flow(data: Dict[str, Any]) -> bool:
    """
    Determine if a JSON file is a cloud flow (Power Automate) vs other
    workflow types. Cloud flows have properties.definition.triggers.
    """
    try:
        props = data.get('properties', {})
        definition = props.get('definition', {})
        return isinstance(definition, dict) and 'triggers' in definition
    except Exception:
        return False


def get_trigger_summary(data: Dict[str, Any]) -> str:
    """Extract a short human-readable trigger description."""
    try:
        triggers = data['properties']['definition'].get('triggers', {})
        if not triggers:
            return 'No trigger'

        _name, trigger = next(iter(triggers.items()))
        trigger_type = trigger.get('type', 'Unknown')
        kind = trigger.get('kind', '')

        type_labels = {
            'Recurrence': 'Scheduled',
            'Request': 'HTTP/Manual',
            'manual': 'Manual',
            'OpenApiConnectionWebhook': 'Automated',
            'OpenApiConnection': 'Automated',
            'ApiConnection': 'Automated',
            'ApiConnectionWebhook': 'Automated',
        }
        label = type_labels.get(trigger_type, trigger_type)
        if kind:
            label = f"{label} ({kind})"
        return label
    except Exception:
        return 'Unknown'


def count_top_level_actions(data: Dict[str, Any]) -> int:
    """Count top-level actions (non-recursive) as a quick size indicator."""
    try:
        return len(data['properties']['definition'].get('actions', {}))
    except Exception:
        return 0


def scan_solution_dir(solution_dir: Path) -> List[Dict[str, Any]]:
    """
    Scan a single solution directory for cloud flow JSON files.
    Returns a list of flow info dicts.
    """
    workflows_dir = solution_dir / 'Workflows'
    if not workflows_dir.is_dir():
        return []

    flows = []
    for json_file in sorted(workflows_dir.glob('*.json')):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not is_cloud_flow(data):
                continue

            flow_name = extract_flow_name(str(json_file))
            trigger = get_trigger_summary(data)
            action_count = count_top_level_actions(data)
            file_size_kb = round(json_file.stat().st_size / 1024, 1)

            flows.append({
                'flowName': flow_name,
                'solution': solution_dir.name,
                'trigger': trigger,
                'topLevelActions': action_count,
                'fileSizeKb': file_size_kb,
                'filePath': str(json_file),
            })
        except (json.JSONDecodeError, OSError):
            # Skip unreadable or invalid files silently
            continue

    return flows


def find_flows(root: Path, solution_filter: Optional[str] = None,
               name_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search for cloud flows under <root>/**/.

    Args:
        root: Repository root path.
        solution_filter: If set, only search the named solution folder.
        name_filter: If set, filter results by flow name (case-insensitive).
    """
    d365_dir = root / 'D365Solution'
    if not d365_dir.is_dir():
        print(f"Error: D365Solution directory not found at {d365_dir}", file=sys.stderr)
        sys.exit(1)

    if solution_filter:
        solution_path = d365_dir / solution_filter
        if not solution_path.is_dir():
            print(f"Error: Solution folder not found: {solution_path}", file=sys.stderr)
            sys.exit(1)
        solution_dirs = [solution_path]
    else:
        solution_dirs = sorted([p for p in d365_dir.iterdir() if p.is_dir()])

    all_flows = []
    for sol_dir in solution_dirs:
        all_flows.extend(scan_solution_dir(sol_dir))

    if name_filter:
        name_lower = name_filter.lower()
        all_flows = [f for f in all_flows if name_lower in f['flowName'].lower()]

    return all_flows


def print_table(flows: List[Dict[str, Any]]) -> None:
    """Print flows as a formatted table."""
    if not flows:
        print("No cloud flows found.")
        return

    # Column widths
    col_name = max(len(f['flowName']) for f in flows)
    col_name = max(col_name, 8)
    col_sol = max(len(f['solution']) for f in flows)
    col_sol = max(col_sol, 8)
    col_trig = max(len(f['trigger']) for f in flows)
    col_trig = max(col_trig, 7)

    header = (
        f"{'Flow Name':<{col_name}}  "
        f"{'Solution':<{col_sol}}  "
        f"{'Trigger':<{col_trig}}  "
        f"{'Actions':>7}  "
        f"{'Size(KB)':>8}"
    )
    separator = '-' * len(header)

    print(f"\nFound {len(flows)} cloud flow(s)\n")
    print(header)
    print(separator)
    for f in flows:
        print(
            f"{f['flowName']:<{col_name}}  "
            f"{f['solution']:<{col_sol}}  "
            f"{f['trigger']:<{col_trig}}  "
            f"{f['topLevelActions']:>7}  "
            f"{f['fileSizeKb']:>8}"
        )

    # Group summary by solution
    from collections import Counter
    by_solution = Counter(f['solution'] for f in flows)
    if len(by_solution) > 1:
        print(f"\nBy solution:")
        for sol, count in sorted(by_solution.items()):
            print(f"  {sol}: {count} flow(s)")


def run_extract_metadata(flows: List[Dict[str, Any]], script_dir: Path) -> None:
    """Run extract-flow-metadata.py on each flow."""
    extractor = script_dir / 'extract-flow-metadata.py'
    if not extractor.exists():
        print(f"Warning: extract-flow-metadata.py not found at {extractor}", file=sys.stderr)
        return

    print(f"\nExtracting metadata for {len(flows)} flow(s)...\n")
    success = 0
    failed = 0

    for flow in flows:
        result = subprocess.run(
            [sys.executable, str(extractor), flow['filePath']],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  ✓ {flow['flowName']}")
            success += 1
        else:
            print(f"  ✗ {flow['flowName']}: {result.stderr.strip()}")
            failed += 1

    print(f"\nExtraction complete: {success} succeeded, {failed} failed")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Find Power Automate cloud flows in D365 solution folders.',
        add_help=False,
    )
    parser.add_argument('solution_name', nargs='?', default=None,
                        help='Solution folder name to search (optional)')
    parser.add_argument('--root', default=None,
                        help='Repository root path (default: current directory)')
    parser.add_argument('--solution', default=None,
                        help='Solution folder name to search')
    parser.add_argument('--filter', default=None, dest='name_filter',
                        help='Filter flows by name (case-insensitive)')
    parser.add_argument('--extract', action='store_true',
                        help='Run extract-flow-metadata.py on each found flow')
    parser.add_argument('--json', action='store_true', dest='output_json',
                        help='Output results as JSON')
    parser.add_argument('-h', '--help', action='store_true')

    args = parser.parse_args()

    if args.help:
        print(__doc__)
        sys.exit(0)

    # Resolve root path
    root = Path(args.root).resolve() if args.root else Path.cwd()

    # Solution filter: positional arg takes precedence, then --solution flag
    solution_filter = args.solution_name or args.solution

    flows = find_flows(root, solution_filter=solution_filter, name_filter=args.name_filter)

    if args.output_json:
        print(json.dumps(flows, indent=2, ensure_ascii=False))
    else:
        print_table(flows)

    if args.extract and flows:
        script_dir = Path(__file__).parent
        run_extract_metadata(flows, script_dir)
    elif args.extract and not flows:
        print("No flows found to extract metadata from.")

    sys.exit(0)


if __name__ == '__main__':
    main()
