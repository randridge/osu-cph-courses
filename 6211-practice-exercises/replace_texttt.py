import glob
import os
import re

def fix_texttt_in_qmd():
    # Look for all .qmd files
    qmd_files = glob.glob("*.qmd")
    
    if not qmd_files:
        print("No .qmd files found in the current directory.")
        return

    print(f"Scanning {len(qmd_files)} files for \\texttt...")
    print("-" * 50)

    for file_path in qmd_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if \texttt exists before processing
            if r'\texttt{' in content:
                # Regex to find \texttt{content} and replace with `content`
                # The (.*?) is a non-greedy capture group
                new_content = re.sub(r'\\texttt\{(.*?)\}', r'`\1`', content)
                
                # Count the number of replacements made
                count = len(re.findall(r'\\texttt\{.*?\}', content))
                
                # Write the changes back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Fixed {count} occurrence(s) in: {file_path}")
            else:
                # Optional: print files that were already clean
                # print(f"--- No matches in: {file_path}")
                pass
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

    print("-" * 50)
    print("Batch update complete.")

if __name__ == "__main__":
    fix_texttt_in_qmd()
