#!/usr/bin/env python3
"""
Generate PNG diagram from a PlantUML (.puml) file using a local plantuml.jar.

Usage:
    python generate_diagram.py <entity> <shortcode>
    python generate_diagram.py wiki/Technical-Reference/North52/mnp_benefitassessment/oIY/diagram.puml

Output:
    Saves diagram.png alongside the .puml file.

Requirements:
    - Java Runtime Environment (JRE) 8+  : https://www.java.com/download/
    - plantuml.jar                        : https://plantuml.com/download
      Place plantuml.jar in one of:
        - .github/tools/plantuml.jar  (project-level, recommended)
        - ~/plantuml.jar              (user home)
        - Any directory on PATH as plantuml.jar
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Locate workspace root
# ---------------------------------------------------------------------------
_script_dir = Path(__file__).resolve().parent
_workspace_root = _script_dir
for _ in range(6):
    if (_workspace_root / ".github").exists():
        break
    _workspace_root = _workspace_root.parent


def _find_plantuml_jar() -> Path:
    """Search for plantuml.jar in known locations.

    Windows-friendly location is included: %USERPROFILE%\AppData\Local\plantuml\plantuml.jar
    """
    candidates = [
        _workspace_root / ".github" / "tools" / "plantuml.jar",
        Path.home() / "AppData" / "Local" / "plantuml" / "plantuml.jar",
        Path.home() / "plantuml.jar",
        Path("/usr/local/lib/plantuml.jar"),
        Path("/usr/share/plantuml/plantuml.jar"),
    ]
    # Also check PATH directories
    for dir_str in os.environ.get("PATH", "").split(os.pathsep):
        candidates.append(Path(dir_str) / "plantuml.jar")

    for p in candidates:
        if p.exists():
            return p
    return None


def _find_java() -> str:
    """Return the java executable path, or raise if not found."""
    java = shutil.which("java")
    if java:
        return java
    # Common install locations
    for candidate in ["/usr/bin/java", "/usr/local/bin/java"]:
        if Path(candidate).exists():
            return candidate
    raise FileNotFoundError(
        "Java Runtime Environment not found.\n"
        "Install Java from: https://www.java.com/download/"
    )


def generate_png(puml_path: Path) -> Path:
    """Run plantuml.jar to generate a PNG next to the .puml file."""
    jar = _find_plantuml_jar()
    if jar is None:
        print("ERROR: plantuml.jar not found.")
        print("Download from https://plantuml.com/download and place it at:")
        print(f"  {_workspace_root / '.github' / 'tools' / 'plantuml.jar'}")
        sys.exit(1)

    java = _find_java()

    cmd = [
        java,
        "-jar", str(jar),
        "-tpng",                         # output format: PNG
        "-charset", "UTF-8",
        str(puml_path),
    ]

    print(f"  Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ERROR: PlantUML failed:")
        print(result.stderr or result.stdout)
        sys.exit(1)

    png_path = puml_path.with_suffix(".png")
    if not png_path.exists():
        print(f"ERROR: Expected output not found: {png_path}")
        sys.exit(1)

    print(f"  Saved: {png_path.relative_to(_workspace_root)}")
    return png_path


def resolve_puml_path(args: list) -> Path:
    if len(args) == 1 and args[0].endswith(".puml"):
        path = Path(args[0])
        return path if path.is_absolute() else _workspace_root / path
    elif len(args) == 2:
        entity, shortcode = args
        return (
            _workspace_root
            / "Documentation"
            / "North52"
            / entity
            / shortcode
            / "diagram.puml"
        )
    raise ValueError("Provide <entity> <shortcode>  OR  <path/to/diagram.puml>")


def main():
    parser = argparse.ArgumentParser(
        description="Generate PNG from a PlantUML file using a local plantuml.jar."
    )
    parser.add_argument(
        "target",
        nargs="+",
        help="Either: <entity> <shortcode>   OR   <path/to/diagram.puml>",
    )
    parsed = parser.parse_args()

    try:
        puml_path = resolve_puml_path(parsed.target)
    except ValueError as e:
        parser.error(str(e))

    if not puml_path.exists():
        print(f"ERROR: PlantUML file not found: {puml_path}")
        sys.exit(1)

    print(f"Generating diagram PNG: {puml_path.name}")
    generate_png(puml_path)


if __name__ == "__main__":
    main()
