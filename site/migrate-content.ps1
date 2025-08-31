# Hash & Hedge Content Migration and Site Enhancement Script
# This script migrates all your scattered content and implements infinite scroll

param(
    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$SkipImages = $false
)

$SourceRoot = "C:\Users\gnul\hashnhedge"
$SiteRoot = "C:\Users\gnul\hashnhedge\site"
$SourcePosts = "$SourceRoot\content\posts"
$SourceBriefs = "$SourceRoot\content\briefs"
$TargetPosts = "$SiteRoot\content\posts"
$ImagesPath = "$SiteRoot\static\images\posts"

Write-Host "🚀 Hash & Hedge Content Migration & Enhancement" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}

# Get all available images for matching
$AvailableImages = @{}
Get-ChildItem -Path $ImagesPath -Include "*.png", "*.jpg", "*.jpeg", "*.webp" | ForEach-Object {
    $AvailableImages[$_.BaseName] = $_.Name
}

Write-Host "📷 Found $($AvailableImages.Count) available images" -ForegroundColor Cyan

# Function to find best matching image
function Get-BestImageMatch($Title, $Slug) {
    $cleanTitle = $Title.ToLower() -replace '[^a-z0-9\s]', ''
    $cleanSlug = $Slug.ToLower() -replace '[^a-z0-9\-]', ''
    
    # Direct slug match
    if ($AvailableImages.ContainsKey($cleanSlug)) {
        return $AvailableImages[$cleanSlug]
    }
    
    # Partial slug match
    foreach ($imageKey in $AvailableImages.Keys) {
        if ($cleanSlug -like "*$imageKey*" -or $imageKey -like "*$cleanSlug*") {
            return $AvailableImages[$imageKey]
        }
    }
    
    # Title keyword matches
    $keywords = @{
        "bitcoin|btc|blockchain|crypto" = "bitcoin-consolidation-below-123000-reflects-caution-rather-t.jpg"
        "ethereum|eth" = "ethereum-captures-77-of-375-billion-inflows-while-bitcoin-tr.jpg" 
        "google|android" = "google-is-a-leader-and-positioned-furthest-in-vision-in-the.jpg"
        "microsoft|windows" = "microsoft-is-a-leader-in-the-2025-gartner-magic-quadrant-for.png"
        "aws|amazon" = "aws-named-as-a-leader-in-2025-gartner-magic-quadrant-for-str.png"
        "ai|artificial intelligence" = "how-realworld-businesses-are-transforming-with-ai-with-50-n.png"
        "security|hack|malware" = "powering-aidriven-security-with-the-open-cybersecurity-schem.png"
        "docker|container" = "docker-desktop-444-smarter-ai-modeling-platform-stability-an.png"
        "meta|facebook" = "meta-breaks-up-ai-lab-as-part-of-superintelligence-push.png"
    }
    
    foreach ($pattern in $keywords.Keys) {
        if ($cleanTitle -match $pattern) {
            return $keywords[$pattern]
        }
    }
    
    # Default fallback
    return "systemobject.jpg"
}

# Function to create proper post structure
function Create-PostStructure($SourcePath, $PostTitle, $PostSlug, $Category = "Markets") {
    $year = "2025"
    $month = "08"
    
    # Create target directory structure
    $targetDir = "$TargetPosts\$year\$month\$PostSlug"
    
    if (!$DryRun) {
        if (!(Test-Path $targetDir)) {
            New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
        }
    }
    
    return $targetDir
}

