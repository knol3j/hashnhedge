#!/usr/bin/env python3
"""
Comprehensive script to fix image display issues and consolidate all stories.
"""
import os
import re
import shutil
import yaml
import frontmatter
from pathlib import Path
import requests
import hashlib
from datetime import datetime
import json

class StoryConsolidator:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.hugo_content_dir = self.base_dir / "site" / "content" / "posts"
        self.hugo_static_dir = self.base_dir / "site" / "static"
        self.jekyll_posts_dir = self.base_dir / "_posts"
        self.images_dir = self.base_dir / "images"
        self.site_images_dir = self.hugo_static_dir / "images"
        
        # Ensure directories exist
        self.hugo_content_dir.mkdir(parents=True, exist_ok=True)
        self.site_images_dir.mkdir(parents=True, exist_ok=True)
        (self.site_images_dir / "posts").mkdir(parents=True, exist_ok=True)
        
    def generate_fallback_image(self, title, output_path):
        """Generate a simple SVG placeholder image."""
        # Create a simple SVG with the title
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a1a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2d3748;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg)"/>
  <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="48" font-weight="bold" 
        fill="#ffffff" text-anchor="middle" dominant-baseline="middle">
    Hash &amp; Hedge
  </text>
  <text x="50%" y="60%" font-family="Arial, sans-serif" font-size="24" 
        fill="#cbd5e0" text-anchor="middle" dominant-baseline="middle">
    {title[:50]}{'...' if len(title) > 50 else ''}
  </text>
  <circle cx="100" cy="530" r="30" fill="#38b2ac"/>
  <text x="100" y="540" font-family="Arial, sans-serif" font-size="20" font-weight="bold" 
        fill="#ffffff" text-anchor="middle">🦔</text>
