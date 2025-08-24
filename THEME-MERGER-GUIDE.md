# Hash & Hedge - Tableless Theme Merger Guide

## 🎯 Merger Objectives
- Integrate the Tableless theme's clean design with Hash & Hedge's existing content
- Preserve all existing content and customizations
- Optimize for performance and SEO
- Maintain AdSense and analytics integration

## ✅ Completed Steps

### 1. Configuration Merge
- Created `config-merged.toml` combining:
  - Hash & Hedge's site identity and content
  - Tableless theme's layout and structure
  - Enhanced related content configuration
  - Preserved analytics and AdSense settings

### 2. Backup Created
- Location: `C:\Users\gnul\hashnhedge\backup-before-merge\`
- Contains original configuration files

## 📋 Next Steps to Complete the Merge

### Step 1: Activate the Merged Configuration
```bash
cd C:\Users\gnul\hashnhedge\site
# Backup current config
copy config.toml config.toml.original

# Apply merged configuration
copy config-merged.toml config.toml
```

### Step 2: Update Theme Path
The theme is already properly configured in the config. Make sure the theme path is correct:
- Current: `theme = "tableless"`
- Theme location: `site\themes\tableless\`

### Step 3: Content Organization
Your content structure should remain:
```
site/content/
├── about.md
├── ai-disclosure.md
├── contact.md
├── editorial-policy.md
├── posts/          # Main blog posts
├── test-posts/     # Test posts section
├── privacy.md
├── terms.md
└── _index.md
```

### Step 4: Custom Styling (Optional)
If you want to customize the Tableless theme appearance:
1. Create custom CSS in `site/static/css/custom.css`
2. Override theme templates by copying them to `site/layouts/`

### Step 5: Test the Site Locally
```bash
cd C:\Users\gnul\hashnhedge\site
hugo server -D
```
Visit: http://localhost:1313

## 🎨 Theme Features Available

### From Tableless Theme:
- Clean, minimalist design
- Optimized for readability
- Built-in code highlighting
- Related posts functionality
- Author taxonomy support
- Responsive layout

### Preserved from Hash & Hedge:
- AdSense integration
- Google Analytics 4
- Custom permalinks
- SEO optimizations
- Social media links
- Content structure

## 🔧 Customization Options

### 1. Logo and Branding
- Current logo: `/logo.svg`
- Update in `static/` directory

### 2. Color Scheme
- Edit theme CSS in `themes/tableless/static/css/`
- Or override with custom CSS

### 3. Homepage Layout
- Customize `themes/tableless/layouts/index.html`
- Or create `site/layouts/index.html` to override

### 4. Post Templates
- Located in `themes/tableless/layouts/_default/`
- Copy to `site/layouts/_default/` to customize

## 🚀 Deployment Checklist

- [ ] Test all pages locally
- [ ] Verify AdSense displays correctly
- [ ] Check Google Analytics tracking
- [ ] Test responsive design
- [ ] Validate RSS feeds
- [ ] Check sitemap generation
- [ ] Test social media links
- [ ] Verify all images load
- [ ] Check 404 page
- [ ] Test contact forms (if any)

## 🛠 Troubleshooting

### If posts don't appear:
- Check the `mainSections` parameter in config
- Verify content directory structure
- Check front matter in markdown files

### If styles look wrong:
- Clear browser cache
- Check for CSS conflicts
- Verify theme path in config

### If build fails:
- Check Hugo version compatibility
- Verify all template syntax
- Look for missing partials

## 📝 Additional Customizations

### To add more features:
1. **Comments**: Add Disqus shortname in config
2. **Search**: Implement lunr.js or Algolia
3. **Newsletter**: Add MailChimp or ConvertKit
4. **Analytics**: Enhanced ecommerce tracking

## 🔄 Rollback Plan

If needed, restore original configuration:
```bash
cd C:\Users\gnul\hashnhedge\site
copy config.toml.original config.toml
hugo server -D
```

## 📚 Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Tableless Theme Repo](https://github.com/tableless/tableless)
- [Hugo Themes Guide](https://gohugo.io/themes/)

---
Last updated: August 2025
