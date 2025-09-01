# Script to generate unique images for every story based on content
# Uses multiple strategies to ensure no duplicate images

param(
    [string]$ContentPath = "content",
    [string]$OutputPath = "static/images/generated",
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

# Create output directory if it doesn't exist
if (-not $DryRun -and -not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}

# Hash table to track used images and ensure uniqueness
$usedImages = @{}
$imageCounter = 0

# Color palettes for generating unique SVGs
$colorPalettes = @(
    @{ Primary = "#1e3c72"; Secondary = "#2a5298"; Accent = "#4CAF50" },
    @{ Primary = "#667eea"; Secondary = "#764ba2"; Accent = "#f093fb" },
    @{ Primary = "#f12711"; Secondary = "#f5af19"; Accent = "#ff6b6b" },
    @{ Primary = "#11998e"; Secondary = "#38ef7d"; Accent = "#00d2ff" },
    @{ Primary = "#373B44"; Secondary = "#4286f4"; Accent = "#00c6ff" },
    @{ Primary = "#DA22FF"; Secondary = "#9733EE"; Accent = "#ff0080" },
    @{ Primary = "#ee0979"; Secondary = "#ff6a00"; Accent = "#ffd200" },
    @{ Primary = "#00c6ff"; Secondary = "#0072ff"; Accent = "#00d4ff" },
    @{ Primary = "#fc4a1a"; Secondary = "#f7b733"; Accent = "#ff9068" },
    @{ Primary = "#22c1c3"; Secondary = "#fdbb2d"; Accent = "#1abc9c" }
)

# Icon patterns for different content types
$iconPatterns = @{
    "crypto" = @'
<g transform="translate(400, 200)">
    <circle cx="0" cy="0" r="60" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.3"/>
    <text x="0" y="10" font-family="monospace" font-size="48" fill="#ffffff" text-anchor="middle" opacity="0.8">₿</text>
</g>
'@
    "ai" = @'
<g transform="translate(400, 200)">
    <rect x="-40" y="-40" width="80" height="80" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.3"/>
    <circle cx="0" cy="0" r="20" fill="#ffffff" opacity="0.5"/>
    <circle cx="-20" cy="-20" r="5" fill="#ffffff"/>
    <circle cx="20" cy="-20" r="5" fill="#ffffff"/>
    <circle cx="-20" cy="20" r="5" fill="#ffffff"/>
    <circle cx="20" cy="20" r="5" fill="#ffffff"/>
</g>
'@
    "finance" = @'
<g transform="translate(400, 200)" opacity="0.4">
    <path d="M-60,20 L-30,-20 L0,10 L30,-30 L60,0" stroke="#ffffff" stroke-width="3" fill="none"/>
    <circle cx="-60" cy="20" r="4" fill="#ffffff"/>
    <circle cx="-30" cy="-20" r="4" fill="#ffffff"/>
    <circle cx="0" cy="10" r="4" fill="#ffffff"/>
    <circle cx="30" cy="-30" r="4" fill="#ffffff"/>
    <circle cx="60" cy="0" r="4" fill="#ffffff"/>
</g>
'@
    "tech" = @'
<g transform="translate(400, 200)" opacity="0.3">
    <path d="M-50,-50 L50,-50 L50,50 L-50,50 Z" fill="none" stroke="#ffffff" stroke-width="2"/>
    <path d="M-30,-30 L30,-30 L30,30 L-30,30 Z" fill="none" stroke="#ffffff" stroke-width="2"/>
    <path d="M-10,-10 L10,-10 L10,10 L-10,10 Z" fill="#ffffff" opacity="0.6"/>
</g>
'@
    "business" = @'
<g transform="translate(400, 200)" opacity="0.4">
    <rect x="-60" y="-40" width="120" height="80" fill="none" stroke="#ffffff" stroke-width="3"/>
    <rect x="-40" y="-20" width="30" height="40" fill="#ffffff" opacity="0.3"/>
    <rect x="-5" y="-30" width="30" height="50" fill="#ffffff" opacity="0.4"/>
    <rect x="30" y="-10" width="30" height="30" fill="#ffffff" opacity="0.3"/>
</g>
'@
    "default" = @'
<g transform="translate(400, 200)" opacity="0.3">
    <polygon points="0,-50 43.3,25 -43.3,25" fill="none" stroke="#ffffff" stroke-width="3"/>
    <circle cx="0" cy="0" r="20" fill="#ffffff" opacity="0.5"/>
</g>
'@
}

# Function to extract keywords from content
function Get-ContentKeywords {
    param([string]$Content)
    
    $keywords = @()
    
    # Common keyword patterns to look for
    $patterns = @{
        "bitcoin" = "crypto"
        "ethereum" = "crypto"
        "blockchain" = "crypto"
        "cryptocurrency" = "crypto"
        "defi" = "crypto"
        "nft" = "crypto"
        "artificial intelligence" = "ai"
        "machine learning" = "ai"
        "ai" = "ai"
        "gpt" = "ai"
        "neural" = "ai"
        "algorithm" = "ai"
        "stock" = "finance"
        "trading" = "finance"
        "investment" = "finance"
        "market" = "finance"
        "finance" = "finance"
        "economy" = "finance"
        "technology" = "tech"
        "software" = "tech"
        "hardware" = "tech"
        "computing" = "tech"
        "digital" = "tech"
        "startup" = "business"
        "company" = "business"
        "business" = "business"
        "corporate" = "business"
        "enterprise" = "business"
    }
    
    $contentLower = $Content.ToLower()
    foreach ($pattern in $patterns.Keys) {
        if ($contentLower -match $pattern) {
            return $patterns[$pattern]
        }
    }
    
    return "default"
}

# Function to generate a unique hash for content
function Get-ContentHash {
    param([string]$Content)
    
    $md5 = [System.Security.Cryptography.MD5]::Create()
    $hash = [System.BitConverter]::ToString($md5.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Content)))
    return $hash.Replace("-", "").Substring(0, 8).ToLower()
}

