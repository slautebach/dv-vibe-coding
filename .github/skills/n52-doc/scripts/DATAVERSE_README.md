# Dataverse Integration for North52 Formula Analyzer

This document describes how to use the Dataverse Web API integration to fetch North52 formulas directly from your Dynamics 365 environment.

## Overview

The Dataverse integration provides an **alternative data source** for the North52 Formula Analyzer. Instead of analyzing formulas from exported solution files, you can now fetch them directly from a live Dataverse environment.

## Why Use Dataverse Retrieval?

**Benefits:**

- ✅ Get the latest formulas without exporting solutions
- ✅ Verify what's currently deployed in an environment
- ✅ Fetch specific formulas on-demand
- ✅ No need to wait for solution exports
- ✅ Compare formulas across environments

**When to Use:**

- You want real-time access to formulas
- You need to verify deployed versions
- You're documenting production formulas
- You want to validate changes before deployment

**When NOT to Use:**

- You're analyzing version-controlled code (use solution files)
- You need offline access
- You're doing bulk historical analysis
- You don't have API access to the environment

## Setup

### 1. Install Dependencies

The Dataverse integration requires two Python packages:

```bash
cd .github/skills/n52-doc/scripts
pip install azure-identity requests
```

**Note:** These dependencies are **optional**. The core formula analysis scripts still work without them using only the Python standard library.

### 2. Configure Environment

Create your `.env` file from the template:

```bash
cp .env.example .env
```

Edit `.env` to add your environment details:

```ini
DATAVERSE_URL=https://dev-org.crm3.dynamics.com
TENANT_ID=fbef0798-20e3-4be7-bdc8-372032610f65
ENVIRONMENT_NAME=dev
ENVIRONMENT_DESCRIPTION=Development environment
MAKE_ENVIRONMENT_ID=your-make-environment-id
MAKE_SOLUTION_ID=your-make-solution-id
NORTH52_APP_ID=your-north52-app-id
```

**Saskatchewan Government Default Tenant:** `fbef0798-20e3-4be7-bdc8-372032610f65`

**Validate Configuration:**

```bash
cd .github/skills/n52-doc/scripts
python config_loader.py --validate
```

### 3. Authentication Setup

You have three authentication options:

#### Option A: Interactive Browser Authentication (Recommended for Development)

No additional setup required! The script will open your browser for Azure AD login.

```bash
python fetch_north52_from_dataverse.py --environment dev --list
```

#### Option B: Service Principal (Recommended for Automation)

1. Register an app in Azure AD
2. Grant it Dynamics 365 API permissions
3. Create a client secret
4. Add CLIENT_ID to your .env (optional)
5. Pass the client_secret via CLI or environment variable

```bash
# Pass secret via CLI
python fetch_north52_from_dataverse.py --environment prod --client-secret "your-secret" --list

# Or use environment variable
export DATAVERSE_CLIENT_SECRET="your-secret"
python fetch_north52_from_dataverse.py --environment prod --list

# Override app_id from config if needed
python fetch_north52_from_dataverse.py --environment prod \\
    --app-id "override-app-id" --client-secret "your-secret" --list
```

#### Option C: DefaultAzureCredential (Managed Identity)

Uses environment credentials (Azure CLI, Managed Identity, etc.)

```python
from dataverse_sdk_client import DataverseClient
from config_loader import load_dataverse_config

config = load_dataverse_config('dev')
client = DataverseClient(config['environment_url'])
client.connect(use_default_credential=True)
```

## Usage Examples

### List All North52 Formulas

```bash
# Interactive authentication (uses dev environment by default)
python fetch_north52_from_dataverse.py --list

# Specify environment
python fetch_north52_from_dataverse.py --environment prod --list

# Service principal
python fetch_north52_from_dataverse.py --environment prod --client-secret "secret" --list
```

**Output:**

```
Found 156 formula(s):

Name: new_n52/formula/mnp_invoiceproductrevision/m35
  Display Name: Invoice Product Revision - Calculate Benefits
  Entity: mnp_invoiceproductrevision
  Short Code: m35
  Type: Save - To Current Record
  Enabled: Yes

Name: new_n52/formula/account/PWa
  Display Name: Account - Primary Contact Validation
  ...
```

### Fetch Formulas for a Specific Entity

```bash
# Just list them
python fetch_north52_from_dataverse.py --environment dev \\
    --entity mnp_invoiceproductrevision

# Save to files for analysis
python fetch_north52_from_dataverse.py --environment dev \\
    --entity mnp_invoiceproductrevision \\
    --save \\
    --output-dir ./downloaded_formulas

# Parse and display metadata
python fetch_north52_from_dataverse.py --environment dev \\
    --entity mnp_invoiceproductrevision \\
    --parse
```

