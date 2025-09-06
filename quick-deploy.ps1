#!/usr/bin/env pwsh
# Hash & Hedge - Quick Deploy

$rootPath = "C:\Users\gnul\hashnhedge"
$sitePath = "$rootPath\site"

Write-Host "Building and deploying Hash & Hedge..." -ForegroundColor Cyan

# Build
Set-Location $sitePath
hugo --gc --minify --cleanDestinationDir

# Deploy
Set-Location $rootPath
git add -A
git commit -m "deploy: Site update"
git push origin main --force

Write-Host "Done! Visit https://hashnhedge.com" -ForegroundColor Green