# Function to generate unique SVG based on content
function Generate-UniqueSVG {
    param(
        [string]$Title,
        [string]$Content,
        [int]$Index
    )
    
    $keyword = Get-ContentKeywords -Content "$Title $Content"
    $contentHash = Get-ContentHash -Content "$Title $Content"
    $paletteIndex = $Index % $colorPalettes.Count
    $palette = $colorPalettes[$paletteIndex]
    
    # Get appropriate icon pattern
    $iconPattern = $iconPatterns[$keyword]
    if (-not $iconPattern) {
        $iconPattern = $iconPatterns["default"]
    }
    
    # Generate unique geometric patterns based on hash
    $hashValue = [Convert]::ToInt32($contentHash.Substring(0, 4), 16)
    $pattern1X = ($hashValue % 200) + 100
    $pattern1Y = (($hashValue * 7) % 150) + 50
    $pattern2X = (($hashValue * 13) % 200) + 500
    $pattern2Y = (($hashValue * 17) % 150) + 200
    
    $svg = @"
<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
    <!-- Unique gradient based on content hash -->
    <defs>
        <linearGradient id="grad_$contentHash" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:$($palette.Primary);stop-opacity:1" />
            <stop offset="50%" style="stop-color:$($palette.Secondary);stop-opacity:1" />
            <stop offset="100%" style="stop-color:$($palette.Accent);stop-opacity:0.8" />
        </linearGradient>
        <filter id="blur_$contentHash">
            <feGaussianBlur stdDeviation="2"/>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="800" height="400" fill="url(#grad_$contentHash)"/>
    
    <!-- Unique geometric patterns based on content hash -->
    <g opacity="0.1">
        <circle cx="$pattern1X" cy="$pattern1Y" r="$(($hashValue % 50) + 30)" fill="#ffffff" filter="url(#blur_$contentHash)"/>
        <circle cx="$pattern2X" cy="$pattern2Y" r="$(($hashValue % 40) + 40)" fill="#ffffff" filter="url(#blur_$contentHash)"/>
        <rect x="$(($hashValue % 300) + 50)" y="$(($hashValue % 200) + 100)" 
              width="$(($hashValue % 100) + 50)" height="$(($hashValue % 80) + 30)" 
              fill="#ffffff" opacity="0.05" transform="rotate($(($hashValue % 45) - 22.5) 400 200)"/>
    </g>
    
    <!-- Content type icon -->
    $iconPattern
    
    <!-- Dynamic pattern overlay -->
    <g opacity="0.15">
        <path d="M0,$(($hashValue % 100) + 150) Q200,$(($hashValue % 50) + 100) 400,$(($hashValue % 100) + 150) T800,$(($hashValue % 100) + 150)" 
              stroke="#ffffff" stroke-width="2" fill="none"/>
        <path d="M0,$(($hashValue % 80) + 250) Q200,$(($hashValue % 60) + 200) 400,$(($hashValue % 80) + 250) T800,$(($hashValue % 80) + 250)" 
              stroke="#ffffff" stroke-width="1" fill="none"/>
    </g>
    
    <!-- Title text -->
    <text x="400" y="350" font-family="Arial, sans-serif" font-size="14" fill="#ffffff" text-anchor="middle" opacity="0.7">
        $(if ($Title.Length -gt 60) { $Title.Substring(0, 57) + "..." } else { $Title })
    </text>
    
    <!-- Unique identifier -->
    <text x="780" y="390" font-family="monospace" font-size="8" fill="#ffffff" text-anchor="end" opacity="0.3">
        #$contentHash
    </text>
</svg>
"@
    
    return $svg
}

