# PAC CLI Solution Commands Reference

Quick reference for common `pac solution` commands used in this skill.

## Prerequisites

- **Power Platform CLI** must be installed: [Installation Guide](https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction)
- **Authentication** required before use: `pac auth create --url https://org.crm.dynamics.com`

## Core Commands

### pac solution export

Export a solution from Dynamics 365 environment.

```powershell
pac solution export --path <folder> --name <solution-name> [options]
```

**Key Options:**
- `--path`: Folder where the solution.zip will be saved
- `--name`: Unique name of the solution (not display name)
- `--managed`: Export as managed (default is unmanaged)
- `--overwrite`: Overwrite existing files
- `--environment-url`: Specify environment URL (uses current auth context if omitted)

**Example:**
```powershell
pac solution export --path "./solutions/MyApp" --name "MyAppSolution" --overwrite
```

### pac solution unpack

Unpack a solution zip file into source-controlled folder structure.

```powershell
pac solution unpack --zipfile <path> --folder <output> --packagetype <type> [options]
```

**Key Options:**
- `--zipfile`: Path to the solution zip file
- `--folder`: Output folder for unpacked files
- `--packagetype`: `Managed` or `Unmanaged`
- `--allowDelete`: Allow deleting files in output folder
- `--allowWrite`: Allow overwriting existing files
- `--clobber`: Overwrite Read-only files
- `--map`: Path to mapping.xml file for file path transformations

**Example:**
```powershell
pac solution unpack --zipfile "solution.zip" --folder "./src" --packagetype Unmanaged --allowDelete --clobber
```

### pac solution version

Update solution version number.

```powershell
pac solution version [options]
```

**Key Options:**
- `-bv <value>`: Update build version (3rd segment)
- `-rv <value>`: Update revision version (4th segment)
- `-sv <value>`: Set full version (major.minor.build.revision)
- `-po <path>`: Path to Other folder containing Solution.xml

**Must be run from the `Other` folder** of an unpacked solution, or specify `--patchoptionfolder`.

**Example:**
```powershell
cd ./MySolution/Other
pac solution version -bv 202602 -rv 181045
```

## Mapping File

A `mapping.xml` file controls how solution components are organized during unpack:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Mapping>
  <FileToPath map="Entities" to="Entities\%folderName%\%fileName%" />
  <FileToPath map="WebResources" to="WebResources\%folderName%\%fileName%" />
  <!-- Add more mappings as needed -->
</Mapping>
```

Place in `<Solutions>/mapping.xml` for automatic discovery by export script.

## Authentication Management

### List authentication profiles
```powershell
pac auth list
```

### Create new authentication
```powershell
pac auth create --url https://org.crm.dynamics.com
```

### Select active profile
```powershell
pac auth select --index <number>
```

### Clear authentication
```powershell
pac auth clear
```

## Complete Documentation

Full PAC CLI reference: https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution
