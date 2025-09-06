#!/usr/bin/env python3
"""
HashNHedge Image Agent - Complete Implementation
This file contains all the necessary code to run the image agent.
Copy the individual components to their respective files for the full setup.
"""

import os
import sys
from pathlib import Path

# Create the necessary directory structure
def setup_directories():
    """Create all necessary directories for the agent."""
    base_dir = Path(__file__).parent
    dirs = [
        base_dir / "image_agent",
        base_dir / "image_agent" / "utils",
        base_dir / "image_agent" / "sources",
        base_dir / "scripts",
        base_dir / "logs",
        base_dir / ".cache" / "downloads",
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create __init__.py files
        init_file = dir_path / "__init__.py"
        if dir_path.name in ["image_agent", "utils", "sources"] and not init_file.exists():
            init_file.write_text("")
    print("✅ Directory structure created")

# Create all utility files
def create_utils():
    """Create utility modules."""
    base_dir = Path(__file__).parent / "image_agent" / "utils"
    
    # logging_setup.py
    (base_dir / "logging_setup.py").write_text('''"""Logging configuration."""
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name):
    """Get configured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        handler = RotatingFileHandler(
            log_dir / "image_agent.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
''')
    
    # keywords.py
    (base_dir / "keywords.py").write_text('''"""Keyword extraction utilities."""
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
''')
    
    # files.py
    (base_dir / "files.py").write_text('''"""File handling utilities."""
import hashlib
from pathlib import Path

class FileHelper:
    """File operations helper."""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
    
    def ensure_dir(self, path):
        """Ensure directory exists."""
        Path(path).mkdir(parents=True, exist_ok=True)
        return Path(path)
    
    def get_file_hash(self, file_path):
        """Get SHA-256 hash of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
''')
    
    # hugo.py
    (base_dir / "hugo.py").write_text('''"""Hugo content management."""
import frontmatter
from pathlib import Path
from typing import Dict, List, Optional

class HugoHelper:
    """Helper for Hugo content operations."""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.content_dir = self.project_root / "content"
    
    def scan_for_missing_images(self, limit: int = 100) -> List[Dict]:
        """Scan for articles without featured images."""
        articles = []
        for md_file in self.content_dir.rglob("*.md"):
            if len(articles) >= limit:
                break
            try:
                post = frontmatter.load(md_file)
                if not post.get('featured_image') and not post.get('image'):
                    articles.append({
                        'path': md_file,
                        'title': post.get('title', md_file.stem),
                        'slug': md_file.stem,
                        'tags': post.get('tags', [])
                    })
            except Exception:
                continue
        return articles
    
    def read_article(self, article_path: str) -> Optional[Dict]:
        """Read article metadata and content."""
        try:
            post = frontmatter.load(article_path)
            return {
                'title': post.get('title', ''),
                'tags': post.get('tags', []),
                'content': post.content[:1000],  # First 1000 chars
                'slug': Path(article_path).stem,
                'featured_image': post.get('featured_image') or post.get('image')
            }
        except Exception:
            return None
    
    def update_article_image(self, article_path: str, hero_path: str, 
                            thumb_path: str, image_data: Dict):
        """Update article with image information."""
        try:
            post = frontmatter.load(article_path)
            post['featured_image'] = hero_path
            post['images'] = [hero_path, thumb_path]
            post['image_alt'] = self._generate_alt_text(
                post.get('title', ''), 
                post.get('tags', [])
            )
            post['image_source'] = image_data.get('provider', '')
            
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            return True
        except Exception:
            return False
    
    def _generate_alt_text(self, title: str, tags: List[str]) -> str:
        """Generate SEO-friendly alt text."""
        alt_parts = [title]
        if tags:
            alt_parts.append(' - ' + ', '.join(tags[:3]))
        alt_text = ''.join(alt_parts)
        return alt_text[:125]  # Max 125 chars
''')
    
    # image_ops.py
    (base_dir / "image_ops.py").write_text('''"""Image processing operations."""
import asyncio
import aiofiles
import httpx
from pathlib import Path
from PIL import Image
import json

class ImageProcessor:
    """Process and optimize images."""
    
    def __init__(self, config):
        self.config = config
        self.project_root = Path(config['project_root'])
        self.static_dir = self.project_root / config['static_images_dir']
        self.cache_dir = self.project_root / Path(config['download_dir'])
        
    async def download_and_process(self, image_data: Dict, slug: str) -> Optional[Dict]:
        """Download and process image."""
        try:
            # Download image
            async with httpx.AsyncClient() as client:
                response = await client.get(image_data['download_url'])
                response.raise_for_status()
                
            # Save to cache
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            temp_file = self.cache_dir / f"{slug}_temp.jpg"
            
            async with aiofiles.open(temp_file, 'wb') as f:
                await f.write(response.content)
            
            # Process image
            img = Image.open(temp_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Create output directory
            output_dir = self.static_dir / slug
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create hero image
            hero_size = (
                self.config['targets']['hero']['width'],
                self.config['targets']['hero']['height']
            )
            hero = img.resize(hero_size, Image.Resampling.LANCZOS)
            hero_path = output_dir / "hero.webp"
            hero.save(hero_path, 'WEBP', quality=85, optimize=True)
            
            # Create thumbnail
            thumb_size = (
                self.config['targets']['thumb']['width'],
                self.config['targets']['thumb']['height']
            )
            thumb = img.resize(thumb_size, Image.Resampling.LANCZOS)
            thumb_path = output_dir / "thumb.webp"
            thumb.save(thumb_path, 'WEBP', quality=80, optimize=True)
            
            # Save metadata
            meta_path = output_dir / "source.json"
            with open(meta_path, 'w') as f:
                json.dump(image_data, f, indent=2)
            
            # Clean up temp file
            temp_file.unlink()
            
            return {
                'hero_path': f"/images/{slug}/hero.webp",
                'thumb_path': f"/images/{slug}/thumb.webp",
                'local_hero': str(hero_path),
                'local_thumb': str(thumb_path)
            }
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
''')
    
    print("✅ Utility modules created")

# Create provider modules
def create_providers():
    """Create image provider modules."""
    base_dir = Path(__file__).parent / "image_agent" / "sources"
    
    # openverse.py - Works without API key
    (base_dir / "openverse.py").write_text('''"""Openverse provider - Creative Commons images."""
import httpx
from typing import List, Dict

class OpenverseProvider:
    """Openverse image provider."""
    
    BASE_URL = "https://api.openverse.engineering/v1"
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for images."""
        try:
            params = {
                'q': query,
                'license_type': 'commercial',
                'category': 'photograph',
                'aspect_ratio': 'wide',
                'size': 'medium',
                'page_size': max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/images/",
                    params=params,
                    timeout=10.0
                )
                
            if response.status_code != 200:
                return []
                
            data = response.json()
            results = []
            
            for item in data.get('results', [])[:max_results]:
                results.append({
                    'id': item.get('id', ''),
                    'preview_url': item.get('thumbnail', ''),
                    'download_url': item.get('url', ''),
                    'page_url': item.get('foreign_landing_url', ''),
                    'width': item.get('width', 0),
                    'height': item.get('height', 0),
                    'alt': item.get('title', ''),
                    'author': item.get('creator', 'Unknown'),
                    'license': item.get('license', 'cc0'),
                    'requires_attribution': item.get('license', '') != 'cc0',
                    'provider': 'openverse'
                })
                
            return results
            
        except Exception as e:
            print(f"Openverse search error: {e}")
            return []
''')
    
    # pixabay.py
    (base_dir / "pixabay.py").write_text('''"""Pixabay provider."""
import httpx
from typing import List, Dict

class PixabayProvider:
    """Pixabay image provider."""
    
    BASE_URL = "https://pixabay.com/api/"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for images."""
        if not self.api_key:
            return []
            
        try:
            params = {
                'key': self.api_key,
                'q': query,
                'image_type': 'photo',
                'orientation': 'horizontal',
                'safesearch': 'true',
                'per_page': max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL, params=params, timeout=10.0)
                
            if response.status_code != 200:
                return []
                
            data = response.json()
            results = []
            
            for item in data.get('hits', []):
                results.append({
                    'id': str(item.get('id', '')),
                    'preview_url': item.get('previewURL', ''),
                    'download_url': item.get('largeImageURL', item.get('webformatURL', '')),
                    'page_url': item.get('pageURL', ''),
                    'width': item.get('imageWidth', 0),
                    'height': item.get('imageHeight', 0),
                    'alt': item.get('tags', ''),
                    'author': item.get('user', 'Unknown'),
                    'license': 'pixabay',
                    'requires_attribution': False,
                    'provider': 'pixabay'
                })
                
            return results
            
        except Exception as e:
            print(f"Pixabay search error: {e}")
            return []
''')
    
    # pexels.py
    (base_dir / "pexels.py").write_text('''"""Pexels provider."""
import httpx
from typing import List, Dict

class PexelsProvider:
    """Pexels image provider."""
    
    BASE_URL = "https://api.pexels.com/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for images."""
        if not self.api_key:
            return []
            
        try:
            headers = {'Authorization': self.api_key}
            params = {
                'query': query,
                'orientation': 'landscape',
                'per_page': max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/search",
                    headers=headers,
                    params=params,
                    timeout=10.0
                )
                
            if response.status_code != 200:
                return []
                
            data = response.json()
            results = []
            
            for item in data.get('photos', []):
                results.append({
                    'id': str(item.get('id', '')),
                    'preview_url': item.get('src', {}).get('medium', ''),
                    'download_url': item.get('src', {}).get('original', ''),
                    'page_url': item.get('url', ''),
                    'width': item.get('width', 0),
                    'height': item.get('height', 0),
                    'alt': item.get('alt', ''),
                    'author': item.get('photographer', 'Unknown'),
                    'license': 'pexels',
                    'requires_attribution': True,
                    'provider': 'pexels'
                })
                
            return results
            
        except Exception as e:
            print(f"Pexels search error: {e}")
            return []
''')
    
    # unsplash.py
    (base_dir / "unsplash.py").write_text('''"""Unsplash provider."""
import httpx
from typing import List, Dict

class UnsplashProvider:
    """Unsplash image provider."""
    
    BASE_URL = "https://api.unsplash.com"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for images."""
        if not self.api_key:
            return []
            
        try:
            headers = {'Authorization': f'Client-ID {self.api_key}'}
            params = {
                'query': query,
                'orientation': 'landscape',
                'per_page': max_results
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/search/photos",
                    headers=headers,
                    params=params,
                    timeout=10.0
                )
                
            if response.status_code != 200:
                return []
                
            data = response.json()
            results = []
            
            for item in data.get('results', []):
                results.append({
                    'id': item.get('id', ''),
                    'preview_url': item.get('urls', {}).get('small', ''),
                    'download_url': item.get('urls', {}).get('full', ''),
                    'page_url': item.get('links', {}).get('html', ''),
                    'width': item.get('width', 0),
                    'height': item.get('height', 0),
                    'alt': item.get('alt_description', ''),
                    'author': item.get('user', {}).get('name', 'Unknown'),
                    'license': 'unsplash',
                    'requires_attribution': True,
                    'provider': 'unsplash'
                })
                
            return results
            
        except Exception as e:
            print(f"Unsplash search error: {e}")
            return []
''')
    
    print("✅ Provider modules created")

# Create manifest file
def create_manifest():
    """Create manifest.json."""
    manifest = {
        "name": "hashnhedge-image-agent",
        "version": "0.1.0",
        "description": "MCP server that finds and manages copyright-compliant images for Hugo posts",
        "author": "HashNHedge",
        "license": "MIT"
    }
    
    import json
    manifest_path = Path(__file__).parent / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("✅ Manifest file created")

# Update Claude configuration
def update_claude_config():
    """Update Claude Desktop configuration."""
    import json
    config_path = Path(os.environ['APPDATA']) / 'Claude' / 'claude_desktop_config.json'
    
    new_server = {
        "hashnhedge-image-agent": {
            "command": str(Path(__file__).parent / ".venv" / "Scripts" / "python.exe"),
            "args": ["server.py"],
            "env": {
                "PYTHONUNBUFFERED": "1",
                "HASHNHEDGE_PROJECT_ROOT": str(Path(__file__).parent.parent.parent)
            },
            "cwd": str(Path(__file__).parent)
        }
    }
    
    try:
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        if 'mcpServers' not in config:
            config['mcpServers'] = {}
        
        config['mcpServers'].update(new_server)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Claude Desktop configuration updated")
        print("⚠️  Please restart Claude Desktop to load the new MCP server")
    except Exception as e:
        print(f"❌ Failed to update Claude config: {e}")
        print(f"   Please manually add to: {config_path}")

# Main setup function
def main():
    """Run complete setup."""
    print("🚀 Setting up HashNHedge Image Agent...")
    print("-" * 50)
    
    setup_directories()
    create_utils()
    create_providers()
    create_manifest()
    update_claude_config()
    
    print("-" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Add your API keys to .env file")
    print("2. Restart Claude Desktop")
    print("3. Use the tools in Claude:")
    print("   - scan_articles")
    print("   - search_images")
    print("   - download_image")
    print("   - batch_autofetch")

if __name__ == "__main__":
    main()
