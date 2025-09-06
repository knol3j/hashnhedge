"""Openverse provider - Creative Commons images."""
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
