"""Keyword extraction utilities."""
import re
from typing import List

class KeywordExtractor:
    """Extract keywords from content."""
    
    STOP_WORDS = {
        'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was',
        'were', 'been', 'be', 'being', 'have', 'has', 'had', 'do', 'does',
        'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
        'can', 'shall', 'to', 'of', 'in', 'for', 'with', 'by', 'from',
        'about', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'then', 'once'
    }
    
    CRYPTO_TERMS = {
        'crypto', 'blockchain', 'bitcoin', 'ethereum', 'defi', 'nft',
        'cryptocurrency', 'trading', 'mining', 'wallet', 'exchange'
    }
    
    def extract_queries(self, title: str, tags: List[str], content: str) -> List[str]:
        """Extract search queries from article data."""
        queries = []
        
        # Clean title
        title_words = [w for w in title.lower().split() 
                      if w not in self.STOP_WORDS and len(w) > 2]
        
        # Add main query from title
        if len(title_words) > 3:
            queries.append(' '.join(title_words[:3]))
        else:
            queries.append(' '.join(title_words))
        
        # Add tag-based query
        if tags:
            tag_query = ' '.join(tags[:3])
            queries.append(tag_query)
        
        # Add crypto-related terms if relevant
        content_lower = (title + ' ' + ' '.join(tags)).lower()
        crypto_matches = [term for term in self.CRYPTO_TERMS 
                         if term in content_lower]
        if crypto_matches:
            queries.append(' '.join(crypto_matches[:2]))
        
        # Ensure we have at least one query
        if not queries:
            queries = ['technology news']
            
        return queries[:3]  # Return top 3 queries
