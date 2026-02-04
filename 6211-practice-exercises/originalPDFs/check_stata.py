import glob
import os
import re

def find_stata_blocks():
    # Look for all .qmd files
    qmd_files = sorted(glob.glob("*.qmd"))
    
    if not qmd_files:
        print("No .qmd files found.")
        return

    print(f"{'FILE NAME':<30} | {'STATA BLOCKS'}")
    print("-" * 50)

    found_any = False
    for file_path in qmd_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # This regex finds either the ::: {.stata} div OR the ```{.text .stata} block
            stata_pattern = r'(::: *\{.*?\.stata.*?\}|``` *\{.*?\.stata.*?\})'
            matches = re.findall(stata_pattern, content, re.IGNORECASE)
            
            if matches:
                found_any = True
                print(f"{file_path:<30} | {len(matches)} block(s) found")
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if not found_any:
        print("No Stata blocks found in any .qmd files.")

if __name__ == "__main__":
    find_stata_blocks()
