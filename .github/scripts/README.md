# Shared Scripts

This directory contains shared utility scripts and libraries that can be used across multiple GitHub Copilot skills and workflows.

## Available Libraries

### dataverse_client.py

Python client for interacting with Microsoft Dynamics 365 / Dataverse Web API.

**Features:**

- Azure authentication (interactive and service principal)
- Persistent token caching (stored in OS keychain/keyring)
- Automatic token refresh when expired
- CRUD operations on Dataverse records
- FetchXML query support
- Metadata retrieval
- Automatic retry handling for 429 (Too Many Requests) errors

**Usage:**

```python
import sys
from pathlib import Path

# Add shared scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from dataverse_client import DataverseClient
from config_loader import load_dataverse_config

# Load environment config
config = load_dataverse_config('dev')

# Connect interactively
client = DataverseClient(config['environment_url'])
client.connect(tenant_id=config['tenant_id'])

# Get records
accounts = client.get_records("accounts", query="?$select=name&$top=10")
for account in accounts['value']:
    print(account['name'])
```

See [dataverse_client.py](dataverse_client.py) for full API documentation.

### config_loader.py

Configuration loader for Dataverse environments from `.github/config.json`.

**Features:**

- Load environment configurations
- Validate configuration structure
- List available environments
- CLI utility for environment management

**Usage:**

```python
from config_loader import load_dataverse_config, list_environments

# Load specific environment
config = load_dataverse_config('dev')
print(f"Connecting to: {config['environment_url']}")

# List all environments
envs = list_environments()
print(f"Available: {', '.join(envs)}")
```

**CLI Usage:**

```bash
# List all environments
python config_loader.py --list

# Validate environment configuration
python config_loader.py --validate dev

# Show environment configuration
python config_loader.py --show prod
```

## Using These Libraries in Skills

To use these shared libraries in your skill scripts:

1. Add the shared scripts directory to your Python path
2. Import the modules as needed

**Example:**

```python
import sys
from pathlib import Path

# Add shared scripts to path (adjust parent levels based on your location)
_SHARED_SCRIPTS_DIR = Path(__file__).parent.parent / 'scripts'
if str(_SHARED_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_SCRIPTS_DIR))

from dataverse_client import DataverseClient
from config_loader import load_dataverse_config
```

**Path Resolution:**

- From `.github/skills/<skill-name>/scripts/`: Use `Path(__file__).parent.parent.parent / 'scripts'`
- From `.github/skills/<skill-name>/`: Use `Path(__file__).parent.parent / 'scripts'`
- From workspace root: Use `Path('.github/scripts')`

## Dependencies

The Dataverse libraries require:

- `azure-identity` - Azure authentication
- `requests` - HTTP client

Install with:

```bash
pip install azure-identity requests
```

## Configuration

Environment configurations are stored in `.github/config.json`. See `.github/config.example.json` for the template.

## Other Shared Scripts

### convert_xlsx_to_csv.py

Convert Excel files to CSV format.

### extract_documents.py

Extract content from various document formats.

### extract_pdfs_to_markdown.py

Convert PDF files to Markdown format.

## Adding New Shared Libraries

When adding new shared libraries to this directory:

1. Ensure the library has comprehensive documentation
2. Add usage examples in this README
3. Update any skills that could benefit from the shared library
4. Consider backward compatibility
5. Add appropriate error handling
6. Include type hints for better IDE support

## Related Documentation

- [North52 Formula Analyzer - Dataverse Integration](../skills/north52-formula-analyzer/scripts/DATAVERSE_README.md)
- [Config File Template](../config.example.json)
