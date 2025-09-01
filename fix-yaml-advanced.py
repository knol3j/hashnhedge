#!/usr/bin/env python3
import os
import re
import glob

def fix_yaml_frontmatter(content):
    """Fix malformed YAML front matter"""
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
    
    # Process YAML lines
    for i in range(yaml_start + 1, yaml_end):
        line = lines[i]
        
        # Fix common YAML issues
        # 1. Mixed quote types like category: 'Markets"
        if re.match(r'^\s*\w+:\s*[\'"][^\'"]*([\'"]\s*$)', line):
            # Extract key and value
            match = re.match(r'^(\s*\w+:\s*)([\'"])([^\'"]*)[\'"]\s*$', line)
            if match:
                prefix, quote, value = match.groups()
                lines[i] = f'{prefix}"{value}"'
        
        # 2. Malformed quotes like title: "something'
        elif re.match(r'^\s*\w+:\s*"[^"]*\'?\s*$', line):
            # Fix quotes that start with " but end with ' or nothing
            match = re.match(r'^(\s*\w+:\s*)"([^"]*)[\']*\s*$', line)
            if match:
                prefix, value = match.groups()
                lines[i] = f'{prefix}"{value}"'
        
        # 3. Malformed quotes like title: 'something"
        elif re.match(r'^\s*\w+:\s*\'[^\']*"?\s*$', line):
            # Fix quotes that start with ' but end with " or nothing
            match = re.match(r'^(\s*\w+:\s*)\'([^\']*)["]*\s*$', line)
            if match:
                prefix, value = match.groups()
                lines[i] = f'{prefix}"{value}"'
                
        # 4. Fix array with mixed quotes like ['news", "markets"]
        elif 'keywords:' in line and '[' in line:
            # Fix mixed quotes in arrays
            line = re.sub(r"(\[|,\s*)'([^']*)'", r'\1"\2"', line)  # ' to "
            line = re.sub(r"(\[|,\s*)'([^']*)\",", r'\1"\2",', line)  # mixed quotes
            lines[i] = line
    
    return '\n'.join(lines)

def fix_file(filepath):
    """Fix a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_yaml_frontmatter(content)
        
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
    
    print(f"Found {len(files)} markdown files")
    
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
        print("Build failed with errors:")
        # Show the key error info
        error_lines = result.stderr.split('\n')
        for line in error_lines:
            if 'Error:' in line or 'failed to unmarshal' in line:
                print(f"  {line}")

if __name__ == "__main__":
    main()
