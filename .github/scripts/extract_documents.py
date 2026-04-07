"""
Extract content from all client documents for AI processing
Outputs markdown files with extracted content from DOCX, XLSX, PDF, and PNG files
"""

import os
import json
from pathlib import Path
import pandas as pd
import pdfplumber
from pypdf import PdfReader
from PIL import Image
import subprocess

# Base directory
base_dir = Path(r"c:\Dev\First West Foundation\Project Documentation\Client Documents")
output_dir = base_dir / "Extracted Content"
output_dir.mkdir(exist_ok=True)

def extract_docx(file_path):
    """Extract DOCX content using pandoc"""
    print(f"Extracting DOCX: {file_path.name}")
    output_md = output_dir / f"{file_path.stem}_extracted.md"
    
    try:
        # Use pandoc to convert to markdown
        result = subprocess.run(
            ["pandoc", str(file_path), "-o", str(output_md), "--track-changes=all"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            with open(output_md, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"✓ Extracted to {output_md.name}\n\nPreview:\n{content[:500]}..."
        else:
            return f"✗ Error: {result.stderr}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def extract_xlsx(file_path):
    """Extract Excel content with sheet structure"""
    print(f"Extracting XLSX: {file_path.name}")
    output_md = output_dir / f"{file_path.stem}_extracted.md"
    
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(file_path)
        
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(f"# {file_path.name}\n\n")
            f.write(f"**Sheets:** {len(excel_file.sheet_names)}\n\n")
            
            for sheet_name in excel_file.sheet_names:
                f.write(f"## Sheet: {sheet_name}\n\n")
                
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Write metadata
                f.write(f"**Rows:** {len(df)}, **Columns:** {len(df.columns)}\n\n")
                
                # Write column names
                f.write("**Columns:**\n")
                for col in df.columns:
                    f.write(f"- {col}\n")
                f.write("\n")
                
                # Write data preview (first 10 rows)
                f.write("**Data Preview (first 10 rows):**\n\n")
                f.write(df.head(10).to_markdown(index=False))
                f.write("\n\n")
                
                # Write summary statistics for numeric columns
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    f.write("**Numeric Summary:**\n\n")
                    f.write(df[numeric_cols].describe().to_markdown())
                    f.write("\n\n")
                
                f.write("---\n\n")
        
        return f"✓ Extracted to {output_md.name}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def extract_pdf(file_path):
    """Extract PDF content with text and tables"""
    print(f"Extracting PDF: {file_path.name}")
    output_md = output_dir / f"{file_path.stem}_extracted.md"
    
    try:
        with pdfplumber.open(file_path) as pdf:
            with open(output_md, 'w', encoding='utf-8') as f:
                f.write(f"# {file_path.name}\n\n")
                f.write(f"**Total Pages:** {len(pdf.pages)}\n\n")
                
                for i, page in enumerate(pdf.pages, 1):
                    f.write(f"## Page {i}\n\n")
                    
                    # Extract text
                    text = page.extract_text()
                    if text:
                        f.write("**Text Content:**\n\n")
                        f.write(text)
                        f.write("\n\n")
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        f.write(f"**Tables Found:** {len(tables)}\n\n")
                        for j, table in enumerate(tables, 1):
                            f.write(f"### Table {j}\n\n")
                            # Convert table to DataFrame for better formatting
                            if table and len(table) > 0:
                                df = pd.DataFrame(table[1:], columns=table[0])
                                f.write(df.to_markdown(index=False))
                                f.write("\n\n")
                    
                    f.write("---\n\n")
        
        return f"✓ Extracted to {output_md.name}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def extract_png(file_path):
    """Extract PNG metadata and basic info"""
    print(f"Extracting PNG: {file_path.name}")
    output_md = output_dir / f"{file_path.stem}_info.md"
    
    try:
        with Image.open(file_path) as img:
            with open(output_md, 'w', encoding='utf-8') as f:
                f.write(f"# {file_path.name}\n\n")
                f.write(f"**Format:** {img.format}\n")
                f.write(f"**Size:** {img.size[0]} x {img.size[1]} pixels\n")
                f.write(f"**Mode:** {img.mode}\n")
                
                # EXIF data if available
                if hasattr(img, '_getexif') and img._getexif():
                    f.write(f"\n**EXIF Data:**\n")
                    for tag, value in img._getexif().items():
                        f.write(f"- {tag}: {value}\n")
                
                f.write(f"\n**File Path:** {file_path}\n")
                f.write(f"\n**Note:** This is a screenshot/image file. ")
                f.write(f"For AI processing, use OCR or vision models to extract text content.\n")
        
        return f"✓ Info extracted to {output_md.name}"
    except Exception as e:
        return f"✗ Error: {str(e)}"

def main():
    """Process all documents in the Client Documents folder"""
    print("=" * 80)
    print("CLIENT DOCUMENT EXTRACTION")
    print("=" * 80)
    
    results = {
        'docx': [],
        'xlsx': [],
        'pdf': [],
        'png': []
    }
    
    # Process DOCX files
    print("\n📄 Processing DOCX files...")
    for file_path in base_dir.glob("*.docx"):
        result = extract_docx(file_path)
        results['docx'].append((file_path.name, result))
    
    # Process XLSX files
    print("\n📊 Processing XLSX files...")
    for file_path in base_dir.glob("*.xlsx"):
        result = extract_xlsx(file_path)
        results['xlsx'].append((file_path.name, result))
    
    # Process PDF files
    print("\n📋 Processing PDF files...")
    for file_path in base_dir.glob("*.pdf"):
        result = extract_pdf(file_path)
        results['pdf'].append((file_path.name, result))
    
    # Process PNG files in Client Screenshots
    print("\n🖼️  Processing PNG files...")
    screenshots_dir = base_dir / "Client Screenshots"
    if screenshots_dir.exists():
        for file_path in screenshots_dir.glob("*.png"):
            result = extract_png(file_path)
            results['png'].append((file_path.name, result))
    
    # Generate summary report
    print("\n" + "=" * 80)
    print("EXTRACTION SUMMARY")
    print("=" * 80)
    
    summary_file = output_dir / "EXTRACTION_SUMMARY.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# Client Document Extraction Summary\n\n")
        f.write(f"**Extraction Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for doc_type, items in results.items():
            f.write(f"## {doc_type.upper()} Files ({len(items)})\n\n")
            for filename, result in items:
                f.write(f"### {filename}\n")
                f.write(f"{result}\n\n")
            f.write("\n")
        
        f.write("## Output Directory\n\n")
        f.write(f"All extracted content saved to: `{output_dir}`\n\n")
        f.write("## Usage\n\n")
        f.write("These extracted markdown files can be used as context for AI processing:\n")
        f.write("- Read files to understand data structures\n")
        f.write("- Reference field names and dropdown values\n")
        f.write("- Analyze workflows and requirements\n")
        f.write("- Map to Dynamics 365 entities\n")
    
    print(f"\n✓ Summary report: {summary_file}")
    print(f"\n✓ All extracted content in: {output_dir}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