### Fetch a Specific Formula

```bash
# By entity and shortcode
python fetch_north52_from_dataverse.py --environment dev \\
    --entity mnp_invoiceproductrevision \\
    --shortcode m35 \\
    --save \\
    --parse

# By exact web resource name
python fetch_north52_from_dataverse.py --environment dev \\
    --name "new_n52/formula/mnp_invoiceproductrevision/m35" \\
    --save \\
    --parse
```

### Output as JSON

```bash
python fetch_north52_from_dataverse.py --environment dev \\
    --entity mnp_invoiceproductrevision \\
    --json > formulas.json
```

## Complete Workflow: Fetch from Dataverse → Analyze → Document

Here's how to fetch a formula from Dataverse and generate full documentation:

```bash
cd .github/skills/n52-doc/scripts

# Step 1: Fetch formula from Dataverse with full analysis
python fetch_north52_from_dataverse.py --environment dev \
    --shortcode m35 \
    --analyze

# This creates in .staging/north52/:
# - .staging/north52/<entity>/<shortcode>/<shortcode>.n52
# - .staging/north52/<entity>/<shortcode>/analysis_metadata.json

# Step 2: Check if AI documentation is needed
python ai_evaluate_formulas.py <entity> m35

# Step 3: Generate <shortcode>.md and code-review.md
# (GitHub Copilot uses the .n52 file and analysis_metadata.json from staging)

# Step 4: Update timestamps after doc generation
python update_ai_timestamps.py <entity> m35
```

## Using the Dataverse Client API

For custom integrations, you can use the `dataverse_sdk_client.py` module directly.

**Note:** The Dataverse client and config loader are now shared libraries located in `.github/scripts/`.

```python
import sys
from pathlib import Path

# Add shared scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'scripts'))

from dataverse_sdk_client import DataverseClient
from config_loader import load_dataverse_config

# Load configuration
config = load_dataverse_config('dev')

# Connect interactively
client = DataverseClient(config['environment_url'])
client.connect(tenant_id=config['tenant_id'])  # Opens browser for authentication

# Or with service principal
client.connect(
    app_id=config.get('app_id'),
    client_secret="your-secret",
    tenant_id=config['tenant_id']
)

# Get records with OData query
accounts = client.get_records("accounts", "?$select=name&$top=10")
for account in accounts['value']:
    print(account['name'])

# Get records with FetchXML
fetch_xml = """
<fetch top="5">
    <entity name="account">
        <attribute name="name"/>
        <attribute name="revenue"/>
        <filter>
            <condition attribute="revenue" operator="gt" value="1000000"/>
        </filter>
    </entity>
</fetch>
"""
results = client.get_records_with_fetchxml("accounts", fetch_xml)

# Get a single record
account = client.get_record("accounts", "guid-here", "?$select=name,revenue")

# Create a record
new_id = client.create_record("contacts", {
    "firstname": "John",
    "lastname": "Doe",
    "emailaddress1": "john.doe@example.com"
})

# Update a record
client.update_record("contacts", new_id, {
    "jobtitle": "Senior Developer"
})

# Delete a record
client.delete_record("contacts", new_id)

# Get metadata
entity_meta = client.get_entity_metadata("account")
attributes = client.get_entity_attributes("account")

# Execute action
result = client.post_action("WhoAmI", {})
print(f"User ID: {result['UserId']}")

# WhoAmI shortcut
who = client.who_am_i()
print(f"User: {who['UserId']}")
print(f"Org: {who['OrganizationId']}")
```

## Advanced Features

### Automatic Token Refresh

The client automatically refreshes expired tokens when it receives a 401 Unauthorized response.

### Retry Logic for Rate Limiting

When Dataverse returns a 429 (Too Many Requests) error, the client:

1. Reads the `Retry-After` header
2. Waits for the specified duration
3. Retries the request (up to 3 times)

### Proxy Support for Debugging

```python
client = DataverseClient(
    "https://yourorg.crm.dynamics.com",
    debug=True,
    proxy_url="http://127.0.0.1:8888"  # Fiddler proxy
)
```

### Error Handling

```python
try:
    results = client.get_records("accounts", "?$select=name")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.text}")
except Exception as e:
    print(f"Error: {e}")
```

## Command-Line Reference

### fetch_north52_from_dataverse.py

