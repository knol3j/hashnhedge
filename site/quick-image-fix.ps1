# Quick Image Fix - Target posts with systemobject.jpg
$ContentPath = "C:\Users\gnul\hashnhedge\site\content\posts"
$ImagesPath = "C:\Users\gnul\hashnhedge\site\static\images\posts"

Write-Host "🎨 Quick Image Fix - Targeting systemobject.jpg posts" -ForegroundColor Yellow

# Get some good images to use
$GoodImages = @{
    "bitcoin" = "bitcoin-consolidation-below-123000-reflects-caution-rather-t.jpg"
    "crypto" = "crypto-stocks-tumble-as-investors-go-into-riskoff-mode.jpeg"
    "ethereum" = "ethereum-captures-77-of-375-billion-inflows-while-bitcoin-tr.jpg"
    "google" = "google-is-a-leader-and-positioned-furthest-in-vision-in-the.jpg"
    "microsoft" = "microsoft-is-a-leader-in-the-2025-gartner-magic-quadrant-for.png"
    "aws" = "aws-named-as-a-leader-in-2025-gartner-magic-quadrant-for-str.png"
    "ai" = "how-realworld-businesses-are-transforming-with-ai-with-50-n.png"
    "security" = "powering-aidriven-security-with-the-open-cybersecurity-schem.png"
    "docker" = "docker-desktop-444-smarter-ai-modeling-platform-stability-an.png"
    "meta" = "meta-breaks-up-ai-lab-as-part-of-superintelligence-push.png"
    "apple" = "in-xcode-26-apple-shows-first-signs-of-offering-chatgpt-alte.jpg"
    "tesla" = "nissan-announces-2026-leaf-pricing-starting-at-29990.jpg"
}

$fixed = 0

# Find posts with systemobject.jpg and fix them
Get-ChildItem -Path $ContentPath -Recurse -Filter "index.md" | Where-Object {
    (Get-Content $_.FullName -Raw) -like '*systemobject.jpg*'
} | ForEach-Object {
    $file = $_
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Extract title for matching
    $title = ""
    if ($content -match 'title:\s*"([^"]+)"') {
        $title = $matches[1].ToLower()
    }
    
    # Find best image based on title keywords
    $newImage = "systemobject.jpg"  # fallback
    
    foreach ($keyword in $GoodImages.Keys) {
        if ($title -like "*$keyword*") {
            $newImage = $GoodImages[$keyword]
            break
        }
    }
    
    # If still using fallback, pick based on other keywords
    if ($newImage -eq "systemobject.jpg") {
        if ($title -match "blockchain|defi|mining") { $newImage = $GoodImages["crypto"] }
        elseif ($title -match "hack|malware|breach|cyber") { $newImage = $GoodImages["security"] }
        elseif ($title -match "machine|learning|intelligence") { $newImage = $GoodImages["ai"] }
        elseif ($title -match "cloud|server|infrastructure") { $newImage = $GoodImages["aws"] }
        elseif ($title -match "android|chrome|search") { $newImage = $GoodImages["google"] }
        elseif ($title -match "windows|office|azure") { $newImage = $GoodImages["microsoft"] }
        elseif ($title -match "container|kubernetes|devops") { $newImage = $GoodImages["docker"] }
        elseif ($title -match "facebook|instagram|social") { $newImage = $GoodImages["meta"] }
        elseif ($title -match "ios|iphone|mac") { $newImage = $GoodImages["apple"] }
        else { $newImage = $GoodImages["crypto"] }  # Default to crypto for finance site
    }
    
    # Update the content
    $newContent = $content -replace 'systemobject\.jpg', $newImage
    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    
    Write-Host "✅ Fixed: $(Split-Path $file.Directory -Leaf) -> $newImage" -ForegroundColor Green
    $fixed++
}

Write-Host "`n🎉 Fixed $fixed posts with better images!" -ForegroundColor Magenta