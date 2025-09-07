#!/usr/bin/env python3
"""
Quick Photo Fix for Hash & Hedge
Uses Lorem Picsum and other free APIs to get real photos for all posts
No API keys required!
"""

import os
import re
import hashlib
import requests
import time
from urllib.parse import urljoin, urlparse

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

def extract_photo_keywords(title):
    """Extract keywords and map to photo categories"""
    # Map crypto/finance terms to visual photo categories
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
        'yield': 'nature',  # Growth concept
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
    
    # Check for matches
    for term, category in keyword_mapping.items():
        if term in title_lower:
            return category
    
    # Default fallback
    return 'business'

def get_lorem_picsum_image(category, width=800, height=400):
    """Get a random image from Lorem Picsum based on category"""
    # Lorem Picsum category mapping (using their seed system)
    category_seeds = {
        'business': ['1', '2', '3', '4', '5', '10', '15', '20', '25', '30'],
        'technology': ['100', '101', '102', '103', '104', '110', '115', '120', '125', '130'],
        'nature': ['200', '201', '202', '203', '204', '210', '215', '220', '225', '230'],
        'abstract': ['300', '301', '302', '303', '304', '310', '315', '320', '325', '330']
    }
    
    import random
    seeds = category_seeds.get(category, category_seeds['business'])
    seed = random.choice(seeds)
    
    # Lorem Picsum URL with seed for consistent but varied images
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
            # Always save as JPG for Lorem Picsum
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

def create_svg_fallback(title, filename):
    """Create SVG as absolute fallback"""
    hash_object = hashlib.md5(title.encode())
    hex_dig = hash_object.hexdigest()
    primary_color = f"#{hex_dig[:6]}"
    
    # Simple complementary color
    r = int(primary_color[1:3], 16)
    g = int(primary_color[3:5], 16)  
    b = int(primary_color[5:7], 16)
    comp_color = f"#{255-r:02x}{255-g:02x}{255-b:02x}"
    
    display_title = title[:35] + "..." if len(title) > 35 else title
    
    svg_content = f'''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{primary_color};stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:{comp_color};stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect width="800" height="400" fill="url(#grad)" />
  <text x="400" y="200" font-family="Arial" font-size="24" font-weight="bold" 
        text-anchor="middle" fill="white">{display_title}</text>
  <text x="400" y="230" font-family="Arial" font-size="14" 
        text-anchor="middle" fill="white" opacity="0.8">Hash & Hedge 🦔</text>
</svg>'''
    
    return svg_content

def fix_post_image(title, base_filename):
    """Fix a single post's image - force photo download"""
    category = extract_photo_keywords(title)
    print(f"Category: {category}")
    
    # Remove existing SVG if it exists
    svg_path = os.path.join(IMAGES_DIR, f"{base_filename}.svg")
    if os.path.exists(svg_path):
        os.remove(svg_path)
        print(f"🗑️  Removed: {base_filename}.svg")
    
    # Try to get a real photo
    image_info = get_lorem_picsum_image(category)
    image_path = os.path.join(IMAGES_DIR, f"{base_filename}.jpg")
    
    downloaded_path, attribution = download_image_simple(image_info, image_path)
    
    if downloaded_path:
        return downloaded_path, attribution, "photo"
    
    # Fallback to SVG only if download fails
    print(f"⚠️  Photo download failed, creating SVG fallback...")
    svg_content = create_svg_fallback(title, base_filename)
    svg_path = os.path.join(IMAGES_DIR, f"{base_filename}.svg")
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return svg_path, "Generated by Hash & Hedge", "svg"

def quick_photo_replacement():
    """Replace SVG images with photos for all posts"""
    if not os.path.exists(POSTS_DIR):
        print(f"❌ Posts directory not found: {POSTS_DIR}")
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
                    print(f"    ✅ PHOTO: {os.path.basename(image_path)}")
                else:
                    print(f"    ⚠️  SVG: {os.path.basename(image_path)}")
                
                # Brief pause to be respectful
                time.sleep(0.5)
                
            else:
                print(f"    ✅ Already has photo")
            
            processed += 1
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            processed += 1
        
        # Progress update
        if i % 10 == 0:
            print(f"\n📈 Progress: {i}/{total_posts} - Photos: {photos_added}, SVGs removed: {svgs_removed}\n")
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 QUICK PHOTO FIX COMPLETE!")
    print("=" * 50)
    print(f"📊 Posts processed: {processed}")
    print(f"📸 Photos added: {photos_added}")
    print(f"🗑️  SVGs removed: {svgs_removed}")
    print()
    print("🦔 CryptoHedgey says: Your posts now have beautiful photos!")
    print("   Much more professional than those SVG placeholders!")
    print()
    print("🎯 Next: commit and push your changes!")

if __name__ == "__main__":
    quick_photo_replacement()