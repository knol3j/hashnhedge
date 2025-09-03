#!/usr/bin/env python3
"""
fetch_images.py - Because a wall of text without pictures is like 
a strip club without poles. Technically functional, but nobody's impressed.
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
    Sucks images from the internet like a digital leech, because 
    original photography is for people with talent and time.
    """
    
    def __init__(self, site_path: str = "site"):
        self.site_path = Path(site_path)
        self.posts_path = self.site_path / "content" / "posts"
        self.images_path = self.site_path / "static" / "images" / "posts"
        self.images_path.mkdir(parents=True, exist_ok=True)
        
        # User agent because websites are paranoid
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def extract_image_from_url(self, url: str) -> str:
        """
        Rip the prettiest picture from a webpage like stealing candy from 
        a baby, except the baby is a copyright lawyer and the candy is pixels.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try Open Graph image first (Facebook's gift to the internet)
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                return urljoin(url, og_image['content'])
            
            # Twitter card image (because Elon needs love too)
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                return urljoin(url, twitter_image['content'])
            
            # Look for the first decent image on the page (desperate times)
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src', '')
                if src and not any(skip in src.lower() for skip in 
                                 ['logo', 'icon', 'avatar', 'profile', 'ad']):
                    # Check if it's reasonably sized (not some 1x1 tracking pixel)
                    width = img.get('width', '999')
                    height = img.get('height', '999')
                    try:
                        if int(width) > 200 and int(height) > 200:
                            return urljoin(url, src)
                    except:
                        pass
                        
            return None
            
        except Exception as e:
            print(f"💩 Failed to extract image from {url}: {e}")
            return None
    
    def download_image(self, image_url: str, filename: str) -> str:
        """
        Download an image and save it locally, because hotlinking is for 
        amateurs and people who enjoy cease-and-desist letters.
        """
        try:
            response = requests.get(image_url, headers=self.headers, 
                                  timeout=15, stream=True)
            response.raise_for_status()
            
            # Get file extension from URL or content type (trust nobody)
            ext = Path(urlparse(image_url).path).suffix.lower()
            if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                content_type = response.headers.get('content-type', '')
                if 'jpeg' in content_type or 'jpg' in content_type:
                    ext = '.jpg'
                elif 'png' in content_type:
                    ext = '.png'
                elif 'webp' in content_type:
                    ext = '.webp'
                else:
                    ext = '.jpg'  # When in doubt, JPEG it out
            
            # Clean filename like we're hiding evidence
            clean_filename = re.sub(r'[^\w\s-]', '', filename)
            clean_filename = re.sub(r'[-\s]+', '-', clean_filename)[:100]
            
            image_path = self.images_path / f"{clean_filename}{ext}"
            
            # Download with the enthusiasm of a teenager cleaning their room
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            # Return the web path, not the file system path
            return f"/images/posts/{image_path.name}"
            
        except Exception as e:
            print(f"💥 Failed to download {image_url}: {e}")
            return None
    
    def process_posts(self):
        """
        Crawl through posts like a digital grave robber, stealing images 
        from the internet to dress up our corpse of content.
        """
        updated_count = 0
        failed_count = 0
        
        # Find all markdown posts (the bodies we need to beautify)
        for post_file in self.posts_path.rglob("*.md"):
            try:
                # Load the post
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Skip if already has an image (we're lazy, not stupid)
                if post.get('image'):
                    continue
                    
                # Get source URL
                source_url = post.get('source_url')
                if not source_url:
                    print(f"⚠️ No source URL for {post_file.name}")
                    continue
                
                print(f"🔍 Processing: {post.get('title', 'Untitled')}")
                
                # Extract image from source
                image_url = self.extract_image_from_url(source_url)
                if not image_url:
                    print(f"  ❌ No image found")
                    failed_count += 1
                    continue
                
                # Download and save
                filename = post_file.stem
                local_path = self.download_image(image_url, filename)
                
                if local_path:
                    # Update frontmatter with our stolen goods
                    post['image'] = local_path
                    post['image_alt'] = post.get('title', 'Article image')
                    
                    # Save the updated post
                    with open(post_file, 'w', encoding='utf-8') as f:
                        f.write(frontmatter.dumps(post))
                    
                    print(f"  ✅ Added image: {local_path}")
                    updated_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                print(f"💀 Error processing {post_file}: {e}")
                failed_count += 1
                
        print(f"\n📊 Summary: {updated_count} updated, {failed_count} failed")
        print("🎭 The show must go on, with or without pretty pictures.")

def main():
    """Main function - where dreams come to die and images come to life."""
    print("🖼️ Hash & Hedge Image Vampire v1.0")
    print("Sucking images from the internet since 5 minutes ago")
    print("=" * 60)
    
    vampire = ImageVampire()
    vampire.process_posts()

if __name__ == "__main__":
    main()