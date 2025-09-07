#!/usr/bin/env python3
"""
Setup all blog posts with proper images and metadata for Hash & Hedge Hugo site
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import yaml
from PIL import Image, ImageDraw
from io import BytesIO

class PostImageSetup:
    """Set up all posts with proper images"""
    
    def __init__(self, site_path="site"):
        self.site_path = Path(site_path)
        self.posts_path = self.site_path / "content" / "posts"
        self.images_path = self.site_path / "static" / "images"
        
        # Ensure directories exist
        self.images_path.mkdir(parents=True, exist_ok=True)
        (self.images_path / "posts").mkdir(exist_ok=True)
        
    def parse_frontmatter(self, content):
        """Parse frontmatter from markdown content"""
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                    return frontmatter, body
            except:
                pass
        return {}, content
    
    def dump_frontmatter(self, metadata, content):
        """Create markdown content with frontmatter"""
        yaml_content = yaml.dump(metadata, default_flow_style=False, sort_keys=False)
        return f"---\n{yaml_content}---\n\n{content}"
        
    def create_placeholder_image(self, title, output_path, size=(1200, 630)):
        """Create a placeholder image with title text"""
        # Create image with gradient background
        img = Image.new('RGB', size, color='#1a1a2e')
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for i in range(size[1]):
            color_val = int(26 + (i/size[1]) * 40)
            draw.rectangle([0, i, size[0], i+1], fill=(color_val, color_val, color_val+20))
        
        # Add title text
        text_color = (255, 255, 255)
        margin = 50
        
        # Wrap text
        words = title.split() if title else ["Untitled"]
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 40:
                if len(current_line) > 1:
                    lines.append(' '.join(current_line[:-1]))
                    current_line = [word]
                else:
                    lines.append(' '.join(current_line))
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))        
        # Draw text
        y_position = size[1] // 2 - (len(lines) * 30)
        for line in lines[:4]:  # Limit to 4 lines
            text_bbox = draw.textbbox((0, 0), line)
            text_width = text_bbox[2] - text_bbox[0]
            x_position = (size[0] - text_width) // 2
            draw.text((x_position, y_position), line, fill=text_color)
            y_position += 40
            
        # Add brand
        draw.text((margin, size[1] - margin - 20), "Hash & Hedge", fill=text_color)
        
        # Save image
        img.save(output_path, 'PNG')
        return True
    
    def process_all_posts(self):
        """Process all posts and ensure they have images"""
        posts_processed = 0
        
        # Ensure logs directory exists
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Get all markdown files in posts directory
        for post_file in self.posts_path.glob("*.md"):
            print(f"\nProcessing: {post_file.name}")
            
            try:
                # Read post content
                with open(post_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse frontmatter
                metadata, body = self.parse_frontmatter(content)
                
                # Extract post slug
                slug = post_file.stem
                
                # Create image directory for this post
                post_image_dir = self.images_path / "posts" / slug
                post_image_dir.mkdir(exist_ok=True)
                
                # Check if hero image exists
                hero_image_path = post_image_dir / "hero.png"
                if not hero_image_path.exists():
                    # Create a hero image
                    title = metadata.get('title', slug.replace('-', ' ').title())
                    if self.create_placeholder_image(title, hero_image_path):
                        print(f"  [OK] Created placeholder hero image")
                
                # Create thumbnail
                thumb_path = post_image_dir / "thumb.png"
                if not thumb_path.exists() and hero_image_path.exists():
                    # Create smaller thumbnail
                    img = Image.open(hero_image_path)
                    img.thumbnail((600, 315), Image.Resampling.LANCZOS)
                    img.save(thumb_path)
                    print(f"  [OK] Created thumbnail")                
                # Update post metadata
                updated = False
                
                # Ensure featured_image is set
                if 'featured_image' not in metadata:
                    metadata['featured_image'] = f"/images/posts/{slug}/hero.png"
                    updated = True
                    
                # Ensure images array is set
                if 'images' not in metadata:
                    metadata['images'] = [
                        f"/images/posts/{slug}/hero.png",
                        f"/images/posts/{slug}/thumb.png"
                    ]
                    updated = True
                
                # Ensure date
                if 'date' not in metadata:
                    # Generate a date based on file position
                    base_date = datetime(2025, 1, 1)
                    days_offset = posts_processed * 3  # 3 days apart
                    metadata['date'] = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%dT%H:%M:%S-07:00")
                    updated = True
                    
                # Ensure draft status
                if 'draft' not in metadata:
                    metadata['draft'] = False
                    updated = True
                    
                # Ensure categories
                if 'categories' not in metadata:
                    # Infer categories from content
                    content_lower = body.lower()
                    categories = []
                    
                    if any(word in content_lower for word in ['bitcoin', 'btc', 'cryptocurrency']):
                        categories.append('crypto')
                    if any(word in content_lower for word in ['defi', 'yield', 'liquidity', 'protocol']):
                        categories.append('defi')
                    if any(word in content_lower for word in ['market', 'price', 'trading', 'analysis']):
                        categories.append('markets')
                    if any(word in content_lower for word in ['invest', 'portfolio', 'strategy']):
                        categories.append('investing')
                        
                    metadata['categories'] = categories or ['crypto']
                    updated = True
                    
                # Ensure tags
                if 'tags' not in metadata:
                    # Generate tags from title and content
                    tags = []
                    title_lower = metadata.get('title', '').lower()
                    
                    # Common crypto tags
                    tag_keywords = {
                        'bitcoin': ['bitcoin', 'btc'],
                        'ethereum': ['ethereum', 'eth'],
                        'defi': ['defi', 'decentralized'],
                        'crypto': ['crypto', 'cryptocurrency'],
                        'trading': ['trading', 'trade', 'market'],
                        'analysis': ['analysis', 'analyze', 'technical'],
                        'investing': ['invest', 'investment'],
                        'altcoins': ['altcoin', 'solana', 'polygon'],
                    }
                    
                    for tag, keywords in tag_keywords.items():
                        if any(kw in title_lower or kw in content_lower for kw in keywords):
                            tags.append(tag)
                    
                    metadata['tags'] = list(set(tags[:5]))  # Unique tags, limit to 5
                    updated = True                    
                # Save updated post if needed
                if updated:
                    new_content = self.dump_frontmatter(metadata, body)
                    with open(post_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  [OK] Updated post metadata")
                    
                posts_processed += 1
                
            except Exception as e:
                print(f"  [ERROR] Failed to process: {e}")
                continue
            
        print(f"\nProcessed {posts_processed} posts")
        return posts_processed


def setup_automation_scripts():
    """Set up the automation scripts for content generation"""
    pipeline_path = Path("pipeline")
    
    # Create enhanced Hugo content generator
    generator_content = '''#!/usr/bin/env python3
"""
Enhanced Hugo content generator with automatic scheduling
"""

import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import requests
from bs4 import BeautifulSoup

class HugoContentGenerator:
    """Generate fresh content for Hugo site"""
    
    def __init__(self, site_path="site"):
        self.site_path = Path(site_path)
        self.posts_path = self.site_path / "content" / "posts"
        self.posts_path.mkdir(parents=True, exist_ok=True)
        
        # Content templates for variety
        self.templates = {
            "market_update": {
                "titles": [
                    "Bitcoin {action} as {catalyst} {impact}",
                    "{crypto} Market Update: {trend} Amid {event}",
                    "Crypto Markets {reaction} to {news}"
                ],
                "categories": ["crypto", "markets"],
                "content_template": """
