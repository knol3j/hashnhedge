"""Image processing operations."""
import asyncio
import aiofiles
import httpx
from pathlib import Path
from PIL import Image
import json
from typing import Dict, Optional

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