# Function to process a single markdown file
function Process-MarkdownFile {
    param(
        [System.IO.FileInfo]$File,
        [int]$Index
    )
    
    try {
        $content = Get-Content $File.FullName -Raw -Encoding UTF8
        
        # Extract title and existing image from front matter
        $title = ""
        $existingImage = ""
        $category = ""
        
        if ($content -match "title:\s*['""](.+?)['""]") {
            $title = $matches[1]
        }
        if ($content -match "image:\s*['""](.+?)['""]") {
            $existingImage = $matches[1]
        }
        if ($content -match "category:\s*(.+?)[\r\n]") {
            $category = $matches[1].Trim()
        }
        
        # Generate unique image name based on content
        $contentHash = Get-ContentHash -Content "$title $category $content"
        $imageName = "img_$contentHash.svg"
        $imagePath = "$OutputPath/$imageName"
        $imageUrl = "/images/generated/$imageName"
        
        # Check if this exact content hash has been used
        if ($usedImages.ContainsKey($contentHash)) {
            if ($Verbose) {
                Write-Host "Duplicate content detected for: $($File.Name)" -ForegroundColor Yellow
            }
            # Generate a variant by adding the file path to the hash
            $contentHash = Get-ContentHash -Content "$title $category $content $($File.FullName)"
            $imageName = "img_$contentHash.svg"
            $imagePath = "$OutputPath/$imageName"
            $imageUrl = "/images/generated/$imageName"
        }
        
        # Mark this image as used
        $usedImages[$contentHash] = $true
        
        # Generate unique SVG
        $svgContent = Generate-UniqueSVG -Title $title -Content $content -Index $Index
        
        if (-not $DryRun) {
            # Save SVG file
            Set-Content -Path $imagePath -Value $svgContent -Encoding UTF8
            
            # Update markdown file with new image
            if ($existingImage -eq "" -or $existingImage -match "/categories/") {
                # Add or replace with unique image
                if ($existingImage -eq "") {
                    $newContent = $content -replace "(category:\s*.+?[\r\n])", "`$1image: `"$imageUrl`"`r`n"
                } else {
                    $newContent = $content -replace "image:\s*['""].+?['""]", "image: `"$imageUrl`""
                }
                Set-Content -Path $File.FullName -Value $newContent -NoNewline -Encoding UTF8
            }
        }
        
        $script:imageCounter++
        
        return @{
            File = $File.Name
            Title = $title
            ImagePath = $imagePath
            ImageUrl = $imageUrl
            Hash = $contentHash
            Status = "Success"
        }
        
    } catch {
        return @{
            File = $File.Name
            Status = "Error"
            Error = $_.Exception.Message
        }
    }
}

# Main processing
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   Unique Image Generator for Stories    " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "Running in DRY RUN mode - no files will be modified" -ForegroundColor Yellow
    Write-Host ""
}

# Get all markdown files
$markdownFiles = Get-ChildItem -Path $ContentPath -Filter "*.md" -Recurse
$totalFiles = $markdownFiles.Count

Write-Host "Found $totalFiles markdown files to process" -ForegroundColor Green
Write-Host ""

# Process each file
$results = @()
$fileIndex = 0

foreach ($file in $markdownFiles) {
    $fileIndex++
    $percentComplete = [math]::Round(($fileIndex / $totalFiles) * 100, 2)
    
    Write-Progress -Activity "Generating unique images" `
                   -Status "Processing $($file.Name)" `
                   -PercentComplete $percentComplete `
                   -CurrentOperation "File $fileIndex of $totalFiles"
    
    $result = Process-MarkdownFile -File $file -Index $fileIndex
    $results += $result
    
    if ($Verbose) {
        if ($result.Status -eq "Success") {
            Write-Host "✓ " -NoNewline -ForegroundColor Green
            Write-Host "$($result.File) -> $($result.ImageUrl)" -ForegroundColor Gray
        } else {
            Write-Host "✗ " -NoNewline -ForegroundColor Red
            Write-Host "$($result.File): $($result.Error)" -ForegroundColor Red
        }
    }
}
}
}
Write-Progress -Activity "Generating unique images" -Completed

# Summary
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "              Summary                     " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$successCount = ($results | Where-Object { $_.Status -eq "Success" }).Count
$errorCount = ($results | Where-Object { $_.Status -eq "Error" }).Count

Write-Host "Total files processed: $totalFiles" -ForegroundColor White
Write-Host "Unique images generated: $successCount" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors encountered: $errorCount" -ForegroundColor Red
}
Write-Host "Duplicate prevention: $($usedImages.Count) unique hashes tracked" -ForegroundColor Yellow

# Export results to CSV for review
$csvPath = "image-generation-report.csv"
$results | Export-Csv -Path $csvPath -NoTypeInformation

Write-Host ""
Write-Host "Detailed report saved to: $csvPath" -ForegroundColor Cyan

# Show sample of generated images
Write-Host ""
Write-Host "Sample of generated unique images:" -ForegroundColor Yellow
$results | Select-Object -First 5 | ForEach-Object {
    if ($_.Status -eq "Success") {
        Write-Host "  • $($_.Title.Substring(0, [Math]::Min(50, $_.Title.Length)))..." -ForegroundColor Gray
        Write-Host "    Hash: $($_.Hash) | Image: $($_.ImageUrl)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Script completed!" -ForegroundColor Green

# Return statistics
return @{
    TotalFiles = $totalFiles
    SuccessCount = $successCount
    ErrorCount = $errorCount
    UniqueImages = $usedImages.Count
    Results = $results
}
