"""
Fetch North52 Formulas from Dataverse

This script retrieves North52 Decision Suite formulas directly from Dataverse
using the Web API from the north52_formulas entity.

Environment configuration is loaded from the .env file at the repository root.
Secrets are passed via CLI arguments or environment variables.

Usage:
    # Interactive authentication (uses dev environment by default)
    python fetch_north52_from_dataverse.py --list
    
    # Specify environment
    python fetch_north52_from_dataverse.py --environment prod --list
    
    # Service principal authentication
    python fetch_north52_from_dataverse.py --environment prod \\
        --client-secret <secret> --list
    
    # If app_id not in config, pass it via CLI
    python fetch_north52_from_dataverse.py --environment prod \\
        --app-id <app-id> --client-secret <secret> --list
    
    # Fetch specific formula by short code (shortcode is unique, no entity needed)
    python fetch_north52_from_dataverse.py --environment dev \\
        --shortcode ToO --save
    
    # Fetch and analyze all formulas (full extraction to Documentation folder)
    python fetch_north52_from_dataverse.py --environment dev \\
        --all --analyze
    
    # Fetch all formulas, skip ones already extracted
    python fetch_north52_from_dataverse.py --environment dev \\
        --all --analyze --skip-existing
    
    # Fetch and analyze formula (generates .n52 and analysis_metadata.json)
    python fetch_north52_from_dataverse.py --environment dev \\
        --shortcode ToO --analyze
    
    # Fetch all formulas for an entity with full analysis
    python fetch_north52_from_dataverse.py --environment dev \\
        --entity mnp_saidmonthlycalculation --analyze
    
    # Fetch formula by name
    python fetch_north52_from_dataverse.py --environment dev \\
        --name "SAID - Monthly Calculation - Save - Perform Action - Update Data" --save
    
    # List available environments
    python config_loader.py --list
"""

from __future__ import annotations

import argparse
import sys
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING, Any
import logging
import xml.dom.minidom

# Add shared scripts directory to path for config_loader and dataverse_client
_SHARED_SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / 'scripts'
if str(_SHARED_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_SCRIPTS_DIR))

from config_loader import load_dataverse_config, list_environments, ConfigurationError

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Optional dependencies for Dataverse retrieval
# These are only needed when actually fetching from Dataverse
DATAVERSE_AVAILABLE = False
IMPORT_ERROR = ""

# Optional dependencies for formula analysis
# These are only needed when using --analyze flag
ANALYSIS_AVAILABLE = False
ANALYSIS_IMPORT_ERROR = ""

try:
    from analyze_formula import North52FormulaParser
    from metadata_builder import build_metadata_v2
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    ANALYSIS_AVAILABLE = False
    ANALYSIS_IMPORT_ERROR = str(e)

if TYPE_CHECKING:
    from dataverse_sdk_client import DataverseClient
else:
    try:
        from dataverse_sdk_client import DataverseClient
        DATAVERSE_AVAILABLE = True
    except ImportError as e:
        DATAVERSE_AVAILABLE = False
        IMPORT_ERROR = str(e)


