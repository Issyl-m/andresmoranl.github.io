from pathlib import Path
import re

def fix_cases_files(directory='.'):
    # Matches \begin{cases}, any amount of whitespace (spaces, tabs, newlines), and \end{cases}
    cases_pattern = re.compile(r'\\begin\{cases\}\s*\\end\{cases\}')
    
    # Iterate through all items in the specified directory
    for file_path in Path(directory).iterdir():
        # Check constraints: file, filename length == 6, and no extension
        if file_path.is_file() and len(file_path.name) == 6 and not file_path.suffix:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Replacement function that checks if a further \end{cases} exists after the match
                def replace_empty_cases(match):
                    remaining_text = match.string[match.end():]
                    if r'\end{cases}' in remaining_text:
                        return r'\begin{cases}'
                    return match.group(0)  # Leave unchanged if no further \end{cases}
                
                # Apply the conditional replacement
                content = cases_pattern.sub(replace_empty_cases, content)
                
                # Write back if changes were made
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"Fixed cases in: {file_path.name}")
                else:
                    print(f"Skipped (no matching patterns): {file_path.name}")
                    
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

if __name__ == '__main__':
    fix_cases_files('.')
