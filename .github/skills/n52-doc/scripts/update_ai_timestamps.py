"""
Update AI Documentation Timestamps

Updates the ai_documentation section in analysis_metadata.json after
README.md and CodeReview.md have been generated.

Usage:
    python update_ai_timestamps.py <entity> <shortcode>
    python update_ai_timestamps.py --all  # Update all that have markdown files

Examples:
    python update_ai_timestamps.py account PWa
    python update_ai_timestamps.py --all
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from extract_decision_tables import check_formula as check_dt_files
from resolve_formula_guid import build_formula_guid_map, resolve_guid


def update_timestamps(workspace_root: Path, entity: str, shortcode: str,
                      verbose: bool = True,
                      guid_map: Optional[dict] = None) -> bool:
    """Update AI documentation timestamps for a formula.
    
    Also backfills formula.formula_id in analysis_metadata.json when it is
    null and a GUID can be resolved from the D365 solution WebResources.
    
    Args:
        workspace_root: Repository root path.
        entity:         Entity logical name (e.g. 'account').
        shortcode:      Formula shortcode (e.g. 'cTk').
        verbose:        Print progress messages.
        guid_map:       Pre-built GUID map from resolve_formula_guid. If None,
                        the map is built on-demand (slow for single calls;
                        pass the map explicitly for batch operations).
    """
    
    formula_path = workspace_root / 'wiki' / 'Technical-Reference' / 'North52' / entity / shortcode
    metadata_file = formula_path / 'analysis_metadata.json'
    description_file = formula_path.parent / f'{shortcode}.md'  # index page at entity level
    codereview_file = formula_path / 'code-review.md'
    
    if verbose:
        print(f"Updating: {entity}/{shortcode}")
    
    # Check if metadata exists
    if not metadata_file.exists():
        if verbose:
            print(f"  ❌ Metadata not found: {metadata_file}")
        return False
    
    # Load metadata
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    except Exception as e:
        if verbose:
            print(f"  ❌ Failed to load metadata: {e}")
        return False
    
    # Check which files exist and update timestamps
    now = datetime.now().isoformat()
    ai_doc = metadata.get('ai_documentation', {})
    updated = False

    # ── Backfill formula_id if missing ──────────────────────────────────────
    current_id = metadata.get('formula', {}).get('formula_id')
    if not current_id:
        if guid_map is None:
            guid_map = build_formula_guid_map(workspace_root)
        resolved = resolve_guid(guid_map, entity, shortcode)
        if resolved:
            metadata.setdefault('formula', {})['formula_id'] = resolved
            updated = True
            if verbose:
                print(f"  ✓ formula_id backfilled: {resolved}")
        elif verbose:
            print(f"  ⚠️  formula_id not found in WebResources (formula may not be exported)")
    # ────────────────────────────────────────────────────────────────────────
    
    if description_file.exists():
        ai_doc['description_generated'] = now
        updated = True
        if verbose:
            print(f"  ✓ README.md timestamp updated")
    
    if codereview_file.exists():
        ai_doc['codereview_generated'] = now
        updated = True
        if verbose:
            print(f"  ✓ CodeReview.md timestamp updated")

    # Check for decision table sheet files
    dt_status = check_dt_files(entity, shortcode)
    if dt_status['has_dt_json'] and dt_status['existing_files']:
        ai_doc['decision_tables_generated'] = now
        updated = True
        if verbose:
            print(f"  ✓ decision_tables_generated timestamp updated "
                  f"({len(dt_status['existing_files'])} dt_ files found)")

    if not updated:
        if verbose:
            print(f"  ⚠️  No markdown files found to update timestamps for")
        return False
    
    # Update metadata
    metadata['ai_documentation'] = ai_doc
    
    # Save metadata
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        if verbose:
            print(f"  ✓ Metadata updated: {metadata_file}")
        return True
    except Exception as e:
        if verbose:
            print(f"  ❌ Failed to save metadata: {e}")
        return False


def update_all_timestamps(workspace_root: Path):
    """Update timestamps for all formulas that have markdown files."""
    
    code_review_root = workspace_root / 'wiki' / 'Technical-Reference' / 'North52'
    
    if not code_review_root.exists():
        print("❌ wiki/Technical-Reference/North52/ folder not found")
        return
    
    print("=" * 80)
    print("UPDATING AI DOCUMENTATION TIMESTAMPS & FORMULA IDs")
    print("=" * 80)
    print()

    # Build GUID map once for all formulas (avoids re-scanning D365Solution/ per formula)
    print("Building formula GUID map from D365 solution WebResources...")
    guid_map = build_formula_guid_map(workspace_root)
    print(f"  Found {len(guid_map)} formula GUIDs in WebResources\n")
    
    updated_count = 0
    skipped_count = 0
    
    for entity_path in code_review_root.iterdir():
        if not entity_path.is_dir():
            continue
        
        entity_name = entity_path.name
        
        for shortcode_path in entity_path.iterdir():
            if not shortcode_path.is_dir():
                continue
            
            shortcode = shortcode_path.name
            
            # Update timestamps, passing the pre-built guid_map
            if update_timestamps(workspace_root, entity_name, shortcode,
                                 verbose=True, guid_map=guid_map):
                updated_count += 1
                print()
            else:
                skipped_count += 1
    
    print("=" * 80)
    print(f"✅ Updated: {updated_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print("=" * 80)


def main():
    # Determine workspace root
    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent.parent.parent.parent
    
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    if sys.argv[1] == '--all':
        update_all_timestamps(workspace_root)
    elif len(sys.argv) >= 3:
        entity = sys.argv[1]
        shortcode = sys.argv[2]
        success = update_timestamps(workspace_root, entity, shortcode,
                                    verbose=True, guid_map=None)
        return 0 if success else 1
    else:
        print(__doc__)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
