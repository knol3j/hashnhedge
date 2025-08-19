# Hash & Hedge

"life in the grey makes you appreciate color in everything."

Niche: Crypto, finance, and security (hacking/pentesting) through the lens of culture and craft. Concise, thoughtful stories.

- Tech stack: Hugo (static), GitHub Pages + Porkbun DNS, Google Analytics 4
- Content: Daily AI-assisted news briefs + periodic explainers
- Monetization: Google AdSense (auto + in-article); ads.txt included
- Automation: Local AI (Windows) + scheduled job to generate Markdown posts and push to GitHub

## Repo layout

- site/                — Hugo site
- pipeline/            — Content generation scripts (local AI)
- data/                — RSS sources and keyword config
- assets/              — Logos, OG templates, shared brand assets
- .github/workflows/   — CI (optional deploy helpers)

## Quick start (local preview)

1) Install Hugo (extended) and Git.
2) Preview: `hugo server -s site` (or via VS Code task).
3) Build: `hugo --gc --minify -s site -d public`.

Deployment is via GitHub Pages using the workflow in `.github/workflows/site.yml`.

## Theme and UI

Option 2 (recommended): use the "hugo-narrow-1.1.3" theme.

1) Place the ZIP on disk, then extract into site/themes/hugo-narrow:
   PowerShell:
   Expand-Archive -Path "C:\\path\\to\\hugo-narrow-1.1.3.zip" -DestinationPath "site\\themes\\hugo-narrow" -Force

2) Enable theme in site/config.toml (add near the top):
   theme = "hugo-narrow"

3) Keep our custom partials (head, consent) — these override theme defaults.

4) Our custom overrides CSS is loaded from /css/custom.css; adjust styles there.

## Branding
- Title: Hash \u0026 Hedge
- Tagline: life in the grey makes you appreciate color in everything.
- Logo: see assets/logo for options
- Colors: Grey base with a vibrant accent for calls to action

## Contact
- Email: ugbuni@proton.me

## SEO and Ads
- robots.txt, sitemap.xml, RSS enabled
- JSON-LD for Organization, WebSite, Breadcrumbs, NewsArticle
- AdSense script/snippets are templated (add your publisher ID once approved)

## Local AI pipeline
- Python 3.11 environment
- Models: local GGUF (Llama/Mistral) via llama-cpp-python
- Generates Markdown posts with frontmatter under site/content/posts/YYYY/MM/slug

### Fetch hero images for posts
- Install deps: pip install requests beautifulsoup4 python-frontmatter
- Run: python pipeline/fetch_images.py
- The script scrapes the first source URL (Open Graph/Twitter image) and downloads to site/static/images/posts/, updating front matter `image:` if missing.

See pipeline/README (to be added) for details.