class North52DataverseFetcher:
    """Fetch North52 formulas directly from Dataverse"""
    
    # Minimal fields for list operations (excludes large description fields)
    MINIMAL_FIELDS = [
        'north52_formulaid',
        'north52_name',
        'north52_shortcode',
        'north52_sourceentityname',
        'north52_category',
        'north52_formulatype',
        'north52_pipelineevent',
        'north52_pipelinestage',
        'north52_executionorder',
        'statecode'
    ]
    
    # Full fields including large description fields
    FULL_FIELDS = MINIMAL_FIELDS + [
        'north52_formuladescription',
        'north52_shortformuladescription'
    ]
    
    def __init__(self, client: DataverseClient):
        """
        Initialize fetcher with Dataverse client
        
        Args:
            client: Connected DataverseClient instance
        """
        self.client = client
    
    def get_all_north52_formulas(self) -> List[Dict]:
        """
        Retrieve all North52 formulas from Dataverse (minimal fields only for performance)
        
        Returns:
            List of formula records with minimal fields (excludes large description fields)
        """
        logger.info("Fetching all North52 formulas...")
        
        attributes = ''.join([f'<attribute name="{field}"/>' for field in self.MINIMAL_FIELDS])
        fetch_xml = f"""
        <fetch>
            <entity name="north52_formula">
                {attributes}
                <filter type="and">
                    <condition attribute="statecode" operator="eq" value="0" />
                </filter>
                <order attribute="north52_name" />
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formulas', fetch_xml)
        formulas = result.get('value', [])
        
        logger.info(f"Found {len(formulas)} North52 formulas")
        return formulas
    
    def get_north52_formula_by_entity(self, entity_name: str) -> List[Dict]:
        """
        Get all North52 formulas for a specific entity (minimal fields only for performance)
        
        Args:
            entity_name: Logical name of the entity (e.g., 'mnp_invoiceproductrevision')
            
        Returns:
            List of formula records with minimal fields (excludes large description fields)
        """
        logger.info(f"Fetching North52 formulas for entity: {entity_name}")
        
        attributes = ''.join([f'<attribute name="{field}"/>' for field in self.MINIMAL_FIELDS])
        fetch_xml = f"""
        <fetch>
            <entity name="north52_formula">
                {attributes}
                <filter type="and">
                    <condition attribute="north52_sourceentityname" operator="eq" value="{entity_name}" />
                    <condition attribute="statecode" operator="eq" value="0" />
                </filter>
                <order attribute="north52_name" />
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formulas', fetch_xml)
        formulas = result.get('value', [])
        
        logger.info(f"Found {len(formulas)} formulas for entity {entity_name}")
        return formulas
    
    def get_north52_formula_by_shortcode(self, shortcode: str) -> Optional[Dict]:
        """
        Get a specific North52 formula by short code (shortcode is guaranteed unique)
        
        Args:
            shortcode: Formula short code (e.g., 'm35', 'ToO') - case insensitive
            
        Returns:
            Formula record with minimal fields or None if not found
        """
        logger.info(f"Fetching North52 formula by shortcode: {shortcode}")
        
        attributes = ''.join([f'<attribute name="{field}"/>' for field in self.MINIMAL_FIELDS])
        fetch_xml = f"""
        <fetch top="1">
            <entity name="north52_formula">
                {attributes}
                <filter type="and">
                    <condition attribute="north52_shortcode" operator="like" value="{shortcode}" />
                    <condition attribute="statecode" operator="eq" value="0" />
                </filter>
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formulas', fetch_xml)
        formulas = result.get('value', [])
        
        if formulas:
            logger.info(f"Found formula: {formulas[0].get('north52_name')}")
            return formulas[0]
        
        logger.warning(f"Formula not found with shortcode: {shortcode}")
        return None
    
    def get_north52_formula_by_name(self, name: str) -> Optional[Dict]:
        """
        Get a North52 formula by exact name (minimal fields only)
        
        Args:
            name: Formula name (e.g., 'SAID - Monthly Calculation - Save - Perform Action - Update Data')
            
        Returns:
            Formula record with minimal fields or None if not found
        """
        logger.info(f"Fetching formula by name: {name}")
        
        attributes = ''.join([f'<attribute name="{field}"/>' for field in self.MINIMAL_FIELDS])
        fetch_xml = f"""
        <fetch top="1">
            <entity name="north52_formula">
                {attributes}
                <filter type="and">
                    <condition attribute="north52_name" operator="eq" value="{name}" />
                    <condition attribute="statecode" operator="eq" value="0" />
                </filter>
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formulas', fetch_xml)
        formulas = result.get('value', [])
        
        if formulas:
            return formulas[0]
        
        logger.warning(f"Formula not found by name: {name}")
        return None
    
    def get_north52_formula_by_id(self, formula_id: str) -> Optional[Dict]:
        """
        Get a North52 formula by ID with all fields (including large description fields)
        
        Args:
            formula_id: Formula GUID
            
        Returns:
            Complete formula record with all fields or None if not found
        """
        logger.info(f"Fetching full formula details by ID: {formula_id}")
        
        attributes = ''.join([f'<attribute name="{field}"/>' for field in self.FULL_FIELDS])
        fetch_xml = f"""
        <fetch top="1">
            <entity name="north52_formula">
                {attributes}
                <filter type="and">
                    <condition attribute="north52_formulaid" operator="eq" value="{formula_id}" />
                </filter>
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formulas', fetch_xml)
        formulas = result.get('value', [])
        
        if formulas:
            record = formulas[0]
            # Guarantee the primary key is always present in the returned record.
            # Some Dataverse configurations omit the primary-key attribute even
            # when it is explicitly requested in the FetchXML select list.
            if not record.get('north52_formulaid'):
                record['north52_formulaid'] = formula_id
            return record
        
        logger.warning(f"Formula not found by ID: {formula_id}")
        return None
    
    def get_north52_formula_details(self, formula_id: str) -> List[Dict]:
        """
        Get all formula details (fetch queries) for a specific formula
        
        Args:
            formula_id: Formula GUID
            
        Returns:
            List of formula detail records (fetch queries)
        """
        logger.info(f"Fetching formula details (fetch queries) for formula ID: {formula_id}")
        
        fetch_xml = f"""
        <fetch>
            <entity name="north52_formuladetail">
                <attribute name="north52_formuladetailid"/>
                <attribute name="north52_name"/>
                <attribute name="north52_query"/>
                <attribute name="north52_querytype"/>
                <attribute name="north52_filter"/>
                <attribute name="north52_filterxml"/>
                <attribute name="north52_filterentityname"/>
                <attribute name="north52_filterattributename"/>
                <attribute name="north52_queryprimarynameattribute"/>
                <attribute name="north52_savedviewid"/>
                <attribute name="north52_command"/>
                <attribute name="north52_layout"/>
                <attribute name="statecode"/>
                <attribute name="statuscode"/>
                <filter type="and">
                    <condition attribute="north52_formula_north52_formuladetail_id" operator="eq" value="{formula_id}" />
                    <condition attribute="statecode" operator="eq" value="0" />
                </filter>
                <order attribute="north52_name" />
            </entity>
        </fetch>
        """
        
        result = self.client.get_records_with_fetchxml('north52_formuladetails', fetch_xml)
        details = result.get('value', [])
        
        logger.info(f"Found {len(details)} formula detail(s) for formula ID: {formula_id}")
        return details
    
    def save_formula_to_file(self, formula: Dict, output_dir: Path, use_doc_structure: bool = False) -> Path:
        """
        Save a formula to a file (fetches full details if not already loaded)
        
        Args:
            formula: Formula record from Dataverse (may have minimal fields)
            output_dir: Directory to save the formula file
            use_doc_structure: If True, save to .staging/north52/<entity>/<shortcode>/ structure
            
        Returns:
            Path to the saved file
        """
        # Check if we have the formula description, if not fetch full details
        if 'north52_formuladescription' not in formula:
            formula_id = formula.get('north52_formulaid')
            if not formula_id:
                raise ValueError("Formula record must have north52_formulaid")
            logger.info("Formula description not loaded, fetching full details...")
            full_formula = self.get_north52_formula_by_id(formula_id)
            if full_formula:
                formula = full_formula
                # get_north52_formula_by_id already guarantees north52_formulaid is set,
                # but be defensive in case the caller bypassed that method.
                if not formula.get('north52_formulaid'):
                    formula['north52_formulaid'] = formula_id
            else:
                raise ValueError(f"Could not retrieve full formula details for ID: {formula_id}")
        
        # Get the formula metadata
        entity_name = formula.get('north52_sourceentityname', 'unknown')
        shortcode = formula.get('north52_shortcode', 'unknown')
        formula_name = formula.get('north52_name', 'Unknown')
        formula_content = formula.get('north52_formuladescription', '')
        
        if use_doc_structure:
            # Use .staging/north52/<entity>/<shortcode>/ structure
            formula_dir = output_dir / '.staging' / 'north52' / entity_name / shortcode
            formula_dir.mkdir(parents=True, exist_ok=True)
            
            # Create .n52 filename using shortcode
            filename = f"{shortcode}.n52"
            file_path = formula_dir / filename
        else:
            # Use flat structure with entity_shortcode.txt naming
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{entity_name}_{shortcode}.txt"
            file_path = output_dir / filename
        
        # Save to file (content is plain text, not base64 encoded)
        file_path.write_text(formula_content, encoding='utf-8')
        logger.info(f"Saved formula to: {file_path}")
        
        return file_path
    
    def parse_formula_content(self, formula: Dict) -> Dict:
        """
        Parse a formula and extract metadata
        
        Args:
            formula: Formula record from Dataverse
            
        Returns:
            Parsed formula data (metadata and code)
        """
        return {
            'metadata': {
                'entity_name': formula.get('north52_sourceentityname', ''),
                'short_code': formula.get('north52_shortcode', ''),
                'formula_type': formula.get('north52_formulatype', ''),
                'category': formula.get('north52_category', ''),
                'pipeline_event': formula.get('north52_pipelineevent', ''),
                'pipeline_stage': formula.get('north52_pipelinestage', ''),
                'execution_order': formula.get('north52_executionorder', ''),
                'state': formula.get('statecode', ''),
            },
            'formula_code': formula.get('north52_formuladescription', ''),
            'short_formula': formula.get('north52_shortformuladescription', ''),
        }
    
    def analyze_and_save_formula(self, formula: Dict, workspace_root: Path) -> Dict:
        """
        Analyze a formula and save it with complete metadata to Documentation folder.
        
        Saves formula as <shortcode>.n52 for consistency and to handle formula name changes.
        
        Args:
            formula: Formula record from Dataverse (must have full fields)
            workspace_root: Root directory of the workspace
            
        Returns:
            Dict with paths to created files and analysis summary
        """
        if not ANALYSIS_AVAILABLE:
            raise RuntimeError(f"Analysis modules not available: {ANALYSIS_IMPORT_ERROR}")
        
        # Capture the formula ID from the minimal record *before* any replacement so
        # it is never lost even if the full-detail fetch omits the primary key field.
        original_formula_id = formula.get('north52_formulaid')

        # Ensure we have full formula details
        if 'north52_formuladescription' not in formula:
            if not original_formula_id:
                raise ValueError("Formula record must have north52_formulaid")
            logger.info("Formula description not loaded, fetching full details...")
            full_formula = self.get_north52_formula_by_id(original_formula_id)
            if full_formula:
                formula = full_formula
                # Defensive: restore primary key if Dataverse omitted it
                if not formula.get('north52_formulaid'):
                    formula['north52_formulaid'] = original_formula_id
            else:
                raise ValueError(f"Could not retrieve full formula details for ID: {original_formula_id}")

        # Extract formula data
        entity_name = formula.get('north52_sourceentityname', 'unknown')
        shortcode = formula.get('north52_shortcode', 'unknown')
        formula_name = formula.get('north52_name', 'Unknown')
        formula_code = formula.get('north52_formuladescription', '')
        formula_type = formula.get('north52_formulatype', '')
        category = formula.get('north52_category', '')
        event = formula.get('north52_pipelineevent', '')
        stage = formula.get('north52_pipelinestage', '')
        mode = formula.get('north52_executionmode', '')
        
        # Create output directory
        output_dir = workspace_root / '.staging' / 'north52' / entity_name / shortcode
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up old files before creating new ones (handles renamed formulas)
        logger.info(f"Cleaning up old formula files in {output_dir}...")
        cleanup_count = 0
        for pattern in ['*.n52f', '*.n52', 'analysis_metadata.json', '*.fetch.xml']:
            for old_file in output_dir.glob(pattern):
                try:
                    old_file.unlink()
                    cleanup_count += 1
                    logger.debug(f"Deleted old file: {old_file.name}")
                except Exception as e:
                    logger.warning(f"Could not delete {old_file.name}: {e}")
        if cleanup_count > 0:
            logger.info(f"Cleaned up {cleanup_count} old file(s)")
        
        # Save .n52 file using shortcode
        n52f_filename = f"{shortcode}.n52"
        n52f_path = output_dir / n52f_filename
        n52f_path.write_text(formula_code, encoding='utf-8')
        logger.info(f"Saved .n52 file: {n52f_path}")
        
        # Fetch and save formula details (fetch queries)
        formula_id = formula.get('north52_formulaid') or original_formula_id
        formula_details = self.get_north52_formula_details(formula_id)
        
        # Save each fetch query to a separate .fetch.xml file
        fetch_query_files = []
        for detail in formula_details:
            detail_name = detail.get('north52_name', 'Unknown')
            query_xml = detail.get('north52_query', '')
            
            if query_xml:
                # Create a safe filename from the detail name
                safe_name = re.sub(r'[^a-zA-Z0-9_\-\s]', '', detail_name)
                safe_name = re.sub(r'\s+', '_', safe_name)
                fetch_filename = f"{safe_name}.fetch.xml"
                fetch_path = output_dir / fetch_filename
                
                # Pretty-print (auto-indent) the fetch.xml
                try:
                    pretty_xml = xml.dom.minidom.parseString(query_xml).toprettyxml(indent="  ")
                except Exception as e:
                    logger.warning(f"Failed to pretty-print fetch.xml for {detail_name}: {e}")
                    pretty_xml = query_xml
                fetch_path.write_text(pretty_xml, encoding='utf-8')
                logger.info(f"Saved fetch query: {fetch_path}")
                fetch_query_files.append(fetch_filename)
        
        # Analyze formula
        logger.info(f"Analyzing formula: {formula_name}")
        parser = North52FormulaParser(formula_code, formula_name)
        analysis = parser.parse()
        
        # Extract complexity indicators
        complexity_indicators = {
            'has_loops': bool(re.search(r'\b(For|While|ForEach)\s*\(', formula_code, re.IGNORECASE)),
            'max_nesting_level': formula_code.count('If(') // 2,  # Rough estimate
            'uses_client_side': 'client' in mode.lower() if mode else False,
            'uses_server_side': 'server' in mode.lower() if mode else True
        }
        
        # Functions are already in dict format (name: count)
        functions_dict = analysis['functions']
        
        # Extract formula details metadata
        formula_details_metadata = []
        for detail in formula_details:
            detail_meta = {
                'id': detail.get('north52_formuladetailid'),
                'name': detail.get('north52_name'),
                'query_type': detail.get('north52_querytype'),
                'filter': detail.get('north52_filter'),
                'filter_entity_name': detail.get('north52_filterentityname'),
                'filter_attribute_name': detail.get('north52_filterattributename'),
                'query_primary_name_attribute': detail.get('north52_queryprimarynameattribute'),
                'saved_view_id': detail.get('north52_savedviewid'),
                'command': detail.get('north52_command'),
                'layout': detail.get('north52_layout'),
                'state': detail.get('statecode'),
                'status': detail.get('statuscode'),
                'has_query': bool(detail.get('north52_query')),
                'has_filter_xml': bool(detail.get('north52_filterxml'))
            }
            formula_details_metadata.append(detail_meta)
        
        # Build metadata
        metadata = build_metadata_v2(
            formula_name=formula_name,
            entity=entity_name,
            shortcode=shortcode,
            formula_type=formula_type,
            event=event,
            category=category,
            mode=mode,
            stage=stage,
            variables=analysis['variables'],
            functions=functions_dict,
            queries=[],  # No FetchXML queries from Dataverse directly
            complexity_indicators=complexity_indicators,
            formula_path=output_dir,
            n52f_filename=n52f_filename,
            workspace_root=workspace_root,
            source_entity=entity_name,
            decision_tables=len(analysis.get('decision_tables', [])),
            last_formula_modified=datetime.now().isoformat(),
            formula_id=formula_id
        )
        
        # Add formula details to metadata
        metadata['formula_details'] = formula_details_metadata
        metadata['fetch_query_files'] = fetch_query_files
        
        # Save metadata JSON
        metadata_path = output_dir / 'analysis_metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata: {metadata_path}")
        
        return {
            'n52f_file': str(n52f_path),
            'metadata_file': str(metadata_path),
            'formula_name': formula_name,
            'entity': entity_name,
            'shortcode': shortcode,
            'function_count': len(analysis['functions']),
            'variable_count': len(analysis['variables']),
            'formula_details_count': len(formula_details),
            'fetch_query_files': fetch_query_files
        }


def main():
    parser = argparse.ArgumentParser(
        description='Fetch North52 formulas from Dataverse',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Environment configuration
    parser.add_argument('--environment', '-e',
                       default='dev',
                       help='Accepted for backward compatibility; configuration is loaded from .env (default: dev)')
    parser.add_argument('--list-environments', action='store_true',
                       help='List available environments and exit')
    
    # Authentication (secrets only - other settings from config)
    parser.add_argument('--app-id', 
                       help='Application (client) ID (overrides CLIENT_ID in .env if set)')
    parser.add_argument('--client-secret', 
                       help='Client secret for service principal authentication')
    parser.add_argument('--clear-auth', action='store_true',
                       help='Clear cached authentication and force re-login')
    
    # Query options
    parser.add_argument('--list', action='store_true',
                       help='List all North52 formulas')
    parser.add_argument('--all', action='store_true',
                       help='Extract all North52 formulas to the Documentation folder (use with --analyze)')
    parser.add_argument('--entity', 
                       help='Entity logical name to filter formulas')
    parser.add_argument('--shortcode', 
                       help='Formula short code (unique identifier)')
    parser.add_argument('--name', 
                       help='Exact formula name')
    
    # Output options
    parser.add_argument('--output-dir', type=Path,
                       default=Path('./north52_formulas'),
                       help='Output directory for saved formulas (default: ./north52_formulas)')
    parser.add_argument('--workspace-root', type=Path,
                       help='Workspace root directory (default: auto-detect from script location)')
    parser.add_argument('--save', action='store_true',
                       help='Save formulas to files')
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze formulas and generate complete metadata (implies --save)')
    parser.add_argument('--skip-existing', action='store_true',
                       help='Skip formulas that already have analysis_metadata.json (useful for incremental updates)')
    parser.add_argument('--parse', action='store_true',
                       help='Parse and display formula metadata')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    
    args = parser.parse_args()
    
    # Handle --list-environments
    if args.list_environments:
        try:
            envs = list_environments()
            print(f"\nAvailable environments: {', '.join(envs)}")
            print("\nUse --environment <name> to select an environment")
            return 0
        except ConfigurationError as e:
            logger.error(str(e))
            return 1
    
    # Check analysis dependencies if --analyze is used
    if args.analyze and not ANALYSIS_AVAILABLE:
        logger.error("Analysis modules not available!")
        logger.error(f"Import error: {ANALYSIS_IMPORT_ERROR}")
        logger.error("\nThe --analyze flag requires additional dependencies.")
        logger.error("Make sure all North52 analyzer scripts are in the same directory.")
        return 1
    
    # Check if Dataverse dependencies are available
    if not DATAVERSE_AVAILABLE:
        logger.error("Required dependencies not installed!")
        logger.error(f"Import error: {IMPORT_ERROR}")
        logger.error("\nTo use Dataverse retrieval, install the required packages:")
        logger.error("  cd .github/skills/n52-doc/scripts")
        logger.error("  pip install azure-identity requests")
        logger.error("\nOr install from requirements.txt:")
        logger.error("  pip install -r requirements.txt")
        return 1
    
    try:
        # Load environment configuration
        logger.info(f"Loading configuration for environment: {args.environment}")
        try:
            config = load_dataverse_config(args.environment)
        except ConfigurationError as e:
            logger.error(str(e))
            logger.info("\nTip: Use --list-environments to see available environments")
            return 1
        
        environment_url = config['environment_url']
        tenant_id = config['tenant_id']
        
        # app_id priority: CLI arg > config > None (will use interactive auth)
        app_id = args.app_id or config.get('app_id')
        
        # client_secret from CLI arg or environment variable
        client_secret = args.client_secret or os.environ.get('DATAVERSE_CLIENT_SECRET')
        
        # Handle --clear-auth flag
        if args.clear_auth:
            auth_dir = Path.home() / ".dataverse"
            if auth_dir.exists():
                for auth_file in auth_dir.glob("auth_record_*.json"):
                    auth_file.unlink()
                    logger.info(f"Cleared cached authentication: {auth_file}")
                logger.info("Cached authentication cleared. Next run will require browser login.")
            else:
                logger.info("No cached authentication found.")
            return 0
        
        # Connect to Dataverse
        logger.info(f"Connecting to {environment_url}...")
        client = DataverseClient(environment_url)
        client.connect(
            app_id=app_id,
            client_secret=client_secret,
            tenant_id=tenant_id
        )
        
        fetcher = North52DataverseFetcher(client)
        
        # Execute the requested operation
        formulas = []
        
        if args.name:
            formula = fetcher.get_north52_formula_by_name(args.name)
            if formula:
                formulas = [formula]
        elif args.shortcode:
            formula = fetcher.get_north52_formula_by_shortcode(args.shortcode)
            if formula:
                formulas = [formula]
        elif args.entity:
            formulas = fetcher.get_north52_formula_by_entity(args.entity)
        elif args.list and not args.analyze:
            # --list without --analyze: display only, no save
            formulas = fetcher.get_all_north52_formulas()
        elif args.all or args.list:
            # --all (or --list combined with --analyze): fetch all formulas for extraction
            formulas = fetcher.get_all_north52_formulas()
        else:
            # Default: list all
            formulas = fetcher.get_all_north52_formulas()
        
        if not formulas:
            logger.warning("No formulas found")
            return 1
        
        # Determine workspace root
        workspace_root = args.workspace_root
        if workspace_root is None:
            # Auto-detect workspace root (go up from scripts folder)
            script_dir = Path(__file__).resolve().parent
            # scripts/ -> n52-doc/ -> skills/ -> .github/ -> workspace root
            workspace_root = script_dir.parent.parent.parent.parent
        
        workspace_root = Path(workspace_root).resolve()
        logger.info(f"Using workspace root: {workspace_root}")
        
        # --all --analyze: bulk extract with progress tracking
        is_bulk = args.all or (args.list and args.analyze)
        if is_bulk and args.analyze:
            print(f"\nExtracting all {len(formulas)} formula(s) to .staging/north52/ ...")
            print(f"Workspace: {workspace_root}\n")
        
        # Process formulas
        results = []
        errors = []
        skipped = []
        for idx, formula in enumerate(formulas, 1):
            formula_info = {
                'id': formula.get('north52_formulaid'),
                'name': formula.get('north52_name'),
                'shortcode': formula.get('north52_shortcode'),
                'entity': formula.get('north52_sourceentityname'),
                'category': formula.get('north52_category')
            }
            
            if args.analyze:
                # --skip-existing: skip if analysis_metadata.json already exists
                if args.skip_existing:
                    entity = formula.get('north52_sourceentityname', 'unknown')
                    shortcode = formula.get('north52_shortcode', 'unknown')
                    metadata_path = workspace_root / 'Documentation' / 'North52' / entity / shortcode / 'analysis_metadata.json'
                    if metadata_path.exists():
                        if is_bulk:
                            print(f"  [{idx}/{len(formulas)}] ⏭  Skipped (exists): {formula.get('north52_name')}")
                        formula_info['skipped'] = True
                        skipped.append(formula_info)
                        results.append(formula_info)
                        continue
                
                # Full analysis workflow
                try:
                    if is_bulk:
                        print(f"  [{idx}/{len(formulas)}] ⚙  Extracting: {formula.get('north52_name')} ...")
                    analysis_result = fetcher.analyze_and_save_formula(formula, workspace_root)
                    formula_info['analysis'] = analysis_result
                    formula_info['saved_to'] = analysis_result['n52f_file']
                    formula_info['metadata_file'] = analysis_result['metadata_file']
                    if is_bulk:
                        print(f"  [{idx}/{len(formulas)}] ✓  Done: {formula.get('north52_name')}")
                except Exception as e:
                    logger.error(f"Error analyzing formula {formula.get('north52_name')}: {e}", exc_info=True)
                    formula_info['analysis_error'] = str(e)
                    if is_bulk:
                        print(f"  [{idx}/{len(formulas)}] ✗  Failed: {formula.get('north52_name')} — {e}")
                    errors.append(formula_info)
            elif args.parse:
                try:
                    parsed = fetcher.parse_formula_content(formula)
                    formula_info['metadata'] = parsed.get('metadata', {})
                    formula_info['formula_code'] = parsed.get('formula_code', '')
                    formula_info['queries'] = parsed.get('queries', [])
                except Exception as e:
                    logger.error(f"Error parsing formula {formula.get('north52_name')}: {e}")
                    formula_info['error'] = str(e)
            elif args.save:
                try:
                    file_path = fetcher.save_formula_to_file(formula, args.output_dir, use_doc_structure=False)
                    formula_info['saved_to'] = str(file_path)
                except Exception as e:
                    logger.error(f"Error saving formula {formula.get('north52_name')}: {e}")
                    formula_info['save_error'] = str(e)
            
            results.append(formula_info)
        
        # Output results
        if args.json:
            print(json.dumps(results, indent=2))
        elif is_bulk and args.analyze:
            # Bulk extract summary
            succeeded = [r for r in results if r.get('analysis') and not r.get('skipped')]
            print(f"\n{'=' * 60}")
            print("BULK EXTRACTION COMPLETE")
            print('=' * 60)
            print(f"  ✓ Extracted:  {len(succeeded)}")
            if skipped:
                print(f"  ⏭  Skipped:   {len(skipped)}")
            if errors:
                print(f"  ✗ Errors:    {len(errors)}")
                print("\nFailed formulas:")
                for r in errors:
                    print(f"  - {r['name']}: {r.get('analysis_error', 'unknown error')}")
            print(f"\nOutput: {workspace_root / '.staging' / 'north52'}")
            print("\nNext step — generate AI documentation:")
            print("  python ai_evaluate_formulas.py --all --list-pending")
        else:
            print(f"\nFound {len(results)} formula(s):\n")
            for info in results:
                if info.get('skipped'):
                    continue
                print(f"Name: {info['name']}")
                if info.get('shortcode'):
                    print(f"  Short Code: {info['shortcode']}")
                if info.get('entity'):
                    print(f"  Entity: {info['entity']}")
                if info.get('category'):
                    print(f"  Category: {info['category']}")
                if info.get('analysis'):
                    analysis = info['analysis']
                    print(f"  ✓ Analysis complete:")
                    print(f"    - Functions: {analysis.get('function_count', 0)}")
                    print(f"    - Variables: {analysis.get('variable_count', 0)}")
                    print(f"    - Formula Details: {analysis.get('formula_details_count', 0)}")
                    if analysis.get('fetch_query_files'):
                        print(f"    - Fetch Queries: {', '.join(analysis['fetch_query_files'])}")
                    print(f"    - Formula file: {analysis.get('n52f_file', '')}")
                    print(f"    - Metadata: {analysis.get('metadata_file', '')}")
                elif info.get('saved_to'):
                    print(f"  Saved to: {info['saved_to']}")
                if 'metadata' in info:
                    meta = info['metadata']
                    print(f"  Formula Type: {meta.get('formula_type', 'N/A')}")
                    print(f"  Pipeline Event: {meta.get('pipeline_event', 'N/A')}")
                    print(f"  Pipeline Stage: {meta.get('pipeline_stage', 'N/A')}")
                    if meta.get('execution_order'):
                        print(f"  Execution Order: {meta['execution_order']}")
                print()
        
        return 0 if not errors else 1
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
