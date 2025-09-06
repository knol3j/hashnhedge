# DEPLOY THIS SHIT TO GITHUB NOW

Write-Host "PUSHING YOUR FIXED SITE TO GITHUB..." -ForegroundColor Green

# Make sure we're in the right place
Set-Location "C:\Users\gnul\hashnhedge"

# Check git status
git status

# Add all changes
git add -A

# Commit with a message that reflects our journey
git commit -m "FIXED: Unfucked the entire Hugo site - removed 498 empty directories, fixed newsroom theme, added real content"

# Push to GitHub (this will trigger your GitHub Actions to deploy)
git push origin main

Write-Host "`nPUSHED! Your site should deploy automatically via GitHub Actions" -ForegroundColor Cyan
Write-Host "Check https://hashnhedge.com in about 5 minutes" -ForegroundColor Yellow
