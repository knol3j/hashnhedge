#!/usr/bin/env python3
"""
Clean Photo Fix for Hash & Hedge - No Unicode characters
Replaces SVG images with real photos using Lorem Picsum
"""

import os
import re
import hashlib
import requests
import time

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

def extract_photo_keywords(title):
    """Extract keywords and map to photo categories"""
    keyword_mapping = {
        'bitcoin': 'technology',
        'ethereum': 'technology', 
        'crypto': 'business',
        'blockchain': 'technology',
        'defi': 'business',
        'trading': 'business',
        'market': 'business',
        'analysis': 'business',
        'finance': 'business',
        'security': 'technology',
        'wallet': 'technology',
        'mining': 'technology',
        'staking': 'business',
        'governance': 'business',
        'compliance': 'business',
        'audit': 'business',
        'yield': 'nature',
        'protocol': 'technology',
        'institutional': 'business',
        'regulation': 'business',
        'smart': 'technology',
        'contract': 'business',
        'investment': 'business',
        'growth': 'nature',
        'price': 'business',
        'trends': 'business',
        'innovation': 'technology',
        'network': 'technology',
        'platform': 'technology',
        'launch': 'business',
        'update': 'technology'
    }
    
    title_lower = title.lower()
    
    for term, category in keyword_mapping.items():
        if term in title_lower:
            return category
    
    return 'business'

def get_lorem_picsum_image(category, width=800, height=400):
    """Get a random image from Lorem Picsum based on category"""
    category_seeds = {
        'business': ['1', '2', '3', '4', '5', '10', '15', '20', '25', '30'],
        'technology': ['100', '101', '102', '103', '104', '110', '115', '120', '125', '130'],
        'nature': ['200', '201', '202', '203', '204', '210', '215', '220', '225', '230'],
        'abstract': ['300', '301', '302', '303', '304', '310', '315', '320', '325', '330']
    }
    
    import random
    seeds = category_seeds.get(category, category_seeds['business'])
    seed = random.choice(seeds)
    
    url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
    
    return {
        'url': url,
        'attribution': f'Photo from Lorem Picsum (ID: {seed})',
        'category': category
    }

def download_image_simple(image_info, filepath):
    """Simple image download"""
    try:
        print(f"Downloading: {image_info['category']} image...")
        response = requests.get(image_info['url'], timeout=15, stream=True)
        
        if response.status_code == 200:
            base_filepath = os.path.splitext(filepath)[0]
            final_filepath = base_filepath + '.jpg'
            
            with open(final_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(final_filepath)
            print(f"Downloaded: {os.path.basename(final_filepath)} ({file_size // 1024} KB)")
            
            return final_filepath, image_info['attribution']
            
    except Exception as e:
        print(f"Download error: {e}")
    
    return None, None

def fix_post_image(title, base_filename):
    """Fix a single post's image - force photo download"""
    category = extract_photo_keywords(title)
    print(f"Category: {category}")
    
    # Remove existing SVG if it exists
    svg_path = os.path.join(IMAGES_DIR, f"{base_filename}.svg")
    if os.path.exists(svg_path):
        os.remove(svg_path)
        print(f"Removed: {base_filename}.svg")
    
    # Try to get a real photo
    image_info = get_lorem_picsum_image(category)
    image_path = os.path.join(IMAGES_DIR, f"{base_filename}.jpg")
    
    downloaded_path, attribution = download_image_simple(image_info, image_path)
    
    if downloaded_path:
        return downloaded_path, attribution, "photo"
    
    # If download fails, don't create SVG - just report failure
    print(f"Failed to download photo for: {title}")
    return None, None, "failed"

def quick_photo_replacement():
    """Replace SVG images with photos for all posts"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    print("CryptoHedgey's Quick Photo Fix")
    print("=" * 50)
    print("Replacing SVG images with real photos!")
    print("Using Lorem Picsum for free, high-quality images")
    print()
    
    # Get all posts
    post_files = [f for f in sorted(os.listdir(POSTS_DIR)) if f.endswith('.md')]
    total_posts = len(post_files)
    
    processed = 0
    photos_added = 0
    svgs_removed = 0
    
    for i, filename in enumerate(post_files, 1):
        post_path = os.path.join(POSTS_DIR, filename)
        
        try:
            with open(post_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'title: ["\']([^"\']+)["\']', content)
            if title_match:
                title = title_match.group(1)
            else:
                title = filename.replace('.md', '').replace('-', ' ').title()
            
            base_name = filename.replace('.md', '')
            
            # Check current image status
            svg_exists = os.path.exists(os.path.join(IMAGES_DIR, f"{base_name}.svg"))
            photo_exists = any(os.path.exists(os.path.join(IMAGES_DIR, f"{base_name}.{ext}")) 
                             for ext in ['jpg', 'jpeg', 'png', 'webp'])
            
            print(f"[{i}/{total_posts}] {title}")
            
            # Only process if no photo exists OR if only SVG exists
            if not photo_exists:
                if svg_exists:
                    svgs_removed += 1
                
                image_path, attribution, image_type = fix_post_image(title, base_name)
                
                if image_type == "photo":
                    photos_added += 1
                    print(f"    SUCCESS: {os.path.basename(image_path)}")
                elif image_type == "failed":
                    print(f"    FAILED: Could not download photo")
                
                # Brief pause to be respectful
                time.sleep(0.5)
                
            else:
                print(f"    OK: Already has photo")
            
            processed += 1
            
        except Exception as e:
            print(f"    ERROR: {e}")
            processed += 1
        
        # Progress update
        if i % 10 == 0:
            print(f"\nProgress: {i}/{total_posts} - Photos: {photos_added}, SVGs removed: {svgs_removed}\n")
    
    # Final summary
    print("\n" + "=" * 50)
    print("QUICK PHOTO FIX COMPLETE!")
    print("=" * 50)
    print(f"Posts processed: {processed}")
    print(f"Photos added: {photos_added}")
    print(f"SVGs removed: {svgs_removed}")
    print()
    print("CryptoHedgey says: Your posts now have beautiful photos!")
    print("Much more professional than those SVG placeholders!")
    print()
    print("Next: commit and push your changes!")

if __name__ == "__main__":
    quick_photo_replacement()