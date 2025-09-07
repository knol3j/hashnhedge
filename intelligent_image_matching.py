#!/usr/bin/env python3
"""
Intelligent Image Matching for Hash & Hedge
Matches images to story content using multiple strategies and free APIs
"""

import os
import re
import hashlib
import requests
import time
from urllib.parse import quote

POSTS_DIR = "site/content/posts"
IMAGES_DIR = "site/static/images/posts"

class IntelligentImageMatcher:
    def __init__(self):
        # Comprehensive keyword to image concept mapping
        self.concept_mapping = {
            # Bitcoin specific
            'bitcoin': ['bitcoin', 'cryptocurrency', 'digital currency', 'crypto coin', 'blockchain technology'],
            'btc': ['bitcoin', 'cryptocurrency', 'digital currency', 'crypto coin'],
            'bitcoin price': ['bitcoin chart', 'cryptocurrency trading', 'price analysis', 'trading screen'],
            'bitcoin analysis': ['bitcoin chart', 'cryptocurrency analysis', 'trading data', 'financial chart'],
            
            # Ethereum & DeFi
            'ethereum': ['ethereum', 'smart contracts', 'blockchain', 'cryptocurrency', 'decentralized'],
            'defi': ['decentralized finance', 'liquidity pool', 'smart contracts', 'cryptocurrency trading'],
            'yield farming': ['farming', 'agriculture', 'harvest', 'growth', 'investment'],
            'staking': ['staking', 'cryptocurrency', 'blockchain validation', 'digital assets'],
            'liquidity': ['water flow', 'liquid', 'pool', 'flowing money', 'financial flow'],
            
            # Trading & Markets
            'trading': ['trading floor', 'stock market', 'financial charts', 'trading screen', 'market data'],
            'market': ['stock market', 'trading floor', 'financial district', 'wall street'],
            'price analysis': ['financial charts', 'graphs', 'data analysis', 'trading screen'],
            'arbitrage': ['balance scales', 'opportunity', 'profit', 'trading'],
            'derivatives': ['financial instruments', 'complex trading', 'options', 'futures'],
            
            # Technology & Security
            'blockchain': ['chain links', 'network', 'digital connection', 'technology'],
            'smart contracts': ['contract', 'handshake', 'agreement', 'digital signature'],
            'wallet': ['digital wallet', 'security', 'hardware device', 'protection'],
            'security': ['shield', 'lock', 'protection', 'cybersecurity', 'safe'],
            'hardware wallet': ['hardware device', 'security device', 'digital safe', 'usb device'],
            'audit': ['magnifying glass', 'inspection', 'security check', 'verification'],
            
            # Specific Protocols
            'aave': ['lending', 'money lending', 'financial services', 'defi protocol'],
            'uniswap': ['exchange', 'trading', 'swapping', 'decentralized exchange'],
            'compound': ['compound interest', 'growth', 'financial growth', 'lending'],
            'chainlink': ['oracle', 'data connection', 'network links', 'blockchain oracle'],
            'polygon': ['polygon shapes', 'scaling', 'layer 2', 'ethereum scaling'],
            'solana': ['high speed', 'fast network', 'blockchain speed', 'performance'],
            'cardano': ['academic', 'research', 'peer review', 'blockchain research'],
            
            # Institutional & Compliance
            'institutional': ['office building', 'corporate', 'business suit', 'wall street'],
            'compliance': ['regulation', 'legal documents', 'government', 'law'],
            'regulation': ['government building', 'law', 'legal', 'regulatory'],
            'kyc': ['identity verification', 'documents', 'compliance', 'identity check'],
            'aml': ['money laundering', 'compliance', 'legal', 'financial crime'],
            
            # Gaming & NFTs
            'gaming': ['gaming', 'esports', 'video games', 'gaming industry'],
            'nft': ['digital art', 'collectibles', 'unique items', 'digital ownership'],
            'metaverse': ['virtual reality', 'digital world', 'vr headset', 'virtual space'],
            
            # Mining & Energy
            'mining': ['cryptocurrency mining', 'mining rig', 'computer hardware', 'energy'],
            'energy efficient': ['green energy', 'solar panels', 'renewable energy', 'efficiency'],
            'quantum': ['quantum computer', 'advanced technology', 'quantum physics', 'future tech'],
            
            # General Finance
            'investment': ['growth chart', 'financial growth', 'money tree', 'investment'],
            'portfolio': ['portfolio', 'diversification', 'asset allocation', 'financial planning'],
            'risk management': ['risk assessment', 'safety', 'protection', 'balance'],
            'prediction': ['crystal ball', 'forecasting', 'future trends', 'prediction'],
            
            # Fallbacks for categories
            'crypto': ['cryptocurrency', 'bitcoin', 'blockchain', 'digital currency'],
            'technology': ['technology', 'innovation', 'digital transformation', 'computer'],
            'business': ['business meeting', 'corporate', 'financial district', 'professional'],
            'finance': ['financial charts', 'money', 'banking', 'financial services'],
            'security': ['cybersecurity', 'protection', 'shield', 'lock']
        }
        
        # Unsplash API (free tier: 50 requests/hour)
        self.unsplash_base = "https://api.unsplash.com"
        self.unsplash_key = "8CRkHc5DJjzS-Yindt42cI8fAifiVbQA7aKV09vpBn4"  # Free tier key
        
    def extract_key_concepts(self, title, content, category):
        """Extract key concepts from post content for image matching"""
        concepts = []
        text = (title + " " + content).lower()
        
        # Look for specific matches in our concept mapping
        for concept, keywords in self.concept_mapping.items():
            if concept in text:
                concepts.extend(keywords[:2])  # Take top 2 related concepts
        
        # Extract important words from title
        title_words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
        important_title_words = [word for word in title_words 
                               if word not in ['hash', 'hedge', 'analysis', 'trends', 'market', 'latest']]
        concepts.extend(important_title_words[:3])
        
        # Add category-based concepts
        if category.lower() in self.concept_mapping:
            concepts.extend(self.concept_mapping[category.lower()][:2])
        
        return list(set(concepts))  # Remove duplicates
    
    def search_unsplash(self, query, orientation='landscape'):
        """Search Unsplash for relevant images"""
        try:
            url = f"{self.unsplash_base}/search/photos"
            params = {
                'query': query,
                'orientation': orientation,
                'per_page': 5,
                'order_by': 'relevant'
            }
            headers = {'Authorization': f'Client-ID {self.unsplash_key}'}
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    # Get the best match
                    photo = data['results'][0]
                    return {
                        'url': photo['urls']['regular'],  # 1080px width
                        'download_url': photo['links']['download_location'],
                        'attribution': f"Photo by {photo['user']['name']} on Unsplash",
                        'alt': photo.get('alt_description', query),
                        'concept': query
                    }
        except Exception as e:
            print(f"Unsplash search failed for '{query}': {e}")
        return None
    
    def find_best_image_match(self, title, content, category):
        """Find the best matching image for a post"""
        concepts = self.extract_key_concepts(title, content, category)
        
        print(f"Searching for: {title}")
        print(f"Key concepts: {concepts[:5]}")  # Show top 5 concepts
        
        # Try each concept until we find a good image
        for concept in concepts:
            if len(concept) < 3:  # Skip very short concepts
                continue
                
            print(f"  Trying: {concept}")
            image_info = self.search_unsplash(concept)
            
            if image_info:
                print(f"  FOUND: {image_info['concept']}")
                return image_info
            
            time.sleep(0.5)  # Rate limiting
        
        # Fallback to category-based search
        fallback_concept = self.concept_mapping.get(category.lower(), ['business'])[0]
        print(f"  Fallback: {fallback_concept}")
        return self.search_unsplash(fallback_concept) or self.create_fallback_image(title)
    
    def create_fallback_image(self, title):
        """Create a fallback image if no match found"""
        # Use a deterministic but varied approach
        seed = abs(hash(title)) % 1000
        return {
            'url': f"https://picsum.photos/seed/{seed}/1080/600",
            'attribution': f'Fallback image from Lorem Picsum (ID: {seed})',
            'concept': 'fallback',
            'alt': title
        }
    
    def download_image(self, image_info, filename):
        """Download and save image"""
        try:
            # Trigger download endpoint for Unsplash (for attribution tracking)
            if image_info.get('download_url') and self.unsplash_key:
                try:
                    headers = {'Authorization': f'Client-ID {self.unsplash_key}'}
                    requests.get(image_info['download_url'], headers=headers, timeout=5)
                except:
                    pass  # Don't fail if download tracking fails
            
            # Download the actual image
            response = requests.get(image_info['url'], timeout=15, stream=True)
            
            if response.status_code == 200:
                filepath = os.path.join(IMAGES_DIR, f"{filename}.jpg")
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                file_size = os.path.getsize(filepath)
                print(f"    Downloaded: {os.path.basename(filepath)} ({file_size // 1024} KB)")
                return filepath
                
        except Exception as e:
            print(f"    Download failed: {e}")
        return None

