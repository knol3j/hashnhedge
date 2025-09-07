#!/usr/bin/env python3
"""
Comprehensive YAML frontmatter fix for all posts
"""

import os
import re
import yaml
from pathlib import Path

POSTS_DIR = "site/content/posts"

def sanitize_string(text):
    """Sanitize string for YAML compatibility"""
    if not text:
        return ""
    
    # Remove or replace problematic characters
    text = text.replace('\u2018', "'").replace('\u2019', "'")  # Smart quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')  # Smart double quotes
    text = text.replace('\u2013', '-').replace('\u2014', '-')  # Em/en dashes
    text = text.strip()
    
    return text

def fix_yaml_frontmatter(content):
    """Comprehensive YAML frontmatter fix"""
    if not content.startswith('---'):
        return content
    
    try:
        # Split content
        parts = content.split('---', 2)
        if len(parts) < 3:
            return content
        
        frontmatter = parts[1].strip()
        body = parts[2].strip()
        
        # Remove BOM
        frontmatter = frontmatter.lstrip('\ufeff')
        
        # Build clean YAML structure
        data = {}
        
        # Extract key fields with robust parsing
        title_match = re.search(r'title:\s*["\']([^"\']*?)["\']?(?:\s*\'|")?', frontmatter, re.DOTALL)
        if title_match:
            title = sanitize_string(title_match.group(1))
            # Truncate very long titles
            if len(title) > 100:
                title = title[:97] + "..."
            data['title'] = title
        else:
            data['title'] = "Untitled"
        
        # Date
        date_match = re.search(r'date:\s*["\']([^"\']*)["\']?', frontmatter)
        if date_match:
            data['date'] = sanitize_string(date_match.group(1))
        
        # Category
        cat_match = re.search(r'category:\s*["\']([^"\']*)', frontmatter)
        if cat_match:
            data['category'] = sanitize_string(cat_match.group(1))
        else:
            data['category'] = "Markets"
        
        # Summary
        data['summary'] = ""
        
        # Slug
        slug_match = re.search(r'slug:\s*["\']([^"\']*)["\']', frontmatter)
        if slug_match:
            data['slug'] = sanitize_string(slug_match.group(1))
        
        # Source URLs
        source_urls_match = re.search(r'source_urls:\s*\n?\s*-\s*["\']([^"\']*)["\']', frontmatter)
        if source_urls_match:
            data['source_urls'] = [sanitize_string(source_urls_match.group(1))]
        
        # Image (add if not present)
        if 'slug' in data:
            image_name = re.sub(r'[^\w\s-]', '', data['slug']).strip()
            image_name = re.sub(r'[-\s]+', '-', image_name).lower()[:50]
            data['image'] = f"/images/posts/{image_name}.svg"
        
        # SEO section
        data['seo'] = {
            'title': data['title'] + " | Hash & Hedge",
            'description': "",
            'keywords': ["news", "markets", "brief"]
        }
        
        # Convert to YAML
        yaml_content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return f"---\n{yaml_content}---\n\n{body}"
        
    except Exception as e:
        print(f"Error processing frontmatter: {e}")
        # Fallback: create minimal valid YAML
        title = "Untitled Post"
        title_match = re.search(r'title:\s*["\']([^"\']{1,50})', content)
        if title_match:
            title = sanitize_string(title_match.group(1))
        
        fallback_yaml = f"""---
title: "{title}"
date: "2025-08-23T12:00:00"
category: "Markets"
summary: ""
image: "/images/posts/default.svg"
seo:
  title: "{title} | Hash & Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---

{parts[2].strip() if len(parts) > 2 else "Content not available."}"""
        return fallback_yaml

def fix_all_posts():
    """Fix all posts with comprehensive YAML repair"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    fixed_count = 0
    error_count = 0
    
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            
            try:
                # Read file
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Fix YAML
                fixed_content = fix_yaml_frontmatter(content)
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                fixed_count += 1
                
                if fixed_count % 50 == 0:
                    print(f"Fixed {fixed_count} files...")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                error_count += 1
    
    print(f"Successfully fixed {fixed_count} files, {error_count} errors")

if __name__ == "__main__":
    fix_all_posts()