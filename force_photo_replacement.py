#!/usr/bin/env python3
"""
Force Photo Replacement System for Hash & Hedge
Replaces ALL SVG images with real photos from Unsplash/Pexels
"""

import os
import re
import hashlib
import requests
import time
from urllib.parse import urljoin, urlparse

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

# Free APIs for photos - You can get these keys from:
# Unsplash: https://unsplash.com/developers
# Pexels: https://www.pexels.com/api/
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_KEY_HERE"  # Replace with your key
PEXELS_API_KEY = "YOUR_PEXELS_KEY_HERE"         # Replace with your key

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
    """Create an SVG image for a post (ONLY as absolute last fallback)"""
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

def extract_financial_keywords(title):
    """Extract financial keywords for better image search"""
    # Enhanced keyword mapping for financial content
    financial_mapping = {
        # Crypto terms -> visual concepts
        'bitcoin': ['cryptocurrency', 'digital currency', 'blockchain technology', 'financial technology'],
        'ethereum': ['blockchain', 'smart contracts', 'cryptocurrency', 'technology'],
        'crypto': ['cryptocurrency', 'digital money', 'blockchain', 'finance technology'],
        'blockchain': ['technology', 'digital network', 'computer technology', 'innovation'],
        'defi': ['decentralized finance', 'financial technology', 'digital banking', 'fintech'],
        'nft': ['digital art', 'blockchain art', 'cryptocurrency art', 'digital assets'],
        'trading': ['stock market', 'financial charts', 'investment', 'business analytics'],
        'market': ['stock exchange', 'financial data', 'business charts', 'economic growth'],
        'analysis': ['business analytics', 'financial charts', 'data visualization', 'graphs'],
        'price': ['financial charts', 'stock market', 'investment graphs', 'business data'],
        'security': ['cybersecurity', 'digital security', 'computer security', 'data protection'],
        'wallet': ['digital wallet', 'mobile payment', 'financial technology', 'digital banking'],
        'mining': ['data center', 'computer servers', 'technology infrastructure', 'digital mining'],
        'staking': ['investment', 'financial growth', 'passive income', 'digital assets'],
        'governance': ['corporate governance', 'business meeting', 'boardroom', 'leadership'],
        'compliance': ['legal documents', 'business compliance', 'corporate law', 'regulations'],
        'audit': ['financial audit', 'accounting', 'business documents', 'financial review'],
        'yield': ['investment returns', 'financial growth', 'profit charts', 'ROI'],
        'protocol': ['technology infrastructure', 'network systems', 'digital architecture', 'tech'],
        'smart contracts': ['legal technology', 'digital contracts', 'automation', 'blockchain'],
        'institutional': ['corporate finance', 'business building', 'institutional investors', 'finance'],
        'regulation': ['legal documents', 'government building', 'compliance', 'law'],
    }
    
    # Convert title to lowercase for matching
    title_lower = title.lower()
    keywords = []
    
    # Find matching financial terms and get visual alternatives
    for term, visual_concepts in financial_mapping.items():
        if term in title_lower:
            keywords.extend(visual_concepts[:2])  # Take first 2 concepts
    
    # If no specific matches, use general business/finance terms
    if not keywords:
        keywords = ['business', 'finance', 'technology', 'growth', 'success']
    
    # Add generic business terms to improve results
    keywords.extend(['professional', 'modern'])
    
    return keywords[:4]  # Return top 4 keywords

def search_unsplash_image(keywords):
    """Search for images on Unsplash with better error handling"""
    if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_KEY_HERE":
        print("⚠️  Unsplash API key not configured")
        return None
    
    search_term = ' '.join(keywords)
    url = f"https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": search_term,
        "per_page": 10,
        "orientation": "landscape",
        "order_by": "relevant"
    }
    
    try:
        print(f"🔍 Searching Unsplash for: {search_term}")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Get the best quality image
                photo = data['results'][0]
                image_url = photo['urls']['regular']  # 1080px width
                return {
                    'url': image_url,
                    'attribution': f"Photo by {photo['user']['name']} on Unsplash",
                    'title': photo.get('description', 'Financial image'),
                    'tags': photo.get('tags', [])
                }
        else:
            print(f"❌ Unsplash API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Unsplash API error: {e}")
    
    return None

