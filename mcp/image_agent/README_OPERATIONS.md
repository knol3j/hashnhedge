# HashNHedge Image Agent - Operations Guide

## Overview
The HashNHedge Image Agent automatically fetches copyright-free, crypto-relevant images for blog posts using multiple image providers (Pexels, Pixabay, Unsplash, Openverse).

## Key Features
- **Crypto-Specific Keywords**: Automatically extracts crypto/finance terms from articles
- **Negative Filtering**: Avoids generic nature images (butterflies, flowers, etc.)
- **Multiple Providers**: Falls back across providers for best results
- **SEO Optimization**: Generates alt text and proper attribution
- **Batch Processing**: Can process multiple articles at once

## Quick Start

### 1. Test Single Article
```powershell
cd C:\Users\gnul\hashnhedge\mcp\image_agent
.venv\Scripts\python test_crypto_images.py
```

### 2. Batch Process All Posts
```powershell
# Dry run (see what needs processing)
.venv\Scripts\python batch_process_all.py --dry-run

# Process up to 10 posts
.venv\Scripts\python batch_process_all.py --max 10

# Process all posts without images
.venv\Scripts\python batch_process_all.py
```

### 3. Check Specific Post
```powershell
.venv\Scripts\python -c "
import asyncio
from image_agent.orchestrator import Orchestrator

async def check():
    o = Orchestrator()
    result = await o.search_images_for_article(
        r'C:\Users\gnul\hashnhedge\content\posts\YOUR-POST.md',
        max_results=5
    )
    print(result)

asyncio.run(check())
"
```

## Configuration

### API Keys (.env file)
```env
UNSPLASH_ACCESS_KEY=your-key-here
PEXELS_API_KEY=your-key-here
PIXABAY_API_KEY=your-key-here
```

### Settings (settings.yaml)
- Provider priority order
- Image dimensions and quality
- Rate limits per provider
- Output directories

## How It Works

### 1. Keyword Extraction
The `CryptoKeywordExtractor` class:
- Extracts crypto terms (bitcoin, ethereum, defi, etc.)
- Adds visual context (trading, chart, digital)
- Applies negative filters (-butterfly, -flower, -nature)

Example queries generated:
- "bitcoin crypto price digital trading -butterfly -flower"
- "defi institutional revolution cryptocurrency -nature"
- "solana sol altcoin market chart -insect"

### 2. Image Search
- Searches across configured providers
- Prioritizes landscape orientation for hero images
- Filters by minimum resolution (1200x675)
- Caches results to avoid duplicate API calls

### 3. Image Processing
- Downloads highest-scoring image
- Creates WebP versions (hero: 1600x900, thumb: 640x360)
- Saves metadata and attribution
- Updates post frontmatter with image paths

## Troubleshooting

### Issue: Getting nature/butterfly images
**Solution**: The crypto keyword extractor now enforces crypto terms and negative filters.

### Issue: API rate limits
**Solution**: The system respects rate limits per provider:
- Pixabay: 4500/hour
- Pexels: 150/hour  
- Unsplash: 45/hour
- Openverse: 1000/hour

### Issue: Encoding errors
**Solution**: Some files may have encoding issues. The batch processor skips these automatically.

### Issue: No images found
**Solution**: Check that:
1. API keys are configured in .env
2. Article has title and tags in frontmatter
3. Internet connection is working

## Revolutionary Hash & Hedge Branding

The project includes powerful crypto revolution themed images in:
```
C:\Users\gnul\hashnhedge\static\images\brand\
```

These can be used for:
- Hero sections
- About pages
- Category headers
- Social media cards

## Automation

### Windows Task Scheduler
Create a daily task to process new posts:
```powershell
schtasks /Create /TN "HashNHedge Daily Images" /TR "C:\Users\gnul\hashnhedge\mcp\image_agent\.venv\Scripts\python.exe C:\Users\gnul\hashnhedge\mcp\image_agent\batch_process_all.py --max 10" /SC DAILY /ST 03:00 /RL HIGHEST
```

### Git Hooks
Add pre-commit hook to validate images exist:
```bash
#!/bin/bash
python .venv/Scripts/python batch_process_all.py --dry-run
```

## Support

For issues or improvements:
1. Check logs in `logs/image_agent.log`
2. Review `batch_process_report.json` for processing details
3. Test with `test_crypto_keywords.py` for debugging

---
*Hash & Hedge - Revolutionary Crypto Content with Proper Imagery*
