# Advanced Image Matcher for Hash & Hedge Posts
# This script intelligently matches posts to appropriate images based on content analysis

$SiteRoot = "C:\Users\gnul\hashnhedge\site"
$ContentPath = "$SiteRoot\content\posts"
$ImagesPath = "$SiteRoot\static\images\posts"

Write-Host "🎨 Advanced Image Matching System" -ForegroundColor Magenta
Write-Host "=================================" -ForegroundColor Magenta

# Get all available images with their metadata
$ImageDatabase = @{}
Get-ChildItem -Path $ImagesPath -Include "*.png", "*.jpg", "*.jpeg", "*.webp" | ForEach-Object {
    $imageName = $_.Name
    $baseName = $_.BaseName.ToLower()
    
    # Categorize images by keywords
    $keywords = @()
    
    # Extract keywords from filename
    $parts = $baseName -split '[-_\s]+'
    $keywords += $parts
    
    # Add contextual keywords based on patterns
    if ($baseName -match 'bitcoin|btc|crypto|blockchain') { $keywords += @('crypto', 'bitcoin', 'blockchain', 'cryptocurrency') }
    if ($baseName -match 'ethereum|eth') { $keywords += @('ethereum', 'eth', 'crypto', 'blockchain') }
    if ($baseName -match 'ai|artificial|intelligence|ml|machine') { $keywords += @('ai', 'artificial-intelligence', 'machine-learning', 'technology') }
    if ($baseName -match 'google|android|chrome') { $keywords += @('google', 'android', 'tech', 'technology') }
    if ($baseName -match 'microsoft|windows|azure') { $keywords += @('microsoft', 'windows', 'tech', 'technology') }
    if ($baseName -match 'apple|ios|macos|iphone') { $keywords += @('apple', 'ios', 'tech', 'technology') }
    if ($baseName -match 'meta|facebook|instagram') { $keywords += @('meta', 'facebook', 'social-media', 'tech') }
    if ($baseName -match 'aws|amazon|cloud') { $keywords += @('aws', 'amazon', 'cloud', 'technology') }
    if ($baseName -match 'docker|container|kubernetes') { $keywords += @('docker', 'containers', 'devops', 'technology') }
    if ($baseName -match 'security|hack|malware|cyber') { $keywords += @('security', 'cybersecurity', 'hacking', 'technology') }
    if ($baseName -match 'tesla|electric|ev') { $keywords += @('tesla', 'electric-vehicle', 'automotive', 'technology') }
    if ($baseName -match 'netflix|streaming|media') { $keywords += @('netflix', 'streaming', 'media', 'entertainment') }
    if ($baseName -match 'market|finance|trading|stock') { $keywords += @('markets', 'finance', 'trading', 'economics') }
    
    $ImageDatabase[$imageName] = @{
        'BaseName' = $baseName
        'Keywords' = $keywords | Sort-Object -Unique
        'FullPath' = $_.FullName
    }
}

Write-Host "📸 Loaded $(${ImageDatabase}.Count) images into database" -ForegroundColor Cyan

# Advanced matching function
function Find-BestImageMatch($PostTitle, $PostSlug, $PostContent = "") {
    $title = $PostTitle.ToLower()
    $slug = $PostSlug.ToLower() 
    $content = $PostContent.ToLower()
    $allText = "$title $slug $content"
    
    $bestMatch = $null
    $highestScore = 0
    
    foreach ($imageName in $ImageDatabase.Keys) {
        $imageData = $ImageDatabase[$imageName]
        $score = 0
        
        # Direct filename matching (highest priority)
        if ($imageData.BaseName -eq $slug) { $score += 100 }
        
        # Partial filename matching
        $slugWords = $slug -split '[-\s]+'
        foreach ($word in $slugWords) {
            if ($word.Length -gt 3 -and $imageData.BaseName -like "*$word*") {
                $score += 20
            }
        }
        
        # Keyword matching
        foreach ($keyword in $imageData.Keywords) {
            if ($allText -like "*$keyword*") {
                $score += 10
            }
        }
        
        # Title word matching
        $titleWords = $title -split '[-\s]+' | Where-Object { $_.Length -gt 3 }
        foreach ($word in $titleWords) {
            if ($imageData.BaseName -like "*$word*") {
                $score += 15
            }
        }
        
        # Update best match
        if ($score -gt $highestScore) {
            $highestScore = $score
            $bestMatch = $imageName
        }
    }
    
    # Fallback to category-appropriate defaults if no good match
    if ($highestScore -lt 10) {
        if ($allText -match 'crypto|bitcoin|ethereum|blockchain') {
            return "bitcoin-consolidation-below-123000-reflects-caution-rather-t.jpg"
        }
        if ($allText -match 'ai|artificial|intelligence|machine|learning') {
            return "how-realworld-businesses-are-transforming-with-ai-with-50-n.png"
        }
        if ($allText -match 'security|hack|malware|cyber') {
            return "powering-aidriven-security-with-the-open-cybersecurity-schem.png"
        }
        if ($allText -match 'google|android') {
            return "google-is-a-leader-and-positioned-furthest-in-vision-in-the.jpg"
        }
        if ($allText -match 'microsoft|windows') {
            return "microsoft-is-a-leader-in-the-2025-gartner-magic-quadrant-for.png"
        }
        if ($allText -match 'aws|amazon') {
            return "aws-named-as-a-leader-in-2025-gartner-magic-quadrant-for-str.png"
        }
        
        # Final fallback
        return "systemobject.jpg"
    }
    
    return $bestMatch
}

