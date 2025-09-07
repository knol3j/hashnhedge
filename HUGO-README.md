# Hash & Hedge - Hugo Site

Your site is now set up with Hugo and the Newsroom theme!

## 🚀 Quick Start

### Local Development
```bash
cd site
hugo server
```
Visit http://localhost:1313 to see your site.

### Build Site
```bash
cd site
hugo --gc --minify
```

### Deploy to GitHub Pages
Simply push to the main branch:
```bash
git add -A
git commit -m "Update content"
git push origin main
```
Or use the deploy script:
```bash
deploy.bat
```

## 📁 Structure
- `site/` - Hugo site directory
  - `content/` - Your content files
    - `posts/` - Blog posts  
    - `briefs/` - News briefs
  - `static/` - Static files (images, CSS, JS)
  - `themes/newsroom/` - Newsroom theme (submodule)
  - `config.toml` - Site configuration

## ✅ GitHub Actions

The site automatically builds and deploys when you push to main branch.

Check deployment status: https://github.com/knol3j/hashnhedge/actions

## 🎨 Theme

Using Newsroom theme: https://github.com/onweru/newsroom

## 📝 Adding Content

Create new posts:
```bash
cd site
hugo new posts/my-new-post.md
```

## 🐛 Troubleshooting

1. **Build errors**: Check that all front matter is valid YAML
2. **Theme missing**: Run `git submodule update --init --recursive`
3. **Deployment fails**: Check GitHub Actions logs

## 🔧 Configuration

Edit `site/config.toml` to update:
- Site title and description
- Menu items
- Social links
- Google Analytics ID
- AdSense ID