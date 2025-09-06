import asyncio
import os
import sys
from pathlib import Path

# Set up environment
sys.path.insert(0, str(Path.cwd()))
os.chdir(r"C:\Users\gnul\hashnhedge\mcp\image_agent")

# Import the image agent
from image_agent.orchestrator import Orchestrator

async def test_image_fetch():
    print("=== HashNHedge Image Agent Test ===\n")
    
    orchestrator = Orchestrator()
    
    # 1. Scan for articles without images
    print("1. Scanning for articles without images...")
    scan_result = await orchestrator.scan_articles(limit=5)
    print(scan_result)
    print("\n" + "="*50 + "\n")
    
    # 2. Test searching images for bitcoin-analysis post
    article_path = r"C:\Users\gnul\hashnhedge\content\posts\bitcoin-analysis-2025.md"
    print(f"2. Searching images for: bitcoin-analysis-2025.md")
    search_result = await orchestrator.search_images_for_article(article_path, max_results=3)
    print(search_result)
    print("\n" + "="*50 + "\n")
    
    # 3. Download and attach the first image
    print("3. Downloading and attaching best image...")
    download_result = await orchestrator.download_and_attach(article_path, image_index=0)
    print(download_result)

if __name__ == "__main__":
    asyncio.run(test_image_fetch())
