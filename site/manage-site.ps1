# Hash & Hedge Site Management Script
# This script helps manage your Hugo site efficiently

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("build", "serve", "deploy", "optimize", "backup")]
    [string]$Action = "serve",
    
    [Parameter(Mandatory=$false)]
    [int]$Port = 1313,
    
    [Parameter(Mandatory=$false)]
    [string]$Environment = "development"
)

$SiteRoot = "C:\Users\gnul\hashnhedge\site"
Set-Location $SiteRoot

Write-Host "Hash & Hedge Site Manager" -ForegroundColor Magenta
Write-Host "=========================" -ForegroundColor Magenta

switch ($Action) {
    "serve" {
        Write-Host "Starting development server on port $Port..." -ForegroundColor Green
        Write-Host "Site will be available at: http://localhost:$Port" -ForegroundColor Cyan
        hugo server --bind 0.0.0.0 --port $Port --buildDrafts --buildFuture
    }
    
    "build" {
        Write-Host "Building production site..." -ForegroundColor Green
        
        # Clean previous build
        if (Test-Path "public") {
            Remove-Item -Path "public" -Recurse -Force
            Write-Host "Cleaned previous build" -ForegroundColor Yellow
        }
        
        # Build with minification for production
        hugo --minify --environment production
        
        Write-Host "Production build completed!" -ForegroundColor Green
        Write-Host "Files are in the 'public' directory" -ForegroundColor Cyan
    }
    
    "optimize" {
        Write-Host "Optimizing site performance..." -ForegroundColor Green
        
        # Clean resources
        if (Test-Path "resources") {
            Remove-Item -Path "resources" -Recurse -Force
            Write-Host "Cleaned resource cache" -ForegroundColor Yellow
        }
        
        # Rebuild with optimizations
        hugo --minify --gc --cleanDestinationDir
        
        Write-Host "Site optimization completed!" -ForegroundColor Green
    }
    
    "backup" {
        Write-Host "Creating site backup..." -ForegroundColor Green
        
        $BackupName = "hashnhedge-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        $BackupPath = "C:\Users\gnul\$BackupName"
        
        # Create backup directory
        New-Item -Path $BackupPath -ItemType Directory -Force | Out-Null
        
        # Copy essential directories
        Copy-Item -Path "content" -Destination "$BackupPath\content" -Recurse
        Copy-Item -Path "static" -Destination "$BackupPath\static" -Recurse
        Copy-Item -Path "config.toml" -Destination "$BackupPath\config.toml"
        
        Write-Host "Backup created at: $BackupPath" -ForegroundColor Green
        Write-Host "Backup includes: content, static files, and configuration" -ForegroundColor Cyan
    }
    
    "deploy" {
        Write-Host "Preparing for deployment..." -ForegroundColor Green
        
        # Build production site
        & $PSCommandPath -Action "build"
        
        Write-Host "Deployment preparation completed!" -ForegroundColor Green
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Upload the 'public' folder to your web hosting" -ForegroundColor White
        Write-Host "2. Point your domain to the hosting provider" -ForegroundColor White
        Write-Host "3. Set up SSL certificate for HTTPS" -ForegroundColor White
    }
}

# Display site statistics
Write-Host "`n=== Site Statistics ===" -ForegroundColor Cyan

# Count posts
$PostCount = (Get-ChildItem -Path "content\posts" -Recurse -Filter "index.md" | Measure-Object).Count
Write-Host "Total Posts: $PostCount" -ForegroundColor White

# Count images
$ImageCount = (Get-ChildItem -Path "static\images\posts" -Include "*.png", "*.jpg", "*.jpeg", "*.webp" | Measure-Object).Count
Write-Host "Available Images: $ImageCount" -ForegroundColor White

# Show last build time
if (Test-Path "public\index.html") {
    $LastBuild = (Get-Item "public\index.html").LastWriteTime
    Write-Host "Last Build: $LastBuild" -ForegroundColor White
} else {
    Write-Host "Last Build: Never" -ForegroundColor Yellow
}

Write-Host "`nFor help: .\manage-site.ps1 -Action [serve|build|deploy|optimize|backup]" -ForegroundColor Gray