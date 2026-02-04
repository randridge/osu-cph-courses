import glob
import os
import re

def find_latex_tables():
    # Look for all .qmd files
    qmd_files = sorted(glob.glob("*.qmd"))
    
    if not qmd_files:
        print("No .qmd files found.")
        return

    print(f"{'FILE NAME':<30} | {'TABLES FOUND'}")
    print("-" * 50)

    total_tables = 0
    for file_path in qmd_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This regex matches the start of any LaTeX tabular environment
            table_pattern = r'\\begin\{tabular\}'
            matches = re.findall(table_pattern, content)
            
            if matches:
                total_tables += len(matches)
                print(f"{file_path:<30} | {len(matches)} table(s) found")
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    print("-" * 50)
    if total_tables == 0:
        print("No LaTeX tabular environments found.")
    else:
        print(f"Total tables needing attention: {total_tables}")

if __name__ == "__main__":
    find_latex_tables()
