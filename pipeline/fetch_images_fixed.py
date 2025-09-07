#!/usr/bin/env python3
"""
fetch_images_fixed.py - Fixed version without emojis
"""

import os
import re
import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import frontmatter
from urllib.parse import urljoin, urlparse

class ImageVampire:
    """
    Fetches images from URLs in post front matter
    """
    
    def __init__(self, site_path: str = "site"):
        self.site_path = Path(site_path)
        self.posts_path = self.site_path / "content" / "posts"
        self.images_path = self.site_path / "static" / "images" / "posts"
        self.images_path.mkdir(parents=True, exist_ok=True)
        
        # User agent 
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_image_from_url(self, url: str) -> str:
        """
        Extract the main image from a webpage
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try Open Graph image first
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return urljoin(url, og_image['content'])
            
            # Twitter card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                return urljoin(url, twitter_image['content'])
            
            # First large image in article
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and ('width' not in img.attrs or int(img.get('width', 0)) > 400):
                    return urljoin(url, src)
                    
            return None
            
        except Exception as e:
            print(f"Error extracting image from {url}: {e}")
            return None
    
    def download_image(self, image_url: str, post_slug: str) -> str:
        """
        Download an image and save it locally
        """
        try:
            response = requests.get(image_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # Get file extension from URL or content-type
            parsed = urlparse(image_url)
            ext = Path(parsed.path).suffix.lower()
            
            if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'webp' in content_type:
                    ext = '.webp'
                else:
                    ext = '.jpg'  # Default
            
            # Create post-specific directory
            post_dir = self.images_path / post_slug
            post_dir.mkdir(exist_ok=True)
            
            # Save the image
            image_filename = f"hero{ext}"
            image_path = post_dir / image_filename
            
            with open(image_path, 'wb') as f:
                f.write(response.content)
                
            # Return the Hugo-friendly path
            return f"/images/posts/{post_slug}/{image_filename}"
            
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
    
    def process_posts(self):
        """
        Process all posts in the content directory
        """
        updated_count = 0
        failed_count = 0
        
        # Process all markdown files
        for post_file in self.posts_path.glob('*.md'):
            print(f"\nProcessing: {post_file.name}")
            
            try:
                # Read the post
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Get post slug
                post_slug = post_file.stem
                
                # Skip if already has a featured_image
                if post.metadata.get('featured_image'):
                    print(f"  -> Already has featured image")
                    continue
                
                # Look for source URLs in metadata
                sources = []
                if 'sources' in post.metadata:
                    sources = post.metadata.get('sources', [])
                elif 'source' in post.metadata:
                    sources = [post.metadata.get('source')]
                
                # Try to extract image from first source
                image_path = None
                for source in sources:
                    if isinstance(source, str) and source.startswith('http'):
                        print(f"  -> Checking source: {source}")
                        image_url = self.extract_image_from_url(source)
                        
                        if image_url:
                            print(f"  -> Found image: {image_url}")
                            image_path = self.download_image(image_url, post_slug)
                            if image_path:
                                break
                
                # Update post with image
                if image_path:
                    post.metadata['featured_image'] = image_path
                    post.metadata['image'] = image_path
                    
                    # Add to images array if not present
                    if 'images' not in post.metadata:
                        post.metadata['images'] = []
                    if image_path not in post.metadata['images']:
                        post.metadata['images'].append(image_path)
                    
                    # Save updated post
                    with open(post_file, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(post))
                    
                    print(f"  -> Updated with image: {image_path}")
                    updated_count += 1
                else:
                    print(f"  -> No image found")
                    failed_count += 1
                    
            except Exception as e:
                print(f"  -> Error: {e}")
                failed_count += 1
                
        print(f"\nSummary: {updated_count} updated, {failed_count} failed")

def main():
    """Main function"""
    print("Hash & Hedge Image Fetcher v1.0")
    print("Fetching images for blog posts")
    print("=" * 60)
    
    vampire = ImageVampire()
    vampire.process_posts()

if __name__ == "__main__":
    main()