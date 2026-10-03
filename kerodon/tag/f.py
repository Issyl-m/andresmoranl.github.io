from pathlib import Path

def replace_ampersands():
    # Iterate through all items in the current directory
    for file_path in Path('.').iterdir():
        # Check if it's a file, name length is 6, and it has no extension/suffix
        if file_path.is_file() and len(file_path.name) == 6 and not file_path.suffix:
            try:
                # Read the file contents
                content = file_path.read_text(encoding='utf-8')
                
                # Replace '&' with '&amp;'
                new_content = content.replace('&', '&amp;')
                
                # Write back if changes were made
                if new_content != content:
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"Updated: {file_path.name}")
                else:
                    print(f"Skipped (no '&' found): {file_path.name}")
                    
            except Exception as e:
                print(f"Error reading/writing {file_path.name}: {e}")

if __name__ == '__main__':
    replace_ampersands()
