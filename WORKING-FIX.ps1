#!/usr/bin/env pwsh
# Hash & Hedge Complete Site Fix - Working Version
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "HASH AND HEDGE COMPLETE SITE FIX" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$rootPath = "C:\Users\gnul\hashnhedge"
$sitePath = "$rootPath\site"

# Step 1: Ensure site directory exists
Write-Host "`n[1/6] Setting up site structure..." -ForegroundColor Yellow

if (-not (Test-Path $sitePath)) {
    New-Item -ItemType Directory -Path $sitePath -Force | Out-Null
}

# Create all necessary directories
$dirs = @(
    "$sitePath\content",
    "$sitePath\content\posts",
    "$sitePath\content\posts\2025",
    "$sitePath\content\posts\2025\01",
    "$sitePath\static",
    "$sitePath\static\images",
    "$sitePath\static\images\posts",
    "$sitePath\static\css",
    "$sitePath\themes",
    "$sitePath\layouts",
    "$sitePath\layouts\partials",
    "$sitePath\data"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "Directory structure created!" -ForegroundColor Green
# Step 2: Move content if needed
Write-Host "`n[2/6] Organizing content..." -ForegroundColor Yellow

if ((Test-Path "$rootPath\content") -and -not (Test-Path "$sitePath\content\posts")) {
    Write-Host "Moving content to site folder..."
    Get-ChildItem "$rootPath\content" -Recurse | ForEach-Object {
        $dest = $_.FullName.Replace("$rootPath\content", "$sitePath\content")
        $destDir = Split-Path $dest -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        if ($_.PSIsContainer -eq $false) {
            Copy-Item $_.FullName -Destination $dest -Force
        }
    }
}

# Step 3: Install Newsroom theme
Write-Host "`n[3/6] Installing Newsroom theme..." -ForegroundColor Yellow

if (-not (Test-Path "$sitePath\themes\newsroom")) {
    Set-Location $sitePath
    git clone https://github.com/onweru/newsroom.git themes/newsroom
    Write-Host "Newsroom theme installed!" -ForegroundColor Green
} else {
    Write-Host "Newsroom theme already exists" -ForegroundColor Green
}

# Step 4: Create optimized config
Write-Host "`n[4/6] Writing configuration..." -ForegroundColor Yellow

$config = @'
baseURL = "https://hashnhedge.com/"
title = "Hash & Hedge"
languageCode = "en-us"
theme = "newsroom"
paginate = 12

[params]
  author = "Hash & Hedge"
  description = "Cryptocurrency and finance insights"
  googleAdsenseID = "ca-pub-4626165154390205"
  enableAdsense = true
  ga_analytics = "G-4BD4Z2JKW3"

[[menu.main]]
  name = "Home"
  url = "/"
  weight = 1

[[menu.main]]
  name = "Crypto"
  url = "/categories/crypto/"
  weight = 2

[taxonomies]
  category = "categories"
  tag = "tags"

[outputs]
  home = ["HTML", "RSS", "JSON"]
  section = ["HTML", "RSS"]
'@

Set-Content -Path "$sitePath\config.toml" -Value $config -Encoding UTF8
Write-Host "Configuration written!" -ForegroundColor Green
# Step 5: Create monetization files
Write-Host "`n[5/6] Setting up monetization files..." -ForegroundColor Yellow

# ads.txt
"google.com, pub-4626165154390205, DIRECT, f08c47fec0942fa0" | Set-Content "$sitePath\static\ads.txt" -Encoding UTF8

# robots.txt
@"
User-agent: *
Allow: /
Sitemap: https://hashnhedge.com/sitemap.xml
"@ | Set-Content "$sitePath\static\robots.txt" -Encoding UTF8

# CNAME
"hashnhedge.com" | Set-Content "$sitePath\static\CNAME" -Encoding UTF8

Write-Host "Monetization files created!" -ForegroundColor Green

# Step 6: Build and deploy
Write-Host "`n[6/6] Building site..." -ForegroundColor Yellow

Set-Location $sitePath

# Build Hugo site
hugo --gc --minify

if (Test-Path "$sitePath\public") {
    Write-Host "Site built successfully!" -ForegroundColor Green
    
    # Copy CNAME to public
    Copy-Item "$sitePath\static\CNAME" "$sitePath\public\CNAME" -Force -ErrorAction SilentlyContinue
}

# Deploy to GitHub
Set-Location $rootPath
git add -A
git commit -m "fix: Complete site overhaul with Newsroom theme and AdSense"
git push origin main --force

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Visit https://hashnhedge.com in 2-3 minutes" -ForegroundColor Yellow
Write-Host "AdSense ID: ca-pub-4626165154390205" -ForegroundColor White
Write-Host "Analytics: G-4BD4Z2JKW3" -ForegroundColor White