The cryptocurrency market has shown {sentiment} movement today as {main_event}.

## Market Overview
{market_analysis}

## Key Highlights
- {highlight1}
- {highlight2}
- {highlight3}

## What This Means for Investors
{investor_insight}

## Looking Ahead
{outlook}
"""
            },
            "defi_analysis": {
                "titles": [
                    "DeFi Protocol {name} {action} with {innovation}",
                    "{sector} DeFi Sector {trend} as {catalyst}",
                    "Yield Farming Update: {opportunity} in {protocol}"
                ],
                "categories": ["defi", "tech"],
                "content_template": """
The DeFi ecosystem continues to evolve with {development}.

## Protocol Overview
{protocol_analysis}

## Yield Opportunities
{yield_details}

## Risk Considerations
{risk_analysis}

## Strategy Recommendations
{recommendations}
"""
            },
            "educational": {
                "titles": [
                    "How to {action} in Crypto: A {level} Guide",
                    "Understanding {concept}: Essential {audience} Knowledge",
                    "{number} Ways to {goal} with Cryptocurrency"
                ],
                "categories": ["education", "guides"],
                "content_template": """
{introduction}

## The Basics
{basics_content}

## Step-by-Step Guide
{steps}

## Common Mistakes to Avoid
{mistakes}

## Pro Tips
{tips}

