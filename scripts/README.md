# Hash & Hedge Scripts Documentation

This directory contains automation scripts for the Hash & Hedge website to generate images, fix URLs, and maintain content.

## Scripts Overview

### 1. generate_images.py - Python Image Generator
**Purpose**: Generates unique JPEG images for blog posts based on title text using geometric patterns.

**Features**:
- Creates 1200x630px images (optimal for social media)
- Generates consistent colors from title using MD5 hash
- 5 different pattern types (circles, lines, squares, triangles, gradients)
- Automatically updates markdown files with image paths

**Requirements**:
- Python 3.x
- PIL/Pillow library (`pip install Pillow`)

**Usage**:
```bash
python scripts/generate_images.py
```

**Configuration**:
- Edit lines 227-228 to change content/output directories
- Modify pattern types in `create_pattern_image()` function
- Adjust image dimensions on line 28

---

### 2. generate-unique-images.ps1 - PowerShell SVG Generator
**Purpose**: Creates unique SVG images with topic-specific designs based on content analysis.

**Features**:
- Topic detection (crypto, bitcoin, ethereum, defi, trading, AI, etc.)
- Topic-specific color palettes and icons
- Abstract geometric patterns and wave effects
- Automatic markdown file updates

**Usage**:
```powershell
# Basic usage
.\scripts\generate-unique-images.ps1

# With custom paths
.\scripts\generate-unique-images.ps1 -ContentPath "content" -OutputPath "static/images/generated"

# Force regenerate all images
.\scripts\generate-unique-images.ps1 -Force
```

**Parameters**:
- `-ContentPath`: Path to content directory (default: "content")
- `-OutputPath`: Path to output directory (default: "static/images/generated")
- `-Force`: Force regenerate existing images

---

### 3. fix-all-urls.ps1 - URL Sanitization Script
**Purpose**: Fixes broken URLs by cleaning filenames and updating references.

**Features**:
- Removes special characters from filenames
- Converts spaces to hyphens
- Makes all filenames lowercase
- Updates image references in markdown files
- Rebuilds Hugo site after fixes

**Usage**:
```powershell
.\scripts\fix-all-urls.ps1
```

**What it does**:
1. Cleans markdown filenames in content directory
2. Cleans image filenames to match
3. Updates image paths in all content files
4. Rebuilds the Hugo site

---

## Recommended Workflow

### Initial Setup
1. First run `fix-all-urls.ps1` to clean all filenames
2. Then generate images using either script:
   - Use `generate_images.py` for JPEG pattern images
   - Use `generate-unique-images.ps1` for SVG topic-specific images

### Daily Content Generation
```powershell
# Generate new content
.\auto-content-generator.ps1

# Generate images for new content
python scripts\generate_images.py
# OR
.\scripts\generate-unique-images.ps1

# Build and deploy
hugo --gc --minify
git add -A
git commit -m "Add new content with images"
git push
```

### Fixing Issues
```powershell
# If URLs are broken
.\scripts\fix-all-urls.ps1

# If images are missing
.\scripts\generate-unique-images.ps1 -Force
```

## Image Types Comparison

| Feature | generate_images.py | generate-unique-images.ps1 |
|---------|-------------------|---------------------------|
| Format | JPEG | SVG |
| File Size | ~50-100KB | ~5-10KB |
| Quality | Raster (fixed resolution) | Vector (scalable) |
| Style | Geometric patterns | Topic-specific designs |
| Colors | Hash-based from title | Topic-based palettes |
| Icons | No | Yes (topic-specific) |
| Best For | Social media sharing | Website display |

## Troubleshooting

### Python Script Issues
```bash
# Install required dependencies
pip install Pillow

# Check Python version
python --version  # Should be 3.x
```

### PowerShell Script Issues
```powershell
# Check PowerShell version
$PSVersionTable.PSVersion  # Should be 5.1 or higher

# Enable script execution if blocked
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Common Issues

**Issue**: "File or directory is corrupted"
**Solution**: Run `chkdsk C: /f` and restart

**Issue**: Images not showing on website
**Solution**: 
1. Check image paths in markdown files
2. Ensure images exist in `static/images/generated/`
3. Run `fix-all-urls.ps1` to fix paths

**Issue**: Script execution blocked
**Solution**: Right-click script > Properties > Unblock

## Best Practices

1. **Always backup before bulk operations**:
   ```powershell
   Copy-Item -Path "content" -Destination "content_backup" -Recurse
   ```

2. **Test on a few files first**:
   - Modify scripts to process only a subset
   - Verify results before full run

3. **Use version control**:
   ```bash
   git add -A
   git commit -m "Before image generation"
   ```

4. **Monitor disk space**:
   - SVG files are smaller (~5-10KB)
   - JPEG files are larger (~50-100KB)
   - Plan storage accordingly

## Customization

### Adding New Topics (generate-unique-images.ps1)
```powershell
# Add to $colorPalettes hashtable (line 16)
newTopic = @("#color1", "#color2", "#color3", "#color4", "#color5")

# Add to Get-TopicFromContent function (line 42)
if ($lowerContent -match "keyword1|keyword2") { return "newTopic" }
```

### Changing Pattern Types (generate_images.py)
```python
# Modify pattern_type selection (line 40)
pattern_type = hash_val % 6  # Increase for more patterns

# Add new pattern (after line 81)
elif pattern_type == 5:
    # Your custom pattern code
    pass
```

## Support

For issues or questions:
1. Check this documentation
2. Review script comments
3. Check Hugo documentation: https://gohugo.io/
4. Test with verbose/debug output

## License

These scripts are part of the Hash & Hedge project and are for internal use only.
