#!/usr/bin/env python3
"""
Fix Image References - Update all post frontmatter to use .jpg instead of .svg
"""

import os
import re

POSTS_DIR = "site/content/posts"

def fix_image_references():
    """Update all post frontmatter to reference .jpg images instead of .svg"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    print("Fixing image references in post frontmatter...")
    print("=" * 50)
    
    fixed_count = 0
    total_posts = 0
    
    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.md'):
            continue
            
        post_path = os.path.join(POSTS_DIR, filename)
        total_posts += 1
        
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the post has an SVG image reference
            svg_pattern = r'image: "/images/posts/([^"]+)\.svg"'
            match = re.search(svg_pattern, content)
            
            if match:
                # Replace .svg with .jpg
                new_content = re.sub(svg_pattern, r'image: "/images/posts/\1.jpg"', content)
                
                # Write the updated content back
                with open(post_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"FIXED: {filename} -> .jpg")
                fixed_count += 1
            else:
                print(f"SKIPPED: {filename} (no SVG reference)")
                
        except Exception as e:
            print(f"ERROR processing {filename}: {e}")
    
    print("\n" + "=" * 50)
    print(f"IMAGE REFERENCE FIX COMPLETE!")
    print("=" * 50)
    print(f"Posts processed: {total_posts}")
    print(f"Posts fixed: {fixed_count}")
    print()
    print("All posts now reference .jpg images instead of .svg")
    print("Run 'hugo --minify' to rebuild the site with correct images")

if __name__ == "__main__":
    fix_image_references()