def search_pexels_image(keywords):
    """Search for images on Pexels with better error handling"""
    if PEXELS_API_KEY == "YOUR_PEXELS_KEY_HERE":
        print("⚠️  Pexels API key not configured")
        return None
    
    search_term = ' '.join(keywords)
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": search_term,
        "per_page": 10,
        "orientation": "landscape",
        "size": "large"
    }
    
    try:
        print(f"🔍 Searching Pexels for: {search_term}")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                # Get the best quality image
                photo = data['photos'][0]
                image_url = photo['src']['large']  # Large size
                return {
                    'url': image_url,
                    'attribution': f"Photo by {photo['photographer']} on Pexels",
                    'title': photo.get('alt', 'Financial image'),
                    'tags': []
                }
        else:
            print(f"❌ Pexels API error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Pexels API error: {e}")
    
    return None

def download_image(image_info, filepath):
    """Download an image from URL with better error handling"""
    try:
        print(f"📥 Downloading image from: {image_info['url'][:50]}...")
        response = requests.get(image_info['url'], timeout=30, stream=True)
        
        if response.status_code == 200:
            # Determine file extension from content type or URL
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'webp' in content_type:
                ext = '.webp'
            else:
                # Fallback to URL extension
                parsed_url = urlparse(image_info['url'])
                ext = os.path.splitext(parsed_url.path)[1] or '.jpg'
            
            # Update filepath with correct extension
            base_filepath = os.path.splitext(filepath)[0]
            final_filepath = base_filepath + ext
            
            # Download with streaming for large files
            with open(final_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(final_filepath)
            print(f"✅ Downloaded: {os.path.basename(final_filepath)} ({file_size // 1024} KB)")
            
            return final_filepath, image_info['attribution']
            
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
    
    return None, None

def force_photo_for_post(title, base_filename, current_svg_path=None):
    """
    Force download a real photo for a post, removing SVG if it exists
    Returns: (image_path, attribution, image_type)
    """
    keywords = extract_financial_keywords(title)
    print(f"\n📝 Processing: {title}")
    print(f"🔑 Keywords: {keywords}")
    
    # Remove existing SVG if it exists
    if current_svg_path and os.path.exists(current_svg_path):
        os.remove(current_svg_path)
        print(f"🗑️  Removed SVG: {os.path.basename(current_svg_path)}")
    
    # Try multiple keyword combinations for better results
    keyword_combinations = [
        keywords,
        keywords[:2] + ['business', 'professional'],
        ['finance', 'business', 'technology'],
        ['cryptocurrency', 'blockchain', 'digital'],
        ['business', 'growth', 'success', 'professional']
    ]
    
    for attempt, kw_combo in enumerate(keyword_combinations, 1):
        print(f"🔄 Attempt {attempt}: {kw_combo}")
        
        # Try Unsplash first
        image_info = search_unsplash_image(kw_combo)
        if image_info:
            image_path = os.path.join(IMAGES_DIR, base_filename)
            downloaded_path, attribution = download_image(image_info, image_path)
            if downloaded_path:
                return downloaded_path, attribution, "photo"
        
        # Try Pexels as backup
        image_info = search_pexels_image(kw_combo)
        if image_info:
            image_path = os.path.join(IMAGES_DIR, base_filename)
            downloaded_path, attribution = download_image(image_info, image_path)
            if downloaded_path:
                return downloaded_path, attribution, "photo"
        
        # Brief pause between attempts
        time.sleep(1)
    
    # Absolute fallback: create SVG (should rarely happen with API keys)
    print(f"⚠️  No photos found for {title}, creating SVG fallback")
    svg_content = create_svg_image(title, base_filename)
    svg_path = os.path.join(IMAGES_DIR, f"{os.path.splitext(base_filename)[0]}.svg")
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return svg_path, "Generated by Hash & Hedge", "generated"

def process_all_posts_force_photos():
    """Process all posts and FORCE photo downloads, removing SVGs"""
    if not os.path.exists(POSTS_DIR):
        print(f"❌ Posts directory not found: {POSTS_DIR}")
        return
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    print("🦔 CryptoHedgey's Photo Enhancement Mission")
    print("=" * 60)
    print("Replacing ALL SVG images with real photos!")
    print(f"📁 Posts directory: {POSTS_DIR}")
    print(f"📁 Images directory: {IMAGES_DIR}")
    print(f"🔑 Unsplash API: {'✅ CONFIGURED' if UNSPLASH_ACCESS_KEY != 'YOUR_UNSPLASH_KEY_HERE' else '❌ NOT CONFIGURED'}")
    print(f"🔑 Pexels API: {'✅ CONFIGURED' if PEXELS_API_KEY != 'YOUR_PEXELS_KEY_HERE' else '❌ NOT CONFIGURED'}")
    print()
    
    if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_KEY_HERE" and PEXELS_API_KEY == "YOUR_PEXELS_KEY_HERE":
        print("⚠️  WARNING: No API keys configured!")
        print("   Get free keys from:")
        print("   - Unsplash: https://unsplash.com/developers")
        print("   - Pexels: https://www.pexels.com/api/")
        print("   Without API keys, all images will be SVG fallbacks.")
        print()
        
        proceed = input("Continue without API keys? (y/n): ").lower()
        if proceed != 'y':
            print("Cancelled.")
            return
    
    processed_count = 0
    photo_count = 0
    svg_removed_count = 0
    generated_count = 0
    
    # Get all posts
    post_files = [f for f in sorted(os.listdir(POSTS_DIR)) if f.endswith('.md')]
    total_posts = len(post_files)
    
    print(f"📊 Processing {total_posts} posts...")
    print()
    
    for i, filename in enumerate(post_files, 1):
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
            
            # Generate base filename for image
            base_name = filename.replace('.md', '')
            
            # Check for existing SVG
            svg_path = os.path.join(IMAGES_DIR, f"{base_name}.svg")
            has_svg = os.path.exists(svg_path)
            
            # Check for existing photos
            photo_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            has_photo = False
            for ext in photo_extensions:
                if os.path.exists(os.path.join(IMAGES_DIR, f"{base_name}{ext}")):
                    has_photo = True
                    break
            
            print(f"[{i}/{total_posts}] {base_name}")
            
            # Force photo download if no photo exists OR if only SVG exists
            if not has_photo or (has_svg and not has_photo):
                if has_svg:
                    svg_removed_count += 1
                
                image_path, attribution, image_type = force_photo_for_post(
                    title, f"{base_name}.jpg", svg_path if has_svg else None
                )
                
                if image_type == "photo":
                    photo_count += 1
                    print(f"    ✅ PHOTO: {os.path.basename(image_path)}")
                    print(f"    📝 {attribution}")
                else:
                    generated_count += 1
                    print(f"    ⚠️  SVG: {os.path.basename(image_path)}")
                
                # Rate limiting for API respect
                time.sleep(2)
                
            else:
                print(f"    ✅ Already has photo")
            
            processed_count += 1
            
        except Exception as e:
            print(f"    ❌ Error processing {filename}: {e}")
            processed_count += 1
        
        # Progress indicator
        if i % 10 == 0:
            print(f"\n📈 Progress: {i}/{total_posts} posts processed")
            print(f"📸 Photos downloaded: {photo_count}")
            print(f"🗑️  SVGs removed: {svg_removed_count}")
            print()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 CRYPTOHEDGEY'S PHOTO MISSION COMPLETE!")
    print("=" * 60)
    print(f"📊 Total posts processed: {processed_count}")
    print(f"📸 Real photos downloaded: {photo_count}")
    print(f"🗑️  SVG images removed: {svg_removed_count}")
    print(f"⚠️  SVG fallbacks created: {generated_count}")
    print()
    
    if photo_count > 0:
        print(f"🦔 CryptoHedgey says: Great success! {photo_count} posts now have beautiful photos!")
        print("   Your site will look much more professional and engaging!")
    else:
        print("🦔 CryptoHedgey says: No photos were downloaded.")
        print("   Make sure your API keys are configured properly!")
    
    print("\n🎯 Next steps:")
    print("1. Check a few images to verify they look good")
    print("2. Commit changes: git add . && git commit -m 'Replace SVGs with photos'")
    print("3. Deploy: git push origin main")

if __name__ == "__main__":
    # Set your API keys here before running!
    # Get free keys from:
    # Unsplash: https://unsplash.com/developers  
    # Pexels: https://www.pexels.com/api/
    
    print("🦔 Hash & Hedge Photo Replacement System")
    print("Make sure to set your API keys at the top of this file!")
    print()
    
    process_all_posts_force_photos()