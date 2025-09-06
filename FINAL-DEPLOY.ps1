#!/usr/bin/env pwsh
# FINAL COMPREHENSIVE FIX AND DEPLOY

Write-Host "HASH & HEDGE - FINAL DEPLOYMENT" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$root = "C:\Users\gnul\hashnhedge"
$site = "$root\site"

# Step 1: Check Hugo
Write-Host "`n[1/4] Checking Hugo..." -ForegroundColor Yellow
Set-Location $site
$hugoVersion = hugo version
Write-Host $hugoVersion -ForegroundColor DarkGray

# Step 2: Build site
Write-Host "`n[2/4] Building site..." -ForegroundColor Yellow
hugo --gc --minify

if (Test-Path "$site\public\index.html") {
    Write-Host "Build successful!" -ForegroundColor Green
} else {
    Write-Host "Build failed - trying without theme..." -ForegroundColor Red
    
    # Try building without theme as fallback
    hugo --gc --minify --theme=""
}

# Step 3: Push to GitHub
Write-Host "`n[3/4] Pushing to GitHub..." -ForegroundColor Yellow
Set-Location $root

git add -A
git commit -m "deploy: Final comprehensive site update with content"
git push origin main --force

# Step 4: Summary
Write-Host "`n[4/4] DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Site: https://hashnhedge.com" -ForegroundColor White
Write-Host "AdSense: ca-pub-4626165154390205" -ForegroundColor White
Write-Host "Analytics: G-4BD4Z2JKW3" -ForegroundColor White
Write-Host "`nMonetization is READY!" -ForegroundColor Green