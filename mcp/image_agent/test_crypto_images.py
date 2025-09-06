#!/usr/bin/env python3
"""Test fetching crypto-relevant images."""

import asyncio
import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

from image_agent.orchestrator import Orchestrator

async def test_crypto_image_fetch():
    """Test fetching crypto-relevant images."""
    orchestrator = Orchestrator()
    
    print("="*60)
    print("CRYPTO IMAGE FETCH TEST")
    print("="*60)
    
    # Test articles
    test_articles = [
        r"C:\Users\gnul\hashnhedge\content\posts\bitcoin-analysis-2025.md",
        r"C:\Users\gnul\hashnhedge\content\posts\defi-institutional-revolution.md",
        r"C:\Users\gnul\hashnhedge\content\posts\solana-500-prediction.md"
    ]
    
    for article_path in test_articles:
        if not Path(article_path).exists():
            continue
            
        article_name = Path(article_path).name
        print(f"\n📄 Testing: {article_name}")
        print("-"*50)
        
        # Search for images
        print("Searching for images...")
        result = await orchestrator.search_images_for_article(article_path, max_results=5)
        
        result_data = json.loads(result)
        if result_data['status'] == 'success':
            print(f"✅ Search successful!")
            print(f"   Query: {result_data['queries'][0] if result_data['queries'] else 'No query'}")
            print(f"   Found: {result_data['total_results']} images")
            
            # Show first 3 results
            print("\n   Top results:")
            for i, img in enumerate(result_data['results'][:3], 1):
                alt_text = img.get('alt', 'No description')[:50]
                print(f"   {i}. {alt_text}... [{img['provider']}]")
            
            # Download the best image
            print("\n   Downloading best image...")
            download_result = await orchestrator.download_and_attach(
                article_path, image_index=0, force=True
            )
            
            download_data = json.loads(download_result)
            if download_data['status'] == 'success':
                print(f"   ✅ Image downloaded successfully!")
                print(f"   Provider: {download_data['image']['provider']}")
                print(f"   Path: {download_data['image']['hero']}")
            else:
                print(f"   ❌ Download failed: {download_data.get('message', 'Unknown error')}")
        else:
            print(f"❌ Search failed: {result_data.get('message', 'Unknown error')}")
    
    print("\n" + "="*60)
    print("✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(test_crypto_image_fetch())