</svg>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return True

    def fix_image_paths(self):
        """Fix image path references in all Hugo posts."""
        fixed_count = 0
        
        for post_file in self.hugo_content_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Check if image exists and fix path
                if 'image' in post.metadata:
                    image_path = post.metadata['image']
                    
                    # Convert to expected path format
                    if image_path.startswith('/images/'):
                        expected_file = self.site_images_dir / image_path[1:]  # Remove leading /
                    else:
                        expected_file = self.site_images_dir / "posts" / f"{post_file.stem}.svg"
                        post.metadata['image'] = f"/images/posts/{post_file.stem}.svg"
                    
                    # Generate image if it doesn't exist
                    if not expected_file.exists():
                        expected_file.parent.mkdir(parents=True, exist_ok=True)
                        title = post.metadata.get('title', post_file.stem.replace('-', ' ').title())
                        self.generate_fallback_image(title, expected_file)
                        print(f"Generated image for: {post_file.name}")
                
                # Write back the updated post
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))
                
                fixed_count += 1
                
            except Exception as e:
                print(f"Error processing {post_file}: {e}")
        
        return fixed_count

    def migrate_jekyll_posts(self):
        """Migrate Jekyll posts to Hugo format."""
        migrated_count = 0
        
        if not self.jekyll_posts_dir.exists():
            return 0
            
        for post_file in self.jekyll_posts_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                # Convert Jekyll frontmatter to Hugo format
                hugo_metadata = {
                    'title': post.metadata.get('title', post_file.stem.replace('-', ' ').title()),
                    'date': post.metadata.get('date', datetime.now().isoformat()),
                    'draft': False,
                    'tags': post.metadata.get('tags', []),
                    'categories': post.metadata.get('categories', ['crypto']),
                    'summary': post.metadata.get('summary', '')[:160],
                }
                
                # Handle image
                if 'image' in post.metadata:
                    hugo_metadata['image'] = post.metadata['image']
                else:
                    # Generate image
                    image_filename = f"{post_file.stem}.svg"
                    image_path = self.site_images_dir / "posts" / image_filename
                    image_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    title = hugo_metadata['title']
                    self.generate_fallback_image(title, image_path)
                    hugo_metadata['image'] = f"/images/posts/{image_filename}"
                
                # SEO enhancements
                hugo_metadata['seo'] = {
                    'title': f"{hugo_metadata['title']} | Hash & Hedge",
                    'description': hugo_metadata['summary'] or f"Expert analysis on {hugo_metadata['title'].lower()} with market insights and trends",
                    'keywords': ['cryptocurrency', 'bitcoin', 'finance', 'analysis'] + hugo_metadata['tags'][:6]
                }
                
                # Create new Hugo post
                hugo_filename = post_file.name
                if not hugo_filename.startswith('20'):
                    # Add date prefix if missing
                    date_obj = datetime.fromisoformat(hugo_metadata['date'].replace('Z', '+00:00').replace(' +0000', '+00:00'))
                    hugo_filename = f"{date_obj.strftime('%Y-%m-%d')}-{hugo_filename}"
                
                hugo_post_path = self.hugo_content_dir / hugo_filename
                
                # Create Hugo post with enhanced content
                hugo_post = frontmatter.Post(post.content, **hugo_metadata)
                
                with open(hugo_post_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(hugo_post))
                
                migrated_count += 1
                print(f"Migrated: {post_file.name} -> {hugo_filename}")
                
            except Exception as e:
                print(f"Error migrating {post_file}: {e}")
        
        return migrated_count

    def enhance_seo_metadata(self):
        """Enhance SEO metadata for all posts."""
        enhanced_count = 0
        
        for post_file in self.hugo_content_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                title = post.metadata.get('title', '')
                
                # Enhance SEO metadata
                if 'seo' not in post.metadata:
                    post.metadata['seo'] = {}
                
                seo = post.metadata['seo']
                
                if not seo.get('title'):
                    seo['title'] = f"{title} | Hash & Hedge - Crypto & Finance Insights"
                
                if not seo.get('description'):
                    summary = post.metadata.get('summary', '')
                    if not summary and post.content:
                        # Extract first paragraph as summary
                        content_lines = [line.strip() for line in post.content.split('\n') if line.strip() and not line.startswith('#')]
                        summary = content_lines[0] if content_lines else f"Expert analysis on {title.lower()}"
                    seo['description'] = summary[:160]
                
                if not seo.get('keywords'):
                    keywords = ['cryptocurrency', 'bitcoin', 'finance', 'analysis', 'trading']
                    if 'tags' in post.metadata:
                        keywords.extend(post.metadata['tags'][:5])
                    if 'categories' in post.metadata:
                        keywords.extend(post.metadata['categories'][:3])
                    seo['keywords'] = list(set(keywords))[:10]
                
                # Add Open Graph and Twitter metadata
                seo['og_type'] = 'article'
                seo['og_image'] = post.metadata.get('image', '/images/default-hero.svg')
                seo['twitter_card'] = 'summary_large_image'
                seo['twitter_image'] = seo['og_image']
                
                # Add canonical URL
                slug = post_file.stem
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', slug)
                if date_match:
                    date_str = date_match.group(1)
                    year, month, day = date_str.split('-')
                    clean_slug = slug.replace(f"{date_str}-", "")
                    seo['canonical'] = f"https://hashnhedge.com/{year}/{month}/{clean_slug}/"
                
                # Write back the enhanced post
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))
                
                enhanced_count += 1
                
            except Exception as e:
                print(f"Error enhancing SEO for {post_file}: {e}")
        
        return enhanced_count

    def create_category_pages(self):
        """Create category and tag pages for better SEO."""
        categories = set()
        tags = set()
        
        # Collect all categories and tags
        for post_file in self.hugo_content_dir.glob("*.md"):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                if 'categories' in post.metadata:
                    categories.update(post.metadata['categories'])
                if 'tags' in post.metadata:
                    tags.update(post.metadata['tags'])
                    
            except Exception as e:
                print(f"Error reading {post_file}: {e}")
        
        # Create category pages
        categories_dir = self.base_dir / "site" / "content" / "categories"
        categories_dir.mkdir(parents=True, exist_ok=True)
        
        for category in categories:
            category_page = categories_dir / f"{category.lower().replace(' ', '-')}" / "_index.md"
            category_page.parent.mkdir(parents=True, exist_ok=True)
            
            if not category_page.exists():
                content = f"""---
title: "{category.title()} News & Analysis"
description: "Latest {category.lower()} news, analysis, and insights from Hash & Hedge"
layout: category
url: /categories/{category.lower().replace(' ', '-')}/
---

# {category.title()} News & Analysis

Stay updated with the latest {category.lower()} news, expert analysis, and market insights from Hash & Hedge.
"""
                with open(category_page, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # Create tags pages
        tags_dir = self.base_dir / "site" / "content" / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)
        
        for tag in tags:
            tag_page = tags_dir / f"{tag.lower().replace(' ', '-')}" / "_index.md"
            tag_page.parent.mkdir(parents=True, exist_ok=True)
            
            if not tag_page.exists():
                content = f"""---
title: "#{tag.title()}"
description: "All posts tagged with {tag.lower()} - expert insights and analysis"
layout: tag
url: /tags/{tag.lower().replace(' ', '-')}/
---

# Posts tagged with #{tag.title()}

Explore all our content related to {tag.lower()}.
"""
                with open(tag_page, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        return len(categories), len(tags)

def main():
    consolidator = StoryConsolidator('/home/user/webapp')
    
    print("🔧 Starting comprehensive site fixes and consolidation...")
    
    # Step 1: Fix image paths in existing Hugo posts
    print("\n1. Fixing image paths in Hugo posts...")
    fixed_images = consolidator.fix_image_paths()
    print(f"✅ Fixed {fixed_images} image references")
    
    # Step 2: Migrate Jekyll posts to Hugo
    print("\n2. Migrating Jekyll posts to Hugo...")
    migrated_posts = consolidator.migrate_jekyll_posts()
    print(f"✅ Migrated {migrated_posts} Jekyll posts")
    
    # Step 3: Enhance SEO metadata
    print("\n3. Enhancing SEO metadata...")
    enhanced_seo = consolidator.enhance_seo_metadata()
    print(f"✅ Enhanced SEO for {enhanced_seo} posts")
    
    # Step 4: Create category and tag pages
    print("\n4. Creating category and tag pages...")
    categories_count, tags_count = consolidator.create_category_pages()
    print(f"✅ Created {categories_count} category pages and {tags_count} tag pages")
    
    print(f"\n🎉 Consolidation complete!")
    print(f"📊 Summary:")
    print(f"   - {fixed_images} posts with fixed images")
    print(f"   - {migrated_posts} Jekyll posts migrated")
    print(f"   - {enhanced_seo} posts with enhanced SEO")
    print(f"   - {categories_count} categories and {tags_count} tags created")

if __name__ == "__main__":
    main()