#!/usr/bin/env python3
"""
Generate posts for Hash & Hedge - because apparently we need robots to tell us 
what to think about crypto and security now. Welcome to the future, it's dumber 
than we thought.
"""

import argparse
import datetime
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import feedparser
    import requests
    from bs4 import BeautifulSoup
    import frontmatter
except ImportError:
    print("Missing dependencies. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                         "feedparser", "requests", "beautifulsoup4", 
                         "python-frontmatter", "lxml"])
    import feedparser
    import requests
    from bs4 import BeautifulSoup
    import frontmatter

# RSS Sources - because we're too lazy to find our own news
RSS_FEEDS = {
    'crypto': [
        'https://cointelegraph.com/rss',
        'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'https://decrypt.co/feed',
        'https://bitcoinmagazine.com/feed',
        'https://cryptonews.com/news/feed/',
    ],
    'security': [
        'https://krebsonsecurity.com/feed/',
        'https://feeds.feedburner.com/TheHackersNews',
        'https://www.bleepingcomputer.com/feed/',
        'https://www.darkreading.com/rss.xml',
        'https://threatpost.com/feed/',
    ],
    'finance': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.ft.com/rss/home',
        'https://feeds.wsj.com/rss/RSSMarketsMain.xml',
        'https://www.marketwatch.com/rss/',
    ]
}

# Keywords that make us care
TRENDING_KEYWORDS = [
    'hack', 'breach', 'exploit', 'vulnerability', 'crypto', 'bitcoin', 
    'ethereum', 'defi', 'nft', 'web3', 'blockchain', 'ransomware',
    'zero-day', 'malware', 'phishing', 'regulation', 'sec', 'cbdc',
    'stablecoin', 'altcoin', 'mining', 'wallet', 'exchange', 'fraud'
]

