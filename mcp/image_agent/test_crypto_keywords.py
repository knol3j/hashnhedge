#!/usr/bin/env python3
"""Test the crypto keyword extractor."""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

from image_agent.utils.crypto_keywords import CryptoKeywordExtractor
from image_agent.orchestrator import Orchestrator

def test_keyword_extraction():
    """Test keyword extraction for various crypto articles."""
    extractor = CryptoKeywordExtractor()
    
    # Test cases
    test_cases = [
        {
            "title": "Bitcoin Price Analysis: What the $118K Level Means for 2025",
            "tags": ["bitcoin", "price analysis", "market trends", "crypto investing"],
            "expected_terms": ["bitcoin", "btc", "price", "analysis"]
        },
        {
            "title": "DeFi's Institutional Revolution: The Trillion Dollar Opportunity",
            "tags": ["defi", "institutional", "tradfi"],
            "expected_terms": ["defi", "trading"]
        },
        {
            "title": "Solana $500 Prediction: Why SOL Could 10x",
            "tags": ["solana", "sol", "altcoin"],
            "expected_terms": ["solana", "sol"]
        }
    ]
    
    print("="*60)
    print("CRYPTO KEYWORD EXTRACTION TEST")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test['title']}")
        print(f"Tags: {test['tags']}")
        
        # Build queries
        queries = extractor.build_search_queries(
            test['title'], 
            test['tags'],
            ""
        )
        
        print(f"\nGenerated Queries:")
        for j, query in enumerate(queries, 1):
            print(f"  {j}. {query}")
        
        # Check for expected terms
        all_queries = ' '.join(queries).lower()
        missing_terms = []
        for term in test['expected_terms']:
            if term not in all_queries:
                missing_terms.append(term)
        
        if missing_terms:
            print(f"⚠️  Missing expected terms: {missing_terms}")
        else:
            print("✅ All expected terms found")
        
        # Check for negative terms
        has_negatives = any('-butterfly' in q or '-flower' in q for q in queries)
        if has_negatives:
            print("✅ Negative terms applied")
        else:
            print("⚠️  No negative terms found")
        
        # Generate alt text
        alt_text = extractor.generate_alt_text(test['title'], test['tags'])
        print(f"\nGenerated Alt Text: {alt_text}")
        
        print("-"*60)

async def test_real_article():
    """Test with a real article from the site."""
    print("\n" + "="*60)
    print("REAL ARTICLE TEST")
    print("="*60)
    
    orchestrator = Orchestrator()
    
    # Test with the Bitcoin analysis article
    article_path = r"C:\Users\gnul\hashnhedge\content\posts\bitcoin-analysis-2025.md"
    print(f"\nTesting with: {Path(article_path).name}")
    
    result = await orchestrator.search_images_for_article(article_path, max_results=3)
    
    import json
    result_data = json.loads(result)
    
    if result_data['status'] == 'success':
        print(f"✅ Search successful!")
        print(f"Article: {result_data.get('article', 'Unknown')}")
        print(f"\nQueries used:")
        for i, query in enumerate(result_data.get('queries', []), 1):
            print(f"  {i}. {query}")
        print(f"\nImages found: {result_data.get('total_results', 0)}")
    else:
        print(f"❌ Search failed: {result_data.get('message', 'Unknown error')}")

if __name__ == "__main__":
    # Run synchronous tests
    test_keyword_extraction()
    
    # Run async tests
    asyncio.run(test_real_article())
    
    print("\n✅ All tests complete!")
