# Hash & Hedge Image Scraping System

## Overview

This system prioritizes **real photos** over generated images for blog posts, with intelligent fallbacks:

1. **Priority 1**: Scraped photos from Unsplash
2. **Priority 2**: Scraped photos from Pexels  
3. **Priority 3**: Generated SVG images (fallback)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_images.txt
```

### 2. Setup API Keys (Optional but Recommended)
```bash
python setup_image_apis.py
```

This will guide you through:
- Getting Unsplash API key (free)
- Getting Pexels API key (free)  
- Creating `.env` file

### 3. Run Image Processing
```bash
python scrape_and_generate_images.py
```

## API Setup Details

### Unsplash API (Recommended)
1. Go to [https://unsplash.com/developers](https://unsplash.com/developers)
2. Create developer account
3. Create new application
4. Copy Access Key
5. Free tier: 50 requests/hour

### Pexels API (Backup)
1. Go to [https://www.pexels.com/api/](https://www.pexels.com/api/)
2. Create free account
3. Generate API key
4. Copy API key
5. Free tier: 200 requests/hour

## How It Works

### Smart Keyword Extraction
- Converts crypto/blockchain terms to generic business terms
- "Bitcoin" → "finance, technology, business"
- "Blockchain" → "technology, network, digital"  
- "DeFi" → "finance, technology"
- "NFT" → "digital, art, technology"

### Image Search Process
1. Extract 3 relevant keywords from post title
2. Search Unsplash API for landscape photos
3. If no results, try Pexels API
4. If no photos found, generate SVG image
5. Download and save with proper file extension

### File Management
- Images saved to: `site/static/images/posts/`
- Naming: `{post-slug}.{ext}` (matches post filename)
- Supports: `.jpg`, `.png`, `.webp`, `.svg`
- Skips existing images (won't overwrite)

## Configuration Options

### Environment Variables
```bash
# .env file (created by setup script)
UNSPLASH_ACCESS_KEY=your_access_key_here
PEXELS_API_KEY=your_api_key_here
```

### Manual Configuration
Edit `scrape_and_generate_images.py`:
```python
UNSPLASH_ACCESS_KEY = "your_key_here"
PEXELS_API_KEY = "your_key_here"
```

## Usage Examples

### Process All Posts
```bash
python scrape_and_generate_images.py
```

### Check What Will Happen (Dry Run)
The script automatically skips existing images, so you can run it safely.

### Force Regenerate Specific Images
Delete the existing image file and run the script:
```bash
rm site/static/images/posts/bitcoin-analysis.jpg
python scrape_and_generate_images.py
```

## Output Examples

### With API Keys
```
Starting image processing...
Unsplash API: YES
Pexels API: YES

Searching for images with keywords: ['finance', 'technology', 'business']
Found Unsplash image for: Bitcoin Price Analysis
[PHOTO] bitcoin-price-analysis.jpg - Photo by John Doe on Unsplash

Processing complete!
Posts processed: 50
Photos downloaded: 12
SVGs generated: 38
```

### Without API Keys
```
Starting image processing...
Unsplash API: NO
Pexels API: NO

No photos found, generating SVG for: Bitcoin Price Analysis
[GENERATED] bitcoin-price-analysis.svg

Processing complete!
Posts processed: 50
Photos downloaded: 0
SVGs generated: 50

WARNING: No API keys configured. Set UNSPLASH_ACCESS_KEY or PEXELS_API_KEY for photo downloads.
```

## File Structure

```
hashnhedge/
├── scrape_and_generate_images.py    # Main image processing script
├── setup_image_apis.py              # API setup helper
├── requirements_images.txt          # Python dependencies
├── .env                            # API keys (created by setup)
└── site/static/images/posts/       # Generated images directory
    ├── bitcoin-analysis.jpg        # Downloaded photo
    ├── ethereum-update.png         # Downloaded photo  
    └── defi-trends.svg            # Generated SVG (fallback)
```

## Benefits

### SEO & Performance
- Real photos improve engagement
- Proper alt tags from post titles
- Optimized file sizes from APIs
- Lazy loading support

### Content Quality  
- Professional stock photography
- Relevant to financial/tech content
- Consistent branding with fallback SVGs
- Attribution included for compliance

### Automation
- Batch processes all posts
- Respects API rate limits
- Handles errors gracefully
- Skips existing images

## Troubleshooting

### No Photos Downloaded
1. Check API keys in `.env` file
2. Verify internet connection
3. Check API quotas (Unsplash: 50/hour, Pexels: 200/hour)
4. Review keyword extraction for your titles

### Unicode Errors
Fixed in current version - uses ASCII-safe symbols.

### Rate Limiting  
Script includes 1-second delays between API calls. Increase if needed:
```python
time.sleep(2)  # 2 second delay
```

### Mixed File Extensions
Script handles `.jpg`, `.png`, `.webp` automatically based on content-type.

## Integration with Hugo

Images are automatically available in Hugo templates:
```html
{{ if .Params.image }}
<img src="{{ .Params.image }}" alt="{{ .Title }}">
{{ end }}
```

The image filename matches the post slug, so Hugo can find them automatically.

## Next Steps

1. Run setup: `python setup_image_apis.py`
2. Process images: `python scrape_and_generate_images.py` 
3. Build site: `hugo server`
4. Verify images load on frontend

## API Costs

Both Unsplash and Pexels offer generous free tiers:
- **Unsplash**: 50 requests/hour (free)
- **Pexels**: 200 requests/hour (free)

For typical blog usage, free tiers are sufficient.