class ContentGenerator:
    """
    The digital content sweatshop where creativity goes to die and 
    SEO optimization is born.
    """
    
    def __init__(self, site_path: str = "../site"):
        self.site_path = Path(site_path)
        self.content_path = self.site_path / "content" / "posts"
        self.static_path = self.site_path / "static" / "images" / "posts"
        
    def fetch_stories(self, category: str) -> List[Dict]:
        """
        Scrape the internet like a digital vulture picking at the 
        carcass of journalism.
        """
        stories = []
        feeds = RSS_FEEDS.get(category, [])
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:5]:  # Top 5 stories per feed
                    story = {
                        'title': entry.get('title', 'Untitled Drivel'),
                        'link': entry.get('link', '#'),
                        'summary': entry.get('summary', ''),
                        'published': entry.get('published_parsed'),
                        'category': category
                    }
                    
                    # Score based on keywords (because algorithms know best)
                    score = sum(1 for kw in TRENDING_KEYWORDS 
                              if kw.lower() in story['title'].lower() + 
                              story['summary'].lower())
                    story['relevance_score'] = score
                    
                    stories.append(story)
            except Exception as e:
                print(f"Failed to fetch {feed_url}: {e}")
                
        # Sort by relevance because engagement metrics rule everything
        return sorted(stories, key=lambda x: x['relevance_score'], reverse=True)
    
    def generate_post_content(self, story: Dict) -> str:
        """
        Transform a boring RSS entry into something that might trick 
        Google's algorithm into thinking we're original.
        """
        # Craft engaging intro with a hook sharper than my existential dread
        intros = [
            f"Look, we need to talk about {story['title']} because apparently nobody else will.",
            f"Another day, another {story['category']} story that makes me question why I even get out of bed.",
            f"So {story['title']} happened, and honestly, I'm not even surprised anymore.",
            f"In today's episode of 'Everything is Terrible,' we have {story['title']}.",
            f"Buckle up, buttercups - {story['title']} is about to ruin your day in the most predictable way possible."
        ]
        
        content = random.choice(intros) + "\n\n"
        
        # Add the summary but make it sound like we care
        if story.get('summary'):
            soup = BeautifulSoup(story['summary'], 'html.parser')
            clean_summary = soup.get_text().strip()
            content += f"Here's the TL;DR for those of you with the attention span of a TikTok video: {clean_summary}\n\n"
        
        # Add some "analysis" (read: hot takes and speculation)
        analysis_templates = [
            "The real question nobody's asking is: who benefits from this clusterfuck?",
            "This is exactly the kind of thing that happens when we let {category} run wild without adult supervision.",
            "If you squint hard enough, you can see the pattern here - and it's not pretty.",
            "Remember when we thought {category} would save us all? Yeah, me neither.",
            "The implications here are staggering, assuming anyone actually gives a damn."
        ]
        
        content += random.choice(analysis_templates).format(category=story['category']) + "\n\n"
        content += f"[Read more at the source]({story['link']}) if you hate yourself that much.\n"
        
        return content
    
    def create_post(self, story: Dict, post_num: int) -> Path:
        """
        Birth another piece of content into this godforsaken internet wasteland.
        Each post crafted with the same enthusiasm I have for my quarterly taxes.
        """
        now = datetime.datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        
        # Create directory structure like we're building a monument to mediocrity
        post_dir = self.content_path / year / month
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate slug from title (remove all the interesting bits)
        slug = re.sub(r'[^\w\s-]', '', story['title'].lower())
        slug = re.sub(r'[-\s]+', '-', slug)[:50]  # Keep it short like my attention span
        slug = f"{slug}-{now.strftime('%Y%m%d%H%M%S')}"
        
        # Frontmatter - the metadata nobody reads but SEO demands
        frontmatter_data = {
            'title': story['title'],
            'date': now.isoformat(),
            'draft': False,
            'categories': [story['category']],
            'tags': [kw for kw in TRENDING_KEYWORDS 
                    if kw.lower() in story['title'].lower()],
            'description': story.get('summary', '')[:160] + '...',
            'author': 'Hash & Hedge Bot',
            'image': '',  # We'll fill this later, like all my promises
            'source_url': story['link'],
            'relevance_score': story['relevance_score']
        }
        
        # Generate content with the enthusiasm of a DMV employee
        content = self.generate_post_content(story)
        
        # Create the post file
        post_path = post_dir / f"{slug}.md"
        post = frontmatter.Post(content, **frontmatter_data)
        
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))
            
        print(f"✍️ Created post: {post_path}")
        return post_path
    
    def bulk_generate(self, count: int = 1) -> List[Path]:
        """
        Mass produce content like a factory farm produces sadness.
        Because quantity over quality is the American way, baby.
        """
        posts_created = []
        all_stories = []
        
        # Gather stories from all categories like we're hoarding toilet paper
        for category in RSS_FEEDS.keys():
            stories = self.fetch_stories(category)
            all_stories.extend(stories[:count * 2])  # Get extras, we're picky
        
        # Sort by relevance and remove duplicates (like my dating life)
        seen_titles = set()
        unique_stories = []
        for story in sorted(all_stories, key=lambda x: x['relevance_score'], reverse=True):
            if story['title'] not in seen_titles:
                seen_titles.add(story['title'])
                unique_stories.append(story)
        
        # Generate the requested number of posts
        for i, story in enumerate(unique_stories[:count]):
            try:
                post_path = self.create_post(story, i + 1)
                posts_created.append(post_path)
            except Exception as e:
                print(f"💥 Failed to create post: {e}")
                
        return posts_created

def main():
    """
    The main event, where all our beautiful dysfunction comes together
    like a car crash you can't look away from.
    """
    parser = argparse.ArgumentParser(
        description="Generate content for Hash & Hedge because human creativity is dead"
    )
    parser.add_argument('--count', type=int, default=1,
                      help='Number of posts to generate (default: 1, max: your sanity)')
    parser.add_argument('--auto-commit', type=bool, default=True,
                      help='Auto-commit to git like you auto-commit to bad decisions')
    parser.add_argument('--site-path', default='../site',
                      help='Path to Hugo site (default: ../site)')
    
    args = parser.parse_args()
    
    print(f"🤖 Hash & Hedge Content Bot v0.0.1 - Now with 50% more existential dread!")
    print(f"📝 Generating {args.count} posts at {datetime.datetime.now()}")
    print("=" * 60)
    
    generator = ContentGenerator(args.site_path)
    posts = generator.bulk_generate(args.count)
    
    print(f"\n✅ Generated {len(posts)} posts")
    
    if args.auto_commit and posts:
        try:
            # Git operations - because version control is the only control we have
            subprocess.run(['git', 'add', '-A'], check=True)
            subprocess.run(['git', 'commit', '-m', 
                          f'content: auto-generated {len(posts)} posts - {datetime.datetime.now()}'], 
                          check=True)
            print("📤 Committed to git (no take-backs)")
        except subprocess.CalledProcessError as e:
            print(f"💩 Git commit failed: {e}")
    
    return 0 if posts else 1

if __name__ == "__main__":
    sys.exit(main())