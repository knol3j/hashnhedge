# Add images to Hash & Hedge posts
# This script matches posts with appropriate images and updates the front matter

$SiteRoot = "C:\Users\gnul\hashnhedge\site"
$PostsPath = "$SiteRoot\content\posts"
$ImagesPath = "$SiteRoot\static\images\posts"

# Get all available images
$ImageFiles = Get-ChildItem -Path $ImagesPath -Include "*.png", "*.jpg", "*.jpeg", "*.webp" -Recurse
$AvailableImages = $ImageFiles | Select-Object -ExpandProperty Name

# Function to find best matching image for a post title
function Find-BestImage($PostTitle, $PostContent = "") {
    $title = $PostTitle.ToLower()
    $content = $PostContent.ToLower()
    
    # Direct keyword matches for common topics
    $keywords = @{
        "bitcoin|btc|blockchain|crypto|ethereum|eth|mining|defi" = @("bitcoin", "btc", "eth", "crypto", "blockchain", "ethereum", "defi")
        "google|android|chrome" = @("google", "android", "chrome")
        "microsoft|windows|azure" = @("microsoft", "windows", "azure")
        "aws|amazon" = @("aws", "amazon")
        "docker|container" = @("docker", "container")
        "security|hack|malware|vulnerability" = @("security", "hack", "malware", "vulnerability", "breach")
        "ai|artificial intelligence|machine learning|ml" = @("ai", "ml", "machine", "artificial")
        "meta|facebook|instagram" = @("meta", "facebook", "instagram")
        "apple|ios|macos" = @("apple", "ios", "macos")
        "netflix|streaming" = @("netflix", "streaming")
        "tesla|ev|electric" = @("tesla", "electric", "vehicle")
    }
    
    # Try to find exact or close matches
    foreach ($pattern in $keywords.Keys) {
        if ($title -match $pattern -or $content -match $pattern) {
            foreach ($keyword in $keywords[$pattern]) {
                $matchingImages = $AvailableImages | Where-Object { $_ -like "*$keyword*" }
                if ($matchingImages) {
                    return $matchingImages[0]  # Return first match
                }
            }
        }
    }
    
    # Fallback to partial title matches
    $titleWords = $title -split '[-\s]+' | Where-Object { $_.Length -gt 3 }
    foreach ($word in $titleWords) {
        $matchingImages = $AvailableImages | Where-Object { $_ -like "*$word*" }
        if ($matchingImages) {
            return $matchingImages[0]
        }
    }
    
    # Default fallback images by category
    $defaultImages = @{
        "Markets" = "btc-and-eth-aths"
        "Tech" = "systemobject"
        "Security" = "security"
        "AI" = "ai"
        "Crypto" = "bitcoin-privacy-the-effects-of-surveillance-on-society"
    }
    
    return $null
}

# Function to update post with image
function Update-PostWithImage($PostPath, $ImageName) {
    $content = Get-Content $PostPath -Raw -Encoding UTF8
    
    # Check if image already exists in front matter
    if ($content -match 'image\s*:' -or $content -match 'featured_image\s*:') {
        Write-Host "Image already exists in $PostPath" -ForegroundColor Yellow
        return $false
    }
    
    # Find the end of the front matter
    $frontMatterEnd = $content.IndexOf('---', 3)
    if ($frontMatterEnd -eq -1) {
        Write-Host "Could not find front matter end in $PostPath" -ForegroundColor Red
        return $false
    }
    
    # Insert image reference before the closing ---
    $beforeClosing = $content.Substring(0, $frontMatterEnd)
    $afterClosing = $content.Substring($frontMatterEnd)
    
    $imageEntry = "image: `"/images/posts/$ImageName.png`"`n"
    $extension = ($ImageName -split '\.')[-1]
    if ($extension) {
        $imageEntry = "image: `"/images/posts/$ImageName`"`n"
    } else {
        # Try to find the actual file extension
        $imageFile = Get-ChildItem -Path $ImagesPath -Name "$ImageName.*" | Select-Object -First 1
        if ($imageFile) {
            $imageEntry = "image: `"/images/posts/$imageFile`"`n"
        }
    }
    
    $newContent = $beforeClosing + $imageEntry + $afterClosing
    
    try {
        Set-Content -Path $PostPath -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "Updated $PostPath with image: $ImageName" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Failed to update $PostPath : $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "Starting image assignment for Hash & Hedge posts..." -ForegroundColor Cyan
Write-Host "Found $($AvailableImages.Count) available images" -ForegroundColor Cyan

$updatedCount = 0
$skippedCount = 0

# Process all posts
Get-ChildItem -Path $PostsPath -Recurse -Filter "index.md" | ForEach-Object {
    $postPath = $_.FullName
    $postContent = Get-Content $postPath -Raw -Encoding UTF8
    
    # Extract title from front matter
    if ($postContent -match 'title\s*:\s*"([^"]+)"') {
        $postTitle = $matches[1]
        Write-Host "`nProcessing: $postTitle" -ForegroundColor White
        
        # Find best matching image
        $bestImage = Find-BestImage -PostTitle $postTitle -PostContent $postContent
        
        if ($bestImage) {
            if (Update-PostWithImage -PostPath $postPath -ImageName $bestImage) {
                $updatedCount++
            } else {
                $skippedCount++
            }
        } else {
            Write-Host "No suitable image found for: $postTitle" -ForegroundColor Yellow
            $skippedCount++
        }
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Posts updated with images: $updatedCount" -ForegroundColor Green
Write-Host "Posts skipped: $skippedCount" -ForegroundColor Yellow
Write-Host "Script completed!" -ForegroundColor Cyan