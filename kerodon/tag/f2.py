from pathlib import Path
import re

def fix_xymatrix_files(directory='.'):
    # Regex 1: Matches \xymatrix followed by spaces and \1
    xymatrix_pattern = re.compile(r'(\\xymatrix)\s+\\1\b')
    
    # Regex 2: Matches \<... > where the inside has no '>' character
    angle_pattern = re.compile(r'\\<([^>]*)>')
    
    # Iterate through all items in the specified directory
    for file_path in Path(directory).iterdir():
        # Check constraints: file, filename length == 6, and no extension
        if file_path.is_file() and len(file_path.name) == 6 and not file_path.suffix:
            try:
                content = file_path.read_text(encoding='utf-8')
                original_content = content
                
                # Apply the replacements
                content = xymatrix_pattern.sub(r'\1', content)
                content = angle_pattern.sub(r'@<\1>', content)
                
                # Write back if changes were made
                if content != original_content:
                    file_path.write_text(content, encoding='utf-8')
                    print(f"Fixed: {file_path.name}")
                else:
                    print(f"Skipped (no matching patterns): {file_path.name}")
                    
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

if __name__ == '__main__':
    fix_xymatrix_files('.')
