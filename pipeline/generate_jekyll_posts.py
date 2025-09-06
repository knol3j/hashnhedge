#!/usr/bin/env python3
"""
Generate curated Jekyll posts into _posts by pulling recent items from
crypto/security/finance RSS feeds, summarizing them, and attaching an
OpenGraph/Twitter image if available.

Writes files like:
  _posts/YYYY-MM-DD-sanitized-slug.md
and places downloaded images under:
  images/posts/

Safe-by-default: if no image is found, uses /images/default-hero.svg.
"""

import argparse
import datetime as dt
import hashlib
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
import frontmatter
from urllib.parse import urljoin, urlparse

# Feeds and keywords
RSS_FEEDS = {
    "crypto": [
        "https://cointelegraph.com/rss",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://decrypt.co/feed",
        "https://bitcoinmagazine.com/feed",
        "https://cryptonews.com/news/feed/",
    ],
    "security": [
        "https://krebsonsecurity.com/feed/",
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/",
        "https://www.darkreading.com/rss.xml",
        "https://threatpost.com/feed/",
    ],
    "finance": [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.ft.com/rss/home",
        "https://feeds.wsj.com/rss/RSSMarketsMain.xml",
        "https://www.marketwatch.com/rss/",
    ],
}

TRENDING_KEYWORDS = [
    "hack", "breach", "exploit", "vulnerability", "crypto", "bitcoin",
    "ethereum", "defi", "nft", "web3", "blockchain", "ransomware",
    "zero-day", "malware", "phishing", "regulation", "sec", "cbdc",
    "stablecoin", "altcoin", "mining", "wallet", "exchange", "fraud"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
IMAGES_DIR = ROOT / "images" / "posts"
DEFAULT_IMAGE = "/images/default-hero.svg"

POSTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len] or "post"


def summarize_html_snippet(html: str, max_len: int = 320) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    text = " ".join(soup.get_text(" ").split())
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0] + "..."
    return text


def fetch_image_url(source_url: str) -> Optional[str]:
    try:
        r = requests.get(source_url, headers=HEADERS, timeout=12)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return urljoin(source_url, og["content"])
        tw = soup.find("meta", attrs={"name": "twitter:image"})
        if tw and tw.get("content"):
            return urljoin(source_url, tw["content"])
        # fallback: sensible <img>
        for img in soup.find_all("img"):
            src = img.get("src")
            if not src:
                continue
            src_l = src.lower()
            if any(b in src_l for b in ["logo", "icon", "avatar", "sprite", "pixel"]):
                continue
            return urljoin(source_url, src)
    except Exception:
        return None
    return None


def download_image(image_url: str, title: str) -> Optional[str]:
    try:
        resp = requests.get(image_url, headers=HEADERS, timeout=15, stream=True)
        resp.raise_for_status()
        # Derive extension
        ext = Path(urlparse(image_url).path).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            ct = resp.headers.get("content-type", "")
            if "jpeg" in ct or "jpg" in ct:
                ext = ".jpg"
            elif "png" in ct:
                ext = ".png"
            elif "webp" in ct:
                ext = ".webp"
            else:
                ext = ".jpg"
        base = slugify(title, 60)
        # Use hash suffix to avoid collisions
        h = hashlib.sha1(image_url.encode("utf-8")).hexdigest()[:8]
        filename = f"{base}-{h}{ext}"
        path = IMAGES_DIR / filename
        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return f"/images/posts/{filename}"
    except Exception:
        return None


def fetch_stories(category: str) -> List[Dict]:
    items: List[Dict] = []
    for feed_url in RSS_FEEDS.get(category, []):
        try:
            feed = feedparser.parse(feed_url)
            for e in feed.entries[:6]:  # top 6 per feed
                title = e.get("title", "Untitled")
                summary = e.get("summary", "")
                link = e.get("link", "")
                score = sum(1 for kw in TRENDING_KEYWORDS if kw in f"{title} {summary}".lower())
                items.append({
                    "title": title,
                    "summary_html": summary,
                    "link": link,
                    "published": e.get("published_parsed"),
                    "category": category,
                    "score": score,
                })
        except Exception:
            continue
    return sorted(items, key=lambda x: x["score"], reverse=True)


def build_content(story: Dict, short_summary: str) -> str:
    parts = []
    parts.append(f"## Summary\n\n{short_summary}\n")
    parts.append("## Source\n")
    parts.append(f"- Original: [{story['title']}]({story['link']})\n")
    parts.append("\n---\n")
    parts.append("*Automated curation. Verify details with the original source.*\n")
    return "\n".join(parts)


def create_post_from_story(story: Dict) -> Optional[Path]:
    now = dt.datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")
    ts_str = now.strftime("%Y-%m-%d %H:%M:%S +0000")
    slug = slugify(story["title"]) or f"post-{now.strftime('%H%M%S')}"
    filename = f"{date_str}-{slug}.md"
    path = POSTS_DIR / filename

    short_summary = summarize_html_snippet(story.get("summary_html", ""))

    # Try to fetch image
    image_url = fetch_image_url(story.get("link", "")) if story.get("link") else None
    local_image = download_image(image_url, story["title"]) if image_url else None

    fm = {
        "title": story["title"],
        "date": ts_str,
        "layout": "post",
        "categories": [story.get("category", "news")],
        "tags": [kw for kw in TRENDING_KEYWORDS if kw in story["title"].lower()],
        "summary": short_summary[:160] + ("..." if len(short_summary) > 160 else ""),
        "image": local_image or DEFAULT_IMAGE,
        "source_url": story.get("link", ""),
    }

    content = build_content(story, short_summary)
    post = frontmatter.Post(content, **fm)

    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))

    return path


def generate(count: int) -> List[Path]:
    results: List[Path] = []
    candidates: List[Dict] = []
    for cat in RSS_FEEDS.keys():
        candidates.extend(fetch_stories(cat)[:count * 2])
    # de-dup by title
    seen = set()
    uniq: List[Dict] = []
    for s in sorted(candidates, key=lambda x: x["score"], reverse=True):
        t = s["title"].strip()
        if t not in seen:
            seen.add(t)
            uniq.append(s)
    for story in uniq[:count]:
        post_path = create_post_from_story(story)
        if post_path:
            results.append(post_path)
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--count", type=int, default=3, help="number of posts to create")
    args = p.parse_args()
    posts = generate(max(1, args.count))
    print(f"Created {len(posts)} curated post(s)")
    return 0 if posts else 1

if __name__ == "__main__":
    raise SystemExit(main())

