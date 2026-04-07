---
name: export-solution
description: Export and unpack Dynamics 365/Dataverse solutions using pac CLI. Use when user asks to export D365 solution, download Dynamics solution, extract solution from environment, sync solution from Dataverse, update solution files, or pull latest solution changes. Works with solution unique names and optionally environment URLs.
---

# Export Dynamics 365 Solutions

Export and unpack Dynamics 365 unmanaged solutions from your environment to the workspace using the Power Platform CLI (`pac`).

**Note**: This skill always exports unmanaged solutions and includes built-in safeguards against file lock issues.

## When to Use

User requests to:

- Export a solution from Dynamics 365
- Download/pull solution from environment
- Extract solution to source control
- Update local solution files with latest changes
- Sync solution from Dataverse

## Prerequisites

1. **Power Platform CLI** installed and available in PATH
   - Install: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction
2. **Authentication** to target environment
   - Run: `pac auth create --url https://org.crm.dynamics.com`
   - Or specify `--EnvironmentUrl` parameter when executing

3. **Solution unique name** (not display name)
   - Example: "IncomeAssistanceCore" not "Income Assistance Core"

## How to Use

Execute the PowerShell script with solution name:

```powershell
.\scripts\export-solution.ps1 -SolutionName "YourSolutionName"
```

### Common Usage Patterns

**Export using current pac auth context:**

```powershell
.\scripts\export-solution.ps1 -SolutionName "IncomeAssistance"
```

**Export from specific environment:**

```powershell
.\scripts\export-solution.ps1 -SolutionName "IncomeAssistanceCore" -EnvironmentUrl "https://org.crm.dynamics.com"
```

**Custom solution base path:**

```powershell
.\scripts\export-solution.ps1 -SolutionName "MyApp" -SolutionPath "custom\path\to\solutions"
```

## What the Script Does

1. **Validates** workspace structure and solution path
2. **Cleans** previous solution files if they exist
3. **Exports** unmanaged solution zip from Dynamics 365 using `pac solution export`
4. **Waits** 3 seconds to ensure file handles are released (prevents file lock errors)
5. **Unpacks** zip to `**/{SolutionName}/` using `pac solution unpack`
6. **Updates** solution version to timestamp format (yyyyMM.ddHHmm)
7. **Cleans up** temporary zip file
8. **Preserves** existing folder structure and applies mapping.xml if present

## Output Structure

```
src/**/
├── mapping.xml (optional)
└── YourSolutionName/
    ├── Entities/
    ├── WebResources/
    ├── Workflows/
    ├── Other/
    │   └── Solution.xml (version updated here)
    └── ...other components
```

## Mapping File Support

If `src/**/mapping.xml` exists, it will be automatically used to control file organization during unpack.

Example mapping.xml:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Mapping>
  <FileToPath map="Entities" to="Entities\%folderName%\%fileName%" />
  <FileToPath map="WebResources" to="WebResources\%folderName%\%fileName%" />
</Mapping>
```

## Error Handling

The script will stop and report errors if:

- Solution name not found in environment
- Authentication expired or invalid
- pac CLI not installed or not in PATH
- Insufficient permissions to export solution
- Solution folder path not found

**Built-in Safeguards:**

- 3-second delay before unpacking prevents "file being used by another process" errors
- Automatic cleanup of previous solution files
- Proper error messages with exit codes

## Parameters Reference

| Parameter      | Required | Default            | Description                     |
| -------------- | -------- | ------------------ | ------------------------------- |
| SolutionName   | Yes      | -                  | Unique name of the solution     |
| EnvironmentUrl | No       | Current auth       | URL of Dynamics 365 environment |
| SolutionPath   | No       | `src\D365Solution` | Base path for solutions         |

## Additional Resources

- **PAC CLI commands**: See [pac-commands.md](references/pac-commands.md) for detailed command reference
- **Official docs**: https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution

## Common Issues

**"Solution not found"**: Verify solution unique name (case-sensitive) matches exactly  
**"Authentication failed"**: Run `pac auth list` to verify active connection, or use `pac auth create`  
**"Access denied"**: Ensure user has System Customizer or System Administrator role  
**"Version update failed"**: Check that Other/Solution.xml exists in unpacked solution  
**"File being used by another process"**: The script now includes a 3-second delay to prevent this, but if it persists, close any programs that might have the solution folder open (e.g., file explorer, other VS Code windows)

## Lessons Learned

**File Lock Issues**: The pac CLI sometimes holds file handles after export. The 3-second delay before unpacking prevents the "file being used by another process" error that can occur when trying to unpack immediately after export.

**Simplified Structure**: Exporting directly to the solution folder (not a 'managed' or 'unmanaged' subfolder) keeps the structure cleaner and aligns with most source control workflows where only unmanaged solutions are tracked.
