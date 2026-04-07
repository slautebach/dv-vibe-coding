"""
extract_decision_tables.py

Parses the North52 decision table spreadsheet data stored as a JSON comment
at the end of .n52 formula files and generates Markdown table files for each
visible sheet.

Each sheet is saved as `dt_<SheetName>.md` alongside the .n52 file. The
README.md generation step then references these files.

Usage:
    python extract_decision_tables.py <entity> <shortcode>
    python extract_decision_tables.py --all               # Process all formulas
    python extract_decision_tables.py --check <entity> <shortcode>  # Check only

Examples:
    python extract_decision_tables.py mnp_writeoff gDt
    python extract_decision_tables.py --all
    python extract_decision_tables.py --check mnp_benefitlineitem m65
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Workspace root resolution
# ---------------------------------------------------------------------------

def get_workspace_root() -> Path:
    """Navigate up from scripts/ to the repository root."""
    # scripts/ -> n52-doc/ -> skills/ -> .github/ -> root
    return Path(__file__).resolve().parent.parent.parent.parent.parent


WORKSPACE_ROOT = get_workspace_root()
DOCS_BASE = WORKSPACE_ROOT / "wiki" / "Technical-Reference" / "North52"


# ---------------------------------------------------------------------------
# Column type metadata
# ---------------------------------------------------------------------------

# Map North52 column type strings → display badge used in the markdown header
COLUMN_TYPE_DISPLAY = {
    "Condition":       "🔵 Condition",
    "Condition-Or":    "🔵 Condition (OR)",
    "Condition-Or-1":  "🔵 Condition (OR-1)",
    "Condition-Or-2":  "🔵 Condition (OR-2)",
    "Condition-Or-3":  "🔵 Condition (OR-3)",
    "Condition-Or-4":  "🔵 Condition (OR-4)",
    "Action-Command":  "🟢 Action (Server)",
    "Action-Clientside": "🟡 Action (Client)",
    "Action-Calc":     "🟠 Action (Calc)",
    "Calc-Inline":     "🟣 Calc (Inline)",
}

# Column types whose cells are typically long North52 code
ACTION_COL_TYPES = {
    "Action-Command",
    "Action-Clientside",
    "Action-Calc",
    "Calc-Inline",
}

# Sheets that are always hidden utility sheets; skip them unless they have data
UTILITY_SHEET_NAMES = {
    "Global Calculations",
    "Global Actions",
    "Global FetchXml",
    "Global FetchXML",
}

# Truncation length for action cell values inside the markdown table cell
TABLE_CELL_MAX = 120


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------

def extract_dt_json(n52_content: str) -> Optional[dict]:
    """
    Extract and parse the North52 decision table JSON comment from the end of
    an .n52 file.

    The comment format is:
        /*{ "version": "...", "sheets": { ... } }*/

    Returns the parsed dict, or None if no valid JSON comment is found.
    """
    # The comment always starts with /*{ and ends with }*/
    # Use a non-greedy match but the JSON is always at the very end of the file
    match = re.search(r'/\*(\{"version".*?\})\s*\*/', n52_content, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        print(f"  ⚠️  Failed to parse decision table JSON: {exc}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Convert a sheet name into a safe filename component."""
    # Replace spaces and special chars with underscores
    safe = re.sub(r"[^\w\-]", "_", name.strip())
    # Collapse multiple underscores
    safe = re.sub(r"_+", "_", safe).strip("_")
    return safe


def escape_md_cell(value: str) -> str:
    """
    Escape characters that break Markdown table cells.
    Newlines become <br>, pipes get backslash-escaped.
    """
    if not value:
        return ""
    value = str(value)
    value = value.replace("|", "\\|")
    value = value.replace("\n", "<br>")
    value = value.replace("\r", "")
    return value


def truncate(value: str, max_len: int) -> str:
    """Truncate a string and append '…' if it exceeds max_len."""
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip() + "…"


