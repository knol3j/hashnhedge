# Local build script for testing (PowerShell version of Netlify build)
Write-Host "Starting local build (mimics Netlify)..." -ForegroundColor Green

# Update git submodules
Write-Host "Updating git submodules..." -ForegroundColor Yellow
git submodule update --init --recursive

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to update submodules" -ForegroundColor Red
    exit 1
}

# Build with Hugo
Write-Host "Building site with Hugo..." -ForegroundColor Yellow
hugo --gc --minify

if ($LASTEXITCODE -ne 0) {
    Write-Host "Hugo build failed" -ForegroundColor Red
    exit 1
}

Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Output is in the 'public' directory" -ForegroundColor Cyan
