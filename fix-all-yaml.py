#!/usr/bin/env python3
"""
Comprehensive YAML front matter fixer for Hugo content files
Fixes all common YAML formatting issues that prevent Hugo builds
"""
import os
import re
import glob

def comprehensive_yaml_fix(content):
    """Apply all YAML fixes comprehensively"""
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
    
    # Process each YAML line
    for i in range(yaml_start + 1, yaml_end):
        original_line = lines[i]
        line = original_line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Skip lines that are just stray quotes
        if line in ['"', "'", '""', "''"]:
            lines[i] = ''
            continue
        
        # Handle key-value pairs
        if ':' in line:
            key_part, value_part = line.split(':', 1)
            key_part = key_part.strip()
            value_part = value_part.strip()
            
            # Handle different value types
            if value_part.startswith('[') and value_part.endswith(']'):
                # Array values - fix quotes inside arrays
                value_part = fix_array_quotes(value_part)
            elif value_part and not value_part.startswith('-'):
                # Scalar values - fix quote issues
                value_part = fix_scalar_quotes(value_part)
            
            # Reconstruct the line maintaining original indentation
            indent = len(original_line) - len(original_line.lstrip())
            lines[i] = ' ' * indent + f'{key_part}: {value_part}'
    
    return '\n'.join(lines)

def fix_scalar_quotes(value):
    """Fix quote issues in scalar YAML values"""
    if not value:
        return '""'
    
    # Remove leading/trailing whitespace
    value = value.strip()
    
    # Handle different quote scenarios
    if value.startswith('"') and value.endswith('"'):
        # Already properly quoted - check for internal issues
        inner = value[1:-1]
        if '"' in inner:
            # Escape internal quotes
            inner = inner.replace('"', '\\"')
            return f'"{inner}"'
        return value
    elif value.startswith("'") and value.endswith("'"):
        # Single quoted - convert to double quoted
        inner = value[1:-1]
        return f'"{inner}"'
    elif value.startswith('"') or value.startswith("'"):
        # Malformed quotes - extract content and requote
        inner = re.sub(r'^[\'"]|[\'"]$', '', value)
        return f'"{inner}"'
    else:
        # Unquoted string - quote it if it contains special characters
        if any(char in value for char in [' ', ':', '"', "'", '#', '\n']):
            return f'"{value}"'
        return value

def fix_array_quotes(array_str):
    """Fix quotes inside array values"""
    # Remove brackets
    inner = array_str[1:-1].strip()
    if not inner:
        return '[]'
    
    # Split by comma and fix each item
    items = []
    for item in inner.split(','):
        item = item.strip()
        if item:
            # Remove any existing quotes and add proper ones
            item = re.sub(r'^[\'"]|[\'"]$', '', item).strip()
            items.append(f'"{item}"')
    
    return '[' + ', '.join(items) + ']'

def clean_unicode_chars(content):
    """Clean problematic Unicode characters"""
    replacements = {
        'â': '-',           # em-dash issues
        'ΓÇó': '•',          # bullet points
        '"': '"',           # smart quotes left
        '"': '"',           # smart quotes right
        ''': "'",           # smart apostrophe left
        ''': "'",           # smart apostrophe right
        '–': '-',           # en dash
        '—': '--',          # em dash
        '…': '...',         # ellipsis
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
        
        # Apply all fixes
        content = clean_unicode_chars(content)
        content = comprehensive_yaml_fix(content)
        
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
    
    print(f"Processing {len(files)} markdown files for comprehensive YAML fixes...")
    
    fixed_count = 0
    for filepath in files:
        if fix_file(filepath):
            filename = os.path.basename(os.path.dirname(filepath)) + '/' + os.path.basename(filepath)
            print(f"Fixed: {filename}")
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files total.")
    
    # Test Hugo build
    print("\nTesting Hugo build...")
    os.chdir(r"C:\Users\gnul\hashnhedge\site")
    
    import subprocess
    result = subprocess.run(["hugo", "--gc", "--minify"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("🎉 SUCCESS: Hugo build completed successfully!")
        print("Your tableless theme is now working properly!")
    else:
        print("❌ Build still failing. Remaining errors:")
        error_lines = result.stderr.split('\n')
        for line in error_lines[:10]:  # Show first 10 lines of errors
            if line.strip():
                print(f"  {line}")

if __name__ == "__main__":
    main()