# ---------------------------------------------------------------------------
# Sheet rendering
# ---------------------------------------------------------------------------

def _get_cell_value(data_table: dict, row: int, col: int) -> str:
    """Safely retrieve a cell value from the sparse data table dict."""
    cell = data_table.get(str(row), {}).get(str(col), {})
    if not cell:
        return ""
    return str(cell.get("value", "") or "")


def _all_columns(data_table: dict) -> list[int]:
    """Return sorted list of all column indices that appear in the data."""
    cols: set[int] = set()
    for row_data in data_table.values():
        for col_key in row_data.keys():
            cols.add(int(col_key))
    return sorted(cols)


def render_decision_sheet(sheet_name: str, data_table: dict, row_indices: list[int]) -> str:
    """
    Render a decision sheet (rows 0-2 are header/field-ref rows, 3+ are rules).

    Returns a Markdown string.
    """
    all_cols = _all_columns(data_table)
    if not all_cols:
        return ""

    lines: list[str] = []
    lines.append(f"## Sheet: {sheet_name}\n")

    # ------------------------------------------------------------------
    # Build header info per column from rows 0, 1, 2
    # ------------------------------------------------------------------
    col_types:  list[str] = []
    col_labels: list[str] = []
    col_fields: list[str] = []

    for c in all_cols:
        col_types.append(_get_cell_value(data_table, row_indices[0], c))
        col_labels.append(_get_cell_value(data_table, row_indices[1], c))
        col_fields.append(_get_cell_value(data_table, row_indices[2], c))

    # ------------------------------------------------------------------
    # Build the Markdown table
    # ------------------------------------------------------------------
    # Header row: "Label (type badge)" with field ref on a second line
    header_cells: list[str] = []
    for label, col_type, field in zip(col_labels, col_types, col_fields):
        badge = COLUMN_TYPE_DISPLAY.get(col_type, col_type)
        # Format:  Label<br>*type*<br>`field_ref`
        parts: list[str] = []
        parts.append(escape_md_cell(label.strip()) if label.strip() else "*(unlabelled)*")
        parts.append(f"*{escape_md_cell(badge)}*")
        if field.strip() and field.strip() != "==":
            parts.append(f"`{escape_md_cell(field.strip())}`")
        header_cells.append("<br>".join(parts))

    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(["---"] * len(all_cols)) + " |")

    # ------------------------------------------------------------------
    # Data rows (row index ≥ 3, or index of the first data row)
    # ------------------------------------------------------------------
    data_row_indices = row_indices[3:]  # rows after the 3-row header block
    overflow_notes: list[tuple[int, int, str]] = []  # (data_row_num, col_idx, full_value)

    for rule_num, row_idx in enumerate(data_row_indices, start=1):
        row_data = data_table.get(str(row_idx), {})
        cells: list[str] = []
        for c_pos, c in enumerate(all_cols):
            raw = str(row_data.get(str(c), {}).get("value", "") or "")
            col_type = col_types[c_pos]
            escaped = escape_md_cell(raw)

            if col_type in ACTION_COL_TYPES and len(raw) > TABLE_CELL_MAX:
                # Show truncated preview + footnote reference
                preview = escape_md_cell(truncate(raw, TABLE_CELL_MAX))
                overflow_notes.append((rule_num, c_pos, raw))
                cells.append(f"{preview} *(see note {len(overflow_notes)})*")
            else:
                cells.append(escaped if escaped else "")

        lines.append("| " + " | ".join(cells) + " |")

    # ------------------------------------------------------------------
    # Overflow notes: full action code in collapsed <details> blocks
    # ------------------------------------------------------------------
    if overflow_notes:
        lines.append("")
        lines.append("### Full Action Values\n")
        for note_num, (rule_num, col_pos, full_value) in enumerate(overflow_notes, start=1):
            label = col_labels[col_pos].strip() or f"Column {col_pos}"
            lines.append(f"<details>")
            lines.append(f"<summary>Note {note_num} — Row {rule_num}, {escape_md_cell(label)}</summary>\n")
            lines.append("```")
            lines.append(full_value)
            lines.append("```")
            lines.append("</details>\n")

    return "\n".join(lines)


