from pathlib import Path
import re

def fix_mathbf_notation(directory='.'):
    # Matches {\mathbf X} where X is an alphanumeric character, with optional spaces
    mathbf_pattern = re.compile(r'\{\s*\\mathbf\s+([a-zA-Z0-9])\s*\}')
    
    # Iterate through all items in the specified directory
    for file_path in Path(directory).iterdir():
        # Check constraints: file, filename length == 6, and no extension
        if file_path.is_file() and len(file_path.name) == 6 and not file_path.suffix:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Perform the replacement: {\mathbf X} -> \mathbf{X}
                content = mathbf_pattern.sub(r'\\mathbf{\1}', content)
                
                # Write back if changes were made
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"Fixed \\mathbf notation in: {file_path.name}")
                else:
                    print(f"Skipped (no matching patterns): {file_path.name}")
                    
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

if __name__ == '__main__':
    fix_mathbf_notation('.')
