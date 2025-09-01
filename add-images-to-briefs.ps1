# Script to add image field to all brief markdown files based on their category

$briefsPath = "content\briefs"
$categoryImageMap = @{
    "Markets" = "/images/categories/markets.svg"
    "Tech" = "/images/categories/tech.svg"
    "Technology" = "/images/categories/tech.svg"
    "Default" = "/images/categories/default.svg"
}

# Get all markdown files in briefs directory
$files = Get-ChildItem -Path $briefsPath -Filter "*.md" -Recurse

$updatedCount = 0
$skippedCount = 0

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Check if image field already exists
    if ($content -match "^image:") {
        Write-Host "Skipping $($file.Name) - already has image" -ForegroundColor Yellow
        $skippedCount++
        continue
    }
    
    # Extract category from front matter
    if ($content -match "category:\s*(.+?)[\r\n]") {
        $category = $matches[1].Trim()
        
        # Get appropriate image based on category
        $image = $categoryImageMap[$category]
        if (-not $image) {
            $image = $categoryImageMap["Default"]
        }
        
        # Add image field after category in front matter
        $newContent = $content -replace "(category:\s*.+?[\r\n])", "`$1image: `"$image`"`r`n"
        
        # Write updated content back to file
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        
        Write-Host "Updated $($file.Name) with image for category: $category" -ForegroundColor Green
        $updatedCount++
    } else {
        Write-Host "Could not find category in $($file.Name)" -ForegroundColor Red
        $skippedCount++
    }
}

Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "Files updated: $updatedCount" -ForegroundColor Green
Write-Host "Files skipped: $skippedCount" -ForegroundColor Yellow
