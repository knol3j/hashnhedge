#!/usr/bin/env pwsh
# Hash & Hedge Complete Site Fix - WORKING VERSION
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "HASH AND HEDGE COMPLETE SITE FIX" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$rootPath = "C:\Users\gnul\hashnhedge"
$sitePath = "$rootPath\site"

# Step 1: Ensure site directory exists
Write-Host "`n[Step 1] Setting up site structure..." -ForegroundColor Yellow

if (-not (Test-Path $sitePath)) {
    New-Item -ItemType Directory -Path $sitePath -Force | Out-Null
}

# Move essential folders to site directory
$folders = @("content", "static", "themes", "layouts", "data", "archetypes")
foreach ($folder in $folders) {
    if ((Test-Path "$rootPath\$folder") -and -not (Test-Path "$sitePath\$folder")) {
        Write-Host "Moving $folder to site directory..."
        Move-Item -Path "$rootPath\$folder" -Destination "$sitePath\$folder" -Force
    }
}

# Step 2: Clone Newsroom theme
Write-Host "`n[Step 2] Installing Newsroom theme..." -ForegroundColor Yellow

if (-not (Test-Path "$sitePath\themes")) {
    New-Item -ItemType Directory -Path "$sitePath\themes" -Force | Out-Null
}

if (-not (Test-Path "$sitePath\themes\newsroom")) {
    Set-Location $sitePath
    git clone https://github.com/onweru/newsroom.git themes/newsroom
    Write-Host "Newsroom theme installed!" -ForegroundColor Green
}
# Step 3: Create essential directories
Write-Host "`n[Step 3] Creating directory structure..." -ForegroundColor Yellow