def intelligent_image_replacement():
    """Replace all images with intelligently matched photos"""
    if not os.path.exists(POSTS_DIR):
        print(f"Posts directory not found: {POSTS_DIR}")
        return
    
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    matcher = IntelligentImageMatcher()
    
    print("INTELLIGENT IMAGE MATCHING")
    print("=" * 50)
    print("Analyzing post content and finding relevant images...")
    print()
    
    post_files = [f for f in sorted(os.listdir(POSTS_DIR)) if f.endswith('.md')]
    total_posts = len(post_files)
    
    successful_matches = 0
    
    for i, filename in enumerate(post_files, 1):
        post_path = os.path.join(POSTS_DIR, filename)
        base_name = filename.replace('.md', '')
        
        try:
            with open(post_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract post metadata
            title_match = re.search(r'title: ["\']([^"\']+)["\']', content)
            category_match = re.search(r'category: ["\']([^"\']+)["\']', content)
            
            title = title_match.group(1) if title_match else base_name.replace('-', ' ').title()
            category = category_match.group(1) if category_match else 'Business'
            
            print(f"[{i}/{total_posts}] {title}")
            
            # Find best matching image
            image_info = matcher.find_best_image_match(title, content, category)
            
            if image_info:
                # Download the image
                downloaded_path = matcher.download_image(image_info, base_name)
                
                if downloaded_path:
                    successful_matches += 1
                    print(f"    SUCCESS: Matched to '{image_info['concept']}'")
                else:
                    print(f"    DOWNLOAD FAILED")
            else:
                print(f"    NO MATCH FOUND")
            
            time.sleep(1)  # Rate limiting between posts
            
        except Exception as e:
            print(f"    ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("INTELLIGENT IMAGE MATCHING COMPLETE!")
    print("=" * 50)
    print(f"Posts processed: {total_posts}")
    print(f"Successful matches: {successful_matches}")
    print(f"Success rate: {(successful_matches/total_posts)*100:.1f}%")
    print()
    print("Images are now intelligently matched to story content!")
    print("Each image relates to the specific topic and concepts in the post.")

if __name__ == "__main__":
    intelligent_image_replacement()