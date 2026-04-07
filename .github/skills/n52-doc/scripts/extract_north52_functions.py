

import os
import re

# Path to the markdown file, resolved relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(script_dir, '..', 'references', 'north52-functions-complete.md')

functions_dict = {}
current_category = None

category_header_re = re.compile(r'^##\s+(.+)$')
table_row_re = re.compile(r'^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*\[Docs\]\(([^)]+)\)\s*\|')

with open(md_path, 'r', encoding='utf-8') as f:
    for line in f:
        # Detect category header
        cat_match = category_header_re.match(line)
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue

        # Parse function table row
        row_match = table_row_re.match(line)
        if row_match and current_category:
            name = row_match.group(1).strip()
            description = row_match.group(2).strip()
            link = row_match.group(3).strip()
            functions_dict[name] = {
                "name": name,
                "category": current_category,
                "description": description,
                "link": link
            }


# Write output to north52_functions.py
output_path = os.path.join(script_dir, 'north52_functions.py')
with open(output_path, 'w', encoding='utf-8') as out:
    out.write('"""\nNorth52 function metadata dictionary\n\nTo update: Run extract_north52_functions.py.\n"""\n')
    out.write('NORTH52_FUNCTIONS = {\n')
    for key in sorted(functions_dict.keys()):
        entry = functions_dict[key]
        out.write(f'    "{entry["name"]}": {{\n')
        out.write(f'        "name": "{entry["name"]}",\n')
        out.write(f'        "category": "{entry["category"]}",\n')
        out.write(f'        "description": "{entry["description"]}",\n')
        out.write(f'        "link": "{entry["link"]}"\n')
        out.write('    },\n')
    out.write('}\n')
print(f"north52_functions.py updated with {len(functions_dict)} functions.")
