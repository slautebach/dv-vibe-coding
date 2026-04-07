"""
North52 Formula Complexity Ranker

Scans all analysis_metadata.json files under wiki/Technical-Reference/North52/ and generates
a ranked Markdown report at wiki/Technical-Reference/North52/FormulaComplexityRanking.md.

Formulas are scored using a weighted composite metric so the highest-priority
candidates for AI analysis are surfaced first.

Complexity Score Formula
------------------------
  score = (total_function_calls * 1)
        + (variable_count       * 5)
        + (fetch_count          * 10)
        + (decision_tables      * 8)
        + (max_nesting_level    * 15)
        + (function_count       * 2)

Tiers
-----
  CRITICAL : score >= 500
  HIGH     : 200 <= score < 500
  MEDIUM   : 50  <= score < 200
  LOW      :        score < 50

Usage
-----
    # Generate ranking for all formulas
    python rank_formula_complexity.py

    # Output to a custom file path
    python rank_formula_complexity.py --output path/to/report.md

    # Show top N formulas only
    python rank_formula_complexity.py --top 50

    # Filter by entity
    python rank_formula_complexity.py --entity mnp_benefitassessment

    # Include only formulas that still need AI documentation
    python rank_formula_complexity.py --needs-docs
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def get_workspace_root(script_path: Path) -> Path:
    """Navigate up: scripts/ -> n52-doc/ -> skills/ -> .github/ -> root."""
    return script_path.parent.parent.parent.parent.parent.resolve()


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

WEIGHTS = {
    "total_function_calls": 1,
    "variable_count": 5,
    "fetch_count": 10,
    "decision_tables": 8,
    "max_nesting_level": 15,
    "function_count": 2,
}

TIERS = [
    (500, "🔴 CRITICAL"),
    (200, "🟠 HIGH"),
    (50,  "🟡 MEDIUM"),
    (0,   "🟢 LOW"),
]


def compute_score(analysis: Dict) -> int:
    complexity = analysis.get("complexity_indicators", {})
    return (
        analysis.get("total_function_calls", 0) * WEIGHTS["total_function_calls"]
        + analysis.get("variable_count", 0)       * WEIGHTS["variable_count"]
        + analysis.get("fetch_count", 0)           * WEIGHTS["fetch_count"]
        + analysis.get("decision_tables", 0)       * WEIGHTS["decision_tables"]
        + complexity.get("max_nesting_level", 0)   * WEIGHTS["max_nesting_level"]
        + analysis.get("function_count", 0)        * WEIGHTS["function_count"]
    )


def get_tier(score: int) -> str:
    for threshold, label in TIERS:
        if score >= threshold:
            return label
    return "🟢 LOW"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_all_formulas(north52_root: Path) -> List[Dict]:
    """Load every analysis_metadata.json and return enriched formula records."""
    records = []

    for metadata_file in sorted(north52_root.rglob("analysis_metadata.json")):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"  ⚠️  Skipping {metadata_file}: {e}", file=sys.stderr)
            continue

        formula = metadata.get("formula", {})
        analysis = metadata.get("analysis", {})
        ai_doc = metadata.get("ai_documentation", {})
        complexity = analysis.get("complexity_indicators", {})

        score = compute_score(analysis)
        tier = get_tier(score)

        has_readme = (metadata_file.parent / "README.md").exists()
        has_codereview = (metadata_file.parent / "CodeReview.md").exists()
        ai_done = bool(
            ai_doc.get("description_generated") and ai_doc.get("codereview_generated")
            and has_readme and has_codereview
        )

        records.append({
            "entity": formula.get("source_entity", metadata_file.parent.parent.name),
            "shortcode": formula.get("shortcode", metadata_file.parent.name),
            "name": formula.get("name", "Unknown"),
            "category": formula.get("category", ""),
            "formula_type": formula.get("formula_type", ""),
            # Metrics
            "score": score,
            "tier": tier,
            "total_function_calls": analysis.get("total_function_calls", 0),
            "function_count": analysis.get("function_count", 0),
            "variable_count": analysis.get("variable_count", 0),
            "fetch_count": analysis.get("fetch_count", 0),
            "decision_tables": analysis.get("decision_tables", 0),
            "max_nesting_level": complexity.get("max_nesting_level", 0),
            "has_loops": complexity.get("has_loops", False),
            # AI docs
            "ai_done": ai_done,
            "has_readme": has_readme,
            "has_codereview": has_codereview,
            # Path
            "path": str(metadata_file.parent.relative_to(metadata_file.parent.parent.parent.parent)),
        })

    return records


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def ai_status_icon(record: Dict) -> str:
    if record["ai_done"]:
        return "✅"
    if record["has_readme"] or record["has_codereview"]:
        return "⚠️ partial"
    return "📝 needed"


def generate_report(
    records: List[Dict],
    top: Optional[int],
    entity_filter: Optional[str],
    needs_docs: bool,
) -> str:
    """Build the full Markdown report string."""

    # Apply filters
    filtered = records
    if entity_filter:
        filtered = [r for r in filtered if r["entity"].lower() == entity_filter.lower()]
    if needs_docs:
        filtered = [r for r in filtered if not r["ai_done"]]

    # Sort by score descending
    filtered.sort(key=lambda r: r["score"], reverse=True)

    total = len(filtered)
    shown = filtered[:top] if top else filtered

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# North52 Formula Complexity Ranking")
    lines.append("")
    lines.append(f"> Generated: {now}  ")
    lines.append(f"> Total formulas analysed: **{total}**  ")
    if top and top < total:
        lines.append(f"> Showing top **{top}** by complexity score  ")
    if entity_filter:
        lines.append(f"> Filtered to entity: `{entity_filter}`  ")
    if needs_docs:
        lines.append(f"> Showing only formulas that **need AI documentation**  ")
    lines.append("")

    # --- Scoring methodology note ---
    lines.append("## Scoring Methodology")
    lines.append("")
    lines.append("| Metric | Weight | Rationale |")
    lines.append("|--------|--------|-----------|")
    lines.append("| Total function calls | ×1 | Overall formula size |")
    lines.append("| Variable count | ×5 | State management complexity |")
    lines.append("| FetchXML queries | ×10 | Data retrieval cost and risk |")
    lines.append("| Decision tables | ×8 | Branching logic complexity |")
    lines.append("| Max nesting level | ×15 | Comprehension difficulty |")
    lines.append("| Unique function count | ×2 | Breadth of logic |")
    lines.append("")
    lines.append("**Tiers:** 🔴 CRITICAL (≥500) · 🟠 HIGH (200–499) · 🟡 MEDIUM (50–199) · 🟢 LOW (<50)")
    lines.append("")

    # --- Tier summary ---
    tier_counts: Dict[str, int] = {}
    ai_needed = sum(1 for r in filtered if not r["ai_done"])
    for r in filtered:
        tier_counts[r["tier"]] = tier_counts.get(r["tier"], 0) + 1

    lines.append("## Summary")
    lines.append("")
    lines.append("| Tier | Count |")
    lines.append("|------|-------|")
    for _, label in TIERS:
        count = tier_counts.get(label, 0)
        if count:
            lines.append(f"| {label} | {count} |")
    lines.append("")
    lines.append(f"**Formulas needing AI documentation:** {ai_needed} / {total}")
    lines.append("")

    # --- Ranked table ---
    lines.append("## Ranked Formula List")
    lines.append("")
    lines.append("| Rank | Tier | Score | Formula Name | Entity | Shortcode | Fn Calls | Vars | Fetches | DTs | Nesting | AI Docs |")
    lines.append("|------|------|-------|--------------|--------|-----------|----------|------|---------|-----|---------|---------|")

    for i, r in enumerate(shown, start=1):
        name_truncated = r["name"][:60] + "…" if len(r["name"]) > 60 else r["name"]
        lines.append(
            f"| {i} "
            f"| {r['tier']} "
            f"| {r['score']} "
            f"| {name_truncated} "
            f"| `{r['entity']}` "
            f"| `{r['shortcode']}` "
            f"| {r['total_function_calls']} "
            f"| {r['variable_count']} "
            f"| {r['fetch_count']} "
            f"| {r['decision_tables']} "
            f"| {r['max_nesting_level']} "
            f"| {ai_status_icon(r)} |"
        )

    lines.append("")

    # --- Per-tier detail sections ---
    for _, label in TIERS:
        tier_formulas = [r for r in shown if r["tier"] == label]
        if not tier_formulas:
            continue

        lines.append(f"## {label} Complexity Formulas")
        lines.append("")
        lines.append(f"*{len(tier_formulas)} formulas — recommend analysing these first.*")
        lines.append("")

        for r in tier_formulas:
            lines.append(f"### `{r['entity']}/{r['shortcode']}` — {r['name']}")
            lines.append("")
            lines.append(f"- **Score**: {r['score']}  ")
            lines.append(f"- **Category**: {r['category'] or 'N/A'}  ")
            lines.append(f"- **Function calls**: {r['total_function_calls']} ({r['function_count']} unique functions)  ")
            lines.append(f"- **Variables**: {r['variable_count']}  ")
            lines.append(f"- **FetchXML queries**: {r['fetch_count']}  ")
            lines.append(f"- **Decision tables**: {r['decision_tables']}  ")
            lines.append(f"- **Max nesting level**: {r['max_nesting_level']}  ")
            lines.append(f"- **Has loops**: {'Yes' if r['has_loops'] else 'No'}  ")
            lines.append(f"- **AI docs status**: {ai_status_icon(r)}  ")
            lines.append(f"- **Path**: `{r['path']}`  ")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Generated by `rank_formula_complexity.py` — part of the n52-doc skill.*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Rank North52 formulas by complexity and generate a prioritised report.",
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: wiki/Technical-Reference/North52/FormulaComplexityRanking.md)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        metavar="N",
        help="Show only the top N formulas by score",
    )
    parser.add_argument(
        "--entity",
        default=None,
        help="Filter to a specific entity name",
    )
    parser.add_argument(
        "--needs-docs",
        action="store_true",
        help="Only include formulas that still need AI documentation",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the report to stdout instead of writing a file",
    )

    args = parser.parse_args()

    workspace_root = get_workspace_root(Path(__file__))
    north52_root = workspace_root / "wiki" / "Technical-Reference" / "North52"

    if not north52_root.exists():
        print(f"❌ wiki/Technical-Reference/North52 not found at {north52_root}", file=sys.stderr)
        return 1

    print(f"📂 Scanning {north52_root} …", file=sys.stderr)
    records = load_all_formulas(north52_root)

    if not records:
        print("No formulas found with analysis_metadata.json", file=sys.stderr)
        return 1

    print(f"   Found {len(records)} formulas", file=sys.stderr)

    report = generate_report(
        records,
        top=args.top,
        entity_filter=args.entity,
        needs_docs=args.needs_docs,
    )

    if args.dry_run:
        print(report)
        return 0

    # Resolve output path
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = workspace_root / output_path
    else:
        output_path = north52_root / "FormulaComplexityRanking.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Report written to: {output_path}", file=sys.stderr)
    print(f"   Formulas ranked: {len(records)}", file=sys.stderr)

    # Print tier summary to stderr
    from collections import Counter
    tier_counts = Counter(r["tier"] for r in records)
    for _, label in TIERS:
        if label in tier_counts:
            print(f"   {label}: {tier_counts[label]}", file=sys.stderr)

    ai_needed = sum(1 for r in records if not r["ai_done"])
    print(f"   Need AI docs: {ai_needed}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
