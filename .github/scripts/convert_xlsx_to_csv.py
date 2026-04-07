"""
Convert all Excel files in Client Documents to CSV format.
For multi-sheet workbooks, creates separate CSV files for each sheet.
"""
import pandas as pd
from pathlib import Path

# Define the directory containing Excel files
client_docs_dir = Path("Project Documentation/Client Documents")

# Find all Excel files
excel_files = list(client_docs_dir.glob("*.xlsx"))

print(f"Found {len(excel_files)} Excel files to convert:\n")

for excel_file in excel_files:
    print(f"Processing: {excel_file.name}")
    
    try:
        # Read all sheets from the Excel file
        all_sheets = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
        
        # If single sheet, create one CSV with same base name
        if len(all_sheets) == 1:
            sheet_name = list(all_sheets.keys())[0]
            df = all_sheets[sheet_name]
            csv_path = excel_file.with_suffix('.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"  ✓ Created: {csv_path.name}")
        
        # If multiple sheets, create separate CSV for each sheet
        else:
            print(f"  Found {len(all_sheets)} sheets:")
            for sheet_name, df in all_sheets.items():
                # Clean sheet name for filename (remove invalid characters)
                clean_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).strip()
                csv_filename = f"{excel_file.stem}_{clean_sheet_name}.csv"
                csv_path = client_docs_dir / csv_filename
                df.to_csv(csv_path, index=False, encoding='utf-8')
                print(f"    ✓ Created: {csv_filename}")
    
    except Exception as e:
        print(f"  ✗ Error processing {excel_file.name}: {str(e)}")
    
    print()

print("Conversion complete!")
