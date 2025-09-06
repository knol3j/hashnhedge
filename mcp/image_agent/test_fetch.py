import asyncio
import sys
from pathlib import Path

# Add current dir to path
sys.path.insert(0, str(Path.cwd()))

# Import orchestrator
from image_agent.orchestrator import Orchestrator

async def main():
    orchestrator = Orchestrator()
    
    # Test 1: Scan articles
    print("Testing: Scanning for articles without images...")
    result = await orchestrator.scan_articles(limit=5)
    print(result)
    print()
    
    # Test 2: Search images for an article
    article_path = r"C:\Users\gnul\hashnhedge\content\posts\bitcoin-analysis-2025.md"
    print(f"Testing: Searching images for {Path(article_path).name}...")
    search_result = await orchestrator.search_images_for_article(article_path, max_results=3)
    print(search_result)

if __name__ == "__main__":
    asyncio.run(main())
