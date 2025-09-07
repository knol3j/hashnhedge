#!/usr/bin/env python3
"""
Script to process copied posts and add them to the main site
"""

import os
import re
from pathlib import Path

# Paths
BACKUP_POSTS_DIR = "site/content/posts-backup-08"
MAIN_POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

def sanitize_filename(filename):
    """Sanitize filename for Hugo compatibility"""
    filename = re.sub(r'[^\w\s-]', '', filename).strip()
    filename = re.sub(r'[-\s]+', '-', filename).lower()
    return filename[:60]  # Reasonable length limit

def process_frontmatter(content, original_dir_name):
    """Process and fix frontmatter for Hugo compatibility"""
    if not content.startswith('---'):
        return content
    
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return content
            
        frontmatter = parts[1]
        body = parts[2].strip()
        
        # Fix common YAML syntax issues
        frontmatter = re.sub(r"title: \"([^\"]*)'", r'title: "\1"', frontmatter)
        frontmatter = re.sub(r"category: '([^']*)", r'category: "\1"', frontmatter)
        frontmatter = re.sub(r"category: \'([^']*)", r'category: "\1"', frontmatter)
        
        # Add image if not present
        if 'image:' not in frontmatter:
            image_name = sanitize_filename(original_dir_name) + '.svg'
            frontmatter = frontmatter.rstrip() + f'\nimage: "/images/posts/{image_name}"'
        
        # Ensure proper YAML formatting
        frontmatter = frontmatter.strip()
        
        return f"---\n{frontmatter}\n---\n\n{body}"
        
    except Exception as e:
        print(f"Error processing frontmatter: {e}")
        return content

def process_posts():
    """Process all backup posts and copy to main directory"""
    if not os.path.exists(BACKUP_POSTS_DIR):
        print(f"Backup posts directory not found: {BACKUP_POSTS_DIR}")
        return
    
    # Create directories
    os.makedirs(MAIN_POSTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    processed_count = 0
    
    # Walk through backup directory
    for root, dirs, files in os.walk(BACKUP_POSTS_DIR):
        for file in files:
            if file == 'index.md':
                source_path = os.path.join(root, file)
                
                # Get original directory name for slug
                original_dir = os.path.basename(root)
                sanitized_name = sanitize_filename(original_dir)
                
                # Create destination filename
                dest_filename = f"{sanitized_name}.md"
                dest_path = os.path.join(MAIN_POSTS_DIR, dest_filename)
                
                try:
                    # Read and process content
                    with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Process the content
                    processed_content = process_frontmatter(content, original_dir)
                    
                    # Write to destination
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        f.write(processed_content)
                    
                    processed_count += 1
                    
                    if processed_count % 50 == 0:
                        print(f"Processed {processed_count} posts...")
                    
                except Exception as e:
                    print(f"Error processing {source_path}: {e}")
    
    print(f"Successfully processed {processed_count} posts")

if __name__ == "__main__":
    process_posts()