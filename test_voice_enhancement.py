#!/usr/bin/env python3
"""
Test Oliver Perry Voice Enhancement on a single post
"""

import os
import sys
import re
sys.path.append('.')
from enhance_post_content import enhance_post_content, count_words

POSTS_DIR = "site/content/posts"

def test_single_post():
    """Test enhancement on first post found"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    # Find first post
    test_file = None
    for filename in sorted(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            test_file = os.path.join(POSTS_DIR, filename)
            break
    
    if not test_file:
        print("No posts found to test")
        return
    
    print(f"Testing enhancement on: {os.path.basename(test_file)}")
    
    # Read original
    with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    
    original_words = count_words(original)
    print(f"Original word count: {original_words}")
    
    # Test enhancement
    success = enhance_post_content(test_file)
    
    if success:
        # Read enhanced
        with open(test_file, 'r', encoding='utf-8', errors='ignore') as f:
            enhanced = f.read()
        
        enhanced_words = count_words(enhanced)
        print(f"Enhanced word count: {enhanced_words}")
        print(f"Word increase: +{enhanced_words - original_words}")
        
        # Show preview
        print("\n" + "="*50)
        print("ENHANCED CONTENT PREVIEW:")
        print("="*50)
        
        # Extract just the body content
        if enhanced.startswith('---'):
            parts = enhanced.split('---', 2)
            if len(parts) >= 3:
                body = parts[2].strip()
                # Show first few paragraphs
                paragraphs = body.split('\n\n')[:3]
                for para in paragraphs:
                    if para.strip():
                        print(para[:300] + "..." if len(para) > 300 else para)
                        print()
    
    print(f"\nOriginal backed up to: backup/original_posts/{os.path.basename(test_file)}")

if __name__ == "__main__":
    test_single_post()