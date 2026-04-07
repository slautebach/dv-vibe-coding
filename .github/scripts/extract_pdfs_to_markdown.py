"""
Extract PDF files to Markdown format with text and table extraction.
Uses pdfplumber for better text and table extraction capabilities.
"""

import pdfplumber
import os
from pathlib import Path


def extract_pdf_to_markdown(pdf_path, output_path=None):
    """
    Extract a PDF file to Markdown format.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Optional output path for the markdown file
    """
    if output_path is None:
        output_path = pdf_path.replace('.pdf', '.md')
    
    print(f"Extracting {pdf_path}...")
    
    markdown_content = []
    markdown_content.append(f"# {Path(pdf_path).stem}\n\n")
    markdown_content.append(f"*Extracted from: {Path(pdf_path).name}*\n\n")
    markdown_content.append("---\n\n")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"  Total pages: {total_pages}")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"  Processing page {page_num}/{total_pages}...")
            
            # Add page header
            markdown_content.append(f"## Page {page_num}\n\n")
            
            # Extract text
            text = page.extract_text()
            if text:
                markdown_content.append(text)
                markdown_content.append("\n\n")
            
            # Extract tables
            tables = page.extract_tables()
            if tables:
                for table_num, table in enumerate(tables, start=1):
                    if table and len(table) > 0:
                        markdown_content.append(f"### Table {table_num} (Page {page_num})\n\n")
                        
                        # Convert table to markdown format
                        if len(table) > 0:
                            # Header row
                            header = table[0]
                            markdown_content.append("| " + " | ".join(str(cell or "") for cell in header) + " |\n")
                            markdown_content.append("| " + " | ".join("---" for _ in header) + " |\n")
                            
                            # Data rows
                            for row in table[1:]:
                                markdown_content.append("| " + " | ".join(str(cell or "") for cell in row) + " |\n")
                            
                            markdown_content.append("\n")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(markdown_content))
    
    print(f"  ✓ Saved to {output_path}\n")
    return output_path


def main():
    """Extract all PDF files in the Client Documents folder."""
    client_docs_path = r"c:\Dev\First West Foundation\Project Documentation\Client Documents"
    
    pdf_files = [
        "FWF_Expression of Interest.pdf",
        "FWF_Payroll Giving Pledge Form.pdf",
        "FINAL D365 Scenarios_First West Foundation.pdf"
    ]
    
    print("=== PDF to Markdown Extraction ===\n")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(client_docs_path, pdf_file)
        if os.path.exists(pdf_path):
            extract_pdf_to_markdown(pdf_path)
        else:
            print(f"⚠ File not found: {pdf_path}")
    
    print("=== Extraction Complete ===")


if __name__ == "__main__":
    main()
