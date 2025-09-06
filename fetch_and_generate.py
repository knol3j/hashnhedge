import os
import requests
import frontmatter
from bs4 import BeautifulSoup
from pathlib import Path
import time
import re
from datetime import datetime
import random

def sanitize_filename(filename):
    """Sanitize filename for file system"""
    filename = re.sub(r'[<>:"/\\|?*]', '-', filename)
    return filename[:100] if len(filename) > 100 else filename

def fetch_crypto_image(keyword):
    """Fetch relevant crypto/finance image from Unsplash"""
    try:
        # Use Unsplash for high-quality free images
        search_terms = [
            "cryptocurrency bitcoin",
            "blockchain technology",
            "financial markets trading",
            "digital currency",
            "stock market charts",
            "ethereum crypto",
            "defi finance",
            "bitcoin mining"
        ]
        
        # Pick a random search term for variety
        search = random.choice(search_terms) if not keyword else keyword
        
        # Unsplash API (no key needed for source URLs)
        image_url = f"https://source.unsplash.com/1200x600/?{search.replace(' ', ',')}"
        
        return image_url
    except Exception as e:
        print(f"Error getting image: {e}")
        return None
def download_image(image_url, save_path):
    """Download image from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(image_url, headers=headers, stream=True, timeout=15)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✓ Downloaded: {os.path.basename(save_path)}")
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

def process_all_posts(site_path):
    """Process all posts and add hero images"""
    content_dir = os.path.join(site_path, "content")
    images_dir = os.path.join(site_path, "static", "images", "posts")
    
    # Ensure images directory exists
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    
    processed = 0
    
    # Find all markdown files
    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                try:
                    # Load post
                    with open(filepath, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)                    
                    # Skip if already has image
                    if 'image' in post.metadata and post.metadata['image']:
                        continue
                    
                    # Generate image based on title/tags
                    title = post.metadata.get('title', 'crypto')
                    tags = post.metadata.get('tags', ['cryptocurrency'])
                    keyword = tags[0] if tags else title.split()[0]
                    
                    # Get image URL
                    image_url = fetch_crypto_image(keyword)
                    
                    if image_url:
                        # Generate filename
                        filename = sanitize_filename(title.lower().replace(' ', '-'))
                        filename = f"{filename}.jpg"
                        save_path = os.path.join(images_dir, filename)
                        
                        # Download image
                        if download_image(image_url, save_path):
                            # Update post frontmatter
                            post.metadata['image'] = f"/images/posts/{filename}"
                            
                            # Save updated post
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(frontmatter.dumps(post))
                            
                            processed += 1
                            print(f"✓ Added image to: {title}")
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    print(f"\n✓ Processed {processed} posts with new images")
    return processed
def generate_seo_content(site_path, topic, category="crypto"):
    """Generate SEO-optimized content for rapid scaling"""
    
    # Content templates for different categories
    templates = {
        "crypto": {
            "titles": [
                f"{topic} Price Analysis: Key Levels to Watch",
                f"Breaking: {topic} Shows Bullish Momentum",
                f"{topic} Technical Update: What Traders Need to Know",
                f"Is {topic} Ready for a Breakout? Analysis Inside",
                f"{topic} Market Update: Institutional Interest Growing"
            ],
            "tags": ["cryptocurrency", "bitcoin", "ethereum", "defi", "trading", "blockchain", "altcoins"],
            "content": """## Market Overview

{topic} continues to capture market attention with recent price movements indicating potential trend changes. Technical indicators suggest interesting developments ahead.

### Key Highlights

- Trading volume shows significant increase
- Support levels holding strong
- Institutional accumulation patterns visible
- Technical indicators turning bullish

### Technical Analysis

The current market structure for {topic} presents several interesting opportunities for both short-term traders and long-term investors.

**Support Levels:**
- Primary support established at recent lows
- Secondary support at previous resistance
- Strong buyer interest at key levels

**Resistance Levels:**
- Immediate resistance at recent highs
- Major resistance at psychological levels
- Volume profile shows selling pressure diminishing

### Market Sentiment

Social media sentiment and on-chain metrics paint an optimistic picture for {topic}. Key metrics to watch:

- Network activity increasing
- Exchange outflows suggesting accumulation
- Funding rates remaining neutral to positive
- Options market showing bullish bias

### What This Means for Investors

Smart money positioning suggests confidence in the medium-term outlook. Consider:

1. Dollar-cost averaging strategies
2. Risk management protocols
3. Portfolio diversification
4. Long-term accumulation zones

### Looking Ahead

The coming weeks will be crucial for {topic} as several catalysts approach:

- Upcoming protocol upgrades
- Regulatory developments
- Institutional adoption metrics
- Market structure evolution

---

*This content is for informational purposes only. Not financial advice. Always conduct your own research before making investment decisions.*"""
        },
        "finance": {
            "titles": [
                f"Smart Money Strategies: {topic} for Beginners",
                f"How to Build Wealth with {topic} in 2025",
                f"{topic}: The Complete Guide for Smart Investors",
                f"Master {topic} with These Simple Steps",
                f"{topic} Secrets That Can Transform Your Finances"
            ],
            "tags": ["finance", "investing", "money", "wealth", "savings", "budgeting", "financial-freedom"],
            "content": """## Introduction

