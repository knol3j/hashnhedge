"""Pixabay provider."""
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
