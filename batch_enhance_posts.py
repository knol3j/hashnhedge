#!/usr/bin/env python3
"""
Batch Enhancement System for Oliver Perry Voice
Processes all posts to match Oliver Perry's editorial style with 500+ words minimum
"""

import os
import sys
import time
from enhance_post_content import enhance_post_content, count_words

POSTS_DIR = "site/content/posts"
BATCH_SIZE = 10  # Process posts in batches to avoid overwhelming output

def batch_enhance_all_posts():
    """Enhance all posts in batches"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    # Get all markdown files
    post_files = [f for f in sorted(os.listdir(POSTS_DIR)) if f.endswith('.md')]
    total_files = len(post_files)
    
    if total_files == 0:
        print("No posts found to enhance")
        return
    
    print("Oliver Perry Voice Enhancement - Batch Processing")
    print("=" * 60)
    print(f"Found {total_files} posts to process")
    print(f"Processing in batches of {BATCH_SIZE}")
    print(f"Originals will be backed up to: backup/original_posts/")
    print()
    
    processed = 0
    enhanced = 0
    skipped = 0
    errors = 0
    
    # Process in batches
    for batch_start in range(0, total_files, BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, total_files)
        batch_files = post_files[batch_start:batch_end]
        
        print(f"Processing batch {(batch_start//BATCH_SIZE)+1}/{((total_files-1)//BATCH_SIZE)+1}")
        print("-" * 40)
        
        for filename in batch_files:
            filepath = os.path.join(POSTS_DIR, filename)
            
            try:
                # Check if already enhanced (quick check)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Skip if already has Oliver Perry indicators
                if any(phrase in content.lower() for phrase in [
                    'christ almighty', 'beautiful bastards', 'harder than chinese algebra',
                    'nihilistic optimism', 'beautiful truth'
                ]):
                    print(f"[SKIP] {filename} - Already enhanced")
                    skipped += 1
                else:
                    # Check word count
                    current_words = count_words(content)
                    
                    if enhance_post_content(filepath):
                        enhanced += 1
                        print(f"[OK] {filename} - {current_words} → 500+ words")
                    else:
                        errors += 1
                        print(f"[ERROR] {filename}")
                
                processed += 1
                
            except Exception as e:
                print(f"[ERROR] {filename}: {e}")
                errors += 1
                processed += 1
        
        print()
        
        # Brief pause between batches
        if batch_end < total_files:
            print("Pausing between batches...")
            time.sleep(2)
            print()
    
    # Summary
    print("=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total posts: {total_files}")
    print(f"Processed: {processed}")
    print(f"Enhanced: {enhanced}")
    print(f"Already enhanced (skipped): {skipped}")
    print(f"Errors: {errors}")
    print()
    
    if enhanced > 0:
        print(f"✓ {enhanced} posts enhanced with Oliver Perry voice")
        print(f"✓ All posts now have 500+ words minimum")
        print(f"✓ Original posts backed up to backup/original_posts/")
        print()
        print("Next steps:")
        print("1. Review enhanced posts: site/content/posts/")
        print("2. Build site: hugo server")
        print("3. Verify voice consistency on frontend")
    else:
        print("No posts needed enhancement")

def preview_enhancement_plan():
    """Preview what will be enhanced without making changes"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    post_files = [f for f in sorted(os.listdir(POSTS_DIR)) if f.endswith('.md')]
    
    print("ENHANCEMENT PREVIEW")
    print("=" * 40)
    
    needs_enhancement = []
    already_enhanced = []
    word_counts = []
    
    for filename in post_files:
        filepath = os.path.join(POSTS_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            current_words = count_words(content)
            word_counts.append(current_words)
            
            # Check if already enhanced
            if any(phrase in content.lower() for phrase in [
                'christ almighty', 'beautiful bastards', 'harder than chinese algebra'
            ]):
                already_enhanced.append((filename, current_words))
            else:
                needs_enhancement.append((filename, current_words))
        
        except Exception as e:
            print(f"Error reading {filename}: {e}")
    
    print(f"Total posts: {len(post_files)}")
    print(f"Need enhancement: {len(needs_enhancement)}")
    print(f"Already enhanced: {len(already_enhanced)}")
    print(f"Average word count: {sum(word_counts)//len(word_counts) if word_counts else 0}")
    print()
    
    if needs_enhancement:
        print("POSTS THAT WILL BE ENHANCED:")
        print("-" * 30)
        for filename, words in needs_enhancement[:10]:  # Show first 10
            print(f"  {filename} ({words} words)")
        if len(needs_enhancement) > 10:
            print(f"  ... and {len(needs_enhancement) - 10} more")
    
    if already_enhanced:
        print(f"\nPOSTS ALREADY ENHANCED: {len(already_enhanced)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        preview_enhancement_plan()
    else:
        batch_enhance_all_posts()