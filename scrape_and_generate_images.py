#!/usr/bin/env python3
"""
Enhanced image system: Web scraping for photos with SVG fallback
Priority: 1. Scraped photos, 2. Generated SVG images
"""

import os
import re
import hashlib
import requests
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

# Image search endpoints
UNSPLASH_ACCESS_KEY = None  # Set your Unsplash API key
PEXELS_API_KEY = None       # Set your Pexels API key

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
    """Create an SVG image for a post (fallback)"""
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

def extract_keywords_from_title(title):
    """Extract relevant keywords for image search"""
    # Remove common crypto/finance words that might not yield good stock photos
    crypto_words = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'nft', 'dao']
    
    # Convert title to keywords
    words = re.findall(r'\b\w+\b', title.lower())
    
    # Filter out very common words and crypto-specific terms
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'are', 'is', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
    
    keywords = []
    for word in words:
        if len(word) > 3 and word not in common_words:
            # Map crypto terms to more generic financial/business terms
            if word in crypto_words:
                if word in ['bitcoin', 'ethereum', 'crypto']:
                    keywords.extend(['finance', 'technology', 'business'])
                elif word == 'blockchain':
                    keywords.extend(['technology', 'network', 'digital'])
                elif word == 'defi':
                    keywords.extend(['finance', 'technology'])
                elif word == 'nft':
                    keywords.extend(['digital', 'art', 'technology'])
                elif word == 'dao':
                    keywords.extend(['organization', 'governance'])
            else:
                keywords.append(word)
    
    # Add generic business/finance keywords if no good keywords found
    if not keywords:
        keywords = ['business', 'finance', 'technology', 'growth']
    
    return keywords[:3]  # Use top 3 keywords

def search_unsplash_image(keywords):
    """Search for images on Unsplash"""
    if not UNSPLASH_ACCESS_KEY:
        return None
    
    search_term = ' '.join(keywords)
    url = f"https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": search_term,
        "per_page": 5,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                # Get the first high-quality image
                photo = data['results'][0]
                image_url = photo['urls']['regular']  # 1080px width
                return {
                    'url': image_url,
                    'attribution': f"Photo by {photo['user']['name']} on Unsplash"
                }
    except Exception as e:
        print(f"Unsplash API error: {e}")
    
    return None

def search_pexels_image(keywords):
    """Search for images on Pexels"""
    if not PEXELS_API_KEY:
        return None
    
    search_term = ' '.join(keywords)
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": search_term,
        "per_page": 5,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                # Get the first high-quality image
                photo = data['photos'][0]
                image_url = photo['src']['large']  # Large size
                return {
                    'url': image_url,
                    'attribution': f"Photo by {photo['photographer']} on Pexels"
                }
    except Exception as e:
        print(f"Pexels API error: {e}")
    
    return None

def download_image(image_info, filepath):
    """Download an image from URL"""
    try:
        response = requests.get(image_info['url'], timeout=30)
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
            
            with open(final_filepath, 'wb') as f:
                f.write(response.content)
            
            return final_filepath, image_info['attribution']
    except Exception as e:
        print(f"Error downloading image: {e}")
    
    return None, None

def scrape_image_for_post(title, base_filename):
    """
    Try to find and download a relevant photo for the post
    Priority: Unsplash -> Pexels -> Generated SVG
    """
    keywords = extract_keywords_from_title(title)
    print(f"Searching for images with keywords: {keywords}")
    
    # Try Unsplash first
    image_info = search_unsplash_image(keywords)
    if image_info:
        print(f"Found Unsplash image for: {title}")
        image_path = os.path.join(IMAGES_DIR, base_filename)
        downloaded_path, attribution = download_image(image_info, image_path)
        if downloaded_path:
            return downloaded_path, attribution, "photo"
    
    # Try Pexels as backup
    image_info = search_pexels_image(keywords)
    if image_info:
        print(f"Found Pexels image for: {title}")
        image_path = os.path.join(IMAGES_DIR, base_filename)
        downloaded_path, attribution = download_image(image_info, image_path)
        if downloaded_path:
            return downloaded_path, attribution, "photo"
    
    # Fallback to generated SVG
    print(f"No photos found, generating SVG for: {title}")
    svg_content = create_svg_image(title, base_filename)
    svg_path = os.path.join(IMAGES_DIR, f"{os.path.splitext(base_filename)[0]}.svg")
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    return svg_path, "Generated by Hash & Hedge", "generated"

def process_posts_with_image_scraping():
    """Process all posts and get images (photos preferred, SVG fallback)"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    processed_count = 0
    photo_count = 0
    generated_count = 0
    
    print("Starting image processing...")
    print(f"Unsplash API: {'YES' if UNSPLASH_ACCESS_KEY else 'NO'}")
    print(f"Pexels API: {'YES' if PEXELS_API_KEY else 'NO'}")
    print()
    
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
                
                # Generate base filename for image
                base_name = filename.replace('.md', '')
                
                # Check if image already exists
                existing_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.svg']
                image_exists = False
                for ext in existing_extensions:
                    if os.path.exists(os.path.join(IMAGES_DIR, f"{base_name}{ext}")):
                        image_exists = True
                        print(f"Image already exists for: {base_name}")
                        break
                
                if not image_exists:
                    # Scrape or generate image
                    try:
                        image_path, attribution, image_type = scrape_image_for_post(title, f"{base_name}.jpg")
                        
                        if image_type == "photo":
                            photo_count += 1
                            print(f"[PHOTO] {os.path.basename(image_path)} - {attribution}")
                        else:
                            generated_count += 1
                            print(f"[GENERATED] {os.path.basename(image_path)}")
                        
                        # Rate limiting to be respectful to APIs
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"Error processing {title}: {e}")
                        # Fallback to SVG generation
                        svg_content = create_svg_image(title, f"{base_name}.svg")
                        svg_path = os.path.join(IMAGES_DIR, f"{base_name}.svg")
                        with open(svg_path, 'w', encoding='utf-8') as f:
                            f.write(svg_content)
                        generated_count += 1
                        print(f"[GENERATED] (fallback): {base_name}.svg")
                
                processed_count += 1
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"\nProcessing complete!")
    print(f"Posts processed: {processed_count}")
    print(f"Photos downloaded: {photo_count}")
    print(f"SVGs generated: {generated_count}")
    
    if photo_count == 0 and UNSPLASH_ACCESS_KEY is None and PEXELS_API_KEY is None:
        print("\nWARNING: No API keys configured. Set UNSPLASH_ACCESS_KEY or PEXELS_API_KEY for photo downloads.")

if __name__ == "__main__":
    # You can set your API keys here or as environment variables
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
    
    process_posts_with_image_scraping()