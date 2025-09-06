#!/usr/bin/env python3
"""
Hash & Hedge Hero Image Fetcher
Automatically fetches and downloads hero images for all blog posts
"""

import os
import re
import time
import requests
import frontmatter
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_free_crypto_image(keyword):
    """Fetch crypto-related images from free sources"""
    # Use Unsplash API (no key needed for basic usage)
    search_urls = [
        f"https://source.unsplash.com/1200x600/?{keyword},cryptocurrency",
        f"https://source.unsplash.com/1200x600/?{keyword},bitcoin",
        f"https://source.unsplash.com/1200x600/?{keyword},finance",
        f"https://source.unsplash.com/1200x600/?{keyword},trading"
    ]
    
    for url in search_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.content, response.url
        except:
            continue
    return None, None

def sanitize_filename(title):
    """Create safe filename from title"""
    filename = re.sub(r'[^a-z0-9]+', '-', title.lower())
    filename = re.sub(r'-+', '-', filename).strip('-')
    return filename[:100] if len(filename) > 100 else filename
def fetch_og_image(url):
    """Try to fetch Open Graph image from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Try Twitter image
        twitter_image = soup.find('meta', {'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            return twitter_image['content']
            
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
    return None

def process_posts(content_dir, images_dir):
    """Process all posts and fetch hero images"""
    
    # Ensure images directory exists
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    
    posts_processed = 0
    images_fetched = 0
    
    # Find all markdown files
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)                
                try:
                    # Load post with frontmatter
                    with open(filepath, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    posts_processed += 1
                    
                    # Skip if image already exists
                    if 'image' in post.metadata and post.metadata['image']:
                        if not post.metadata['image'].startswith('/images/posts/'):
                            continue
                    
                    # Generate image based on title or tags
                    title = post.metadata.get('title', 'crypto')
                    tags = post.metadata.get('tags', ['bitcoin'])
                    keyword = tags[0] if tags else title.split()[0]
                    
                    print(f"Fetching image for: {title}")
                    
                    # Try to get image from sources or generate
                    sources = post.metadata.get('sources', [])
                    image_url = None
                    
                    # Try sources first
                    for source in sources[:2]:
                        if isinstance(source, dict) and 'url' in source:
                            image_url = fetch_og_image(source['url'])
                            if image_url:
                                break
                    
                    # If no source image, get free crypto image
                    if not image_url:
                        image_data, _ = get_free_crypto_image(keyword)
                        if image_data:
                            filename = f"{sanitize_filename(title)}.jpg"
                            save_path = os.path.join(images_dir, filename)
                            
                            with open(save_path, 'wb') as f:
                                f.write(image_data)
                            
                            # Update post frontmatter
                            post.metadata['image'] = f"/images/posts/{filename}"
                            
                            # Save updated post
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(frontmatter.dumps(post))
                            
                            images_fetched += 1
                            print(f"✓ Saved image for: {title}")
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\n✅ Processed {posts_processed} posts, fetched {images_fetched} images")

if __name__ == "__main__":
    content_dir = r"C:\Users\gnul\hashnhedge\site\content"
    images_dir = r"C:\Users\gnul\hashnhedge\site\static\images\posts"
    
    print("Starting hero image fetch for Hash & Hedge...")
    print("=" * 50)
    
    process_posts(content_dir, images_dir)
    
    print("\n✨ Hero image fetch complete!")
    print("Run 'hugo server' to preview your site with images")