```
python fetch_north52_from_dataverse.py [options]

Environment Configuration:
  --environment ENV, -e ENV
                        Accepted for backward compatibility; config is loaded from .env
  --list-environments   List configured environment and exit

Authentication:
  --app-id              Application (client) ID (overrides CLIENT_ID in .env if set)
  --client-secret       Client secret for service principal auth
                        Can also use DATAVERSE_CLIENT_SECRET env var

Query Options:
  --list                List all North52 formulas
  --entity ENTITY       Filter formulas by entity logical name
  --shortcode CODE      Specific formula short code (requires --entity)
  --name NAME           Exact web resource name

Output Options:
  --save                Save formulas to files
  --output-dir DIR      Output directory (default: ./north52_formulas)
  --parse               Parse and display formula metadata
  --json                Output as JSON
```

### config_loader.py

```
python config_loader.py [options]

Options:
  --list                Show configured environment
  --validate            Validate current configuration
  --show                Show configuration (excluding secrets)
  --env-path            Show path to .env file
```

## Troubleshooting

### Configuration Errors

**Error:** `.env file not found`

**Solution:** Create .env from template:

```bash
cp .env.example .env
# Edit .env with your environment details
```

**Error:** `.env is missing required values`

**Solution:** Ensure DATAVERSE_URL and TENANT_ID are set in `.env`:

```bash
python config_loader.py --validate
```

### Authentication Errors

**Error:** `DefaultAzureCredential failed to retrieve a token`

**Solution:** Use interactive authentication or provide service principal credentials:

```bash
# Interactive (default)
python fetch_north52_from_dataverse.py --environment dev --list

# Service principal with secret
python fetch_north52_from_dataverse.py --environment prod --client-secret "secret" --list

# Or use environment variable
export DATAVERSE_CLIENT_SECRET="your-secret"
python fetch_north52_from_dataverse.py --environment prod --list
```

### Permission Errors

**Error:** `403 Forbidden`

**Solution:** Ensure your user/app has permission to:

- Read web resources
- Access Dynamics 365 Web API
- Read entity metadata (if using `--parse`)

### Formula Not Found

**Error:** `Formula not found: entity/shortcode`

**Solution:** The script tries multiple name patterns. If still not found:

1. Use `--list` to see all available formulas
2. Use `--name` with the exact web resource name
3. Verify the entity logical name is correct (not display name)

### Rate Limiting

**Error:** `429 Too Many Requests`

**Solution:** The client automatically retries with backoff. If you still hit limits:

- Add delays between requests
- Reduce batch sizes
- Use `--entity` to filter instead of `--list` for all

## Best Practices

1. **Centralize Configuration:** Maintain environment settings in `.env` at the repository root
2. **Use Service Principal for Automation:** Don't use interactive auth in scripts/CI/CD
3. **Secure Secrets:** Never commit client secrets to git. Use environment variables or Azure Key Vault
4. **Cache Results:** Fetched formulas can be saved and reused for multiple analyses
5. **Respect Rate Limits:** Don't hammer the API with rapid requests
6. **Verify Permissions:** Test with a non-admin account to ensure proper RBAC
7. **Log API Calls:** Use the logging output to track what's being fetched
8. **Compare Environments:** Fetch from DEV and PROD to verify formula consistency
9. **List Before Fetch:** Use `python config_loader.py --list` to verify configuration

## Environment Configuration

**Example `.env` Structure:**

```ini
DATAVERSE_URL=https://dev-yourorg.crm3.dynamics.com
TENANT_ID=fbef0798-20e3-4be7-bdc8-372032610f65
ENVIRONMENT_NAME=dev
ENVIRONMENT_DESCRIPTION=Development environment
MAKE_ENVIRONMENT_ID=your-make-environment-id
MAKE_SOLUTION_ID=your-make-solution-id
NORTH52_APP_ID=your-north52-app-id
# For service principal auth:
# CLIENT_ID=your-app-registration-client-id
# CLIENT_SECRET=your-client-secret
```

(Replace `yourorg` with your actual organization name. See `.env.example` for all available settings.)

## Security Considerations

- **Never commit secrets:** Don't put client secrets in code or git
- **Use environment variables:** Store credentials in Azure Key Vault or env vars
- **Rotate secrets regularly:** Change client secrets on a schedule
- **Use Managed Identity:** When running in Azure, use Managed Identity instead of secrets
- **Audit API access:** Monitor who's accessing formulas via API

## Support and Feedback

For issues or questions about the Dataverse integration:

1. Check the main [SKILL.md](../SKILL.md) documentation
2. Review error messages and logs
3. Verify authentication and permissions
4. Check that dependencies are installed (`azure-identity`, `requests`)

## Related Documentation

- [SKILL.md](../SKILL.md) - Main skill documentation
- [dataverse_sdk_client.py](dataverse_sdk_client.py) - API client implementation
- [fetch_north52_from_dataverse.py](fetch_north52_from_dataverse.py) - CLI tool
- [Microsoft Dataverse Web API Reference](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