# Process all posts and update images
$updatedCount = 0
$skippedCount = 0
$processedCount = 0

Write-Host "`n🔄 Processing posts and updating images..." -ForegroundColor Blue

Get-ChildItem -Path $ContentPath -Recurse -Filter "index.md" | ForEach-Object {
    $postFile = $_
    $processedCount++
    
    try {
        $content = Get-Content $postFile.FullName -Raw -Encoding UTF8
        
        # Extract current metadata
        if ($content -match '^---\s*\n(.*?)\n---\s*\n(.*)$') {
            $frontMatter = $matches[1]
            $bodyContent = $matches[2]
            
            # Extract title
            $title = ""
            if ($frontMatter -match 'title:\s*"([^"]+)"') {
                $title = $matches[1]
            }
            
            # Extract slug
            $slug = ""
            if ($frontMatter -match 'slug:\s*"([^"]+)"') {
                $slug = $matches[1]
            }
            
            # Skip if no title found
            if (!$title) {
                Write-Host "⚠️  No title found in: $($postFile.Directory.Name)" -ForegroundColor Yellow
                $skippedCount++
                return
            }
            
            # Find best matching image
            $bestImage = Find-BestImageMatch -PostTitle $title -PostSlug $slug -PostContent $bodyContent
            $imagePath = "/images/posts/$bestImage"
            
            # Check if image needs updating (not already the best match)
            $currentImage = ""
            if ($frontMatter -match 'image:\s*"([^"]+)"') {
                $currentImage = $matches[1]
            }
            
            if ($currentImage -ne $imagePath) {
                # Update the front matter with new image
                if ($frontMatter -match 'image:\s*"[^"]+"') {
                    $newFrontMatter = $frontMatter -replace 'image:\s*"[^"]+"', "image: `"$imagePath`""
                } else {
                    # Add image line if it doesn't exist
                    $newFrontMatter = $frontMatter + "`nimage: `"$imagePath`""
                }
                
                $newContent = "---`n$newFrontMatter`n---`n$bodyContent"
                Set-Content -Path $postFile.FullName -Value $newContent -Encoding UTF8
                
                Write-Host "✅ Updated: $title -> $bestImage" -ForegroundColor Green
                $updatedCount++
            } else {
                Write-Host "⚪ Already optimal: $title" -ForegroundColor Gray
                $skippedCount++
            }
        }
    }
    catch {
        Write-Host "❌ Error processing: $($postFile.Directory.Name) - $($_.Exception.Message)" -ForegroundColor Red
        $skippedCount++
    }
    
    # Progress indicator
    if ($processedCount % 50 -eq 0) {
        Write-Host "📊 Processed $processedCount posts..." -ForegroundColor Cyan
    }
}

Write-Host "`n🎉 Image Matching Complete!" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta
Write-Host "✅ Updated: $updatedCount posts with better images" -ForegroundColor Green
Write-Host "⚪ Optimal: $skippedCount posts (no changes needed)" -ForegroundColor Gray
Write-Host "📊 Total processed: $processedCount posts" -ForegroundColor Cyan

Write-Host "`n🔄 Rebuilding site..." -ForegroundColor Blue
hugo --quiet
Write-Host "✅ Site rebuilt with optimized images!" -ForegroundColor Green