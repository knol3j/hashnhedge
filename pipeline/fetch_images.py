import os
import re
import sys
import pathlib
import hashlib
import time
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    import frontmatter
except ImportError:
    print("Missing dependencies. Install with: pip install requests beautifulsoup4 python-frontmatter", file=sys.stderr)
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


def update_frontmatter_image(md_path: pathlib.Path, image_rel_path: str) -> bool:
    post = frontmatter.load(md_path)
    changed = False
    if not post.get("image"):
        post["image"] = image_rel_path
        changed = True
    if changed:
        with open(md_path, "wb") as f:
            frontmatter.dump(post, f)
    return changed


def process_post(md_path: pathlib.Path):
    post = frontmatter.load(md_path)
    # Prefer explicit sources in frontmatter
    sources = post.get("source_urls") or post.get("sources") or []
    if isinstance(sources, str):
        sources = [sources]
    if not sources:
        # Try to parse from body: look for first http(s) link
        m = re.search(r"https?://\S+", post.content)
        if m:
            sources = [m.group(0)]
    if not sources:
        print(f"No sources for {md_path}")
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
    slug = slugify(post.get("slug") or md_path.parent.name or md_path.stem)
    ext = ensure_ext(img_url)
    filename = f"{slug}.{ext}"
    dest = STATIC_DIR / filename

    if download_image(img_url, dest):
        rel_path = f"/images/posts/{filename}"
        if update_frontmatter_image(md_path, rel_path):
            print(f"Updated {md_path} with image {rel_path}")
        else:
            print(f"Downloaded {rel_path} (frontmatter image already set)")


def main():
    # Walk all posts and their index.md
    targets = []
    if POSTS.exists():
        for p in POSTS.rglob("index.md"):
            targets.append(p)
    if not targets:
        print("No posts found under site/content/posts/**/index.md")
        return
    for md in targets:
        process_post(md)
        time.sleep(0.3)

if __name__ == "__main__":
    main()

