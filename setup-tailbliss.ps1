#!/usr/bin/env pwsh

# Hash & Hedge Site Setup Script
Write-Host "Setting up Hash & Hedge with TailBliss theme..." -ForegroundColor Green

# Copy the new site over the old one
Write-Host "Backing up old site..." -ForegroundColor Yellow
if (Test-Path "C:\Users\gnul\hashnhedge\site-old") {
    Remove-Item -Path "C:\Users\gnul\hashnhedge\site-old" -Recurse -Force
}
if (Test-Path "C:\Users\gnul\hashnhedge\site") {
    Move-Item -Path "C:\Users\gnul\hashnhedge\site" -Destination "C:\Users\gnul\hashnhedge\site-old"
}

Write-Host "Installing new TailBliss-based site..." -ForegroundColor Yellow
Move-Item -Path "C:\Users\gnul\hashnhedge\site-new" -Destination "C:\Users\gnul\hashnhedge\site"

Write-Host "Site setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. cd C:\Users\gnul\hashnhedge\site" -ForegroundColor White
Write-Host "2. npm install (if not already done)" -ForegroundColor White
Write-Host "3. npm run start (for development)" -ForegroundColor White
Write-Host "4. npm run build (for production)" -ForegroundColor White
Write-Host ""
Write-Host "Your site will be available at http://localhost:1313/" -ForegroundColor Cyan
Write-Host ""
Write-Host "To integrate with your existing automation:" -ForegroundColor Yellow
Write-Host "- Update your publish.ps1 script to use the new site directory"
Write-Host "- Your pipeline scripts should work with the new content structure"
Write-Host "- The site builds much faster now!"
Write-Host ""