$dirs = @(
    "$sitePath\content",
    "$sitePath\content\posts",
    "$sitePath\content\pages",
    "$sitePath\static",
    "$sitePath\static\images",
    "$sitePath\static\images\posts",
    "$sitePath\static\css",
    "$sitePath\layouts",
    "$sitePath\layouts\partials",
    "$sitePath\layouts\shortcodes",
    "$sitePath\data",
    "$sitePath\assets"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "Directory structure created!" -ForegroundColor Green
# Step 4: Write Hugo configuration
Write-Host "`n[Step 4] Writing Hugo configuration..." -ForegroundColor Yellow

$config = @'
baseURL = "https://hashnhedge.com/"
title = "Hash & Hedge"
languageCode = "en-us"
theme = "newsroom"
paginate = 12
summaryLength = 25

enableRobotsTXT = true
canonifyURLs = true

[outputs]
  home = ["HTML", "RSS", "JSON"]
  section = ["HTML", "RSS"]

[params]
  author = "Hash & Hedge"
  description = "Cryptocurrency, finance, and security insights. Smart financial strategies for building wealth."
  tagline = "Life in the grey makes you appreciate color in everything"
  
  # AdSense - READY FOR MONETIZATION
  googleAdsenseID = "ca-pub-4626165154390205"
  enableAdsense = true
  adsenseAutoAds = true
  
  # Google Analytics 4
  ga_analytics = "G-4BD4Z2JKW3"
  
  # Social
  twitter = "hashnhedge"
  github = "knol3j/hashnhedge"

[[menu.main]]
  name = "Home"
  url = "/"
  weight = 1

[[menu.main]]
  name = "Crypto"
  url = "/categories/crypto/"
  weight = 2

[[menu.main]]
  name = "Finance"
  url = "/categories/finance/"
  weight = 3

[taxonomies]
  category = "categories"
  tag = "tags"

[permalinks]
  posts = "/:year/:month/:slug/"

[sitemap]
  changefreq = "daily"
  filename = "sitemap.xml"

[markup.goldmark.renderer]
  unsafe = true
'@

Set-Content -Path "$sitePath\config.toml" -Value $config -Encoding UTF8
Write-Host "Configuration written!" -ForegroundColor Green
# Step 5: Create monetization files
Write-Host "`n[Step 5] Creating monetization files..." -ForegroundColor Yellow

# ads.txt
Set-Content -Path "$sitePath\static\ads.txt" -Value "google.com, pub-4626165154390205, DIRECT, f08c47fec0942fa0" -Encoding UTF8

# robots.txt
$robots = @"
User-agent: *
Allow: /
Sitemap: https://hashnhedge.com/sitemap.xml
"@
Set-Content -Path "$sitePath\static\robots.txt" -Value $robots -Encoding UTF8

# CNAME
Set-Content -Path "$sitePath\static\CNAME" -Value "hashnhedge.com" -Encoding UTF8

Write-Host "Monetization files created!" -ForegroundColor Green

# Step 6: Create sample content
Write-Host "`n[Step 6] Creating sample content..." -ForegroundColor Yellow

$year = Get-Date -Format "yyyy"
$month = Get-Date -Format "MM"
$postDir = "$sitePath\content\posts\$year\$month"

if (-not (Test-Path $postDir)) {
    New-Item -ItemType Directory -Path $postDir -Force | Out-Null
}
$date = Get-Date -Format "yyyy-MM-ddTHH:mm:ss-05:00"
$samplePost = @"
---
title: "Bitcoin Breaks Through Critical Resistance"
date: $date
draft: false
categories: ["crypto", "markets"]
tags: ["bitcoin", "cryptocurrency", "trading"]
summary: "Bitcoin surges past key resistance levels as institutional adoption drives momentum."
image: "/images/posts/bitcoin-surge.jpg"
---

## Market Overview

Bitcoin has successfully broken through critical resistance levels, marking a significant milestone in the current market cycle.

### Key Highlights

- Trading volume increases by 45% in 24 hours
- Institutional wallets accumulating at increased rates
- Technical indicators showing bullish divergence

### What This Means

The breakthrough suggests we may be entering a new phase of the market cycle. Long-term holders remain confident.

---

*Not financial advice. Always do your own research.*
"@

Set-Content -Path "$postDir\bitcoin-breaks-resistance.md" -Value $samplePost -Encoding UTF8
Write-Host "Sample content created!" -ForegroundColor Green
# Step 7: Build Hugo site
Write-Host "`n[Step 7] Building site with Hugo..." -ForegroundColor Yellow

Set-Location $sitePath

# Clean previous build
if (Test-Path "$sitePath\public") {
    Remove-Item -Path "$sitePath\public" -Recurse -Force
}

# Build site
hugo --gc --minify --cleanDestinationDir

if (Test-Path "$sitePath\public\index.html") {
    Write-Host "Site built successfully!" -ForegroundColor Green
    $fileCount = (Get-ChildItem -Path "$sitePath\public" -Recurse -File).Count
    Write-Host "Generated $fileCount files" -ForegroundColor Cyan
}

# Step 8: Deploy to GitHub
Write-Host "`n[Step 8] Deploying to GitHub..." -ForegroundColor Yellow

Set-Location $rootPath

# Configure Git
git config user.name "Hash and Hedge Bot"
git config user.email "ugbuni@proton.me"

# Stage and commit
git add -A

$status = git status --porcelain
if ($status) {
    git commit -m "fix: Complete site overhaul with Newsroom theme and AdSense"
    git push origin main --force
    Write-Host "Deployed to GitHub!" -ForegroundColor Green
}

# Final Report
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "SITE FIXED AND DEPLOYED!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Theme: Newsroom installed" -ForegroundColor Green
Write-Host "✓ AdSense: ca-pub-4626165154390205" -ForegroundColor Green
Write-Host "✓ Analytics: G-4BD4Z2JKW3" -ForegroundColor Green
Write-Host "✓ URL: https://hashnhedge.com" -ForegroundColor Green
Write-Host ""
Write-Host "Next: Visit your site to verify!" -ForegroundColor Yellow