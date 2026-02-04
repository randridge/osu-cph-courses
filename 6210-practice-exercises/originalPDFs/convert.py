import os
import glob
import re

def find_balanced_braces(text, start_index):
    """Finds the content within the next set of balanced braces."""
    start = text.find('{', start_index)
    if start == -1: return None, None
    count = 0
    for i in range(start, len(text)):
        if text[i] == '{': count += 1
        elif text[i] == '}':
            count -= 1
            if count == 0: return text[start+1:i], i + 1
    return None, None

def clean_latex_formatting(text):
    # 1. STRIP COMMENTS
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)

    # 2. REMOVE STRUCTURAL ELEMENTS
    text = re.sub(r'\\documentclass\[.*?\]\{.*?\}', '', text)
    text = re.sub(r'\\documentclass\{.*?\}', '', text)
    text = re.sub(r'\\toggle(true|false)\{.*?\}', '', text)
    text = re.sub(r'\\usepackage(\[.*?\])?\{.*?\}', '', text)
    text = text.replace(r'\begin{document}', '').replace(r'\end{document}', '')

    # 3. TRANSFORM EXERCISES
    exercise_count = 1
    i = 0
    while i < len(text):
        if text.startswith(r'\exercise', i):
            orig_num, next_pos = find_balanced_braces(text, i + 8)
            if next_pos:
                content, end_pos = find_balanced_braces(text, next_pos)
                if end_pos:
                    replacement = f"\nHEADER_TOKEN_1 Exercise {exercise_count}\n\n{content}\n"
                    text = text[:i] + replacement + text[end_pos:]
                    i += len(replacement)
                    exercise_count += 1
                    continue
        i += 1

    # 4. TRANSFORM STATA ENVIRONMENTS TO CLEAN DIVS
    # Replaces \begin{stata}...\end{stata} with ::: {.stata} ... :::
    text = re.sub(r'\\begin\{stata\}', '\n::: {.stata}\n', text)
    text = text.replace(r'\end{stata}', '\n:::\n')
    # Expand tabs to 4 spaces to ensure alignment in monospace blocks
    text = text.expandtabs(4)

    # 5. TRANSFORM ANSWERS
    while True:
        match = re.search(r'\\answer\s*\{', text)
        if not match: break
        start_idx = match.start()
        _, first_end = find_balanced_braces(text, start_idx + 7)
        if first_end:
            ans_content, second_end = find_balanced_braces(text, first_end)
            if second_end:
                replacement = f"\n\n::: {{.answer .hidden}}\n{ans_content}\n:::\n\n"
                text = text[:start_idx] + replacement + text[second_end:]
                continue
        break

    # 6. SWAP FORMATTING
    text = re.sub(r'\\section\{(.*?)\}', r'HEADER_TOKEN_1 \1', text)
    text = re.sub(r'\\subsection\{(.*?)\}', r'HEADER_TOKEN_2 \1', text)
    text = re.sub(r'\\textbf\{(.*?)\}', r'**\1**', text)
    text = re.sub(r'\\textit\{(.*?)\}', r'*\1*', text)
    
    # 7. QUOTE FIXES
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace("`", "'")

    # 8. ESCAPED CHARACTER FIXES
    text = text.replace(r'\#', '&#35;')
    text = text.replace(r'\%', '%')
    text = text.replace(r'\&', '&')
    text = text.replace(r'\_', '_')

    # 9. CONVERT HEADER TOKENS BACK
    text = text.replace('HEADER_TOKEN_1', '#')
    text = text.replace('HEADER_TOKEN_2', '##')

    # 10. REMOVE SPACING COMMANDS
    text = re.sub(r'\\(quad|qquad|,|:|;)', '', text)

    # 11. REPLACE FIGURES WITH SMART PLACEHOLDERS
    while True:
        match = re.search(r'\\includegraphics\s*(?:\[.*?\])?\s*\{', text)
        if not match: break
        start_idx = match.start()
        filename, end_idx = find_balanced_braces(text, start_idx)
        if end_idx:
            placeholder = f"\n\n**[FIGURE HERE: {filename}]**\n\n"
            text = text[:start_idx] + placeholder + text[end_idx:]
            continue
        break
    
    # 12. HANDLE LINE BREAKS
    text = re.sub(r'\\\\\s*\[.*?\]', '\n\n', text)
    text = re.sub(r'~\s*\\\\', '\n\n', text)
    text = re.sub(r'\\\\\s*$', '\n\n', text, flags=re.MULTILINE)
    
    # 13. FINAL NOISE CLEANUP
    text = text.replace(r'\noindent', '')
    text = text.replace(r'\newpage', '\n---\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def batch_convert():
    tex_files = glob.glob("*.tex")
    for input_file in tex_files:
        base_name = os.path.splitext(input_file)[0]
        suffix_match = re.search(r'(\d+[A-Za-z]?)', base_name)
        suffix = suffix_match.group(1) if suffix_match else ""
        display_title = f"PUBHBIO 6210: Practice Exercises {suffix}"
        
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                raw_latex = f.read()
            cleaned_text = clean_latex_formatting(raw_latex)
            yaml = (
                "---\n"
                f"title: \"{display_title}\"\n"
                "format:\n"
                "  html:\n"
                "    embed-resources: true\n"
                "    toc: true\n"
                "    html-math-method: mathjax\n"
                "    include-in-header: header.html\n"
                "---\n\n"
            )
            with open(f"{base_name}.qmd", 'w', encoding='utf-8') as f:
                f.write(yaml + cleaned_text)
            print(f"✅ Created/Updated: {base_name}.qmd")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    batch_convert()
