import glob
import os
import re

def check_for_figures():
    # Look for all .qmd files
    qmd_files = sorted(glob.glob("*.qmd"))
    
    if not qmd_files:
        print("No .qmd files found in this directory.")
        return

    print(f"{'FILE NAME':<30} | {'FIGURES FOUND'}")
    print("-" * 50)

    found_any = False
    for file_path in qmd_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Search for the specific placeholder text created by our conversion script
            # Pattern matches **[FIGURE HERE: filename.ext]**
            figures = re.findall(r'\*\*\[FIGURE HERE: (.*?)\]\*\*', content)
            
            if figures:
                found_any = True
                figure_list = ", ".join(figures)
                print(f"{file_path:<30} | {len(figures)} figure(s) ({figure_list})")
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    if not found_any:
        print("No figure placeholders found in any .qmd files.")

if __name__ == "__main__":
    check_for_figures()
