#!/usr/bin/env python3
"""Fix YAML front matter in Markdown files"""

import argparse
import os
import io
import re
import sys
import yaml
from datetime import datetime

def slugify(text):
    """Convert text to URL-friendly slug"""
    s = re.sub(r'[^a-zA-Z0-9\- ]+', '', str(text)).strip().lower()
    s = re.sub(r'\s+', '-', s)
    return s[:60] or "post"

def fix_yaml_in_file(filepath):
    """Fix YAML front matter in a single file"""
    issues = []
    changed = False
    
    try:
        with io.open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Cannot read file: {e}"]
    
    # Check if file has front matter
    if not content.strip().startswith('---'):
        # Add minimal front matter
        basename = os.path.basename(filepath)
        title = os.path.splitext(basename)[0].replace('-', ' ').title()
        date = datetime.now().strftime('%Y-%m-%d')
        
        new_content = f"""---
title: "{title}"
date: "{date}"
draft: false
---

{content}"""
        
        with io.open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, ["Added missing YAML front matter"]
    
    # Split front matter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False, ["Malformed front matter structure"]
    
    yaml_content = parts[1]
    body_content = parts[2] if len(parts) > 2 else ""
    
    # Parse YAML
    try:
        data = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError as e:
        # Try to fix common issues
        lines = yaml_content.strip().split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix mismatched quotes
            if ':' in line:
                key_val = line.split(':', 1)
                if len(key_val) == 2:
                    key = key_val[0].strip()
                    val = key_val[1].strip()
                    
                    # Fix quote issues
                    if val.startswith('"') and not val.endswith('"'):
                        val = val + '"'
                    elif val.startswith("'") and not val.endswith("'"):
                        val = val + "'"
                    elif '"' in val and not (val.startswith('"') and val.endswith('"')):
                        val = '"' + val.replace('"', "'") + '"'
                    
                    # Fix indentation for nested fields
                    if key in ['title', 'description', 'keywords'] and '  ' in line[:len(line) - len(line.lstrip())]:
                        line = f"  {key}: {val}"
                    else:
                        line = f"{key}: {val}"
            
            fixed_lines.append(line)
        
        yaml_content = '\n'.join(fixed_lines)
        
        try:
            data = yaml.safe_load(yaml_content) or {}
            changed = True
            issues.append("Fixed YAML syntax errors")
        except:
            return False, [f"Cannot parse YAML: {str(e)[:100]}"]
    
    # Ensure required fields
    if 'title' not in data or not data['title']:
        basename = os.path.basename(filepath)
        data['title'] = os.path.splitext(basename)[0].replace('-', ' ').title()
        changed = True
        issues.append("Added missing title")
    
    if 'date' not in data or not data['date']:
        # Try to extract from filename
        basename = os.path.basename(filepath)
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', basename)
        if date_match:
            data['date'] = date_match.group(1)
        else:
            data['date'] = datetime.now().strftime('%Y-%m-%d')
        changed = True
        issues.append("Added missing date")
    
    # Normalize date format
    if isinstance(data.get('date'), str) and 'T' in data['date']:
        try:
            dt = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            data['date'] = dt.strftime('%Y-%m-%d')
            changed = True
            issues.append("Normalized date format")
        except:
            pass
    
    # Ensure slug
    if 'slug' not in data or not data['slug']:
        data['slug'] = slugify(data.get('title', 'post'))
        changed = True
        issues.append("Added slug")
    
    # Fix SEO section if needed
    if 'seo' in data and isinstance(data['seo'], dict):
        seo = data['seo']
        if not seo.get('title'):
            seo['title'] = data.get('title', '') + ' | Hash n Hedge'
            changed = True
        if not seo.get('description'):
            seo['description'] = ''
            changed = True
        if not seo.get('keywords'):
            seo['keywords'] = ['news', 'markets', 'brief']
            changed = True
    
    # Clean up problematic fields
    for key in list(data.keys()):
        if key is None or str(key).strip() == '':
            del data[key]
            changed = True
            issues.append(f"Removed empty key")
    
    # Write back if changed
    if changed or issues:
        yaml_str = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        new_content = f"---\n{yaml_str}---\n{body_content}"
        
        with io.open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, issues
    
    return False, []

def main():
    parser = argparse.ArgumentParser(description='Fix YAML front matter in Markdown files')
    parser.add_argument('--path', required=True, help='Directory containing Markdown files')
    parser.add_argument('--check-only', action='store_true', help='Only check, do not modify')
    parser.add_argument('--write', action='store_true', help='Write changes to files')
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    total = 0
    changed_count = 0
    problems = 0
    
    for root, dirs, files in os.walk(args.path):
        for name in files:
            if name.lower().endswith('.md'):
                total += 1
                filepath = os.path.join(root, name)
                
                if args.check_only:
                    # Just check, don't modify
                    with io.open(filepath, 'r', encoding='utf-8-sig') as f:
                        content = f.read()
                    if not content.strip().startswith('---'):
                        problems += 1
                        print(f"[{filepath}] Missing YAML front matter")
                else:
                    changed, issues = fix_yaml_in_file(filepath)
                    if issues:
                        problems += 1
                        print(f"[{filepath}] " + " | ".join(issues))
                    if changed:
                        changed_count += 1
    
    print(f"\nScanned: {total} files")
    print(f"Changed: {changed_count} files")
    print(f"Files with issues: {problems}")
    
    if args.check_only and problems > 0:
        sys.exit(2)

if __name__ == "__main__":
    main()
