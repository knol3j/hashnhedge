import os
import re
import sys
import pathlib
import hashlib
import time
from urllib.parse import urlparse
import yaml

try:
    import requests
    from bs4 import BeautifulSoup
    import frontmatter
except ImportError as e:
    print(f"Missing dependencies: {e}. Install with: pip install requests beautifulsoup4 python-frontmatter pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
POSTS = SITE / "content" / "posts"
STATIC_DIR = SITE / "static" / "images" / "posts"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"
}

IMG_EXTS = {"jpg", "jpeg", "png", "webp"}

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def pick_image_url(soup: BeautifulSoup):
    # Priority: og:image, twitter:image, first <img src>
    og = soup.find("meta", property="og:image")
    if og and og.get("content"):
        return og.get("content")
    tw = soup.find("meta", attrs={"name": "twitter:image"})
    if tw and tw.get("content"):
        return tw.get("content")
    img = soup.find("img")
    if img and img.get("src"):
        return img.get("src")
    return None


def ensure_ext(url: str) -> str:
    path = urlparse(url).path
    ext = pathlib.Path(path).suffix.lower().lstrip(".")
    if ext in IMG_EXTS:
        return ext
    # default to jpg
    return "jpg"


def download_image(url: str, dest_path: pathlib.Path) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        dest_path.write_bytes(r.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}", file=sys.stderr)
        return False


def read_post(md_path: pathlib.Path):
    """Read a markdown file with frontmatter"""
    content = md_path.read_text(encoding='utf-8')
    
    # Parse frontmatter manually
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            try:
                fm_data = yaml.safe_load(fm_text)
            except:
                fm_data = {}
            return fm_data, body
    return {}, content


def write_post(md_path: pathlib.Path, fm_data: dict, body: str):
    """Write a markdown file with frontmatter"""
    fm_text = yaml.dump(fm_data, default_flow_style=False, sort_keys=False)
    content = f"---\n{fm_text}---\n{body}"
    md_path.write_text(content, encoding='utf-8')


def update_frontmatter_image(md_path: pathlib.Path, image_rel_path: str) -> bool:
    fm_data, body = read_post(md_path)
    changed = False
    
    # Only update if image is missing or is the default
    if not fm_data.get("image") or fm_data.get("image") == "/images/default-hero.svg":
        fm_data["image"] = image_rel_path
        changed = True
    
    if changed:
        write_post(md_path, fm_data, body)
    
    return changed


def process_post(md_path: pathlib.Path):
    fm_data, body = read_post(md_path)
    
    # Look for source_url field first (common in your posts)
    sources = []
    if fm_data.get("source_url"):
        sources = [fm_data.get("source_url")]
    elif fm_data.get("source_urls"):
        sources = fm_data.get("source_urls")
    elif fm_data.get("sources"):
        sources = fm_data.get("sources")
    
    if isinstance(sources, str):
        sources = [sources]
    
    if not sources:
        # Try to parse from body: look for first http(s) link in the Source section
        match = re.search(r"\[.*?\]\((https?://\S+)\)", body)
        if match:
            sources = [match.group(1)]
    
    if not sources:
        print(f"No sources for {md_path.name}")
        return

    url = sources[0]
    try:
        html = requests.get(url, headers=HEADERS, timeout=15)
        html.raise_for_status()
    except Exception as e:
        print(f"Fetch failed for {url}: {e}")
        return

    soup = BeautifulSoup(html.text, "html.parser")
    img_url = pick_image_url(soup)
    if not img_url:
        print(f"No image found at {url}")
        return

    # Normalize relative image urls
    if img_url.startswith("//"):
        img_url = "https:" + img_url
    elif img_url.startswith("/"):
        parsed = urlparse(url)
        img_url = f"{parsed.scheme}://{parsed.netloc}{img_url}"

    # Build destination file path under static
    # Use the filename stem (without date prefix) as the slug
    filename_stem = md_path.stem
    if filename_stem.startswith("2025-"):  # Remove date prefix if present
        filename_stem = filename_stem[11:]  # Skip "2025-09-09-"
    slug = slugify(fm_data.get("slug") or filename_stem)
    
    # Check if an image with this slug already exists
    existing_images = list(STATIC_DIR.glob(f"{slug}.*"))
    if existing_images:
        # Use existing image
        existing_filename = existing_images[0].name
        rel_path = f"/images/posts/{existing_filename}"
        if update_frontmatter_image(md_path, rel_path):
            print(f"Updated {md_path.name} with existing image {rel_path}")
        return
    
    ext = ensure_ext(img_url)
    filename = f"{slug}.{ext}"
    dest = STATIC_DIR / filename

    if download_image(img_url, dest):
        rel_path = f"/images/posts/{filename}"
        if update_frontmatter_image(md_path, rel_path):
            print(f"Updated {md_path.name} with new image {rel_path}")
        else:
            print(f"Downloaded {rel_path} (frontmatter image already set)")


def main():
    # Walk all posts and their .md files
    targets = []
    if POSTS.exists():
        for p in POSTS.rglob("*.md"):
            # Skip non-post files like _index.md
            if not p.name.startswith("_"):
                targets.append(p)
    if not targets:
        print("No posts found under site/content/posts/**/*.md")
        return
    
    print(f"Found {len(targets)} posts to process")
    processed = 0
    updated = 0
    
    for md in targets:
        # Only process posts that have default-hero.svg as their image or no image
        fm_data, _ = read_post(md)
        if fm_data.get("image") == "/images/default-hero.svg" or not fm_data.get("image"):
            print(f"Processing: {md.name}")
            process_post(md)
            processed += 1
            time.sleep(0.3)
    
    print(f"\nSummary:")
    print(f"- Total posts found: {len(targets)}")
    print(f"- Posts needing images: {processed}")
    print(f"- Posts updated: Check git diff to see changes")

if __name__ == "__main__":
    main()
