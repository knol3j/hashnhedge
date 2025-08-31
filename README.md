# Hash & Hedge - Hugo Static Site

"life in the grey makes you appreciate color in everything."

A Hugo-powered static site for cryptocurrency, finance, and technology news using the Newsroom theme.

## Current Status ✅

- **Successfully Built**: 2,562 pages with Hugo Extended 0.148.2
- **Theme**: Newsroom theme (installed as git submodule)
- **Deployment**: GitHub Actions workflow for automated GitHub Pages deployment
- **Domain**: Configured for hashnhedge.com custom domain
- **Content**: Focused on working briefs content (424 paginator pages)
- **Build Output**: 1,710 optimized files

## Repo layout

- site/                — Hugo site
- pipeline/            — Content generation scripts (local AI)
- data/                — RSS sources and keyword config
- assets/              — Logos, OG templates, shared brand assets
- .github/workflows/   — CI (optional deploy helpers)

## Quick start (local development)

```bash
# Clone with submodules (includes Newsroom theme)
git clone --recurse-submodules https://github.com/knol3j/hashnhedge.git
cd hashnhedge

# Preview site locally
hugo server

# Build optimized site
hugo --gc --minify
```

## Deployment

**Automatic Deployment**: Site automatically deploys to GitHub Pages when pushed to:
- `main` branch (production)
- `chore/newsroom-setup` branch (testing)

GitHub Actions workflow (`.github/workflows/hugo.yml`):
1. Installs Hugo Extended 0.148.2
2. Builds site with optimization
3. Deploys to GitHub Pages
4. Serves at https://hashnhedge.com

## Theme: Newsroom

**Current Setup**: Using Newsroom theme as git submodule
- **Theme Repository**: https://github.com/onweru/newsroom
- **Installation**: `git submodule add https://github.com/onweru/newsroom.git themes/newsroom`
- **Configuration**: `theme = "newsroom"` in `hugo.toml`
- **Features**: News-focused, responsive, SEO optimized

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