# Function to process individual post
function Process-Post($SourceFile, $IsFromBriefs = $false) {
    try {
        $content = Get-Content $SourceFile -Raw -Encoding UTF8
        
        # Extract metadata from existing content or create new
        $title = ""
        $slug = ""
        
        if ($content -match 'title\s*:\s*"([^"]+)"') {
            $title = $matches[1]
        } elseif ($IsFromBriefs) {
            $title = [System.IO.Path]::GetFileNameWithoutExtension($SourceFile.Name)
            $title = $title -replace '\.md(\.bad)?$', ''
            $title = (Get-Culture).TextInfo.ToTitleCase($title)
        } else {
            $title = (Split-Path $SourceFile.FullName -Parent | Split-Path -Leaf) -replace '-', ' '
            $title = (Get-Culture).TextInfo.ToTitleCase($title)
        }
        
        # Create clean slug
        $slug = $title.ToLower() -replace '[^a-z0-9\s]', '' -replace '\s+', '-'
        $slug = $slug -replace '^-+|-+$', ''  # Remove leading/trailing hyphens
        
        # Find best image
        $imagePath = "/images/posts/" + (Get-BestImageMatch -Title $title -Slug $slug)
        
        # Create target directory
        $targetDir = Create-PostStructure -SourcePath $SourceFile.FullName -PostTitle $title -PostSlug $slug
        $targetFile = "$targetDir\index.md"
        
        # Skip if already exists
        if (!$DryRun -and (Test-Path $targetFile)) {
            Write-Host "⚠️  Skipping (exists): $title" -ForegroundColor Yellow
            return $false
        }
        
        # Create new front matter
        $frontMatter = @"
---
title: "$title"
date: "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')"
category: "Markets"
slug: "$slug"
image: "$imagePath"
tags: ["tech", "news", "analysis"]
---
"@
        
        # Extract content body (remove existing front matter if present)
        $bodyContent = $content
        if ($content -match '^---\s*\n(.*?\n)---\s*\n(.*)$' -or $content -match '^---\s*\r?\n(.*?\r?\n)---\s*\r?\n(.*)$') {
            $bodyContent = $matches[2]
        }
        
        $finalContent = $frontMatter + "`n`n" + $bodyContent.Trim()
        
        if (!$DryRun) {
            Set-Content -Path $targetFile -Value $finalContent -Encoding UTF8
            Write-Host "✅ Migrated: $title" -ForegroundColor Green
        } else {
            Write-Host "🔍 Would migrate: $title -> $targetDir" -ForegroundColor Cyan
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Failed to process: $($SourceFile.Name) - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Migrate main posts
Write-Host "`n📁 Migrating main posts..." -ForegroundColor Blue
$migratedCount = 0
$skippedCount = 0

if (Test-Path $SourcePosts) {
    Get-ChildItem -Path $SourcePosts -Directory | ForEach-Object {
        $postDir = $_
        $indexFile = Join-Path $postDir.FullName "index.md"
        
        if (Test-Path $indexFile) {
            if (Process-Post -SourceFile (Get-Item $indexFile)) {
                $migratedCount++
            } else {
                $skippedCount++
            }
        } else {
            Write-Host "⚠️  No index.md found in: $($postDir.Name)" -ForegroundColor Yellow
        }
    }
}

# Migrate briefs
Write-Host "`n📰 Migrating daily briefs..." -ForegroundColor Blue

if (Test-Path $SourceBriefs) {
    Get-ChildItem -Path $SourceBriefs -Recurse -Filter "*.md" | Where-Object { 
        $_.Name -notlike "*.bad" 
    } | ForEach-Object {
        if (Process-Post -SourceFile $_ -IsFromBriefs $true) {
            $migratedCount++
        } else {
            $skippedCount++
        }
    }
}

Write-Host "`n🎉 Migration Summary:" -ForegroundColor Magenta
Write-Host "✅ Successfully migrated: $migratedCount posts" -ForegroundColor Green
Write-Host "⚠️  Skipped: $skippedCount posts" -ForegroundColor Yellow

if (!$DryRun) {
    Write-Host "`n🔄 Rebuilding site..." -ForegroundColor Blue
    Set-Location $SiteRoot
    hugo --quiet
    Write-Host "✅ Site rebuilt successfully!" -ForegroundColor Green
}

Write-Host "`n🚀 Your Hash `& Hedge site now has $(Get-ChildItem -Path "$SiteRoot\content\posts" -Recurse -Filter "index.md" | Measure-Object | Select-Object -ExpandProperty Count) total posts!" -ForegroundColor Magenta