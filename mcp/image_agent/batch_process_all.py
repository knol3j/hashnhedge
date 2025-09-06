#!/usr/bin/env python3
"""
Batch process all HashNHedge posts to fix frontmatter and add crypto-relevant images.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
import frontmatter

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

from image_agent.orchestrator import Orchestrator

class BatchProcessor:
    """Process all posts for the HashNHedge site."""
    
    def __init__(self):
        self.orchestrator = Orchestrator()
        self.content_dir = Path(r"C:\Users\gnul\hashnhedge\content")
        self.stats = {
            'total_posts': 0,
            'posts_without_images': 0,
            'images_added': 0,
            'failed': 0,
            'skipped': 0
        }
        
    def scan_posts(self):
        """Scan all posts and identify those needing images."""
        posts_needing_images = []
        all_posts = []
        
        for md_file in self.content_dir.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                    
                all_posts.append(md_file)
                
                # Check if post needs an image
                has_image = (
                    post.get('featured_image') or 
                    post.get('image') or 
                    post.get('cover', {}).get('image')
                )
                
                if not has_image:
                    posts_needing_images.append({
                        'path': md_file,
                        'title': post.get('title', md_file.stem),
                        'tags': post.get('tags', [])
                    })
            except Exception as e:
                print(f"Error reading {md_file}: {e}")
                
        self.stats['total_posts'] = len(all_posts)
        self.stats['posts_without_images'] = len(posts_needing_images)
        
        return posts_needing_images
    
    async def process_post(self, post_info):
        """Process a single post to add crypto-relevant image."""
        try:
            article_path = str(post_info['path'])
            print(f"\n📄 Processing: {post_info['path'].name}")
            print(f"   Title: {post_info['title']}")
            
            # Search for images
            print("   🔍 Searching for crypto-relevant images...")
            search_result = await self.orchestrator.search_images_for_article(
                article_path, max_results=5
            )
            
            search_data = json.loads(search_result)
            if search_data['status'] != 'success':
                print(f"   ❌ Search failed: {search_data.get('message')}")
                self.stats['failed'] += 1
                return False
            
            print(f"   ✅ Found {search_data['total_results']} images")
            print(f"   Query: {search_data['queries'][0] if search_data['queries'] else 'No query'}")
            
            # Download and attach the best image
            print("   📥 Downloading best match...")
            download_result = await self.orchestrator.download_and_attach(
                article_path, image_index=0, force=False
            )
            
            download_data = json.loads(download_result)
            if download_data['status'] == 'success':
                print(f"   ✅ Image added successfully!")
                print(f"   Provider: {download_data['image']['provider']}")
                print(f"   Path: {download_data['image']['hero']}")
                self.stats['images_added'] += 1
                return True
            elif download_data['status'] == 'skipped':
                print(f"   ⏭️  Skipped: {download_data.get('message')}")
                self.stats['skipped'] += 1
                return True
            else:
                print(f"   ❌ Failed: {download_data.get('message')}")
                self.stats['failed'] += 1
                return False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.stats['failed'] += 1
            return False
    
    async def run(self, max_posts=None):
        """Run the batch processor."""
        print("="*70)
        print("HASHNHEDGE BATCH IMAGE PROCESSOR")
        print("="*70)
        print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Scan posts
        print("📊 Scanning content directory...")
        posts_needing_images = self.scan_posts()
        
        print(f"   Total posts: {self.stats['total_posts']}")
        print(f"   Posts without images: {self.stats['posts_without_images']}")
        
        if not posts_needing_images:
            print("\n✅ All posts already have images!")
            return
        
        # Process posts
        posts_to_process = posts_needing_images[:max_posts] if max_posts else posts_needing_images
        print(f"\n🚀 Processing {len(posts_to_process)} posts...")
        print("-"*70)
        
        for post_info in posts_to_process:
            await self.process_post(post_info)
            # Small delay to avoid rate limiting
            await asyncio.sleep(1)
        
        # Final report
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"✅ Images added: {self.stats['images_added']}")
        print(f"⏭️  Skipped: {self.stats['skipped']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"📊 Total processed: {self.stats['images_added'] + self.stats['skipped'] + self.stats['failed']}")
        
        # Save report
        report_file = Path("batch_process_report.json")
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'stats': self.stats,
                'posts_processed': [str(p['path']) for p in posts_to_process]
            }, f, indent=2)
        print(f"\n📝 Report saved to: {report_file}")
        
        print(f"\n✅ Batch processing complete!")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch process HashNHedge posts')
    parser.add_argument('--max', type=int, help='Maximum number of posts to process')
    parser.add_argument('--dry-run', action='store_true', help='Only scan, don\'t process')
    
    args = parser.parse_args()
    
    processor = BatchProcessor()
    
    if args.dry_run:
        print("DRY RUN MODE - Only scanning, not processing")
        posts = processor.scan_posts()
        print(f"\nFound {len(posts)} posts needing images:")
        for post in posts[:10]:  # Show first 10
            print(f"  - {post['path'].name}: {post['title']}")
        if len(posts) > 10:
            print(f"  ... and {len(posts) - 10} more")
    else:
        await processor.run(max_posts=args.max)

if __name__ == "__main__":
    asyncio.run(main())
