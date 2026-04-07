#!/usr/bin/env python3
"""
Pandoc-based document converter. Primary purpose: convert office documents,
HTML, PDF, RST, LaTeX, and CSV to Markdown (gfm/markdown), and publish
Markdown back to docx, html, pptx, or pdf.

Supports single-file and batch conversion for any pandoc-supported format pair.

Usage:
    python convert.py -i <input> -t <to-format> [-o <output>] [-f <from-format>] [-r]

TO MARKDOWN (primary):
    # DOCX -> GFM markdown (single file)
    python convert.py -i report.docx -t gfm

    # Batch: all .docx in a folder -> markdown alongside originals
    python convert.py -i "Document Gathering" -t gfm

    # Batch recursive with a separate output folder
    python convert.py -i "Document Gathering" -t gfm -r -o "Document Gathering/Markdown"

FROM MARKDOWN (secondary):
    # Markdown -> DOCX
    python convert.py -i notes.md -t docx -o notes.docx

    # Markdown -> HTML
    python convert.py -i notes.md -t html

    # Markdown -> PPTX
    python convert.py -i notes.md -t pptx

UTILITIES:
    # List all pandoc-supported formats
    python convert.py --list-formats
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Maps format name -> file extensions used when globbing a directory
FORMAT_EXTENSIONS = {
    "docx": [".docx"],
    "odt": [".odt"],
    "pptx": [".pptx"],
    "epub": [".epub"],
    "html": [".html", ".htm"],
    "markdown": [".md", ".markdown"],
    "gfm": [".md", ".markdown"],
    "commonmark": [".md", ".markdown"],
    "rst": [".rst"],
    "latex": [".tex"],
    "pdf": [".pdf"],
    "mediawiki": [".wiki"],
    "org": [".org"],
    "textile": [".textile"],
    "asciidoc": [".adoc", ".asciidoc"],
    "json": [".json"],
    "csv": [".csv"],
    "tsv": [".tsv"],
    "txt": [".txt"],
}

# Maps target format -> preferred file extension for output files
OUTPUT_EXTENSIONS = {
    "docx": ".docx",
    "odt": ".odt",
    "pptx": ".pptx",
    "epub": ".epub",
    "html": ".html",
    "markdown": ".md",
    "gfm": ".md",
    "commonmark": ".md",
    "commonmark_x": ".md",
    "rst": ".rst",
    "latex": ".tex",
    "pdf": ".pdf",
    "mediawiki": ".wiki",
    "org": ".org",
    "textile": ".textile",
    "asciidoc": ".adoc",
    "json": ".json",
}


def check_pandoc():
    """Verify pandoc is installed and return its version."""
    try:
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        version_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        return version_line
    except FileNotFoundError:
        print("ERROR: pandoc not found. Install from https://pandoc.org/installing.html")
        sys.exit(1)


def list_formats():
    """Print pandoc's supported input and output formats."""
    print("=== Supported INPUT formats ===")
    subprocess.run(["pandoc", "--list-input-formats"])
    print("\n=== Supported OUTPUT formats ===")
    subprocess.run(["pandoc", "--list-output-formats"])


def build_pandoc_cmd(input_file: Path, output_file: Path, to_fmt: str, from_fmt: str | None) -> list[str]:
    cmd = ["pandoc", str(input_file), "-o", str(output_file), "-t", to_fmt]
    if from_fmt:
        cmd += ["-f", from_fmt]
    # Preserve tracked changes when reading DOCX
    if (from_fmt or input_file.suffix.lower()) in (".docx", "docx"):
        cmd += ["--track-changes=all"]
    return cmd


def convert_file(input_file: Path, output_file: Path, to_fmt: str, from_fmt: str | None) -> bool:
    """Convert a single file with pandoc. Returns True on success."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = build_pandoc_cmd(input_file, output_file, to_fmt, from_fmt)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  OK  {input_file.name}  ->  {output_file}")
        return True
    else:
        print(f"  FAIL  {input_file.name}: {result.stderr.strip()}")
        return False


def collect_input_files(input_path: Path, from_fmt: str | None, recursive: bool) -> list[Path]:
    """Return list of files to convert."""
    if input_path.is_file():
        return [input_path]

    # Determine which extensions to look for
    extensions: list[str] = []
    if from_fmt:
        extensions = FORMAT_EXTENSIONS.get(from_fmt, [f".{from_fmt}"])
    else:
        # Flatten all known extensions
        for exts in FORMAT_EXTENSIONS.values():
            extensions.extend(exts)
        extensions = list(set(extensions))

    glob_fn = input_path.rglob if recursive else input_path.glob
    files: list[Path] = []
    for ext in extensions:
        files.extend(glob_fn(f"*{ext}"))

    return sorted(set(files))


def resolve_output(input_file: Path, input_root: Path, output_root: Path | None, to_fmt: str) -> Path:
    """Compute the output file path, mirroring the directory structure."""
    ext = OUTPUT_EXTENSIONS.get(to_fmt, f".{to_fmt}")
    relative = input_file.relative_to(input_root) if input_root.is_dir() else Path(input_file.name)
    stem = relative.with_suffix(ext)
    base = output_root or (input_root if input_root.is_dir() else input_root.parent)
    return base / stem


def main():
    parser = argparse.ArgumentParser(
        description="Convert documents using pandoc (single-file or batch)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("-i", "--input", help="Input file or folder")
    parser.add_argument("-t", "--to", help="Target format (e.g. markdown, gfm, docx, html, pdf)")
    parser.add_argument("-o", "--output", help="Output file or folder (default: alongside input)")
    parser.add_argument("-f", "--from", dest="from_fmt", help="Source format override (pandoc auto-detects if omitted)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recurse into subdirectories (batch mode only)")
    parser.add_argument("--list-formats", action="store_true", help="List all pandoc-supported formats and exit")
    args = parser.parse_args()

    version = check_pandoc()
    print(f"Using {version}\n")

    if args.list_formats:
        list_formats()
        return

    if not args.input or not args.to:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve() if args.output else None

    if not input_path.exists():
        print(f"ERROR: Input path does not exist: {input_path}")
        sys.exit(1)

    files = collect_input_files(input_path, args.from_fmt, args.recursive)
    if not files:
        print("No matching files found.")
        sys.exit(0)

    print(f"Converting {len(files)} file(s) to '{args.to}'...\n")
    ok = fail = 0
    for f in files:
        # Single-file conversion with explicit -o: use it directly as the output file path
        if input_path.is_file() and output_path:
            out = output_path
        else:
            out = resolve_output(f, input_path, output_path, args.to)
        if convert_file(f, out, args.to, args.from_fmt):
            ok += 1
        else:
            fail += 1

    print(f"\nDone: {ok} succeeded, {fail} failed.")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
