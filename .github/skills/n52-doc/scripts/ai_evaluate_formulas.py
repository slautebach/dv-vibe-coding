"""
North52 Formula AI Evaluator (Step 2)

Evaluates which formulas need AI documentation (README.md and CodeReview.md)
by comparing formula modification timestamps with last AI analysis timestamps.

This script operates in two modes:
1. CHECK mode (default): Reports which formulas need AI analysis
2. GENERATE mode (--generate): Outputs prompts for generating documentation

Usage:
    # Check which formulas need AI analysis
    python ai_evaluate_formulas.py [--all | <entity> <shortcode>]
    
    # Force regeneration (ignore timestamps)
    python ai_evaluate_formulas.py --force [--all | <entity> <shortcode>]
    
    # Generate documentation for a specific formula
    python ai_evaluate_formulas.py --generate <entity> <shortcode>
    
    # Batch check all formulas and show status
    python ai_evaluate_formulas.py --all
    
Examples:
    python ai_evaluate_formulas.py --all                    # Check all formulas
    python ai_evaluate_formulas.py account PWa              # Check specific formula
    python ai_evaluate_formulas.py --force account PWa      # Force regeneration
    python ai_evaluate_formulas.py --generate account PWa   # Generate docs for one formula
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional, Tuple

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from extract_decision_tables import check_formula as check_dt_files


def get_workspace_root(script_path: Path) -> Path:
    """Get workspace root by navigating up from scripts folder."""
    # scripts/ -> n52-doc/ -> skills/ -> .github/ -> workspace root
    return script_path.parent.parent.parent.parent.parent.resolve()


class FormulaEvaluationStatus:
    """Status of a formula's AI documentation."""
    
    UP_TO_DATE = "up_to_date"
    NEEDS_GENERATION = "needs_generation"
    NEEDS_UPDATE = "needs_update"
    MISSING_METADATA = "missing_metadata"
    ERROR = "error"


