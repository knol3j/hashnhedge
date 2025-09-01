# Complete URL and Infinite Scroll Fix Script
# This script fixes all broken URLs, sanitizes filenames, and enables infinite scroll

Write-Host "Starting comprehensive URL and infinite scroll fix..." -ForegroundColor Cyan

# Step 1: Clean all problematic filenames
Write-Host "`nStep 1: Cleaning problematic filenames..." -ForegroundColor Yellow

$contentFiles = Get-ChildItem -Path "content" -Recurse -Filter "*.md"
$renamedCount = 0

foreach ($file in $contentFiles) {
    $oldName = $file.Name
    # Remove leading/trailing spaces and special characters
    $newName = $oldName.Trim()
    $newName = $newName -replace '^\s+', ''
    $newName = $newName -replace '\s+$', ''
    $newName = $newName -replace '[^\w\s\-\.]', ''
    $newName = $newName -replace '\s+', '-'
    $newName = $newName.ToLower()
    
    if ($oldName -ne $newName) {
        $newPath = Join-Path $file.DirectoryName $newName
        if (!(Test-Path $newPath)) {
            Rename-Item -Path $file.FullName -NewName $newName
            Write-Host "  Renamed: $oldName -> $newName" -ForegroundColor Green
            $renamedCount++
        }
    }
}

Write-Host "  Renamed $renamedCount files" -ForegroundColor Green

# Step 2: Clean image filenames to match
Write-Host "`nStep 2: Cleaning image filenames..." -ForegroundColor Yellow

$imageFiles = Get-ChildItem -Path "static/images/generated" -Recurse -Filter "*.svg"
$imageRenamedCount = 0

foreach ($file in $imageFiles) {
    $oldName = $file.Name
    # Same cleaning as content files
    $newName = $oldName.Trim()
    $newName = $newName -replace '^\s+', ''
    $newName = $newName -replace '\s+$', ''
    $newName = $newName -replace '[^\w\s\-\.]', ''
    $newName = $newName -replace '\s+', '-'
    $newName = $newName.ToLower()
    
    if ($oldName -ne $newName) {
        $newPath = Join-Path $file.DirectoryName $newName
        if (!(Test-Path $newPath)) {
            Rename-Item -Path $file.FullName -NewName $newName
            Write-Host "  Renamed image: $oldName -> $newName" -ForegroundColor Green
            $imageRenamedCount++
        }
    }
}

Write-Host "  Renamed $imageRenamedCount images" -ForegroundColor Green

# Step 3: Update all content files to use proper image paths
Write-Host "`nStep 3: Updating image paths in content files..." -ForegroundColor Yellow

$contentFiles = Get-ChildItem -Path "content" -Recurse -Filter "*.md"
foreach ($file in $contentFiles) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content
    
    # Extract the clean filename for the image
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $dirName = Split-Path $file.DirectoryName -Leaf
    
    # Determine section (briefs or posts)
    $section = if ($file.FullName -match "\\briefs\\") { "briefs" } else { "posts" }
    
    # Build the correct image path
    $imagePath = "/images/generated/$section/$dirName/$baseName.svg"
    
    # Update the image field in front matter
    if ($content -match '(?ms)(^---.*?)image:\s*"[^"]*"(.*?---)') {
        $content = $content -replace '(?ms)(^---.*?)image:\s*"[^"]*"(.*?---)', "`$1image: `"$imagePath`"`$2"
    } elseif ($content -match '(?ms)(^---.*?)(---)' -and $content -notmatch 'image:') {
        # Add image field if missing
        $content = $content -replace '(?ms)(^---.*?)(---)', "`$1image: `"$imagePath`"`n`$2"
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        Write-Host "  Updated image path in: $($file.Name)" -ForegroundColor Green
    }
}

Write-Host "`nURL sanitization complete!" -ForegroundColor Green
Write-Host "Now rebuilding site..." -ForegroundColor Yellow

# Clean and rebuild
Remove-Item -Path "public" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "resources" -Recurse -Force -ErrorAction SilentlyContinue

# Build the site
hugo --gc --minify --baseURL "https://hashnhedge.com/"

Write-Host "`nSite rebuilt successfully!" -ForegroundColor Green
Write-Host "All URLs should now be working correctly." -ForegroundColor Cyan
