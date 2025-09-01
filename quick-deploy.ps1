# Hash & Hedge Site Deployment Script
Write-Host "Starting Hash & Hedge deployment..." -ForegroundColor Cyan

Set-Location "C:\Users\gnul\hashnhedge"

# Build the site
Write-Host "Building site with Hugo..." -ForegroundColor Yellow
hugo --gc --minify --baseURL "https://hashnhedge.com"

# Check if build succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful!" -ForegroundColor Green
    
    # Git operations
    Write-Host "Deploying to GitHub..." -ForegroundColor Yellow
    git add -A
    git commit -m "Update: new content, images, and SEO optimizations"
    git push origin main --force
    
    Write-Host "Deployment complete!" -ForegroundColor Green
    Write-Host "Visit https://hashnhedge.com to see your site" -ForegroundColor Cyan
} else {
    Write-Host "Build failed - please check for errors" -ForegroundColor Red
}
