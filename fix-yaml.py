#!/usr/bin/env python3
import os
import re
import glob

def fix_yaml_quotes(content):
    """Fix unescaped quotes in YAML front matter"""
    # Pattern: title: "text with "quoted" text"
    content = re.sub(r'title:\s*"([^"]*)"([^"]*)"([^"]*)"', r'title: "\1\'\2\'\3"', content)
    # Also fix SEO titles
    content = re.sub(r'(\s+title:\s*)"([^"]*)"([^"]*)"([^"]*)"', r'\1"\2\'\3\'\4"', content)
    return content

def fix_problematic_chars(content):
    """Fix problematic Unicode characters"""
    # Common problematic characters
    replacements = {
        'â': '-',           # em-dash issues
        'ΓÇó': '•',          # bullet point
        '"': '"',           # smart quotes
        '"': '"',           # smart quotes
        ''': "'",           # smart apostrophe
        ''': "'",           # smart apostrophe
        '–': '-',           # en dash
        '—': '--',          # em dash
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    return content

def fix_file(filepath):
    """Fix a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_yaml_quotes(content)
        content = fix_problematic_chars(content)
        
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
        print(result.stderr)

if __name__ == "__main__":
    main()