Understanding {topic} is crucial for building long-term wealth and financial security. This guide breaks down everything you need to know.

### Why {topic} Matters

In today's economic environment, mastering {topic} can make the difference between financial struggle and financial freedom.

**Key Benefits:**
- Build sustainable wealth over time
- Protect against inflation
- Create multiple income streams
- Achieve financial independence

### Getting Started with {topic}

Starting your journey with {topic} doesn't require significant capital. Here's how to begin:

1. **Educate Yourself**
   - Read reputable sources
   - Follow market trends
   - Understand basic principles

2. **Start Small**
   - Begin with what you can afford
   - Focus on consistency over size
   - Build habits gradually

3. **Track Progress**
   - Monitor your results
   - Adjust strategies as needed
   - Celebrate small wins

### Common Mistakes to Avoid

Many beginners make these errors with {topic}:

- Starting without a plan
- Ignoring risk management
- Following emotions over logic
- Lacking patience and discipline

### Advanced Strategies

Once you've mastered the basics:

- Explore diversification options
- Consider automation tools
- Implement tax-efficient strategies
- Scale successful approaches

### Tools and Resources

Essential tools for {topic} success:

- Tracking applications
- Educational platforms
- Community forums
- Professional advisors

---

*Always consult with qualified professionals before making significant financial decisions.*"""
        }
    }
    
    # Select template
    template = templates.get(category, templates["crypto"])
    
    # Generate post
    title = random.choice(template["titles"]).format(topic=topic.title())
    tags = random.sample(template["tags"], 4)
    content = template["content"].format(topic=topic.title())
    
    # Create filename
    date = datetime.now()
    slug = title.lower().replace(' ', '-').replace(':', '').replace('?', '')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Create post directory
    year = date.strftime("%Y")
    month = date.strftime("%m")
    post_dir = os.path.join(site_path, "content", "posts", year, month)
    Path(post_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate frontmatter
    frontmatter_content = f"""---
title: "{title}"
date: {date.strftime("%Y-%m-%dT%H:%M:%S-05:00")}
draft: false
categories: ["{category}"]
tags: {tags}
summary: "Comprehensive analysis and insights on {topic} with actionable strategies for smart investors."
image: "/images/posts/{slug}.jpg"
sources:
  - url: "https://coindesk.com"
    title: "CoinDesk"
  - url: "https://cointelegraph.com"
    title: "Cointelegraph"
---

{content}"""
    
    # Save post
    filepath = os.path.join(post_dir, f"{slug}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter_content)
    
    print(f"✓ Generated: {title}")
    
    # Download image for the post
    image_url = fetch_crypto_image(topic)
    if image_url:
        images_dir = os.path.join(site_path, "static", "images", "posts")
        Path(images_dir).mkdir(parents=True, exist_ok=True)
        image_path = os.path.join(images_dir, f"{slug}.jpg")
        download_image(image_url, image_path)
    
    return filepath
def generate_content_library(site_path):
    """Generate a library of SEO-optimized content"""
    
    # Topics for content generation
    crypto_topics = [
        "Bitcoin", "Ethereum", "Solana", "Cardano", "Polygon",
        "Chainlink", "Avalanche", "Polkadot", "DeFi", "NFTs",
        "Web3", "Metaverse", "Layer 2", "Staking", "Yield Farming"
    ]
    
    finance_topics = [
        "Emergency Fund", "Passive Income", "Side Hustles", "Budgeting",
        "Credit Score", "Debt Management", "Investment Strategy", "Retirement Planning",
        "Tax Optimization", "Real Estate", "Stock Market", "Dollar Cost Averaging"
    ]
    
    security_topics = [
        "Wallet Security", "Phishing Protection", "2FA Setup", "Cold Storage",
        "Smart Contract Risks", "Exchange Security", "Privacy Coins", "VPN Usage"
    ]
    
    generated = 0
    
    # Generate crypto content
    for topic in crypto_topics[:5]:  # Start with 5 posts
        generate_seo_content(site_path, topic, "crypto")
        generated += 1
        time.sleep(1)
    
    # Generate finance content
    for topic in finance_topics[:5]:  # Start with 5 posts
        generate_seo_content(site_path, topic, "finance")
        generated += 1
        time.sleep(1)
    
    print(f"\n✓ Generated {generated} SEO-optimized posts!")
    return generated

def main():
    """Main function to process images and generate content"""
    site_path = r"C:\Users\gnul\hashnhedge\site"
    
    print("=" * 50)
    print("HASH & HEDGE CONTENT AUTOMATION")
    print("=" * 50)
    
    # Process existing posts for images
    print("\n[1/2] Processing existing posts for images...")
    process_all_posts(site_path)
    
    # Generate new content
    print("\n[2/2] Generating SEO-optimized content...")
    generate_content_library(site_path)
    
    print("\n" + "=" * 50)
    print("✓ CONTENT AUTOMATION COMPLETE!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Run: cd C:\\Users\\gnul\\hashnhedge\\site && hugo")
    print("2. Commit and push changes to GitHub")
    print("3. Monitor AdSense dashboard for revenue")

if __name__ == "__main__":
    main()