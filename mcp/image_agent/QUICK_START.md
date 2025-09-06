# 🚀 HashNHedge Image Agent - Quick Start Guide

## ✅ Installation Complete!

Your MCP image agent is fully installed and ready to use. Here's everything you need to know:

## 📍 What's Been Set Up

1. **MCP Agent Location**: `C:\Users\gnul\hashnhedge\mcp\image_agent`
2. **118 blog posts** found and ready for image processing
3. **Claude Desktop** configured with the agent
4. **All dependencies** installed and verified

## 🔑 Step 1: Add API Keys (Optional but Recommended)

Edit the file: `C:\Users\gnul\hashnhedge\mcp\image_agent\.env`

Add your free API keys:
```
PEXELS_API_KEY=your_key_here
PIXABAY_API_KEY=your_key_here
UNSPLASH_ACCESS_KEY=your_key_here
```

**Get free keys from:**
- Pexels: https://www.pexels.com/api/
- Pixabay: https://pixabay.com/api/docs/
- Unsplash: https://unsplash.com/developers

*Note: The agent works without keys using Openverse (Creative Commons images)*

## 🔄 Step 2: Restart Claude Desktop

Close Claude completely and reopen it to load the new MCP agent.

## 💬 Step 3: Use in Claude

Just type these commands in Claude:

### See which articles need images:
```
Use the scan_articles tool to find posts without images
```

### Automatically add images to 5 articles:
```
Use batch_autofetch to add images to 5 articles
```

### Search images for a specific article:
```
Search images for the bitcoin ETF article
```

### Download a specific image:
```
Download the first image for content/posts/bitcoin-etf-approval-2025.md
```

## 📊 Current Status

- **Total Articles**: 118
- **Articles Needing Images**: To be determined (use scan_articles)
- **Available Providers**: Openverse (always), Pixabay, Pexels, Unsplash (with keys)

## 🎯 Quick Commands Reference

| Task | Claude Command |
|------|---------------|
| Scan all articles | "scan_articles" |
| Auto-add 10 images | "batch_autofetch with max_articles=10" |
| Search specific post | "search_images for article path content/posts/[filename].md" |
| Force replace image | "download_image with force=true" |

## 🔧 Troubleshooting

### If Claude doesn't see the agent:
1. Make sure Claude is fully closed
2. Reopen Claude
3. Check for "hashnhedge-image-agent" in available tools

### If no images are found:
1. The agent works without API keys using Openverse
2. Adding API keys gives you access to more/better images
3. Try different search terms or articles

## 📈 Daily Automation (Optional)

To run automatically every day, execute in PowerShell as Administrator:
```powershell
C:\Users\gnul\hashnhedge\mcp\image_agent\scripts\register_scheduled_task.ps1
```

## 🎉 You're Ready!

Your image agent is fully operational. Just restart Claude and start using the commands above!

---
*For detailed documentation, see README.md*
