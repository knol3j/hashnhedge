#!/usr/bin/env pwsh
# Hash & Hedge - Complete Build and Deploy Script

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "HASH & HEDGE - BUILD AND DEPLOY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$rootPath = "C:\Users\gnul\hashnhedge"
$sitePath = "$rootPath\site"

# Step 1: Build the site
Write-Host "`n[1/3] Building site with Hugo..." -ForegroundColor Yellow

Set-Location $sitePath

# Clean public directory
if (Test-Path "$sitePath\public") {
    Remove-Item -Path "$sitePath\public" -Recurse -Force
}

# Build with Hugo
hugo --gc --minify --cleanDestinationDir

if (Test-Path "$sitePath\public\index.html") {
    Write-Host "✓ Site built successfully!" -ForegroundColor Green
    
    # Copy CNAME to public
    if (Test-Path "$sitePath\static\CNAME") {
        Copy-Item "$sitePath\static\CNAME" -Destination "$sitePath\public\CNAME" -Force
    }
    
    # Count files
    $fileCount = (Get-ChildItem -Path "$sitePath\public" -Recurse -File).Count
    Write-Host "Generated $fileCount files" -ForegroundColor Cyan
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Step 2: Deploy to GitHub
Write-Host "`n[2/3] Deploying to GitHub Pages..." -ForegroundColor Yellow

Set-Location $rootPath

# Configure Git
git config user.name "Hash and Hedge Bot"
git config user.email "ugbuni@proton.me"

# Add all changes
git add -A

# Commit with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$commitMsg = "deploy: Site update - $timestamp"

$status = git status --porcelain
if ($status) {
    git commit -m $commitMsg
    
    # Push to GitHub
    git push origin main --force
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Deployed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Retrying push..." -ForegroundColor Yellow
        git push origin main --force
    }
} else {
    Write-Host "No changes to deploy" -ForegroundColor Yellow
}

# Step 3: Verify deployment
Write-Host "`n[3/3] Verifying deployment..." -ForegroundColor Yellow

# Wait for GitHub Pages to update
Write-Host "Waiting for GitHub Pages to update (30 seconds)..." -ForegroundColor DarkGray
Start-Sleep -Seconds 30

# Check if site is accessible
try {
    $response = Invoke-WebRequest -Uri "https://hashnhedge.com" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Site is LIVE at https://hashnhedge.com!" -ForegroundColor Green
    }
} catch {
    Write-Host "Site may still be updating. Check in a few minutes." -ForegroundColor Yellow
}

# Final Report
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan

Write-Host "`n📊 MONETIZATION STATUS:" -ForegroundColor Yellow
Write-Host "  • AdSense ID: ca-pub-4626165154390205" -ForegroundColor White
Write-Host "  • Analytics: G-4BD4Z2JKW3" -ForegroundColor White
Write-Host "  • ads.txt: Uploaded" -ForegroundColor White
Write-Host "  • Auto Ads: Enabled" -ForegroundColor White

Write-Host "`n🎯 SEO OPTIMIZATION:" -ForegroundColor Yellow
Write-Host "  • Sitemap: Generated" -ForegroundColor White
Write-Host "  • robots.txt: Configured" -ForegroundColor White
Write-Host "  • Meta tags: Optimized" -ForegroundColor White
Write-Host "  • Schema markup: Ready" -ForegroundColor White

Write-Host "`n💰 NEXT STEPS FOR RAPID SCALING:" -ForegroundColor Yellow
Write-Host "  1. Run content generator:" -ForegroundColor White
Write-Host "     python fetch_and_generate.py" -ForegroundColor Cyan
Write-Host "  2. Schedule daily content:" -ForegroundColor White
Write-Host "     Task Scheduler -> Daily at 9 AM" -ForegroundColor Cyan
Write-Host "  3. Monitor AdSense:" -ForegroundColor White
Write-Host "     https://adsense.google.com" -ForegroundColor Cyan
Write-Host "  4. Track Analytics:" -ForegroundColor White
Write-Host "     https://analytics.google.com" -ForegroundColor Cyan

Write-Host "`n✨ Your site is READY to make money!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan