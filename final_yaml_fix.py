#!/usr/bin/env python3
"""
Final YAML fix - remove BOM and fix all malformed frontmatter
"""

import os
import re

POSTS_DIR = "site/content/posts"

def clean_yaml_file(filepath):
    """Clean a single YAML file"""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
            content = f.read()
        
        if not content.strip():
            return False
        
        # If no frontmatter, skip
        if not content.startswith('---'):
            return False
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False
        
        frontmatter = parts[1].strip()
        body = parts[2].strip()
        
        # Extract basic info
        title = "Untitled"
        date = "2025-08-23T12:00:00"
        category = "Markets"
        slug = ""
        
        # Extract title - handle various quote issues
        title_patterns = [
            r'title:\s*"([^"]*)"',
            r"title:\s*'([^']*)'", 
            r'title:\s*"([^"\']*)',
            r"title:\s*'([^'\"]*)",
            r'title:\s*([^"\'\n]*)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, frontmatter)
            if match:
                title = match.group(1).strip()
                # Clean title
                title = re.sub(r'[\\]+', '', title)  # Remove backslashes
                title = title.replace('\\"', '"')   # Fix escaped quotes
                break
        
        # Truncate very long titles
        if len(title) > 100:
            title = title[:97] + "..."
        
        # Extract date
        date_match = re.search(r'date:\s*["\']?([^"\']*)["\']?', frontmatter)
        if date_match:
            date = date_match.group(1).strip()
        
        # Extract category
        cat_match = re.search(r'category:\s*["\']?([^"\']*)["\']?', frontmatter)
        if cat_match:
            category = cat_match.group(1).strip()
        
        # Extract slug
        slug_match = re.search(r'slug:\s*["\']([^"\']*)["\']', frontmatter)
        if slug_match:
            slug = slug_match.group(1).strip()
        
        # Create clean filename for image
        if slug:
            image_name = re.sub(r'[^\w\s-]', '', slug)
            image_name = re.sub(r'[-\s]+', '-', image_name)
            image_name = image_name.lower().strip('-')[:50]
        else:
            base = os.path.basename(filepath).replace('.md', '')
            image_name = base[:50]
        
        # Build clean YAML
        clean_yaml = f'''---
title: "{title}"
date: "{date}"
category: "{category}"
summary: ""
image: "/images/posts/{image_name}.svg"
seo:
  title: "{title} | Hash & Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---

{body}'''
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(clean_yaml)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def fix_all_posts():
    """Fix all posts"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    fixed_count = 0
    
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            if clean_yaml_file(filepath):
                fixed_count += 1
                if fixed_count % 50 == 0:
                    print(f"Fixed {fixed_count} files...")
    
    print(f"Successfully cleaned {fixed_count} files")

if __name__ == "__main__":
    fix_all_posts()