"""Hugo content management."""
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