def render_global_sheet(sheet_name: str, data_table: dict, row_indices: list[int]) -> str:
    """
    Render a utility sheet (Global Calculations / Global Actions / Global FetchXml).

    Row 0 is a header row; rows 1+ are data.
    Returns a Markdown string, or empty string if the sheet has no data rows.
    """
    all_cols = _all_columns(data_table)
    if not all_cols:
        return ""

    data_rows = [r for r in row_indices if r > 0]
    if not data_rows:
        return ""

    lines: list[str] = []
    lines.append(f"## Sheet: {sheet_name}\n")

    # Header from row 0
    header = [escape_md_cell(_get_cell_value(data_table, 0, c) or f"Col {c}") for c in all_cols]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(all_cols)) + " |")

    overflow_notes: list[tuple[int, int, str]] = []

    for row_num, r in enumerate(data_rows, start=1):
        row_data = data_table.get(str(r), {})
        cells = []
        for c_pos, c in enumerate(all_cols):
            raw = str(row_data.get(str(c), {}).get("value", "") or "")
            escaped = escape_md_cell(raw)
            if len(raw) > TABLE_CELL_MAX:
                preview = escape_md_cell(truncate(raw, TABLE_CELL_MAX))
                overflow_notes.append((row_num, c_pos, raw))
                cells.append(f"{preview} *(see note {len(overflow_notes)})*")
            else:
                cells.append(escaped)
        lines.append("| " + " | ".join(cells) + " |")

    if overflow_notes:
        lines.append("")
        lines.append("### Full Values\n")
        for note_num, (row_num, col_pos, full_value) in enumerate(overflow_notes, start=1):
            col_header = header[col_pos] if col_pos < len(header) else f"Column {col_pos}"
            lines.append(f"<details>")
            lines.append(f"<summary>Note {note_num} — Row {row_num}, {col_header}</summary>\n")
            lines.append("```")
            lines.append(full_value)
            lines.append("```")
            lines.append("</details>\n")

    return "\n".join(lines)


def render_sheet(sheet_name: str, sheet: dict) -> Optional[str]:
    """
    Determine the sheet type and dispatch to the correct renderer.

    Returns a Markdown string, or None if the sheet has no renderable content.
    """
    data_table: dict = sheet.get("data", {}).get("dataTable", {})
    if not data_table:
        return None

    row_indices = sorted(int(k) for k in data_table.keys())
    if not row_indices:
        return None

    # Detect sheet type by the value in cell (row=0, col=0)
    first_cell = _get_cell_value(data_table, row_indices[0], 0)
    is_decision_sheet = first_cell in COLUMN_TYPE_DISPLAY or first_cell in (
        "Condition", "Action-Command", "Action-Clientside", "Calc-Inline",
        "Action-Calc",
    )

    if is_decision_sheet and len(row_indices) >= 3:
        return render_decision_sheet(sheet_name, data_table, row_indices)
    elif not is_decision_sheet and len(row_indices) >= 2:
        # Global sheet — only render if it has actual data rows
        data_rows = [r for r in row_indices if r > 0]
        if data_rows:
            return render_global_sheet(sheet_name, data_table, row_indices)
    return None


# ---------------------------------------------------------------------------
# Per-formula orchestration
# ---------------------------------------------------------------------------

