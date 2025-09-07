#!/usr/bin/env python3
"""
setup_post_images.py - Ensure all posts have proper images
"""

import os
import shutil
from pathlib import Path
import frontmatter

def setup_post_images(site_path="site"):
    """Ensure all posts have images set up"""
    
    site_path = Path(site_path)
    posts_path = site_path / "content" / "posts"
    images_path = site_path / "static" / "images"
    
    # Check backup location for existing images
    backup_images = Path("static_images_backup")
    
    # Process each post
    for post_file in posts_path.glob("*.md"):
        print(f"\nProcessing: {post_file.name}")
        
        # Read post
        with open(post_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        post_slug = post_file.stem
        post_image_dir = images_path / "posts" / post_slug
        post_image_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if images already exist in backup
        backup_post_dir = backup_images / post_slug
        if backup_post_dir.exists():
            # Copy images from backup
            for img in backup_post_dir.glob("*"):
                dest = post_image_dir / img.name
                if not dest.exists():
                    shutil.copy2(img, dest)
                    print(f"  -> Copied {img.name} from backup")
        
        # Update post metadata with correct image paths
        hero_image = f"/images/posts/{post_slug}/hero.webp"
        thumb_image = f"/images/posts/{post_slug}/thumb.webp"
        
        # Check if hero.webp exists, if not try other extensions
        hero_path = post_image_dir / "hero.webp"
        if not hero_path.exists():
            # Try other formats
            for ext in ['.jpg', '.png', '.svg']:
                alt_hero = post_image_dir / f"hero{ext}"
                if alt_hero.exists():
                    hero_image = f"/images/posts/{post_slug}/hero{ext}"
                    break
            else:
                # Check if any image exists in the directory
                images_in_dir = list(post_image_dir.glob("*"))
                if images_in_dir:
                    hero_image = f"/images/posts/{post_slug}/{images_in_dir[0].name}"
        
        # Update metadata
        updated = False
        
        if 'featured_image' not in post.metadata or not post.metadata['featured_image']:
            post.metadata['featured_image'] = hero_image
            updated = True
        
        if 'image' not in post.metadata:
            post.metadata['image'] = hero_image
            updated = True
        
        if 'images' not in post.metadata:
            post.metadata['images'] = [hero_image]
            updated = True
        elif hero_image not in post.metadata['images']:
            post.metadata['images'].append(hero_image)
            updated = True
        
        # Add other useful metadata if missing
        if 'image_alt' not in post.metadata:
            post.metadata['image_alt'] = post.metadata.get('title', 'Featured image')
            updated = True
        
        if updated:
            # Save updated post
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            print(f"  -> Updated metadata")
        else:
            print(f"  -> Already configured")

def create_placeholder_images(site_path="site"):
    """Create placeholder images for posts without images"""
    
    site_path = Path(site_path)
    posts_path = site_path / "content" / "posts"
    images_path = site_path / "static" / "images"
    
    # Use a default image as placeholder
    default_image = images_path / "default-cover.svg"
    
    for post_file in posts_path.glob("*.md"):
        post_slug = post_file.stem
        post_image_dir = images_path / "posts" / post_slug
        post_image_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if any images exist
        existing_images = list(post_image_dir.glob("*"))
        if not existing_images and default_image.exists():
            # Copy default image as placeholder
            dest = post_image_dir / "hero.svg"
            shutil.copy2(default_image, dest)
            print(f"Created placeholder for: {post_slug}")

def main():
    print("Hash & Hedge Image Setup")
    print("=" * 60)
    
    print("\nSetting up post images...")
    setup_post_images()
    
    print("\nCreating placeholders for missing images...")
    create_placeholder_images()
    
    print("\nDone!")

if __name__ == "__main__":
    main()