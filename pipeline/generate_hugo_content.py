#!/usr/bin/env python3
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
        self.briefs_path = self.site_path / "content" / "briefs"
        
        # Ensure directories exist
        self.posts_path.mkdir(parents=True, exist_ok=True)
        self.briefs_path.mkdir(parents=True, exist_ok=True)
        
        # RSS feeds for content inspiration
        self.rss_feeds = [
            "https://cointelegraph.com/rss",
            "https://www.coindesk.com/arc/outboundfeeds/rss/",
            "https://decrypt.co/feed",
            "https://bitcoinmagazine.com/feed"
        ]
        
    def fetch_trending_topics(self):
        """Fetch trending topics from RSS feeds"""
        topics = []
        try:
            for feed_url in self.rss_feeds[:2]:  # Limit to avoid rate limiting
                response = requests.get(feed_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'xml')
                    items = soup.find_all('item')[:5]  # Get top 5 items
                    for item in items:
                        title = item.find('title')
                        if title:
                            topics.append(title.text)
        except:
            pass
        return topics
    
    def generate_title(self, template_type="market"):
        """Generate dynamic post title"""
        templates = {
            "market": [
                "Bitcoin {action} Above ${price}K as {catalyst}",
                "{altcoin} Outperforms Market with {percent}% Gain",
                "Crypto Market {sentiment}: What {timeframe} Holds"
            ],
            "defi": [
                "DeFi TVL {action} to ${amount}B Amid {trend}",
                "{protocol} Protocol Launches {feature} for {benefit}",
                "Yield Farming Alert: {percent}% APY on {platform}"
            ],
            "analysis": [
                "Technical Analysis: {crypto} {pattern} Signals {direction}",
                "{indicator} Suggests {crypto} {action} Incoming",
                "On-Chain Data Reveals {insight} for {crypto}"
            ]
        }
        
        variables = {
            "action": ["Surges", "Rallies", "Consolidates", "Breaks", "Tests"],
            "price": [100, 105, 110, 115, 120],
            "catalyst": ["Institutional Buying", "ETF Momentum", "Fed Decision", "Tech Breakout"],
            "altcoin": ["Ethereum", "Solana", "Avalanche", "Polygon", "Arbitrum"],
            "percent": [5, 10, 15, 20, 25],
            "sentiment": ["Bullish", "Cautious", "Optimistic", "Mixed"],
            "timeframe": ["This Week", "February", "Q1 2025", "The Coming Days"],
            "amount": [150, 200, 250, 300],
            "protocol": ["Aave", "Compound", "Uniswap", "Curve", "MakerDAO"],
            "feature": ["Staking V2", "Cross-Chain Bridge", "Governance Token", "Liquidity Mining"],
            "benefit": ["Higher Yields", "Lower Fees", "Better Security", "More Flexibility"],
            "platform": ["Ethereum", "Arbitrum", "Optimism", "Base"],
            "crypto": ["BTC", "ETH", "SOL", "AVAX"],
            "pattern": ["Bull Flag", "Cup and Handle", "Ascending Triangle", "Double Bottom"],
            "direction": ["Breakout", "Rally", "Reversal", "Continuation"],
            "indicator": ["RSI", "MACD", "Moving Averages", "Volume"],
            "insight": ["Accumulation Phase", "Whale Activity", "Exchange Outflows", "Strong Demand"]
        }        
        # Select template
        template_list = templates.get(template_type, templates["market"])
        template = random.choice(template_list)
        
        # Fill in variables
        for var, values in variables.items():
            if f"{{{var}}}" in template:
                value = random.choice(values)
                template = template.replace(f"{{{var}}}", str(value))
                
        return template
    
    def generate_content(self, title, template_type="market"):
        """Generate post content based on type"""
        
        # Market update template
        if "market" in template_type.lower() or "bitcoin" in title.lower():
            content = f"""
The cryptocurrency market continues to evolve with significant developments impacting investor sentiment and market dynamics.

## Market Overview

{self._generate_market_overview()}

## Technical Analysis

{self._generate_technical_analysis()}

## Key Factors to Watch

{self._generate_key_factors()}

## Investment Implications

{self._generate_investment_implications()}

## Conclusion

{self._generate_conclusion(title)}
"""
        
        # DeFi template
        elif "defi" in template_type.lower() or "protocol" in title.lower():
            content = f"""
The decentralized finance ecosystem shows continued innovation and growth opportunities for savvy investors.

## Protocol Overview

{self._generate_protocol_overview()}

## Yield Opportunities

{self._generate_yield_analysis()}

## Risk Assessment

{self._generate_risk_assessment()}

## Strategy Recommendations

{self._generate_strategy_recommendations()}
"""
        
        # Default analysis template
        else:
            content = f"""
Our latest analysis reveals important insights for cryptocurrency investors and traders.

## Executive Summary

{self._generate_executive_summary()}

## Detailed Analysis

{self._generate_detailed_analysis()}

## Market Implications

{self._generate_market_implications()}

## Action Items

{self._generate_action_items()}
"""
        
        return content.strip()
    
    def _generate_market_overview(self):
        """Generate market overview section"""
        templates = [
            "Bitcoin's price action suggests {trend} momentum as {indicator} shows {signal}. Trading volume has {volume_action} significantly, indicating {market_sentiment} market participation.",
            "The broader cryptocurrency market is experiencing {market_condition} conditions, with {percentage}% of altcoins {altcoin_action} against Bitcoin. This suggests {market_phase} in the current cycle.",
            "Institutional interest remains {institutional_sentiment} with {metric} reaching {value}. This aligns with {narrative} narrative gaining traction among {investor_type} investors."
        ]
        
        variables = {
            "trend": ["bullish", "neutral", "consolidating"],
            "indicator": ["RSI", "MACD", "moving averages"],
            "signal": ["positive divergence", "support holding", "breakout potential"],
            "volume_action": ["increased", "remained steady", "picked up"],
            "market_sentiment": ["growing", "stable", "cautious"],
            "market_condition": ["favorable", "mixed", "challenging"],
            "percentage": [60, 65, 70, 75],
            "altcoin_action": ["gaining", "holding steady", "showing strength"],
            "market_phase": ["accumulation", "expansion", "consolidation"],
            "institutional_sentiment": ["strong", "growing", "steady"],
            "metric": ["on-chain volume", "wallet addresses", "network activity"],
            "value": ["new highs", "multi-month highs", "significant levels"],
            "narrative": ["adoption", "institutional", "DeFi growth"],
            "investor_type": ["retail", "institutional", "long-term"]
        }
        
        template = random.choice(templates)
        for var, values in variables.items():
            if f"{{{var}}}" in template:
                template = template.replace(f"{{{var}}}", str(random.choice(values)))
                
        return template    
    def _generate_technical_analysis(self):
        """Generate technical analysis section"""
        price = random.randint(90000, 120000)
        support = price - random.randint(5000, 10000)
        resistance = price + random.randint(5000, 10000)
        
        return f"""Current price action shows Bitcoin trading around ${price:,}, with immediate support at ${support:,} and resistance at ${resistance:,}. The {random.choice(['4-hour', 'daily', 'weekly'])} chart displays a {random.choice(['bullish flag', 'ascending triangle', 'consolidation pattern'])}, suggesting potential for {random.choice(['upward continuation', 'breakout', 'trend reversal'])}."""
    
    def _generate_key_factors(self):
        """Generate key factors section"""
        factors = [
            "Institutional adoption metrics showing continued growth",
            "On-chain data indicating accumulation by long-term holders",
            "Macroeconomic factors favoring risk-on assets",
            "Technical indicators approaching key decision points",
            "Network fundamentals remaining robust"
        ]
        selected = random.sample(factors, 3)
        return "\n".join([f"- {factor}" for factor in selected])
    
    def _generate_investment_implications(self):
        """Generate investment implications"""
        implications = [
            "Long-term holders may view current levels as accumulation opportunities",
            "Short-term traders should monitor key support/resistance levels closely",
            "Dollar-cost averaging strategies remain effective in current market conditions",
            "Risk management becomes crucial during periods of elevated volatility"
        ]
        return random.choice(implications)
    
    def _generate_conclusion(self, title):
        """Generate conclusion based on title"""
        return f"As the market continues to evolve, staying informed about these developments helps investors make better decisions. {title.split()[0]} remains a key focus for market participants."
    
    # Simplified stub methods for other content types
    def _generate_protocol_overview(self):
        return "Leading DeFi protocols continue to innovate with new features designed to attract liquidity and users."
    
    def _generate_yield_analysis(self):
        return f"Current yield opportunities range from {random.randint(5,15)}% to {random.randint(20,50)}% APY across various protocols."
    
    def _generate_risk_assessment(self):
        return "Smart contract risk, impermanent loss, and market volatility remain primary considerations."
    
    def _generate_strategy_recommendations(self):
        return "Diversification across protocols and careful position sizing can help optimize risk-adjusted returns."
    
    def _generate_executive_summary(self):
        return "Market conditions present both opportunities and challenges for cryptocurrency investors."
    
    def _generate_detailed_analysis(self):
        return "Technical and fundamental factors align to suggest continued market development."
    
    def _generate_market_implications(self):
        return "These developments may lead to increased market participation and price discovery."
    
    def _generate_action_items(self):
        return "Monitor key levels, maintain disciplined risk management, and stay informed about market developments."
    
    def generate_post(self):
        """Generate a complete blog post"""
        # Determine post type
        post_types = ["market", "defi", "analysis"]
        weights = [0.5, 0.3, 0.2]  # 50% market, 30% defi, 20% analysis
        post_type = random.choices(post_types, weights=weights)[0]
        
        # Generate title
        title = self.generate_title(post_type)
        
        # Generate slug from title
        slug = title.lower()
        slug = slug.replace(" ", "-").replace("$", "").replace("%", "percent")
        slug = slug.replace(":", "").replace("?", "").replace("'", "")
        slug = slug[:60]  # Limit length
        
        # Generate content
        content = self.generate_content(title, post_type)
        
        # Create metadata
        now = datetime.now()
        metadata = {
            "title": title,
            "date": now.strftime("%Y-%m-%dT%H:%M:%S-07:00"),
            "draft": False,
            "categories": self._get_categories(post_type),
            "tags": self._get_tags(title, post_type),
            "description": f"{title}. Get the latest cryptocurrency market analysis and insights.",
            "featured_image": f"/images/posts/{slug}/hero.png",
            "images": [
                f"/images/posts/{slug}/hero.png",
                f"/images/posts/{slug}/thumb.png"
            ]
        }
        
        return {
            "filename": f"{now.strftime('%Y%m%d')}-{slug}.md",
            "metadata": metadata,
            "content": content
        }    
    def _get_categories(self, post_type):
        """Get categories based on post type"""
        category_map = {
            "market": ["crypto", "markets"],
            "defi": ["defi", "tech"],
            "analysis": ["analysis", "trading"]
        }
        return category_map.get(post_type, ["crypto"])
    
    def _get_tags(self, title, post_type):
        """Generate relevant tags"""
        tags = []
        
        # Check title for keywords
        title_lower = title.lower()
        if "bitcoin" in title_lower or "btc" in title_lower:
            tags.append("bitcoin")
        if "ethereum" in title_lower or "eth" in title_lower:
            tags.append("ethereum")
        if "defi" in title_lower:
            tags.append("defi")
        if "market" in title_lower:
            tags.append("market analysis")
        if "technical" in title_lower:
            tags.append("technical analysis")
            
        # Add type-specific tags
        if post_type == "market":
            tags.extend(["trading", "price analysis"])
        elif post_type == "defi":
            tags.extend(["yield farming", "liquidity"])
        elif post_type == "analysis":
            tags.extend(["cryptocurrency", "investing"])
            
        # Return unique tags
        return list(set(tags))[:5]
    
    def save_post(self, post_data):
        """Save the generated post to file"""
        # Create post directory structure
        post_slug = post_data["metadata"]["title"].lower().replace(" ", "-")[:60]
        post_slug = ''.join(c for c in post_slug if c.isalnum() or c == '-')
        
        # Create image directory
        image_dir = self.site_path / "static" / "images" / "posts" / post_slug
        image_dir.mkdir(parents=True, exist_ok=True)
        
        # Create placeholder images if they don't exist
        from setup_all_post_images import PostImageSetup
        image_setup = PostImageSetup(str(self.site_path))
        
        hero_path = image_dir / "hero.png"
        if not hero_path.exists():
            image_setup.create_placeholder_image(
                post_data["metadata"]["title"],
                hero_path
            )
        
        thumb_path = image_dir / "thumb.png"
        if not thumb_path.exists() and hero_path.exists():
            # Copy hero as thumb for now
            import shutil
            shutil.copy(hero_path, thumb_path)
        
        # Create the post content
        yaml_header = yaml.dump(post_data["metadata"], default_flow_style=False, sort_keys=False)
        full_content = f"---\n{yaml_header}---\n\n{post_data['content']}"
        
        # Save the post
        post_path = self.posts_path / post_data["filename"]
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
            
        print(f"[OK] Created post: {post_data['filename']}")
        return post_path


def main():
    """Main execution function"""
    print("Hash & Hedge Content Generator")
    print("==============================\n")
    
    generator = HugoContentGenerator()
    
    # Get trending topics (optional)
    print("Fetching trending topics...")
    topics = generator.fetch_trending_topics()
    if topics:
        print(f"Found {len(topics)} trending topics")
    
    # Generate a new post
    print("\nGenerating new post...")
    post = generator.generate_post()
    
    # Save the post
    saved_path = generator.save_post(post)
    
    print(f"\nPost Details:")
    print(f"Title: {post['metadata']['title']}")
    print(f"Categories: {', '.join(post['metadata']['categories'])}")
    print(f"Tags: {', '.join(post['metadata']['tags'])}")
    print(f"File: {saved_path}")
    
    print("\nContent generation complete!")


if __name__ == "__main__":
    main()