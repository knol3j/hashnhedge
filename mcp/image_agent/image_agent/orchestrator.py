"""Orchestrator module - coordinates image fetching workflow."""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import yaml
from dotenv import load_dotenv

from .utils.logging_setup import get_logger
from .utils.hugo import HugoHelper
from .utils.keywords import KeywordExtractor
from .utils.crypto_keywords import CryptoKeywordExtractor
from .utils.files import FileHelper
from .utils.image_ops import ImageProcessor
from .sources.openverse import OpenverseProvider
from .sources.pixabay import PixabayProvider
from .sources.pexels import PexelsProvider
from .sources.unsplash import UnsplashProvider

# Load environment variables
load_dotenv()

class Orchestrator:
    """Main orchestrator for image fetching workflow."""
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.logger = get_logger(__name__)
        self.config = self._load_config()
        self.hugo = HugoHelper(self.config['project_root'])
        self.keywords = KeywordExtractor()
        self.crypto_keywords = CryptoKeywordExtractor()
        self.files = FileHelper(self.config['project_root'])
        self.image_processor = ImageProcessor(self.config)
        self.providers = self._init_providers()
        self.search_cache = {}
        
    def _load_config(self) -> Dict:
        """Load configuration from settings.yaml and environment."""
        settings_path = Path(__file__).parent.parent / 'settings.yaml'
        with open(settings_path, 'r') as f:
            config = yaml.safe_load(f)
            
        # Override with environment variables if present
        if project_root := os.getenv('HASHNHEDGE_PROJECT_ROOT'):
            config['project_root'] = project_root
            
        return config
        
    def _init_providers(self) -> Dict:
        """Initialize image providers based on available API keys."""
        providers = {}
        
        # Always include Openverse (no API key required)
        providers['openverse'] = OpenverseProvider()
        
        # Add providers with API keys
        if os.getenv('PIXABAY_API_KEY'):
            providers['pixabay'] = PixabayProvider(os.getenv('PIXABAY_API_KEY'))
        if os.getenv('PEXELS_API_KEY'):
            providers['pexels'] = PexelsProvider(os.getenv('PEXELS_API_KEY'))
        if os.getenv('UNSPLASH_ACCESS_KEY'):
            providers['unsplash'] = UnsplashProvider(os.getenv('UNSPLASH_ACCESS_KEY'))
            
        self.logger.info(f"Initialized providers: {list(providers.keys())}")
        return providers
        
    async def scan_articles(self, limit: int = 100) -> str:
        """Scan content directory for articles needing images."""
        try:
            articles = self.hugo.scan_for_missing_images(limit)
            
            result = {
                "status": "success",
                "total_found": len(articles),
                "articles": [
                    {
                        "path": str(article['path']),
                        "title": article['title'],
                        "slug": article['slug'],
                        "tags": article.get('tags', [])
                    }
                    for article in articles
                ]
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            self.logger.error(f"Error scanning articles: {e}")
            return json.dumps({"status": "error", "message": str(e)})
            
    async def search_images_for_article(self, article_path: str, max_results: int = 5) -> str:
        """Search for images matching article keywords."""
        try:
            # Read article metadata
            article = self.hugo.read_article(article_path)
            if not article:
                return json.dumps({"status": "error", "message": "Article not found"})
                
            # Extract keywords using crypto-specific extractor
            queries = self.crypto_keywords.build_search_queries(
                article.get('title', ''),
                article.get('tags', []),
                article.get('content', '')
            )
            
            # Search across providers
            all_results = []
            for provider_name in self.config['provider_priority']:
                if provider_name not in self.providers:
                    continue
                    
                provider = self.providers[provider_name]
                try:
                    results = await provider.search(queries[0], max_results)
                    for result in results:
                        result['provider'] = provider_name
                    all_results.extend(results)
                except Exception as e:
                    self.logger.warning(f"Provider {provider_name} failed: {e}")
                    
            # Cache results for later download
            cache_key = Path(article_path).stem
            self.search_cache[cache_key] = all_results
            
            return json.dumps({
                "status": "success",
                "article": article['title'],
                "queries": queries,
                "total_results": len(all_results),
                "results": all_results[:max_results * len(self.providers)]
            }, indent=2)
            
        except Exception as e:
            self.logger.error(f"Error searching images: {e}")
            return json.dumps({"status": "error", "message": str(e)})
            
    async def download_and_attach(self, article_path: str, provider: Optional[str] = None,
                                 image_index: int = 0, force: bool = False) -> str:
        """Download and attach an image to an article."""
        try:
            # Read article
            article = self.hugo.read_article(article_path)
            if not article:
                return json.dumps({"status": "error", "message": "Article not found"})
                
            # Check if article already has image
            if article.get('featured_image') and not force:
                return json.dumps({
                    "status": "skipped",
                    "message": "Article already has featured image"
                })
                
            # Get cached search results or search again
            cache_key = Path(article_path).stem
            if cache_key not in self.search_cache:
                await self.search_images_for_article(article_path)
                
            results = self.search_cache.get(cache_key, [])
            if not results:
                return json.dumps({"status": "error", "message": "No images found"})
                
            # Filter by provider if specified
            if provider:
                results = [r for r in results if r['provider'] == provider]
                
            if image_index >= len(results):
                return json.dumps({"status": "error", "message": "Invalid image index"})
                
            # Download and process image
            image_data = results[image_index]
            processed = await self.image_processor.download_and_process(
                image_data, article['slug']
            )
            
            if not processed:
                return json.dumps({"status": "error", "message": "Failed to process image"})
                
            # Update article front matter
            self.hugo.update_article_image(
                article_path,
                processed['hero_path'],
                processed['thumb_path'],
                image_data
            )
            
            # Save attribution
            self._save_attribution(article['slug'], image_data)
            
            return json.dumps({
                "status": "success",
                "message": "Image downloaded and attached",
                "image": {
                    "provider": image_data['provider'],
                    "author": image_data.get('author'),
                    "hero": processed['hero_path'],
                    "thumb": processed['thumb_path']
                }
            }, indent=2)
            
        except Exception as e:
            self.logger.error(f"Error downloading image: {e}")
            return json.dumps({"status": "error", "message": str(e)})
            
    async def batch_autofetch(self, max_articles: int = 5, per_article: int = 1) -> str:
        """Automatically fetch images for multiple articles."""
        try:
            # Scan for articles needing images
            articles = self.hugo.scan_for_missing_images(max_articles)
            
            results = []
            for article in articles:
                try:
                    # Search for images
                    await self.search_images_for_article(str(article['path']))
                    
                    # Download first available image
                    download_result = await self.download_and_attach(
                        str(article['path']), image_index=0
                    )
                    
                    result = json.loads(download_result)
                    results.append({
                        "article": article['title'],
                        "status": result['status']
                    })
                    
                except Exception as e:
                    self.logger.error(f"Failed to process {article['title']}: {e}")
                    results.append({
                        "article": article['title'],
                        "status": "error",
                        "error": str(e)
                    })
                    
            return json.dumps({
                "status": "success",
                "processed": len(results),
                "results": results
            }, indent=2)
            
        except Exception as e:
            self.logger.error(f"Batch autofetch error: {e}")
            return json.dumps({"status": "error", "message": str(e)})
            
    def _save_attribution(self, slug: str, image_data: Dict) -> None:
        """Save image attribution data."""
        try:
            attribution_file = Path(self.config['project_root']) / self.config['metadata_dir'] / 'image_attributions.yaml'
            attribution_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing attributions
            attributions = {}
            if attribution_file.exists():
                with open(attribution_file, 'r') as f:
                    attributions = yaml.safe_load(f) or {}
                    
            # Add new attribution
            attributions[slug] = {
                'provider': image_data['provider'],
                'author': image_data.get('author', 'Unknown'),
                'page_url': image_data.get('page_url', ''),
                'license': image_data.get('license', ''),
                'downloaded_at': datetime.now().isoformat()
            }
            
            # Save attributions
            with open(attribution_file, 'w') as f:
                yaml.safe_dump(attributions, f, default_flow_style=False)
                
        except Exception as e:
            self.logger.error(f"Failed to save attribution: {e}")
