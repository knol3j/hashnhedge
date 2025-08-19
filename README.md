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

## Branding
- Title: Hash & Hedge
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

See pipeline/README (to be added) for details.

