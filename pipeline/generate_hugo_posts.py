#!/usr/bin/env python3
"""
generate_hugo_posts.py - Generate posts for Hugo site
"""

import os
import re
import random
import json
from datetime import datetime, timedelta
from pathlib import Path
import frontmatter
import feedparser
import requests
from bs4 import BeautifulSoup

class HugoContentGenerator:
    """Generate content for Hugo site"""
    
    def __init__(self, site_path="site"):
        self.site_path = Path(site_path)
        self.posts_path = self.site_path / "content" / "posts"
        self.posts_path.mkdir(parents=True, exist_ok=True)
        
        # Content templates
        self.post_templates = [
            {
                "title": "Bitcoin {action} as {catalyst} {timeframe}",
                "categories": ["crypto", "markets"],
                "tags": ["bitcoin", "price analysis", "market news"]
            },
            {
                "title": "{altcoin} {movement} Amid {market_condition}",
                "categories": ["crypto", "altcoins"],
                "tags": ["altcoins", "ethereum", "defi"]
            },
            {
                "title": "DeFi Protocol {action} with {innovation}",
                "categories": ["defi", "tech"],
                "tags": ["defi", "yield farming", "liquidity"]
            }
        ]
        
        # Template variables
        self.template_vars = {
            "action": ["Surges", "Consolidates", "Breaks Out", "Tests Support", "Rallies"],
            "catalyst": ["Institutional Adoption", "Regulatory News", "Market Sentiment", "Technical Breakout"],
            "timeframe": ["Continues", "Accelerates", "Signals New Trend", "Approaches Key Level"],
            "altcoin": ["Ethereum", "Solana", "Avalanche", "Polygon", "Arbitrum"],
            "movement": ["Gains Momentum", "Shows Strength", "Outperforms", "Breaks Resistance"],
            "market_condition": ["Bitcoin Rally", "Market Volatility", "DeFi Revival", "Bull Market"],
            "innovation": ["New Yield Strategy", "Cross-Chain Integration", "Layer 2 Solution", "Governance Update"]
        }
        
        # RSS feeds for content inspiration
        self.rss_feeds = [
            "https://cointelegraph.com/rss",
            "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "https://decrypt.co/feed",
            "https://bitcoinmagazine.com/feed"
        ]
    
    def generate_slug(self, title):
        """Generate URL-friendly slug"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def fetch_rss_content(self):
        """Fetch latest headlines from RSS feeds"""
        headlines = []
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Get top 5 from each
                    headlines.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', '')[:200]
                    })
            except Exception as e:
                print(f"Error fetching {feed_url}: {e}")
        return headlines
    
    def generate_content(self, headline=None):
        """Generate post content"""
        # Select random template
        template = random.choice(self.post_templates)
        
        # Generate title
        title_template = template["title"]
        for var, values in self.template_vars.items():
            if f"{{{var}}}" in title_template:
                title_template = title_template.replace(f"{{{var}}}", random.choice(values))
        
        title = title_template
        
        # Generate content based on headline or template
        if headline:
            content = f"""
The cryptocurrency market continues to evolve with significant developments. {headline.get('summary', '')}

## Market Overview

Recent market activity has shown increased interest in digital assets, with trading volumes reaching new highs across major exchanges. This trend reflects growing institutional adoption and retail investor confidence.

## Technical Analysis

Key support and resistance levels are being tested as the market navigates through various macroeconomic factors. Traders are closely monitoring these levels for potential breakout opportunities.

### Key Levels to Watch:
- Primary resistance at current highs
- Support zones holding strong
- Volume indicators suggesting continued momentum

## What This Means for Investors

For both retail and institutional investors, these developments present unique opportunities:

1. **Short-term traders** can capitalize on volatility
2. **Long-term holders** should focus on fundamental strength
3. **DeFi participants** can explore yield opportunities

## Looking Ahead

The market continues to mature with improved infrastructure and regulatory clarity. As we move forward, expect to see:

- Enhanced institutional participation
- Improved scalability solutions
- Greater mainstream adoption

Stay tuned for more updates as this story develops.

*Source: [{headline.get('title', 'Market Analysis')}]({headline.get('link', '#')})*
"""
        else:
            content = f"""
The cryptocurrency ecosystem continues to demonstrate resilience and innovation as market participants navigate the evolving landscape.

## Current Market Dynamics

Today's market action reflects the ongoing maturation of the digital asset space. With increased institutional participation and technological advancement, we're witnessing unprecedented growth in various sectors.

## Key Developments

### Infrastructure Improvements
Recent upgrades to major blockchain networks have enhanced transaction throughput and reduced costs, making DeFi more accessible to mainstream users.

### Regulatory Progress
Regulatory clarity continues to improve globally, with several jurisdictions establishing comprehensive frameworks for digital asset operations.

### Innovation in DeFi
New protocols are pushing the boundaries of what's possible in decentralized finance, offering innovative yield strategies and cross-chain functionality.

## Investment Considerations

When evaluating opportunities in the current market:

- **Risk Management**: Always employ proper risk management strategies
- **Due Diligence**: Research thoroughly before investing
- **Diversification**: Consider a balanced approach across different sectors

## Conclusion

As the market continues to evolve, staying informed and maintaining a strategic approach will be key to navigating the opportunities ahead.
"""
        
        return {
            'title': title,
            'content': content.strip(),
            'categories': template['categories'],
            'tags': template['tags']
        }
    
    def create_post(self, count=1):
        """Create new blog posts"""
        # Fetch RSS content for inspiration
        headlines = self.fetch_rss_content()
        
        for i in range(count):
            # Use RSS headline or generate from template
            headline = random.choice(headlines) if headlines and random.random() > 0.5 else None
            
            # Generate content
            post_data = self.generate_content(headline)
            
            # Create filename
            date_str = datetime.now().strftime('%Y-%m-%d')
            slug = self.generate_slug(post_data['title'])
            filename = f"{date_str}-{slug}.md"
            filepath = self.posts_path / filename
            
            # Skip if exists
            if filepath.exists():
                print(f"Post already exists: {filename}")
                continue
            
            # Create post with frontmatter
            post = frontmatter.Post(post_data['content'])
            post['title'] = post_data['title']
            post['date'] = datetime.now().isoformat()
            post['draft'] = False
            post['categories'] = post_data['categories']
            post['tags'] = post_data['tags']
            post['description'] = post_data['content'][:160] + "..."
            
            # Add placeholder image paths
            post['featured_image'] = f"/images/posts/{slug}/hero.jpg"
            post['images'] = [f"/images/posts/{slug}/hero.jpg"]
            
            # Save post
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            print(f"Created post: {filename}")
            
            # Create image directory
            image_dir = self.site_path / "static" / "images" / "posts" / slug
            image_dir.mkdir(parents=True, exist_ok=True)

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Hugo posts")
    parser.add_argument('--count', type=int, default=1, help='Number of posts to generate')
    parser.add_argument('--site-path', default='site', help='Path to Hugo site')
    
    args = parser.parse_args()
    
    print("Hash & Hedge Hugo Content Generator")
    print("=" * 60)
    
    generator = HugoContentGenerator(args.site_path)
    generator.create_post(args.count)
    
    print("\nDone! Remember to run fetch_images to add images.")

if __name__ == "__main__":
    main()