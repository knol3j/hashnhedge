"""Unsplash provider."""
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
