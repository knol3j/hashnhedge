# HashNHedge Image Agent 🖼️

An automated MCP agent that fetches copyright-free images for your Hugo blog posts from multiple sources.

## ✨ Quick Start (For Non-Technical Users)

### What This Does
This agent automatically:
- Scans your blog posts for missing featured images
- Searches copyright-free image sources (Unsplash, Pexels, Pixabay, Openverse)
- Downloads and optimizes images for web (WebP format)
- Updates your blog posts with the images
- Tracks image attributions for legal compliance

### 🚀 One-Time Setup (5 minutes)

1. **Get Free API Keys (Optional but Recommended)**
   - **Pexels**: https://www.pexels.com/api/ (Free, instant)
   - **Pixabay**: https://pixabay.com/api/docs/ (Free, instant)
   - **Unsplash**: https://unsplash.com/developers (Free, requires app creation)
   
   *Note: The agent works without API keys using Openverse, but having keys gives you better images*

2. **Add Your API Keys**
   - Open the file: `C:\Users\gnul\hashnhedge\mcp\image_agent\.env`
   - Add your keys:
     ```
     PEXELS_API_KEY=your_pexels_key_here
     PIXABAY_API_KEY=your_pixabay_key_here
     UNSPLASH_ACCESS_KEY=your_unsplash_key_here
     ```
   - Save and close the file

3. **Restart Claude Desktop**
   - Close Claude completely
   - Open Claude again
   - You should see "hashnhedge-image-agent" in the MCP tools

### 📝 How to Use in Claude

Just type these commands:

**To see which articles need images:**
```
Use the scan_articles tool to show me articles without images
```

**To automatically add images to 5 articles:**
```
Use batch_autofetch to add images to articles
```

**To search images for a specific article:**
```
Search images for the article about bitcoin
```

### 🎯 Common Tasks

| What You Want | What to Type in Claude |
|--------------|------------------------|
| Add images to all articles | "Use batch_autofetch with max_articles=20" |
| See what needs images | "Scan for articles missing images" |
| Add image to specific post | "Download image for article path content/posts/my-post.md" |
| Search but don't download | "Search images for article about crypto" |

## 🛠️ Technical Details

### Architecture
```
mcp/image_agent/
├── server.py           # MCP server entry point
├── orchestrator.py     # Main workflow coordinator
├── utils/             
│   ├── hugo.py        # Hugo content management
│   ├── keywords.py    # Smart keyword extraction
│   ├── image_ops.py   # Image processing (resize, WebP)
│   └── logging.py     # Logging configuration
├── sources/           
│   ├── openverse.py   # Creative Commons images (no key)
│   ├── pixabay.py     # Pixabay provider
│   ├── pexels.py      # Pexels provider
│   └── unsplash.py    # Unsplash provider
└── scripts/
    └── auto_run.py    # Standalone automation script
```

### Features
- ✅ Multiple image sources with fallback
- ✅ Automatic keyword extraction from content
- ✅ WebP conversion with hero + thumbnail
- ✅ License compliance tracking
- ✅ Hugo front matter updates
- ✅ De-duplication by content hash
- ✅ Rate limiting and retry logic
- ✅ SEO-optimized alt text generation

### Configuration Files

**settings.yaml** - Main configuration
```yaml
provider_priority: [openverse, pixabay, pexels, unsplash]
targets:
  hero: {width: 1600, height: 900, format: webp}
  thumb: {width: 640, height: 360, format: webp}
```

**.env** - API keys and limits
```
PEXELS_API_KEY=your_key
MAX_DAILY_DOWNLOADS=50
```

## 🔧 Troubleshooting

### "No images found"
- Check your API keys in `.env`
- Try different keywords
- Verify internet connection

### "Article already has image"
- Use `force=true` to overwrite
- Or manually delete the image field in the markdown file

### "MCP server not found"
- Restart Claude Desktop
- Check `claude_desktop_config.json` has the agent configured
- Verify Python virtual environment is activated

## 📊 Daily Automation

To run automatically every day at 6 AM:
```powershell
# Run this once in PowerShell as Administrator
C:\Users\gnul\hashnhedge\mcp\image_agent\scripts\register_scheduled_task.ps1
```

## 📈 Usage Limits

| Provider | Free Tier Limit | Per Hour |
|----------|----------------|----------|
| Openverse | Unlimited | 1000 |
| Pixabay | 5000/hour | 4500 |
| Pexels | 200/hour | 150 |
| Unsplash | 50/hour | 45 |

## 🤝 Contributing

Feel free to extend the agent with new providers or features. The modular design makes it easy to add new image sources.

## 📄 License

MIT License - Use freely for your HashNHedge site!

---
*Built with ❤️ for automated blog management*