## Conclusion
{conclusion}
"""
            }
        }
        
        # Dynamic content variables
        self.variables = {
            "action": ["Surges", "Consolidates", "Breaks Out", "Rallies", "Stabilizes"],
            "catalyst": ["Institutional Adoption", "Regulatory Clarity", "Market Sentiment", "Technical Breakout"],
            "impact": ["Signals Bullish Trend", "Sparks Investor Interest", "Drives Volume Higher"],
            "crypto": ["Bitcoin", "Ethereum", "Altcoin"],
            "trend": ["Gains Momentum", "Shows Strength", "Faces Pressure"],
            "event": ["Fed Decision", "ETF Approval", "Major Partnership"],
            "reaction": ["React Positively", "Show Volatility", "Find Support"],
            "news": ["Banking Integration", "Regulatory Update", "Institutional Investment"],
            "sentiment": ["positive", "mixed", "cautious"],
            "sector": ["Lending", "DEX", "Stablecoin"],
            "innovation": ["Novel Yield Strategy", "Cross-chain Integration", "Governance Update"],
            "protocol": ["Aave", "Compound", "Uniswap", "Curve"],
            "level": ["Beginner's", "Advanced", "Complete"],
            "concept": ["DeFi Yields", "Staking Rewards", "Liquidity Pools"],
            "audience": ["Investor", "Trader", "Developer"],
            "number": ["5", "7", "10"],
            "goal": ["Maximize Returns", "Minimize Risk", "Build Wealth"]
        }
    '''
    
    generator_path = pipeline_path / "generate_hugo_content.py"
    with open(generator_path, 'w', encoding='utf-8') as f:
        f.write(generator_content)    
    print(f"[OK] Created content generator: {generator_path}")
    
    # Create scheduler batch file
    scheduler_content = """@echo off
REM Hugo Content Generation Scheduler
REM Runs 3 times daily to generate fresh content

cd /d C:\\Users\\gnul\\hashnhedge

echo [%date% %time%] Starting content generation... >> logs\\scheduler.log

REM Generate new content
echo Generating new posts...
python pipeline\\generate_hugo_content.py

REM Fetch images for new posts
echo Fetching images...
python pipeline\\fetch_images.py

REM Build the site
echo Building Hugo site...
cd site
hugo --gc --minify
cd ..

REM Optional: Auto-deploy
REM git add -A
REM git commit -m "Auto: Content update %date% %time%"
REM git push origin main

echo [%date% %time%] Content generation complete >> logs\\scheduler.log
"""
    
    scheduler_path = pipeline_path / "hugo_content_scheduler.bat"
    with open(scheduler_path, 'w') as f:
        f.write(scheduler_content)
    
    print(f"[OK] Created scheduler: {scheduler_path}")
    
    # Create PowerShell setup script
    ps_setup_content = """# Setup scheduled tasks for Hugo content generation
Write-Host "Setting up Hash & Hedge content automation..." -ForegroundColor Cyan

$taskPath = "C:\\Users\\gnul\\hashnhedge\\pipeline\\hugo_content_scheduler.bat"

# Create 3 daily tasks
$times = @("08:00", "14:00", "20:00")
foreach ($time in $times) {
    $taskName = "HashHedge-Post-$($time.Replace(':', ''))"
    
    # Remove existing
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Create new
    $action = New-ScheduledTaskAction -Execute $taskPath
    $trigger = New-ScheduledTaskTrigger -Daily -At $time
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings
    Write-Host "[OK] Created task: $taskName at $time" -ForegroundColor Green
}

Write-Host "`nSetup complete! Content will be generated 3 times daily." -ForegroundColor Green
"""
    
    ps_path = pipeline_path / "Setup-HugoAutomation.ps1"
    with open(ps_path, 'w') as f:
        f.write(ps_setup_content)
    
    print(f"[OK] Created PowerShell setup: {ps_path}")
    

if __name__ == "__main__":
    print("Hash & Hedge - Complete Setup Script")
    print("====================================\n")
    
    # Set up all post images
    print("Setting up post images...")
    setup = PostImageSetup()
    posts_count = setup.process_all_posts()
    
    # Set up automation scripts
    print("\nSetting up automation...")
    setup_automation_scripts()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print(f"\nProcessed: {posts_count} posts")
    print("\nNext Steps:")
    print("1. Review generated images in: site/static/images/posts/")
    print("2. Run PowerShell as Administrator:")
    print("   powershell -File pipeline\\Setup-HugoAutomation.ps1")
    print("3. Content will be generated automatically 3x daily")
    print("\nManual content generation:")
    print("   python pipeline\\generate_hugo_content.py")
    print("\nManual image fetch:")
    print("   python pipeline\\fetch_images.py")