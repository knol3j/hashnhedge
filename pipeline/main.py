import os
import sys
import json
import yaml
import typer
from loguru import logger
from datetime import datetime
from pathlib import Path
import feedparser
import requests
from slugify import slugify
import frontmatter

app = typer.Typer(help="Hash & Hedge content pipeline")
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
CONTENT_ROOT = SITE / "content" / "posts"
DATA = ROOT / "data"


def ensure_dirs():
    CONTENT_ROOT.mkdir(parents=True, exist_ok=True)


def load_sources():
    with open(DATA / "sources.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_feed(url: str):
    try:
        return feedparser.parse(url)
    except Exception as e:
        logger.error(f"Failed to parse feed {url}: {e}")
        return None


@app.command()
def seed_post():
    """Create a starter post to verify the site builds."""
    ensure_dirs()
    now = datetime.utcnow()
    title = "Welcome to Hash & Hedge"
    slug = slugify(title)
    dest = CONTENT_ROOT / f"{now:%Y}/{now:%m}/{slug}/index.md"
    dest.parent.mkdir(parents=True, exist_ok=True)

    fm = {
        "title": title,
        "description": "A quick hello and what to expect.",
        "date": now.isoformat() + "Z",
        "lastmod": now.isoformat() + "Z",
        "slug": slug,
        "draft": False,
        "author": "Hash & Hedge Newsroom",
        "categories": ["News"],
        "tags": ["welcome"],
        "sources": [],
    }

    body = (
        "## What to expect\n\n"
        "Concise, thoughtful stories on crypto, finance, security, and culture.\n\n"
        "## Why the grey\n\n"
        "Because nuance matters — the edges are where insights emerge.\n"
    )

    post = frontmatter.Post(body, **fm)
    with open(dest, "w", encoding="utf-8") as f:
        frontmatter.dump(post, f)
    typer.echo(f"Created {dest}")


if __name__ == "__main__":
    app()

