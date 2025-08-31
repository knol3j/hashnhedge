# Improved script to add images to Hash & Hedge posts
$SiteRoot = "C:\Users\gnul\hashnhedge\site"
$PostsPath = "$SiteRoot\content\posts"
$ImagesPath = "$SiteRoot\static\images\posts"

# Get all image files with full paths
$AllImages = Get-ChildItem -Path $ImagesPath -Include "*.png", "*.jpg", "*.jpeg", "*.webp"

Write-Host "Found $($AllImages.Count) total images" -ForegroundColor Green

# Function to find the best matching image for a post
function Get-BestImageForPost($PostTitle) {
    $title = $PostTitle.ToLower()
    
    # Keywords to image mappings - more specific matches
    $directMatches = @{
        "google" = "google-is-a-leader-and-positioned-furthest-in-vision-in-the.jpg"
        "bitcoin|btc" = "bitcoin-consolidation-below-123000-reflects-caution-rather-t.jpg"
        "crypto" = "crypto-stocks-tumble-as-investors-go-into-riskoff-mode.jpeg"
        "ethereum|eth" = "ethereum-captures-77-of-375-billion-inflows-while-bitcoin-tr.jpg"
        "microsoft|windows" = "microsoft-is-a-leader-in-the-2025-gartner-magic-quadrant-for.png"
        "aws|amazon" = "aws-named-as-a-leader-in-2025-gartner-magic-quadrant-for-str.png"
        "docker" = "docker-desktop-444-smarter-ai-modeling-platform-stability-an.png"
        "meta|facebook" = "meta-breaks-up-ai-lab-as-part-of-superintelligence-push.png"
        "apple|macos|ios" = "in-xcode-26-apple-shows-first-signs-of-offering-chatgpt-alte.jpg"
        "ai|artificial intelligence" = "how-realworld-businesses-are-transforming-with-ai-with-50-n.png"
        "security|hack|malware" = "powering-aidriven-security-with-the-open-cybersecurity-schem.png"
        "linux" = "tuning-linux-swap-for-kubernetes-a-deep-dive.png"
        "database|sqlite" = "show-hn-base-an-sqlite-database-editor-for-macos.png"
    }
    
    # Try direct keyword matches first
    foreach ($pattern in $directMatches.Keys) {
        if ($title -match $pattern) {
            $imageName = $directMatches[$pattern]
            if (Test-Path "$ImagesPath\$imageName") {
                return $imageName
            }
        }
    }
    
    # Fallback to title-based search
    $titleWords = $title -split '[-\s]+' | Where-Object { $_.Length -gt 3 }
    foreach ($word in $titleWords) {
        $matchingImage = $AllImages | Where-Object { $_.BaseName -like "*$word*" } | Select-Object -First 1
        if ($matchingImage) {
            return $matchingImage.Name
        }
    }
    
    # Final fallback - generic tech image
    return "systemobject.jpg"
}

# Function to update a post with an image
function Update-PostWithImage($PostPath, $ImageFileName) {
    $content = Get-Content $PostPath -Raw -Encoding UTF8
    
    # Skip if already has image
    if ($content -match 'image\s*:') {
        Write-Host "Already has image: $(Split-Path $PostPath -Leaf)" -ForegroundColor Yellow
        return $false
    }
    
    # Find front matter end
    $lines = $content -split "`r?`n"
    $frontMatterEndIndex = -1
    
    for ($i = 1; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -eq "---") {
            $frontMatterEndIndex = $i
            break
        }
    }
    
    if ($frontMatterEndIndex -eq -1) {
        Write-Host "Could not find front matter in: $(Split-Path $PostPath -Leaf)" -ForegroundColor Red
        return $false
    }
    
    # Insert image line before the closing ---
    $lines[$frontMatterEndIndex] = "image: `"/images/posts/$ImageFileName`"`n---"
    
    $newContent = $lines -join "`n"
    
    try {
        Set-Content -Path $PostPath -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "Updated $(Split-Path $PostPath -Parent | Split-Path -Leaf) with: $ImageFileName" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Failed to update $(Split-Path $PostPath -Leaf): $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "Starting improved image assignment..." -ForegroundColor Cyan

$updated = 0
$skipped = 0

# Get all posts and update them
Get-ChildItem -Path $PostsPath -Recurse -Filter "index.md" | ForEach-Object {
    $postPath = $_.FullName
    $content = Get-Content $postPath -Raw -Encoding UTF8
    
    if ($content -match 'title\s*:\s*"([^"]+)"') {
        $postTitle = $matches[1]
        Write-Host "`nProcessing: $postTitle"
        
        $bestImage = Get-BestImageForPost -PostTitle $postTitle
        
        if (Update-PostWithImage -PostPath $postPath -ImageFileName $bestImage) {
            $updated++
        } else {
            $skipped++
        }
    }
}

Write-Host "`n=== Final Summary ===" -ForegroundColor Cyan
Write-Host "Successfully updated: $updated posts" -ForegroundColor Green  
Write-Host "Skipped: $skipped posts" -ForegroundColor Yellow