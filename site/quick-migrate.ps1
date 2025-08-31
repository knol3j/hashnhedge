# Quick Content Migration - Move 20 posts as a test
$SourceRoot = "C:\Users\gnul\hashnhedge"
$SiteRoot = "C:\Users\gnul\hashnhedge\site"
$SourcePosts = "$SourceRoot\content\posts"
$TargetPosts = "$SiteRoot\content\posts\2025\08"
$ImagesPath = "$SiteRoot\static\images\posts"

Write-Host "🚀 Quick Migration - Adding 20 additional posts" -ForegroundColor Green

# Get available images for matching
$AvailableImages = Get-ChildItem -Path $ImagesPath -Include "*.png", "*.jpg", "*.jpeg", "*.webp" | Select-Object -ExpandProperty Name

$count = 0
$maxPosts = 20

Get-ChildItem -Path $SourcePosts -Directory | Select-Object -First $maxPosts | ForEach-Object {
    $sourceDir = $_
    $sourcePath = Join-Path $sourceDir.FullName "index.md"
    
    if (Test-Path $sourcePath) {
        $count++
        $slug = $sourceDir.Name
        $targetDir = "$TargetPosts\$slug"
        
        # Skip if already exists
        if (Test-Path $targetDir) {
            Write-Host "⚠️  Skipping existing: $slug" -ForegroundColor Yellow
            return
        }
        
        # Create directory
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
        
        # Read source content
        $content = Get-Content $sourcePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
        
        if ($content) {
            # Extract title or create from slug
            $title = ($slug -replace '-', ' ' | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) })
            
            # Find matching image
            $imageName = $AvailableImages | Where-Object { $_ -like "*$($slug.Split('-')[0])*" } | Select-Object -First 1
            if (!$imageName) {
                $imageName = "systemobject.jpg"  # fallback
            }
            
            # Create new content with proper front matter
            $newContent = @"
---
title: "$title"
date: "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')"
category: "Tech"
slug: "$slug"
image: "/images/posts/$imageName"
tags: ["tech", "news"]
---

$($content -replace '^---.*?---\s*', '')
"@
            
            # Write to target
            $targetFile = "$targetDir\index.md"
            Set-Content -Path $targetFile -Value $newContent.Trim() -Encoding UTF8
            
            Write-Host "✅ Added: $title" -ForegroundColor Green
        }
    }
}

Write-Host "`n🎉 Successfully added $count additional posts!" -ForegroundColor Magenta
Write-Host "Total posts now: $(Get-ChildItem -Path "$SiteRoot\content\posts" -Recurse -Filter "index.md" | Measure-Object | Select-Object -ExpandProperty Count)" -ForegroundColor Cyan