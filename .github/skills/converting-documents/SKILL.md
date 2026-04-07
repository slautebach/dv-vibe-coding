---
name: converting-documents
description: Convert documents to or from Markdown using pandoc. Primary use cases are converting office formats (docx, odt, pptx), HTML, PDF, RST, LaTeX, and CSV to Markdown for AI/wiki ingestion, and publishing Markdown back to docx, html, pdf, or pptx. Handles single files and batch folder conversion (with optional recursion). Use when asked to convert, export, or transform documents to/from markdown. Do NOT use for XLSX files (use the xlsx skill first to export CSV, then convert) or for scanned PDFs with no text layer (OCR required first).
---

# Converting Documents

Convert documents to or from Markdown -- and between any other pandoc-supported formats -- using `scripts/convert.py`.

## To Markdown (primary use case)

Extract readable, AI-friendly content from office documents, web pages, and more.

```powershell
# DOCX -> GFM markdown (single file)
python .github/skills/converting-documents/scripts/convert.py -i report.docx -t gfm

# Batch: every .docx in a folder -> markdown alongside the originals
python .github/skills/converting-documents/scripts/convert.py -i "Document Gathering" -t gfm

# Batch recursive with a separate output folder
python .github/skills/converting-documents/scripts/convert.py -i "Document Gathering" -t gfm -r -o "Document Gathering\Markdown"
```

| Source format | Flag | Notes |
|---------------|------|-------|
| DOCX | `-t gfm` | Preserves tracked changes (`--track-changes=all` applied automatically) |
| PDF | `-t gfm` | Text-layer PDFs only; scanned PDFs need OCR first |
| PPTX | `-t gfm` | Each slide becomes a heading + bullet list |
| HTML | `-t gfm` | Strips tags, preserves structure |
| ODT | `-t gfm` | |
| RST / LaTeX | `-t gfm` | |
| CSV / TSV | `-t gfm` | Produces a markdown table |

Use `-t markdown` instead of `-t gfm` for richer pandoc-flavoured markdown (footnotes, definition lists, etc.). Use `-t gfm` for GitHub wikis and most AI ingestion pipelines.

## From Markdown (secondary use case)

Publish markdown to deliverable formats.

```powershell
# Markdown -> DOCX
python .github/skills/converting-documents/scripts/convert.py -i notes.md -t docx

# Markdown -> DOCX with a Word template for styles
python .github/skills/converting-documents/scripts/convert.py -i notes.md -t docx -o notes.docx
# then open in Word or add --reference-doc=template.docx to the pandoc call

# Markdown -> HTML
python .github/skills/converting-documents/scripts/convert.py -i notes.md -t html

# Markdown -> PPTX (H1 = section, H2 = slide title)
python .github/skills/converting-documents/scripts/convert.py -i notes.md -t pptx

# Markdown -> PDF (requires LaTeX or wkhtmltopdf)
python .github/skills/converting-documents/scripts/convert.py -i notes.md -t pdf
```

## Options

| Flag | Description |
|------|-------------|
| `-i` / `--input` | Input file or folder |
| `-t` / `--to` | Target format: `gfm`, `markdown`, `docx`, `html`, `pdf`, `pptx`, ... |
| `-o` / `--output` | Output file or folder (default: alongside input) |
| `-f` / `--from` | Source format override (pandoc auto-detects from extension) |
| `-r` / `--recursive` | Recurse into subfolders (batch mode) |
| `--list-formats` | Print all pandoc input/output formats and exit |

## Prerequisites

- **pandoc** -- install from https://pandoc.org/installing.html
- **PDF output** -- also requires LaTeX (`pdflatex` / `xelatex`) or `wkhtmltopdf`

## Format reference

For the complete format list, extra flags (`--track-changes`, `--reference-doc`, `--extract-media`, `--wrap`, `--toc`), and known limitations, see `references/pandoc-formats.md`.
