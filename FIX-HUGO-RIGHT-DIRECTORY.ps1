# ACTUAL EMERGENCY FIX - IN THE RIGHT FUCKING DIRECTORY THIS TIME
Write-Host "FIXING YOUR HUGO SITE (FOR REAL THIS TIME)..." -ForegroundColor Red

# Change to the actual site directory first, you absolute muppet
Set-Location "C:\Users\gnul\hashnhedge"

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow

# First, let's fix those empty post directories by converting ONE to a real post
$realPost = @"
---
title: "Bitcoin Analysis: Why Everyone's Wrong About the Next Bull Run"
date: 2025-01-21T10:30:00-07:00
draft: false
categories: ["crypto", "analysis"]
tags: ["bitcoin", "market-analysis", "trading"]
image: "/images/posts/bitcoin-bull.jpg"
description: "The uncomfortable truth about Bitcoin's next move that nobody wants to admit"
---

Everyone's waiting for the next bull run like it's the second coming of Christ, clutching their hardware wallets and refreshing CoinGecko every thirty seconds. Here's why they're all fucked.

## The Denial Phase

You know what nobody talks about? How every single "crypto expert" on Twitter is basically a carnival fortune teller with a Tradingview subscription. They draw lines on charts like toddlers with crayons, pretending they can predict the future while their own portfolios look like crime scenes.

## The Real Pattern

Here's the pattern that actually matters:
1. Retail gets excited
2. Whales dump on their heads
3. "Diamond hands" become "ramen for dinner"
4. Repeat until poverty

## What's Actually Coming

The next bull run will happen when you've already sold everything at a loss to pay for your therapist who's helping you deal with the trauma of losing your life savings to a dog coin.

That's not financial advice. That's just life in the grey zone where hope goes to die.
"@

# Create the content properly this time
Write-Host "Creating real content..." -ForegroundColor Cyan
New-Item -Path "content\posts\bitcoin-analysis-real.md" -ItemType File -Force | Out-Null
Set-Content -Path "content\posts\bitcoin-analysis-real.md" -Value $realPost

# Now let's fix the config for newsroom theme
$workingConfig = @'
baseURL = "https://hashnhedge.com/"
languageCode = "en-us"
title = "Hash & Hedge"
theme = "newsroom"
paginate = 10

[params]
  author = "Hash & Hedge"
  description = "Life in the grey makes you appreciate color in everything"
  subtitle = "Crypto, finance, and security through the lens of existential dread"
  
[menu]
  [[menu.main]]
    identifier = "home"
    name = "Home"
    url = "/"
    weight = 10
  [[menu.main]]
    identifier = "posts"
    name = "Posts"  
    url = "/posts/"
    weight = 20

[outputs]
  home = ["HTML", "RSS", "JSON"]
'@

# Backup and replace config
if (Test-Path "config.toml") {
    Copy-Item "config.toml" "config.toml.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Force
}
Set-Content -Path "config.toml" -Value $workingConfig

# Create a simple image placeholder
Write-Host "Creating image placeholders..." -ForegroundColor Cyan
New-Item -Path "static\images\posts" -ItemType Directory -Force | Out-Null

# Download a real placeholder image or create one
$imageUrl = "https://via.placeholder.com/1200x630/1a1a1a/666666?text=Hash+and+Hedge"
try {
    Invoke-WebRequest -Uri $imageUrl -OutFile "static\images\posts\bitcoin-bull.jpg"
} catch {
    Write-Host "Couldn't download image, creating SVG instead" -ForegroundColor Yellow
    $svg = @'
<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#1a1a1a"/>
  <text x="50%" y="50%" text-anchor="middle" font-size="48" fill="#666" font-family="Arial">
    Hash &amp; Hedge
  </text>
</svg>
'@
    Set-Content -Path "static\images\posts\placeholder.svg" -Value $svg
}

# Remove all those empty directories that are pretending to be posts
Write-Host "Cleaning up empty post directories..." -ForegroundColor Yellow
Get-ChildItem -Path "content\posts" -Directory | ForEach-Object {
    if ((Get-ChildItem $_.FullName | Measure-Object).Count -eq 0) {
        Remove-Item $_.FullName -Force -Recurse
        Write-Host "Removed empty directory: $($_.Name)" -ForegroundColor DarkGray
    }
}

# Let's also create an index page for the theme
$indexContent = @'
---
title: "Home"
---

Welcome to the digital wasteland where your crypto dreams come to die and finance bros pretend they understand blockchain.
'@

if (-not (Test-Path "content\_index.md")) {
    New-Item -Path "content\_index.md" -ItemType File -Force | Out-Null
    Set-Content -Path "content\_index.md" -Value $indexContent
}

# Test the build
Write-Host "`nTesting Hugo build..." -ForegroundColor Yellow
hugo --gc --minify
$buildSuccess = $LASTEXITCODE -eq 0

if ($buildSuccess) {
    Write-Host "`nBUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "Your site should actually work now." -ForegroundColor Green
    
    # Check if public folder has actual content
    if (Test-Path "public\index.html") {
        $indexSize = (Get-Item "public\index.html").Length
        Write-Host "Index.html size: $indexSize bytes" -ForegroundColor Cyan
        
        if ($indexSize -gt 1000) {
            Write-Host "Content generated successfully!" -ForegroundColor Green
        } else {
            Write-Host "Warning: Index file seems suspiciously small" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "`nBUILD FAILED!" -ForegroundColor Red
    Write-Host "Check the errors above" -ForegroundColor Red
}

Write-Host "`nNEXT STEPS:" -ForegroundColor Magenta
Write-Host "1. Run: hugo server -D" -ForegroundColor White
Write-Host "2. Open: http://localhost:1313" -ForegroundColor White
Write-Host "3. If it looks good, commit and push to GitHub" -ForegroundColor White
Write-Host "4. Your GitHub Actions should deploy it automatically" -ForegroundColor White

Write-Host "`nTo add more content:" -ForegroundColor Cyan
Write-Host "- Put actual .md files in content/posts/ (not empty directories)" -ForegroundColor White
Write-Host "- Add real images to static/images/posts/" -ForegroundColor White
Write-Host "- Stop creating empty folders and expecting magic" -ForegroundColor White