def extract_tables_for_formula(entity: str, shortcode: str) -> list[Path]:
    """
    Read the .n52 file for the given formula, extract the decision table JSON,
    and write one `dt_<SheetName>.md` file per renderable sheet.

    Returns the list of .md files written.
    """
    formula_path = DOCS_BASE / entity / shortcode
    n52_file = formula_path / f"{shortcode}.n52"

    if not n52_file.exists():
        print(f"  ❌ .n52 file not found: {n52_file}", file=sys.stderr)
        return []

    content = n52_file.read_text(encoding="utf-8")
    dt_json = extract_dt_json(content)

    if dt_json is None:
        # No decision table JSON in this file
        return []

    sheets: dict = dt_json.get("sheets", {})
    if not sheets:
        return []

    written: list[Path] = []
    index_entries: list[tuple[str, str]] = []  # (sheet_name, filename)

    for sheet_name, sheet_data in sheets.items():
        # Skip hidden utility sheets that have no data rows
        is_utility = sheet_name.strip() in UTILITY_SHEET_NAMES
        visible = sheet_data.get("visible", True)

        # For utility sheets that are explicitly hidden and have no real data, skip
        data_table = sheet_data.get("data", {}).get("dataTable", {})
        data_rows = [int(k) for k in data_table.keys() if int(k) >= 1]
        if not data_rows:
            continue

        md_content = render_sheet(sheet_name, sheet_data)
        if not md_content:
            continue

        # Build the output file path
        safe_name = sanitize_filename(sheet_name)
        out_file = formula_path / f"dt_{safe_name}.md"

        # Prepend a document header
        doc_header = (
            f"# Decision Table: {sheet_name}\n\n"
            f"> **Formula:** {shortcode} · **Entity:** {entity}\n\n"
        )
        out_file.write_text(doc_header + md_content + "\n", encoding="utf-8")
        written.append(out_file)
        index_entries.append((sheet_name, out_file.name))
        print(f"  ✓ Written: {out_file.name}")

    if written:
        _write_index(formula_path, entity, shortcode, index_entries)

    return written


def _write_index(formula_path: Path, entity: str, shortcode: str,
                 entries: list[tuple[str, str]]) -> None:
    """
    Write (or overwrite) `dt_index.md` — a summary listing all decision table
    sheet files for this formula. README.md can include a single link to this.
    """
    index_file = formula_path / "dt_index.md"
    lines = [
        f"# Decision Tables: {shortcode}\n",
        f"> **Entity:** {entity}\n",
        "",
        "This formula contains the following decision table sheets:\n",
        "| Sheet | File |",
        "|-------|------|",
    ]
    for sheet_name, filename in entries:
        lines.append(f"| {sheet_name} | [{filename}]({filename}) |")

    lines.append("")
    index_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  ✓ Written: {index_file.name}")


# ---------------------------------------------------------------------------
# Status check (no file writes)
# ---------------------------------------------------------------------------

def check_formula(entity: str, shortcode: str) -> dict:
    """
    Check whether a formula has decision table data and whether dt_ files exist.

    Returns a status dict:
        has_dt_json:    bool — .n52 file contains decision table JSON
        sheet_names:    list[str] — sheet names found in JSON (visible sheets)
        existing_files: list[str] — existing dt_*.md files
        missing_files:  list[str] — sheets without a corresponding dt_ file
    """
    formula_path = DOCS_BASE / entity / shortcode
    n52_file = formula_path / f"{shortcode}.n52"
    result = {
        "has_dt_json": False,
        "sheet_names": [],
        "existing_files": [],
        "missing_files": [],
    }

    if not n52_file.exists():
        return result

    content = n52_file.read_text(encoding="utf-8")
    dt_json = extract_dt_json(content)
    if dt_json is None:
        return result

    result["has_dt_json"] = True
    sheets = dt_json.get("sheets", {})

    for sheet_name, sheet_data in sheets.items():
        data_table = sheet_data.get("data", {}).get("dataTable", {})
        data_rows = [int(k) for k in data_table.keys() if int(k) >= 1]
        if not data_rows:
            continue
        # Only report renderable sheets
        md_content = render_sheet(sheet_name, sheet_data)
        if not md_content:
            continue

        safe_name = sanitize_filename(sheet_name)
        expected_file = formula_path / f"dt_{safe_name}.md"
        result["sheet_names"].append(sheet_name)
        if expected_file.exists():
            result["existing_files"].append(expected_file.name)
        else:
            result["missing_files"].append(expected_file.name)

    return result


