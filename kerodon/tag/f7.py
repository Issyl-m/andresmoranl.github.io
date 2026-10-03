from pathlib import Path
import re

def fix_xymatrix_blocks(directory='.'):
    # Matches xymatrix, non-greedy characters up to '{', 
    # then greedy characters (.*) up to the *last* '}' on the line
    xymatrix_pattern = re.compile(r'(xymatrix.*?\{)(.*)(\})')
    
    # Matches a dot followed by variable spaces (0 or more) and a closing brace
    dot_brace_pattern = re.compile(r'\.\s*\}')
    
    # Iterate through all items in the specified directory
    for file_path in Path(directory).iterdir():
        # Check constraints: file, filename length == 6, and no extension
        if file_path.is_file() and len(file_path.name) == 6 and not file_path.suffix:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.splitlines(keepends=True)
                new_lines = []
                changed = False
                
                for line in lines:
                    if 'xymatrix' in line:
                        def sub_block(match):
                            nonlocal changed
                            full_match = match.group(0)
                            # Perform the replacement strictly inside the match pattern
                            new_match, count = dot_brace_pattern.subn(r'}', full_match)
                            if count > 0:
                                changed = True
                            return new_match
                        
                        # Apply transformation to matching lines
                        new_line = xymatrix_pattern.sub(sub_block, line)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
                
                # Write back if changes were made
                if changed:
                    file_path.write_text(''.join(new_lines), encoding='utf-8')
                    print(f"Fixed xymatrix blocks in: {file_path.name}")
                else:
                    print(f"Skipped (no matching patterns): {file_path.name}")
                    
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")

if __name__ == '__main__':
    fix_xymatrix_blocks('.')
