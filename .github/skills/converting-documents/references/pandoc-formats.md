# Pandoc Format Reference

Quick reference for the formats most commonly used with the `converting-documents` skill.

## Table of Contents

- [Input formats](#input-formats)
- [Output formats](#output-formats)
- [Useful pandoc flags](#useful-pandoc-flags)
- [Notes and limitations](#notes-and-limitations)

---

## Input formats

| Format | Extensions | Notes |
|--------|-----------|-------|
| `docx` | `.docx` | Full fidelity; use `--track-changes=all` to preserve edits |
| `odt` | `.odt` | OpenDocument Text |
| `pptx` | `.pptx` | Slides converted to headings + bullet lists |
| `epub` | `.epub` | E-book |
| `html` | `.html`, `.htm` | Strips tags; preserves structure |
| `pdf` | `.pdf` | Text-layer only; scanned PDFs require OCR pre-processing |
| `rst` | `.rst` | reStructuredText |
| `latex` | `.tex` | |
| `mediawiki` | `.wiki` | |
| `org` | `.org` | Emacs Org-mode |
| `asciidoc` | `.adoc`, `.asciidoc` | |
| `csv` | `.csv` | Converted to markdown table |
| `tsv` | `.tsv` | Converted to markdown table |

Run `pandoc --list-input-formats` for the full list.

---

## Output formats

| Format | Flag value | Extension | Notes |
|--------|-----------|-----------|-------|
| Markdown (Pandoc) | `markdown` | `.md` | Richest; includes footnotes, divs |
| GitHub Flavored Markdown | `gfm` | `.md` | Best for GitHub wikis / READMEs |
| CommonMark | `commonmark` | `.md` | Strict spec-compliant markdown |
| DOCX | `docx` | `.docx` | Use `--reference-doc` for custom template |
| ODT | `odt` | `.odt` | |
| HTML | `html` | `.html` | |
| PDF | `pdf` | `.pdf` | Requires LaTeX (`pdflatex`) or `wkhtmltopdf` |
| PPTX | `pptx` | `.pptx` | H1 = section break, H2 = slide title |
| EPUB | `epub` | `.epub` | |
| reStructuredText | `rst` | `.rst` | |
| LaTeX | `latex` | `.tex` | |
| Plain text | `plain` | `.txt` | Strips all formatting |

Run `pandoc --list-output-formats` for the full list.

---

## Useful pandoc flags

| Flag | Purpose |
|------|---------|
| `--track-changes=all` | Preserve tracked changes when reading DOCX |
| `--reference-doc=template.docx` | Apply a Word template's styles to DOCX output |
| `--extract-media=./media` | Save embedded images to a folder |
| `--wrap=none` | No line-wrapping in text output (cleaner diffs) |
| `--toc` | Add a table of contents |
| `--standalone` / `-s` | Produce a complete document (with header/footer) |
| `--columns=N` | Set line width (default 72) |
| `-V key:value` | Set template variable (e.g., `-V geometry:margin=1in` for PDF) |

---

## Notes and limitations

- **XLSX is not supported** — use the `xlsx` skill to convert spreadsheets to CSV first, then pandoc can read CSV.
- **Scanned PDFs** contain no text layer; run OCR (e.g., `tesseract`) before converting with pandoc.
- **PPTX output**: pandoc creates slides from headings. Level-1 headings become new sections; level-2 become slide titles.
- **PDF output** requires a LaTeX distribution (`pdflatex`, `xelatex`, or `lualatex`) or `wkhtmltopdf` to be installed. On Windows, install MiKTeX or TeX Live.
- **Images** in DOCX/HTML are embedded by default. Use `--extract-media` to save them separately.
