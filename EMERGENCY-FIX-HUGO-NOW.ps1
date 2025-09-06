# EMERGENCY FIX: Make this fucking Hugo site work with newsroom theme
Write-Host "FIXING YOUR BROKEN ASS HUGO SITE..." -ForegroundColor Red

# First, let's create an actual functioning post
$testPost = @"
---
title: "Test Post That Actually Works"
date: 2025-01-21T10:30:00-07:00
draft: false
categories: ["crypto"]
tags: ["test"]
description: "If you can see this, we're making progress"
---

# Holy Shit It Works!

This is a test post to make sure your newsroom theme isn't completely fucked.

If you're reading this, it means:
1. The theme is loading
2. Posts are rendering
3. We can start fixing the rest of this mess
"@

# Create a proper post structure
New-Item -Path "content\posts\test-post-that-works.md" -ItemType File -Force
Set-Content -Path "content\posts\test-post-that-works.md" -Value $testPost

# Fix the config to ensure newsroom theme works
$newConfig = @"
baseURL = "https://hashnhedge.com/"
title = "Hash & Hedge"
theme = "newsroom"
languageCode = "en-us"
paginate = 10

[params]
  author = "Hash & Hedge"
  description = "Life in the grey makes you appreciate color in everything"
  tagline = "Crypto, finance, and security through the lens of existential dread"
  
  # Enable features
  showDate = true
  showReadTime = true
  showWordCount = true
  showAuthor = true
  
  # Social
  twitter = "hashnhedge"
  github = "knol3j/hashnhedge"

[menu]
  [[menu.main]]
    name = "Home"
    url = "/"
    weight = 1
  [[menu.main]]
    name = "Posts"
    url = "/posts/"
    weight = 2
  [[menu.main]]
    name = "About"
    url = "/about/"
    weight = 3

[outputs]
  home = ["HTML", "RSS"]
  section = ["HTML", "RSS"]

[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
"@

# Backup old config
Copy-Item -Path "config.toml" -Destination "config.toml.backup" -Force

# Write new config
Set-Content -Path "config.toml" -Value $newConfig

# Create sample images directory
New-Item -Path "static\images\posts" -ItemType Directory -Force

# Generate a simple placeholder image using HTML/SVG
$placeholderSVG = @"
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1a1a1a"/>
  <text x="50%" y="50%" text-anchor="middle" font-size="24" fill="#666">
    Image Placeholder - Fix Me Later
  </text>
</svg>
"@

# Save placeholder for posts
Set-Content -Path "static\images\posts\placeholder.svg" -Value $placeholderSVG

# Create an about page
$aboutPage = @"
---
title: "About"
date: 2025-01-21
draft: false
---

# About Hash & Hedge

Life in the grey makes you appreciate color in everything.

We cover crypto, finance, and security through the lens of someone who's given up on traditional optimism but found meaning in the digital chaos.

Contact: ugbuni@proton.me
"@

New-Item -Path "content\about.md" -ItemType File -Force
Set-Content -Path "content\about.md" -Value $aboutPage

# Test build
Write-Host "`nTesting Hugo build..." -ForegroundColor Yellow
Push-Location -Path $PSScriptRoot
hugo --gc --minify
$buildSuccess = $LASTEXITCODE -eq 0
Pop-Location

if ($buildSuccess) {
    Write-Host "`nBUILD SUCCESSFUL! Your site should work now." -ForegroundColor Green
    Write-Host "Check public\index.html to see if content is there" -ForegroundColor Cyan
} else {
    Write-Host "`nBUILD FAILED! Check the errors above." -ForegroundColor Red
}

Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Run 'hugo server' to preview locally"
Write-Host "2. Check http://localhost:1313 in your browser"
Write-Host "3. If it works, push to GitHub"