class FormulaAIEvaluator:
    """Evaluates formulas to determine if AI documentation is needed."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.code_review_root = workspace_root / 'wiki' / 'Technical-Reference' / 'North52'
    
    def find_all_formulas(self) -> List[Tuple[str, str]]:
        """Find all formulas that have metadata in wiki/Technical-Reference/North52/."""
        formulas = []
        
        if not self.code_review_root.exists():
            return formulas
        
        for entity_path in self.code_review_root.iterdir():
            if not entity_path.is_dir():
                continue
            
            entity_name = entity_path.name
            
            for shortcode_path in entity_path.iterdir():
                if not shortcode_path.is_dir():
                    continue
                
                shortcode = shortcode_path.name
                
                # Check if metadata exists
                metadata_file = shortcode_path / 'analysis_metadata.json'
                if metadata_file.exists():
                    formulas.append((entity_name, shortcode))
        
        return formulas
    
    def check_formula_status(self, entity: str, shortcode: str, force: bool = False) -> Dict:
        """
        Check if a formula needs AI documentation.
        
        Returns dict with:
            - status: FormulaEvaluationStatus
            - reason: explanation
            - metadata: loaded metadata (if available)
            - paths: relevant file paths
        """
        formula_path = self.code_review_root / entity / shortcode
        metadata_file = formula_path / 'analysis_metadata.json'
        # Index page is at <entity>/<shortcode>.md; code review is in <entity>/<shortcode>/
        description_file = self.code_review_root / entity / f'{shortcode}.md'
        codereview_file = formula_path / 'code-review.md'
        
        result = {
            'entity': entity,
            'shortcode': shortcode,
            'status': FormulaEvaluationStatus.ERROR,
            'reason': '',
            'metadata': None,
            'paths': {
                'folder': str(formula_path),
                'metadata': str(metadata_file),
                'description': str(description_file),  # <entity>/<shortcode>.md
                'codereview': str(codereview_file)       # <entity>/<shortcode>/code-review.md
            }
        }
        
        # Check if metadata exists
        if not metadata_file.exists():
            result['status'] = FormulaEvaluationStatus.MISSING_METADATA
            result['reason'] = 'analysis_metadata.json not found - run extraction first'
            return result
        
        # Load metadata
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            result['metadata'] = metadata
        except Exception as e:
            result['status'] = FormulaEvaluationStatus.ERROR
            result['reason'] = f'Failed to load metadata: {e}'
            return result
        
        # Extract timestamps
        ai_doc = metadata.get('ai_documentation', {})
        last_formula_modified = ai_doc.get('last_formula_modified')
        description_generated = ai_doc.get('description_generated')
        codereview_generated = ai_doc.get('codereview_generated')
        
        # If force flag is set, always regenerate
        if force:
            result['status'] = FormulaEvaluationStatus.NEEDS_UPDATE
            result['reason'] = 'Force regeneration requested'
            return result
        
        # Check if markdown files exist
        description_exists = description_file.exists()
        codereview_exists = codereview_file.exists()
        
        if not description_exists or not codereview_exists:
            result['status'] = FormulaEvaluationStatus.NEEDS_GENERATION
            missing = []
            if not description_exists:
                missing.append('<shortcode>.md')
            if not codereview_exists:
                missing.append('code-review.md')
            result['reason'] = f'Missing files: {", ".join(missing)}'
            return result

        # Check if decision table sheet files are present (when applicable)
        dt_status = check_dt_files(entity, shortcode)
        if dt_status['has_dt_json'] and dt_status['missing_files']:
            result['status'] = FormulaEvaluationStatus.NEEDS_GENERATION
            result['reason'] = (
                f'Missing decision table files: {", ".join(dt_status["missing_files"])}'
            )
            result['missing_dt_files'] = dt_status['missing_files']
            return result

        # Check if AI has been run before
        if not description_generated or not codereview_generated:
            result['status'] = FormulaEvaluationStatus.NEEDS_UPDATE
            result['reason'] = 'AI documentation timestamps not set'
            return result
        
        # Compare timestamps - if formula was modified after AI analysis, need update
        try:
            # Verify timestamps are valid strings before parsing
            if not last_formula_modified or not isinstance(last_formula_modified, str):
                result['status'] = FormulaEvaluationStatus.NEEDS_UPDATE
                result['reason'] = 'Invalid or missing last_formula_modified timestamp'
                return result
            
            if not isinstance(description_generated, str) or not isinstance(codereview_generated, str):
                result['status'] = FormulaEvaluationStatus.NEEDS_UPDATE
                result['reason'] = 'Invalid AI documentation timestamps'
                return result
            
            formula_time = datetime.fromisoformat(last_formula_modified)
            desc_time = datetime.fromisoformat(description_generated)
            review_time = datetime.fromisoformat(codereview_generated)
            
            # Use the newer of the two AI generation times
            last_ai_time = max(desc_time, review_time)
            
            if formula_time > last_ai_time:
                result['status'] = FormulaEvaluationStatus.NEEDS_UPDATE
                result['reason'] = f'Formula modified {formula_time.isoformat()} after last AI analysis {last_ai_time.isoformat()}'
                return result
        except Exception as e:
            result['status'] = FormulaEvaluationStatus.ERROR
            result['reason'] = f'Failed to parse timestamps: {e}'
            return result
        
        # All checks passed - AI documentation is up to date
        result['status'] = FormulaEvaluationStatus.UP_TO_DATE
        result['reason'] = f'AI analysis up to date (last run: {last_ai_time.isoformat()})'
        return result
    
    def get_formula_info(self, metadata: Dict) -> Dict:
        """Extract key formula information from metadata."""
        formula = metadata.get('formula', {})
        analysis = metadata.get('analysis', {})
        source_files = metadata.get('source_files', {})
        
        return {
            'name': formula.get('name', 'Unknown'),
            'source_entity': formula.get('source_entity', 'Unknown'),
            'formula_type': formula.get('formula_type', 'Unknown'),
            'event': formula.get('event', 'Unknown'),
            'decision_tables': analysis.get('decision_tables', 0),
            'variable_count': analysis.get('variable_count', 0),
            'function_count': analysis.get('function_count', 0),
            'fetch_count': analysis.get('fetch_count', 0),
            'n52f_file': source_files.get('n52f_file', ''),
        }


def print_status_summary(results: List[Dict]):
    """Print summary of formula evaluation results."""
    
    # Group by status
    grouped = {
        FormulaEvaluationStatus.UP_TO_DATE: [],
        FormulaEvaluationStatus.NEEDS_GENERATION: [],
        FormulaEvaluationStatus.NEEDS_UPDATE: [],
        FormulaEvaluationStatus.MISSING_METADATA: [],
        FormulaEvaluationStatus.ERROR: []
    }
    
    for result in results:
        status = result['status']
        grouped[status].append(result)
    
    print("\n" + "=" * 80)
    print("AI DOCUMENTATION STATUS SUMMARY")
    print("=" * 80)
    
    # Up to date
    if grouped[FormulaEvaluationStatus.UP_TO_DATE]:
        print(f"\n✅ UP TO DATE ({len(grouped[FormulaEvaluationStatus.UP_TO_DATE])} formulas)")
        for r in grouped[FormulaEvaluationStatus.UP_TO_DATE]:
            print(f"   {r['entity']}/{r['shortcode']}")
    
    # Needs generation (first time)
    if grouped[FormulaEvaluationStatus.NEEDS_GENERATION]:
        print(f"\n📝 NEEDS GENERATION ({len(grouped[FormulaEvaluationStatus.NEEDS_GENERATION])} formulas)")
        for r in grouped[FormulaEvaluationStatus.NEEDS_GENERATION]:
            print(f"   {r['entity']}/{r['shortcode']} - {r['reason']}")
    
    # Needs update (formula changed)
    if grouped[FormulaEvaluationStatus.NEEDS_UPDATE]:
        print(f"\n🔄 NEEDS UPDATE ({len(grouped[FormulaEvaluationStatus.NEEDS_UPDATE])} formulas)")
        for r in grouped[FormulaEvaluationStatus.NEEDS_UPDATE]:
            print(f"   {r['entity']}/{r['shortcode']} - {r['reason']}")
    
    # Missing metadata (need extraction first)
    if grouped[FormulaEvaluationStatus.MISSING_METADATA]:
        print(f"\n⚠️  MISSING METADATA ({len(grouped[FormulaEvaluationStatus.MISSING_METADATA])} formulas)")
        for r in grouped[FormulaEvaluationStatus.MISSING_METADATA]:
            print(f"   {r['entity']}/{r['shortcode']} - Run extraction first")
    
    # Errors
    if grouped[FormulaEvaluationStatus.ERROR]:
        print(f"\n❌ ERRORS ({len(grouped[FormulaEvaluationStatus.ERROR])} formulas)")
        for r in grouped[FormulaEvaluationStatus.ERROR]:
            print(f"   {r['entity']}/{r['shortcode']} - {r['reason']}")
    
    print("\n" + "=" * 80)
    print(f"Total formulas: {len(results)}")
    print()


def generate_documentation_for_formula(evaluator: FormulaAIEvaluator, entity: str, shortcode: str):
    """Generate <shortcode>.md and code-review.md for a specific formula."""
    
    print(f"\n{'=' * 80}")
    print(f"GENERATING AI DOCUMENTATION: {entity}/{shortcode}")
    print('=' * 80)
    
    # Check status
    result = evaluator.check_formula_status(entity, shortcode, force=False)
    
    if result['status'] == FormulaEvaluationStatus.MISSING_METADATA:
        print(f"\n❌ Error: {result['reason']}")
        print(f"   Run extraction first: python fetch_north52_from_dataverse.py --shortcode <code> --analyze")
        return False
    
    if result['status'] == FormulaEvaluationStatus.ERROR:
        print(f"\n❌ Error: {result['reason']}")
        return False
    
    metadata = result['metadata']
    formula_info = evaluator.get_formula_info(metadata)
    formula_path = evaluator.code_review_root / entity / shortcode
    n52f_file = formula_path / formula_info['n52f_file']
    
    print(f"\n📋 Formula Info:")
    print(f"   Name: {formula_info['name']}")
    print(f"   Type: {formula_info['formula_type']}")
    print(f"   Event: {formula_info['event']}")
    print(f"   Entity: {formula_info['source_entity']}")
    print(f"   Decision Tables: {formula_info['decision_tables']}")
    print(f"   Variables: {formula_info['variable_count']}")
    print(f"   Functions: {formula_info['function_count']}")
    print(f"   FetchXML Queries: {formula_info['fetch_count']}")
    
    # Check if .n52f file exists
    if not n52f_file.exists():
        print(f"\n❌ Error: Formula file not found: {n52f_file}")
        return False
    
    # Read formula code
    with open(n52f_file, 'r', encoding='utf-8') as f:
        formula_code = f.read()
    
    print(f"\n📄 Files:")
    print(f"   Formula: {n52f_file}")
    print(f"   Metadata: {formula_path / 'analysis_metadata.json'}")
    print(f"   Output: {evaluator.code_review_root / entity / f'{shortcode}.md'}")
    print(f"   Output: {formula_path / 'code-review.md'}")
    
    # This is where AI evaluation would happen
    # For now, output instructions for manual/AI generation
    print(f"\n{'=' * 80}")
    print("📝 READY FOR AI GENERATION")
    print('=' * 80)
    print("\nNext steps:")
    print("1. Use GitHub Copilot or AI to generate <shortcode>.md and code-review.md")
    print("2. Reference the analysis_metadata.json and .n52f file")
    print("3. Follow the SKILL.md guidelines for content structure")
    print("4. After generating, update timestamps with: python update_ai_timestamps.py")
    print()
    print(f"Files to read:")
    print(f"  - {n52f_file}")
    print(f"  - {formula_path / 'analysis_metadata.json'}")
    print()
    print(f"Files to create:")
    print(f"  - {evaluator.code_review_root / entity / f'{shortcode}.md'}")
    print(f"  - {formula_path / 'code-review.md'}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate North52 formulas for AI documentation needs',
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('entity', nargs='?', help='Entity name (or use --all)')
    parser.add_argument('shortcode', nargs='?', help='Formula shortcode')
    parser.add_argument('--all', action='store_true', help='Check all formulas')
    parser.add_argument('--force', action='store_true', help='Force regeneration (ignore timestamps)')
    parser.add_argument('--generate', action='store_true', help='Generate documentation for specified formula')
    parser.add_argument('--list-pending', action='store_true', help='List only formulas that need generation/update')
    
    args = parser.parse_args()
    
    # Determine workspace root using shared resolver
    workspace_root = get_workspace_root(Path(__file__))
    
    evaluator = FormulaAIEvaluator(workspace_root)
    
    # Generate mode - for a specific formula
    if args.generate:
        if not args.entity or not args.shortcode:
            print("Error: --generate requires entity and shortcode")
            print("Example: python ai_evaluate_formulas.py --generate account PWa")
            return 1
        
        success = generate_documentation_for_formula(evaluator, args.entity, args.shortcode)
        return 0 if success else 1
    
    # Check mode - check one or all formulas
    if args.all:
        # Check all formulas
        formulas = evaluator.find_all_formulas()
        
        if not formulas:
            print("No formulas found with metadata in wiki/Technical-Reference/North52/")
            print("\nRun extraction first:")
            print("  python fetch_north52_from_dataverse.py --list")
            print("  python fetch_north52_from_dataverse.py --entity <name> --analyze")
            return 1
        
        print(f"Checking {len(formulas)} formulas...")
        
        results = []
        for entity, shortcode in formulas:
            result = evaluator.check_formula_status(entity, shortcode, args.force)
            results.append(result)
        
        # Show summary
        if args.list_pending:
            # Only show formulas that need work
            pending = [r for r in results if r['status'] in [
                FormulaEvaluationStatus.NEEDS_GENERATION,
                FormulaEvaluationStatus.NEEDS_UPDATE
            ]]
            
            if pending:
                print("\n📋 FORMULAS NEEDING AI DOCUMENTATION:")
                for r in pending:
                    print(f"   {r['entity']}/{r['shortcode']}")
                    print(f"      Reason: {r['reason']}")
                    print()
            else:
                print("\n✅ All formulas have up-to-date AI documentation!")
        else:
            print_status_summary(results)
        
        # Show next steps if there are pending formulas
        needs_work = [r for r in results if r['status'] in [
            FormulaEvaluationStatus.NEEDS_GENERATION,
            FormulaEvaluationStatus.NEEDS_UPDATE
        ]]
        
        if needs_work:
            print("\n📝 Next Steps:")
            print("   Use GitHub Copilot to generate documentation for pending formulas:")
            print(f"   Example: python ai_evaluate_formulas.py --generate {needs_work[0]['entity']} {needs_work[0]['shortcode']}")
    
    elif args.entity and args.shortcode:
        # Check specific formula
        result = evaluator.check_formula_status(args.entity, args.shortcode, args.force)
        
        print(f"\n{'=' * 80}")
        print(f"FORMULA STATUS: {args.entity}/{args.shortcode}")
        print('=' * 80)
        
        status_symbols = {
            FormulaEvaluationStatus.UP_TO_DATE: '✅',
            FormulaEvaluationStatus.NEEDS_GENERATION: '📝',
            FormulaEvaluationStatus.NEEDS_UPDATE: '🔄',
            FormulaEvaluationStatus.MISSING_METADATA: '⚠️',
            FormulaEvaluationStatus.ERROR: '❌'
        }
        
        symbol = status_symbols.get(result['status'], '❓')
        print(f"\nStatus: {symbol} {result['status'].upper().replace('_', ' ')}")
        print(f"Reason: {result['reason']}")
        
        if result['metadata']:
            formula_info = evaluator.get_formula_info(result['metadata'])
            print(f"\nFormula: {formula_info['name']}")
            print(f"Type: {formula_info['formula_type']}")
            print(f"Event: {formula_info['event']}")
        
        print(f"\nPaths:")
        print(f"  Metadata: {result['paths']['metadata']}")
        print(f"  Description: {result['paths']['description']}")
        print(f"  CodeReview: {result['paths']['codereview']}")
        
        if result['status'] in [FormulaEvaluationStatus.NEEDS_GENERATION, FormulaEvaluationStatus.NEEDS_UPDATE]:
            print(f"\n💡 To generate documentation:")
            print(f"   python ai_evaluate_formulas.py --generate {args.entity} {args.shortcode}")
        
        print()
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
