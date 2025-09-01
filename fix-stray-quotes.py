#!/usr/bin/env python3
import os
import re
import glob

def fix_stray_quotes(content):
    """Fix stray quotes in YAML front matter"""
    lines = content.split('\n')
    
    # Find YAML front matter boundaries
    yaml_start = -1
    yaml_end = -1
    
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if yaml_start == -1:
                yaml_start = i
            else:
                yaml_end = i
                break
    
    if yaml_start == -1 or yaml_end == -1:
        return content
    
    # Remove lines that are just stray quotes
    new_lines = []
    for i, line in enumerate(lines):
        if yaml_start < i < yaml_end:
            # Skip lines that are just a quote character
            if line.strip() in ['"', "'", '""', "''"]:
                continue
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_file(filepath):
    """Fix a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_stray_quotes(content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return False

def main():
    site_root = r"C:\Users\gnul\hashnhedge\site\content"
    pattern = os.path.join(site_root, "**", "*.md")
    files = glob.glob(pattern, recursive=True)
    
    print(f"Processing {len(files)} markdown files...")
    
    fixed_count = 0
    for filepath in files:
        if fix_file(filepath):
            print(f"Fixed: {os.path.basename(filepath)}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files total.")
    
    # Test Hugo build
    print("Testing Hugo build...")
    os.chdir(r"C:\Users\gnul\hashnhedge\site")
    
    import subprocess
    result = subprocess.run(["hugo", "--gc", "--minify"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("SUCCESS: Hugo build completed successfully!")
    else:
        print("Build failed. Next error:")
        error_lines = result.stderr.split('\n')
        for line in error_lines:
            if 'Error:' in line:
                print(f"  {line}")
                break

if __name__ == "__main__":
    main()
