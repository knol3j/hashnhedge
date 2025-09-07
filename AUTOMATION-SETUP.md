# Hash & Hedge Content Automation Setup

## ✅ Content & Images Added

All blog posts have been added to the site with proper images:
- 11 blog posts in `site/content/posts/`
- Images configured for each post in `site/static/images/posts/`
- Hero images and thumbnails properly linked

## 🤖 Automated Content Generation

### Components:

1. **Content Generator** (`pipeline/generate_hugo_posts.py`)
   - Generates new blog posts automatically
   - Fetches inspiration from crypto RSS feeds
   - Creates SEO-optimized content with proper front matter

2. **Image Fetcher** (`pipeline/fetch_images_fixed.py`)
   - Extracts images from source URLs
   - Downloads and saves images for each post
   - Updates post metadata with image paths

3. **Scheduler** (`pipeline/hugo_scheduler.bat`)
   - Runs content generation
   - Fetches images
   - Builds Hugo site
   - Commits and pushes to GitHub

### 📅 Setup Automated Scheduling:

1. **Run as Administrator**:
   ```powershell
   cd C:\Users\gnul\hashnhedge\pipeline
   powershell -ExecutionPolicy Bypass -File Setup-HugoScheduler.ps1
   ```

2. **Schedule Details**:
   - Morning Post: 9:00 AM
   - Afternoon Post: 3:00 PM  
   - Evening Post: 9:00 PM

3. **Manual Generation**:
   ```bash
   cd C:\Users\gnul\hashnhedge
   pipeline\hugo_scheduler.bat
   ```

### 🛠️ Manual Commands:

**Generate new post**:
```bash
python pipeline\generate_hugo_posts.py --count 1
```

**Fetch images for posts**:
```bash
python pipeline\fetch_images_fixed.py
```

**Setup post images**:
```bash
python pipeline\setup_post_images.py
```

**Build and deploy**:
```bash
cd site
hugo --gc --minify
cd ..
git add -A
git commit -m "Update content"
git push origin main
```

### 📊 Current Status:

- ✅ 11 blog posts live
- ✅ Images configured for all posts
- ✅ Automated generation scripts ready
- ✅ Windows Task Scheduler scripts ready
- ✅ Hugo site building successfully

### 🔄 Workflow:

1. Scheduler runs at set times
2. Generates new crypto/finance content
3. Fetches relevant images
4. Builds Hugo site
5. Commits to GitHub
6. GitHub Actions deploys to GitHub Pages
7. Site updates at https://hashnhedge.com

### 📝 Notes:

- RSS feeds used for content inspiration:
  - CoinTelegraph
  - CoinDesk
  - Decrypt
  - Bitcoin Magazine

- Content categories:
  - Crypto markets
  - DeFi
  - Altcoins
  - Analysis
  - Trading

- All generated content is SEO-optimized with:
  - Meta descriptions
  - Keywords
  - Categories & tags
  - Featured images