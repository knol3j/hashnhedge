"""Crypto-specific keyword extraction utilities."""
import re
from typing import List, Set
from pathlib import Path

class CryptoKeywordExtractor:
    """Extract crypto-relevant keywords from content."""
    
    # Core crypto/finance terms that should be included
    CRYPTO_TERMS = {
        'crypto', 'cryptocurrency', 'bitcoin', 'btc', 'ethereum', 'eth',
        'blockchain', 'defi', 'nft', 'web3', 'mining', 'wallet', 'ledger',
        'exchange', 'binance', 'coinbase', 'trading', 'market', 'chart',
        'halving', 'airdrop', 'token', 'stablecoin', 'altcoin', 'hodl',
        'bull', 'bear', 'whale', 'satoshi', 'gwei', 'gas', 'staking',
        'yield', 'farming', 'liquidity', 'dex', 'cex', 'dao', 'dapp',
        'smart contract', 'consensus', 'proof of work', 'proof of stake',
        'hash', 'hedge', 'portfolio', 'investment', 'analysis', 'price',
        'volume', 'capitalization', 'dominance', 'resistance', 'support'
    }
    
    # Expanded coin/token names and tickers
    COIN_MAPPINGS = {
        'bitcoin': ['bitcoin', 'btc'],
        'ethereum': ['ethereum', 'eth', 'ether'],
        'solana': ['solana', 'sol'],
        'cardano': ['cardano', 'ada'],
        'ripple': ['ripple', 'xrp'],
        'polkadot': ['polkadot', 'dot'],
        'chainlink': ['chainlink', 'link'],
        'polygon': ['polygon', 'matic'],
        'avalanche': ['avalanche', 'avax'],
        'cosmos': ['cosmos', 'atom'],
        'algorand': ['algorand', 'algo'],
        'near': ['near', 'near protocol'],
        'fantom': ['fantom', 'ftm'],
        'arbitrum': ['arbitrum', 'arb'],
        'optimism': ['optimism', 'op'],
    }
    
    # Terms to avoid in image searches (nature/generic images)
    NEGATIVE_TERMS = {
        'butterfly', 'flower', 'nature', 'animal', 'landscape', 'beach',
        'sky', 'food', 'cute', 'cat', 'dog', 'bird', 'tree', 'forest',
        'mountain', 'ocean', 'sunset', 'sunrise', 'rainbow', 'cloud',
        'insect', 'dragonfly', 'bee', 'plant', 'garden', 'park'
    }
    
    # Visual/aesthetic terms that work well for crypto imagery
    VISUAL_TERMS = {
        'digital', 'cyber', 'neon', 'futuristic', 'technology', 'network',
        'matrix', 'circuit', 'code', 'data', 'graph', 'candlestick',
        'dashboard', 'monitor', 'screen', 'computer', 'server', 'fintech',
        'revolution', 'disruption', 'innovation', 'decentralized'
    }
    
    def __init__(self):
        """Initialize the keyword extractor."""
        self.stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was',
            'were', 'been', 'be', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
            'can', 'shall', 'to', 'of', 'in', 'for', 'with', 'by', 'from',
            'about', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then', 'once'
        }
    
    def extract_crypto_terms(self, text: str) -> Set[str]:
        """Extract crypto-specific terms from text."""
        text_lower = text.lower()
        found_terms = set()
        
        # Check for crypto terms
        for term in self.CRYPTO_TERMS:
            if term in text_lower:
                found_terms.add(term)
        
        # Check for coin names and add their variants
        for coin, variants in self.COIN_MAPPINGS.items():
            if any(variant in text_lower for variant in variants):
                found_terms.update(variants[:2])  # Add main name and ticker
        
        return found_terms
    
    def clean_title(self, title: str) -> List[str]:
        """Extract clean keywords from title."""
        # Remove special characters and numbers from title
        clean = re.sub(r'[^\w\s-]', '', title.lower())
        clean = re.sub(r'[\d]+', '', clean)
        
        # Split and filter
        words = [w for w in clean.split() 
                if w not in self.stop_words and len(w) > 2]
        
        return words[:5]  # Return top 5 words
    
    def build_search_queries(self, title: str, tags: List[str], 
                           content: str = "") -> List[str]:
        """Build optimized search queries for crypto content."""
        queries = []
        
        # Extract crypto terms from all text
        all_text = f"{title} {' '.join(tags)} {content[:500]}"
        crypto_terms = self.extract_crypto_terms(all_text)
        
        # Clean title words
        title_words = self.clean_title(title)
        
        # Query 1: Crypto terms + visual terms
        if crypto_terms:
            # Pick 2-3 crypto terms and add visual context
            selected_crypto = list(crypto_terms)[:3]
            visual_additions = ['digital', 'trading', 'chart']
            query1 = ' '.join(selected_crypto + visual_additions[:2])
            queries.append(query1)
        
        # Query 2: Title-based with crypto context
        if title_words:
            # Use title words and ensure crypto context
            title_query = ' '.join(title_words[:3])
            if not any(term in title_query for term in ['crypto', 'bitcoin', 'blockchain']):
                title_query += ' cryptocurrency'
            queries.append(title_query)
        
        # Query 3: Tag-based with specific focus
        if tags:
            tag_query = ' '.join([tag.lower() for tag in tags[:3]])
            if 'analysis' in tag_query or 'price' in tag_query:
                tag_query += ' chart candlestick'
            elif 'defi' in tag_query:
                tag_query += ' decentralized finance'
            queries.append(tag_query)
        
        # Fallback query if no specific terms found
        if not queries or not crypto_terms:
            queries.append('cryptocurrency bitcoin trading digital')
        
        # Add negative terms to all queries
        negative_string = ' -' + ' -'.join(list(self.NEGATIVE_TERMS)[:5])
        queries = [q + negative_string for q in queries]
        
        # Ensure uniqueness and limit
        return list(dict.fromkeys(queries))[:3]
    
    def generate_alt_text(self, title: str, tags: List[str], 
                         provider: str = "") -> str:
        """Generate SEO-friendly alt text for crypto images."""
        # Start with title
        alt_parts = [title]
        
        # Add relevant tags
        if tags:
            relevant_tags = [tag for tag in tags[:3] 
                           if tag.lower() in self.CRYPTO_TERMS 
                           or any(coin in tag.lower() 
                                 for coin in self.COIN_MAPPINGS)]
            if relevant_tags:
                alt_parts.append('featuring ' + ', '.join(relevant_tags))
        
        # Add crypto context
        alt_parts.append('- cryptocurrency and blockchain content')
        
        # Add site branding
        alt_parts.append('| Hash & Hedge')
        
        alt_text = ' '.join(alt_parts)
        return alt_text[:125]  # Limit to 125 chars for SEO
