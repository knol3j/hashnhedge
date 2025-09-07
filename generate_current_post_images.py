#!/usr/bin/env python3
"""
Generate images for current posts
"""

import os
import re
import hashlib

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

def get_color_from_title(title):
    """Generate a consistent color based on title"""
    hash_object = hashlib.md5(title.encode())
    hex_dig = hash_object.hexdigest()
    return f"#{hex_dig[:6]}"

def get_complementary_color(hex_color):
    """Get a complementary color for contrast"""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    
    comp_r = 255 - r
    comp_g = 255 - g
    comp_b = 255 - b
    
    return f"#{comp_r:02x}{comp_g:02x}{comp_b:02x}"

def create_svg_image(title, filename):
    """Create an SVG image for a post"""
    primary_color = get_color_from_title(title)
    secondary_color = get_complementary_color(primary_color)
    
    display_title = title[:40] + "..." if len(title) > 40 else title
    
    svg_content = f'''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{primary_color};stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:{secondary_color};stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect width="800" height="400" fill="url(#grad1)" />
  <rect x="40" y="40" width="720" height="320" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7" />
  <text x="400" y="180" font-family="Arial, sans-serif" font-size="24" font-weight="bold" 
        text-anchor="middle" fill="#ffffff" opacity="0.9">{display_title}</text>
  <text x="400" y="220" font-family="Arial, sans-serif" font-size="16" 
        text-anchor="middle" fill="#ffffff" opacity="0.7">Hash &amp; Hedge</text>
  <circle cx="80" cy="80" r="30" fill="#ffffff" opacity="0.1" />
  <circle cx="720" cy="320" r="40" fill="#ffffff" opacity="0.05" />
</svg>'''
    
    return svg_content

def generate_current_images():
    """Generate images for current posts"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    generated_count = 0
    
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            post_path = os.path.join(POSTS_DIR, filename)
            
            try:
                with open(post_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Extract title from frontmatter
                title_match = re.search(r'title: ["\']([^"\']+)["\']', content)
                if title_match:
                    title = title_match.group(1)
                else:
                    title = filename.replace('.md', '').replace('-', ' ').title()
                
                # Generate image filename based on post filename
                base_name = filename.replace('.md', '')
                image_filename = f"{base_name}.svg"
                image_path = os.path.join(IMAGES_DIR, image_filename)
                
                # Generate and save SVG
                svg_content = create_svg_image(title, image_filename)
                with open(image_path, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                generated_count += 1
                print(f"Generated: {image_filename}")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"Successfully generated {generated_count} images")

if __name__ == "__main__":
    generate_current_images()