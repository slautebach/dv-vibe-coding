"""
Config Loader for Dataverse Environments

This module loads and validates Dataverse environment configurations from
the centralized config file at .github/config.json

Usage:
    from config_loader import load_dataverse_config, list_environments
    
    # Load dev environment (default)
    config = load_dataverse_config()
    
    # Load specific environment
    config = load_dataverse_config('prod')
    
    # List all available environments
    envs = list_environments()
    print(f"Available: {', '.join(envs)}")
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is missing or invalid"""
    pass


def get_config_file_path() -> Path:
    """
    Get the path to the config.json file
    
    Returns:
        Path to .github/config.json
    """
    # This script is in .github/scripts/
    # Config file is at .github/config.json
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / 'config.json'
    return config_path


def load_config_file() -> Dict:
    """
    Load the entire config.json file
    
    Returns:
        Dictionary containing all configuration
        
    Raises:
        ConfigurationError: If config file is missing or invalid JSON
    """
    config_path = get_config_file_path()
    
    if not config_path.exists():
        raise ConfigurationError(
            f"Configuration file not found: {config_path}\n"
            f"Please create it from the template:\n"
            f"  cp {config_path.parent}/config.example.json {config_path}\n"
            f"Then update it with your environment details."
        )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        raise ConfigurationError(
            f"Invalid JSON in config file {config_path}: {e}"
        )
    except Exception as e:
        raise ConfigurationError(
            f"Error reading config file {config_path}: {e}"
        )


def list_environments() -> List[str]:
    """
    List all available environment names in the config
    
    Returns:
        List of environment names (e.g., ['dev', 'test', 'prod'])
        
    Raises:
        ConfigurationError: If config is invalid
    """
    config = load_config_file()
    
    if 'dataverse_environments' not in config:
        raise ConfigurationError(
            "Config file is missing 'dataverse_environments' section"
        )
    
    environments = config['dataverse_environments']
    if not isinstance(environments, dict):
        raise ConfigurationError(
            "'dataverse_environments' must be a dictionary"
        )
    
    return list(environments.keys())


def load_dataverse_config(environment_name: str = 'dev') -> Dict[str, str]:
    """
    Load Dataverse configuration for a specific environment
    
    Args:
        environment_name: Name of the environment (e.g., 'dev', 'test', 'prod')
                         Defaults to 'dev'
    
    Returns:
        Dictionary with keys: environment_url, tenant_id, app_id (optional), description
        
    Raises:
        ConfigurationError: If environment not found or configuration is invalid
    
    Example:
        config = load_dataverse_config('dev')
        print(f"Connecting to: {config['environment_url']}")
        print(f"Tenant: {config['tenant_id']}")
    """
    config = load_config_file()
    
    # Validate structure
    if 'dataverse_environments' not in config:
        raise ConfigurationError(
            "Config file is missing 'dataverse_environments' section"
        )
    
    environments = config['dataverse_environments']
    
    if environment_name not in environments:
        available = ', '.join(environments.keys())
        raise ConfigurationError(
            f"Environment '{environment_name}' not found in config.\n"
            f"Available environments: {available}"
        )
    
    env_config = environments[environment_name]
    
    # Validate required fields
    required_fields = ['environment_url', 'tenant_id']
    missing_fields = [f for f in required_fields if f not in env_config]
    
    if missing_fields:
        raise ConfigurationError(
            f"Environment '{environment_name}' is missing required fields: "
            f"{', '.join(missing_fields)}"
        )
    
    # Validate environment_url format
    url = env_config['environment_url']
    if not url.startswith('https://'):
        raise ConfigurationError(
            f"Invalid environment_url in '{environment_name}': Must start with https://"
        )
    
    # Return a clean config dict (filter out None values for optional fields)
    result = {
        'environment_url': env_config['environment_url'],
        'tenant_id': env_config['tenant_id'],
        'description': env_config.get('description', ''),
    }
    
    # Only include app_id if it's not None/null
    if env_config.get('app_id'):
        result['app_id'] = env_config['app_id']
    
    logger.info(f"Loaded config for environment: {environment_name}")
    if result.get('description'):
        logger.info(f"  Description: {result['description']}")
    logger.info(f"  URL: {result['environment_url']}")
    
    return result


def get_environment_from_env_var(default: str = 'dev') -> str:
    """
    Get environment name from DATAVERSE_ENVIRONMENT environment variable
    
    Args:
        default: Default environment if env var not set
        
    Returns:
        Environment name
    """
    return os.environ.get('DATAVERSE_ENVIRONMENT', default)


def main():
    """CLI tool to list and validate environments"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Dataverse Configuration Utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all environments
    python config_loader.py --list
    
    # Validate specific environment
    python config_loader.py --validate dev
    
    # Show config for environment
    python config_loader.py --show prod
        """
    )
    
    parser.add_argument('--list', action='store_true',
                       help='List all available environments')
    parser.add_argument('--validate', metavar='ENV',
                       help='Validate configuration for environment')
    parser.add_argument('--show', metavar='ENV',
                       help='Show configuration for environment (excluding secrets)')
    parser.add_argument('--config-path', action='store_true',
                       help='Show path to config file')
    
    args = parser.parse_args()
    
    try:
        if args.config_path:
            print(f"Config file: {get_config_file_path()}")
            return 0
        
        if args.list:
            envs = list_environments()
            print(f"\nAvailable environments ({len(envs)}):")
            for env in envs:
                config = load_dataverse_config(env)
                desc = config.get('description', '(no description)')
                print(f"  {env:10s} - {desc}")
            return 0
        
        if args.validate:
            config = load_dataverse_config(args.validate)
            print(f"\n✓ Environment '{args.validate}' configuration is valid")
            print(f"  URL: {config['environment_url']}")
            print(f"  Tenant: {config['tenant_id']}")
            if config.get('app_id'):
                print(f"  App ID: {config['app_id']}")
            return 0
        
        if args.show:
            config = load_dataverse_config(args.show)
            print(f"\nConfiguration for '{args.show}':")
            print(json.dumps(config, indent=2))
            return 0
        
        # Default: show help
        parser.print_help()
        return 0
        
    except ConfigurationError as e:
        logger.error(str(e))
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
