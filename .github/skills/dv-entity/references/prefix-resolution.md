# Publisher Prefix Resolution Algorithm

The skill resolves the publisher prefix using this 4-step waterfall. Stop at the first successful resolution and warn the user if falling back to step 4.

## Resolution Order

```
1. --prefix flag (explicit CLI argument)
2. Solution.xml Publisher/UniqueName
3. .env or config.json PUBLISHER_PREFIX
4. Fallback: "mnp" (warn user)
```

## Step 1: --prefix Flag

If the user explicitly passes `--prefix grants` (or similar), use that value directly. No file reading required.

```python
# Example: user says "Create a Payment table for the Grants solution -- use the grants prefix"
# Copilot extracts prefix="grants" from the request
prefix = "grants"
```

## Step 2: Read Solution.xml

Locate the unpacked solution's `Solution.xml` file. The publisher prefix is the `<UniqueName>` element under the `<Publisher>` node.

```xml
<!-- Solution.xml excerpt -->
<ImportExportXml>
  <SolutionManifest>
    <UniqueName>IncomeAssistanceCore</UniqueName>
    <Publisher>
      <UniqueName>mnp</UniqueName>       <!-- <-- This is the prefix -->
      <EMailAddress></EMailAddress>
      <CustomizationPrefix>mnp</CustomizationPrefix>
    </Publisher>
  </SolutionManifest>
</ImportExportXml>
```

```python
import xml.etree.ElementTree as ET
from pathlib import Path

def resolve_prefix_from_solution_xml(solution_dir: str) -> str | None:
    """Read publisher prefix from unpacked Solution.xml."""
    candidates = list(Path(solution_dir).rglob("Solution.xml"))
    for path in candidates:
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            # Try both paths: nested under SolutionManifest and direct
            for xpath in [
                ".//SolutionManifest/Publisher/UniqueName",
                ".//Publisher/UniqueName",
            ]:
                node = root.find(xpath)
                if node is not None and node.text:
                    return node.text.strip().lower()
        except Exception:
            continue
    return None
```

**Where to look for Solution.xml:**

Search common locations in the repo:
```
StarterKits/{kit}/Solutions/{SolutionName}/Other/Solution.xml
StarterKits/{kit}/Solutions/{SolutionName}/Solution.xml
```

## Step 3: .env / config.json

Check for `PUBLISHER_PREFIX` in `.env` (at repo root) or `config.json`.

```python
import os
import json
from pathlib import Path
from dotenv import load_dotenv

def resolve_prefix_from_config(repo_root: str) -> str | None:
    """Read publisher prefix from .env or config.json."""
    # Try .env first
    env_path = Path(repo_root) / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        val = os.getenv("PUBLISHER_PREFIX")
        if val:
            return val.strip().lower()

    # Try config.json
    config_path = Path(repo_root) / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        val = config.get("PUBLISHER_PREFIX") or config.get("publisher_prefix")
        if val:
            return str(val).strip().lower()

    return None
```

## Step 4: Fallback — "mnp"

If none of the above resolve the prefix, default to `"mnp"` and **warn the user**:

```
Warning: Could not resolve publisher prefix from --prefix flag, Solution.xml, .env, or config.json.
Defaulting to "mnp". Pass --prefix <prefix> to override.
```

## Full Resolution Function

```python
def resolve_publisher_prefix(
    prefix_flag: str | None = None,
    solution_dir: str | None = None,
    repo_root: str = ".",
) -> tuple[str, str]:
    """
    Resolve publisher prefix using 4-step waterfall.
    Returns (prefix, source) where source describes how it was resolved.
    """
    # Step 1: explicit flag
    if prefix_flag:
        return prefix_flag.lower(), "--prefix flag"

    # Step 2: Solution.xml
    if solution_dir:
        val = resolve_prefix_from_solution_xml(solution_dir)
        if val:
            return val, "Solution.xml"

    # Also search StarterKits/ for any Solution.xml
    val = resolve_prefix_from_solution_xml(repo_root)
    if val:
        return val, "Solution.xml (auto-discovered)"

    # Step 3: .env / config.json
    val = resolve_prefix_from_config(repo_root)
    if val:
        return val, ".env/config.json"

    # Step 4: fallback
    print("Warning: Could not resolve publisher prefix. Defaulting to 'mnp'.")
    return "mnp", "fallback default"
```

## Example Usage in Skill

When generating any entity or attribute name, always resolve the prefix first:

```
User: "Create a new Application table"
Copilot: Resolves prefix -> "mnp" (from Solution.xml)
         Proposes logical name: mnp_application
```

```
User: "Create a Payment table for the Grants solution -- use the grants prefix"
Copilot: Resolves prefix -> "grants" (from --prefix flag in request)
         Proposes logical name: grants_payment
```
