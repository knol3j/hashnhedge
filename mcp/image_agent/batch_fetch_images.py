import asyncio
import os
import sys
from pathlib import Path

# Set up environment
sys.path.insert(0, str(Path.cwd()))
os.chdir(r"C:\Users\gnul\hashnhedge\mcp\image_agent")

# Import the image agent
from image_agent.orchestrator import Orchestrator

async def batch_fetch_images():
    print("=== HashNHedge Batch Image Fetcher ===\n")
    
    orchestrator = Orchestrator()
    
    # Batch process all articles without images
    print("Starting batch image fetch for all articles without images...")
    result = await orchestrator.batch_autofetch(max_articles=10, per_article=1)
    print(result)
    
    print("\n✅ Batch processing complete!")

if __name__ == "__main__":
    asyncio.run(batch_fetch_images())