# ---------------------------------------------------------------------------
# Batch processing
# ---------------------------------------------------------------------------

def process_all(force: bool = False) -> None:
    """Extract decision tables for all formulas in wiki/Technical-Reference/North52/."""
    if not DOCS_BASE.exists():
        print(f"❌ wiki/Technical-Reference/North52/ not found at {DOCS_BASE}")
        return

    total = 0
    updated = 0
    skipped = 0
    no_dt = 0

    for entity_path in sorted(DOCS_BASE.iterdir()):
        if not entity_path.is_dir():
            continue
        for sc_path in sorted(entity_path.iterdir()):
            if not sc_path.is_dir():
                continue
            entity = entity_path.name
            shortcode = sc_path.name
            total += 1

            status = check_formula(entity, shortcode)
            if not status["has_dt_json"]:
                no_dt += 1
                continue

            if not force and not status["missing_files"]:
                skipped += 1
                continue

            print(f"\n{entity}/{shortcode}")
            files = extract_tables_for_formula(entity, shortcode)
            if files:
                updated += 1
            else:
                no_dt += 1

    print(f"\n{'=' * 60}")
    print(f"Total formulas scanned : {total}")
    print(f"Decision tables found  : {total - no_dt}")
    print(f"Updated (files written): {updated}")
    print(f"Skipped (up to date)   : {skipped}")
    print(f"No DT data             : {no_dt}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract North52 decision table sheets to Markdown files",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("entity", nargs="?", help="Entity name")
    parser.add_argument("shortcode", nargs="?", help="Formula shortcode")
    parser.add_argument("--all", action="store_true", help="Process all formulas")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing dt_ files")
    parser.add_argument("--check", action="store_true",
                        help="Report status without writing files")

    args = parser.parse_args()

    if args.all:
        process_all(force=args.force)
        return 0

    if not args.entity or not args.shortcode:
        parser.print_help()
        return 1

    entity = args.entity
    shortcode = args.shortcode

    if args.check:
        status = check_formula(entity, shortcode)
        print(f"\n{'=' * 60}")
        print(f"DECISION TABLE STATUS: {entity}/{shortcode}")
        print("=" * 60)
        if not status["has_dt_json"]:
            print("  ℹ️  No decision table JSON found in .n52 file")
        else:
            print(f"  ✅ Decision table JSON found")
            print(f"  Sheets: {', '.join(status['sheet_names']) or '(none renderable)'}")
            if status["existing_files"]:
                print(f"  Existing dt_ files: {', '.join(status['existing_files'])}")
            if status["missing_files"]:
                print(f"  Missing dt_ files:  {', '.join(status['missing_files'])}")
            else:
                print("  ✅ All dt_ files are present")
        print()
        return 0

    # Default: extract
    formula_path = DOCS_BASE / entity / shortcode
    if not formula_path.exists():
        print(f"❌ Formula folder not found: {formula_path}")
        return 1

    # Check if already up to date
    if not args.force:
        status = check_formula(entity, shortcode)
        if status["has_dt_json"] and not status["missing_files"] and status["sheet_names"]:
            print(f"✅ {entity}/{shortcode} — decision table files already exist "
                  f"({len(status['existing_files'])} files). Use --force to regenerate.")
            return 0

    print(f"\nExtracting decision tables: {entity}/{shortcode}")
    written = extract_tables_for_formula(entity, shortcode)
    if not written:
        print("  ℹ️  No decision table data found or nothing to write.")
    else:
        print(f"\n✅ Written {len(written)} file(s) to "
              f"wiki/Technical-Reference/North52/{entity}/{shortcode}/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
