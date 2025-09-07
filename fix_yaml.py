#!/usr/bin/env python3
"""
Fix YAML frontmatter issues in all posts
"""

import os
import re
from pathlib import Path

POSTS_DIR = "site/content/posts"

def fix_yaml_frontmatter(content):
    """Fix common YAML frontmatter issues"""
    if not content.startswith('---'):
        return content
    
    try:
        # Split content
        parts = content.split('---', 2)
        if len(parts) < 3:
            return content
        
        frontmatter = parts[1]
        body = parts[2].strip()
        
        # Remove BOM if present
        frontmatter = frontmatter.lstrip('\ufeff')
        
        # Fix mixed quotes and malformed YAML
        lines = frontmatter.strip().split('\n')
        fixed_lines = []
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # Fix title field with mixed quotes
            if line.strip().startswith('title:'):
                # Extract title content between quotes
                title_match = re.search(r'title:\s*["\']([^"\']*)', line)
                if title_match:
                    title = title_match.group(1).replace('"', '\\"')
                    fixed_lines.append(f'title: "{title}"')
                else:
                    fixed_lines.append(line)
            
            # Fix date field with mixed quotes
            elif line.strip().startswith('date:'):
                date_match = re.search(r'date:\s*["\']([^"\']*)', line)
                if date_match:
                    date = date_match.group(1)
                    fixed_lines.append(f'date: "{date}"')
                else:
                    fixed_lines.append(line)
            
            # Fix category field with mixed quotes
            elif line.strip().startswith('category:'):
                cat_match = re.search(r'category:\s*["\']([^"\']*)', line)
                if cat_match:
                    category = cat_match.group(1)
                    fixed_lines.append(f'category: "{category}"')
                else:
                    fixed_lines.append(line)
            
            # Fix SEO title with mixed quotes
            elif 'title:' in line and line.strip().startswith('title:') and any(s in ''.join(fixed_lines[-5:]) for s in ['seo:', 'SEO:']):
                title_match = re.search(r'title:\s*["\']([^"\']*)', line)
                if title_match:
                    title = title_match.group(1).replace('"', '\\"')
                    fixed_lines.append(f'  title: "{title}"')
                else:
                    fixed_lines.append(line)
            
            # Fix description field
            elif line.strip().startswith('description:'):
                desc_match = re.search(r'description:\s*["\']([^"\']*)', line)
                if desc_match:
                    desc = desc_match.group(1)
                    fixed_lines.append(f'  description: "{desc}"')
                else:
                    fixed_lines.append(line)
            
            # Fix keywords array
            elif line.strip().startswith('keywords:'):
                # Simple fix for keywords array
                if '[' in line:
                    keywords_content = re.search(r'\[(.*?)\]', line)
                    if keywords_content:
                        keywords = keywords_content.group(1)
                        # Clean up the keywords
                        keywords = re.sub(r'["\']([^"\']*)["\']', r'"\1"', keywords)
                        fixed_lines.append(f'  keywords: [{keywords}]')
                    else:
                        fixed_lines.append('  keywords: ["news", "markets", "brief"]')
                else:
                    fixed_lines.append(line)
            
            else:
                fixed_lines.append(line)
        
        # Reconstruct frontmatter
        fixed_frontmatter = '\n'.join(fixed_lines)
        return f"---\n{fixed_frontmatter}\n---\n\n{body}"
        
    except Exception as e:
        print(f"Error fixing YAML: {e}")
        return content

def fix_all_posts():
    """Fix YAML in all post files"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    fixed_count = 0
    error_count = 0
    
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            
            try:
                # Read file
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Fix YAML
                fixed_content = fix_yaml_frontmatter(content)
                
                # Write back if changed
                if fixed_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    fixed_count += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                error_count += 1
    
    print(f"Fixed {fixed_count} files, {error_count} errors")

if __name__ == "__main__":
    fix_all_posts()