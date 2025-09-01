# Advanced Unique Image Generation System for Hash & Hedge
# This script generates unique SVG images for each article based on content analysis

param(
    [string]$ContentPath = "content",
    [string]$OutputPath = "static/images/generated",
    [switch]$Force = $false
)

# Ensure output directory exists
if (!(Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
}

# Color palettes for different topics
$colorPalettes = @{
    crypto = @("#f7931a", "#627eea", "#26d07c", "#3c3c3d", "#1e1e1e")
    bitcoin = @("#f2a900", "#ff9500", "#4d4d4d", "#1a1a1a", "#333333")
    ethereum = @("#627eea", "#8198ee", "#3c3c3d", "#454a75", "#282c34")
    defi = @("#26d07c", "#1abc9c", "#2ecc71", "#27ae60", "#16a085")
    trading = @("#e74c3c", "#c0392b", "#3498db", "#2980b9", "#34495e")
    finance = @("#2c3e50", "#34495e", "#3498db", "#2980b9", "#1abc9c")
    technology = @("#9b59b6", "#8e44ad", "#3498db", "#2980b9", "#34495e")
    ai = @("#00d4ff", "#0099ff", "#6c5ce7", "#a29bfe", "#74b9ff")
    security = @("#e74c3c", "#c0392b", "#95a5a6", "#7f8c8d", "#2c3e50")
    market = @("#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50")
    default = @("#667eea", "#764ba2", "#f093fb", "#709fb0", "#726a95")
}

# Icon patterns for different topics
$iconPatterns = @{
    crypto = @("M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5")
    bitcoin = @("M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z")
    chart = @("M3 13h2v7H3zm4-8h2v15H7zm4 5h2v10h-2zm4-3h2v13h-2zm4 6h2v7h-2z")
    shield = @("M12 2L4 7v5c0 4.97 3.47 9.62 8 10.75 4.53-1.13 8-5.78 8-10.75V7l-8-5z")
    network = @("M12 2C6.48 2 2 6.48 2 12c0 5.52 4.48 10 10 10s10-4.48 10-10c0-5.52-4.48-10-10-10zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z")
    code = @("M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z")
    data = @("M12 2L2 7v10c0 5.52 4.48 10 10 10s10-4.48 10-10V7l-10-5z")
    gear = @("M12 15.5A3.5 3.5 0 0 1 8.5 12 3.5 3.5 0 0 1 12 8.5a3.5 3.5 0 0 1 3.5 3.5 3.5 3.5 0 0 1-3.5 3.5z")
}

function Get-TopicFromContent($content, $title) {
    $lowerContent = ($content + " " + $title).ToLower()
    
    # Check for specific topics
    if ($lowerContent -match "bitcoin|btc|satoshi") { return "bitcoin" }
    if ($lowerContent -match "ethereum|eth|smart contract|solidity") { return "ethereum" }
    if ($lowerContent -match "defi|decentralized finance|yield|liquidity|swap") { return "defi" }
    if ($lowerContent -match "trading|trader|exchange|market|price|chart") { return "trading" }
    if ($lowerContent -match "ai|artificial intelligence|machine learning|llm|gpt") { return "ai" }
    if ($lowerContent -match "security|hack|vulnerability|breach|attack") { return "security" }
    if ($lowerContent -match "crypto|blockchain|token|nft|web3") { return "crypto" }
    if ($lowerContent -match "finance|money|investment|bank|fund") { return "finance" }
    if ($lowerContent -match "technology|tech|software|hardware|computer") { return "technology" }
    if ($lowerContent -match "market|stock|trading|economy") { return "market" }
    
    return "default"
}

function Get-HashFromString($string) {
    $md5 = [System.Security.Cryptography.MD5]::Create()
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($string)
    $hash = $md5.ComputeHash($bytes)
    return [BitConverter]::ToString($hash).Replace("-", "").ToLower()
}

function Generate-UniquePattern($seed) {
    $patterns = @()
    $hash = Get-HashFromString $seed
    $random = [System.Random]::new($hash.GetHashCode())
    
    # Generate geometric patterns
    for ($i = 0; $i -lt 5; $i++) {
        $x = $random.Next(50, 450)
        $y = $random.Next(50, 250)
        $size = $random.Next(20, 80)
        $opacity = [math]::Round($random.NextDouble() * 0.3 + 0.1, 2)
        
        $shapeType = $random.Next(0, 4)
        switch ($shapeType) {
            0 { # Circle
                $patterns += "<circle cx='$x' cy='$y' r='$size' opacity='$opacity'/>"
            }
            1 { # Rectangle
                $patterns += "<rect x='$($x - $size/2)' y='$($y - $size/2)' width='$size' height='$size' rx='5' opacity='$opacity'/>"
            }
            2 { # Triangle
                $points = "$x,$($y - $size) $($x - $size),$($y + $size) $($x + $size),$($y + $size)"
                $patterns += "<polygon points='$points' opacity='$opacity'/>"
            }
            3 { # Hexagon
                $angle = 0
                $points = @()
                for ($j = 0; $j -lt 6; $j++) {
                    $px = $x + $size * [math]::Cos($angle)
                    $py = $y + $size * [math]::Sin($angle)
                    $points += "$px,$py"
                    $angle += [math]::PI / 3
                }
                $pointsStr = $points -join " "
                $patterns += "<polygon points='$pointsStr' opacity='$opacity'/>"
            }
        }
    }
    
    return $patterns -join "`n"
}

function Generate-WavePattern($seed, $color) {
    $hash = Get-HashFromString $seed
    $random = [System.Random]::new($hash.GetHashCode())
    
    $amplitude = $random.Next(20, 50)
    $frequency = $random.NextDouble() * 0.02 + 0.01
    $phase = $random.NextDouble() * [math]::PI * 2
    
    $path = "M0,150 "
    for ($x = 0; $x -le 500; $x += 10) {
        $y = 150 + $amplitude * [math]::Sin($frequency * $x + $phase)
        $path += "L$x,$y "
    }
    $path += "L500,300 L0,300 Z"
    
    return "<path d='$path' fill='$color' opacity='0.3'/>"
}

function Create-UniqueSVG($title, $content, $outputFile) {
    $topic = Get-TopicFromContent $content $title
    $colors = $colorPalettes[$topic]
    if (-not $colors) { $colors = $colorPalettes["default"] }
    
    # Create unique seed for this article
    $seed = "$title-$content"
    $hash = Get-HashFromString $seed
    $random = [System.Random]::new($hash.GetHashCode())
    
    # Select colors
    $primaryColor = $colors[$random.Next(0, $colors.Count)]
    $secondaryColor = $colors[$random.Next(0, $colors.Count)]
    $accentColor = $colors[$random.Next(0, $colors.Count)]
    
    # Generate gradient
    $gradientId = "grad-$hash"
    $gradient = @"
    <defs>
        <linearGradient id='$gradientId' x1='0%' y1='0%' x2='100%' y2='100%'>
            <stop offset='0%' style='stop-color:$primaryColor;stop-opacity:1' />
            <stop offset='50%' style='stop-color:$secondaryColor;stop-opacity:1' />
            <stop offset='100%' style='stop-color:$accentColor;stop-opacity:1' />
        </linearGradient>
        <filter id='blur'>
            <feGaussianBlur in='SourceGraphic' stdDeviation='0.5' />
        </filter>
    </defs>
"@
    
    # Generate unique patterns
    $patterns = Generate-UniquePattern $seed
    $wave1 = Generate-WavePattern "${seed}-1" $primaryColor
    $wave2 = Generate-WavePattern "${seed}-2" $secondaryColor
    
    # Add topic-specific icon if available
    $icon = ""
    if ($iconPatterns.ContainsKey($topic)) {
        $iconPath = $iconPatterns[$topic]
        $iconX = 225
        $iconY = 125
        $icon = "<g transform='translate($iconX, $iconY) scale(3)'><path d='$iconPath' fill='white' opacity='0.8'/></g>"
    }
    
    # Generate abstract shapes
    $shapes = @()
    for ($i = 0; $i -lt 3; $i++) {
        $cx = $random.Next(100, 400)
        $cy = $random.Next(50, 250)
        $r = $random.Next(30, 100)
        $opacity = [math]::Round($random.NextDouble() * 0.3 + 0.2, 2)
        $shapes += "<circle cx='$cx' cy='$cy' r='$r' fill='url(#$gradientId)' opacity='$opacity' filter='url(#blur)'/>"
    }
    $shapesStr = $shapes -join "`n"
    
    # Create the SVG
    $svg = @"
<svg width='500' height='300' xmlns='http://www.w3.org/2000/svg'>
    $gradient
    <!-- Background -->
    <rect width='500' height='300' fill='url(#$gradientId)' opacity='0.1'/>
    
    <!-- Wave patterns -->
    $wave1
    $wave2
    
    <!-- Abstract shapes -->
    $shapesStr
    
    <!-- Unique patterns -->
    <g fill='url(#$gradientId)'>
        $patterns
    </g>
    
    <!-- Icon overlay -->
    $icon
    
    <!-- Title text background -->
    <rect x='10' y='240' width='480' height='50' fill='black' opacity='0.7' rx='5'/>
    
    <!-- Title text -->
    <text x='250' y='270' font-family='Arial, sans-serif' font-size='16' fill='white' text-anchor='middle' font-weight='bold'>
        $($title.Substring(0, [Math]::Min($title.Length, 50)))
    </text>
</svg>
"@
    
    # Save the SVG
    $svg | Out-File -FilePath $outputFile -Encoding UTF8
    return $outputFile
}

# Process all markdown files
$files = Get-ChildItem -Path $ContentPath -Recurse -Filter "*.md"
$processedCount = 0
$updatedCount = 0

foreach ($file in $files) {
    $processedCount++
    Write-Progress -Activity "Generating unique images" -Status "Processing $($file.Name)" -PercentComplete (($processedCount / $files.Count) * 100)
    
    # Read the file content
    $content = Get-Content $file.FullName -Raw
    
    # Extract front matter
    if ($content -match '(?s)^---(.+?)---') {
        $frontMatter = $matches[1]
        $restContent = $content.Substring($matches[0].Length)
        
        # Extract title
        if ($frontMatter -match 'title:\s*"?([^"\n]+)"?' -or $frontMatter -match "title:\s*'?([^'\n]+)'?") {
            $title = $matches[1].Trim('"', "'")
            
            # Generate image path
            $fullContentPath = (Get-Item $ContentPath).FullName
            $relativePath = $file.FullName.Replace($fullContentPath, "").TrimStart("\")
            $imageName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
            $imageDir = [System.IO.Path]::GetDirectoryName($relativePath)
            if ($imageDir) {
                $imageDir = $imageDir.Replace("\", "/")
                $imageOutputDir = Join-Path $OutputPath $imageDir
            } else {
                $imageOutputDir = $OutputPath
            }
            
            if (!(Test-Path $imageOutputDir)) {
                New-Item -ItemType Directory -Path $imageOutputDir -Force | Out-Null
            }
            
            $imageFile = Join-Path $imageOutputDir "$imageName.svg"
            $imageUrl = "/images/generated/$imageDir/$imageName.svg".Replace("\", "/").Replace("//", "/")
            
            # Check if image already exists or if Force flag is set
            $shouldGenerate = $Force -or !(Test-Path $imageFile)
            
            # Check if the post already has a unique generated image
            if (!$shouldGenerate -and ($frontMatter -match 'image:\s*.*/images/generated/')) {
                continue # Skip if already has a generated image and not forcing
            }
            
            if ($shouldGenerate -or !($frontMatter -match 'image:\s*.*/images/generated/')) {
                # Generate the unique image
                Create-UniqueSVG $title $restContent $imageFile | Out-Null
                
                # Update the front matter with the new image
                if ($frontMatter -match 'image:\s*.+') {
                    $newFrontMatter = $frontMatter -replace 'image:\s*.+', "image: `"$imageUrl`""
                } else {
                    # Add image field if it doesn't exist
                    $newFrontMatter = $frontMatter.TrimEnd() + "`nimage: `"$imageUrl`"`n"
                }
                
                # Save the updated content
                $newContent = "---$newFrontMatter---$restContent"
                $newContent | Out-File -FilePath $file.FullName -Encoding UTF8 -NoNewline
                $updatedCount++
                
                Write-Host "Generated unique image for: $title" -ForegroundColor Green
            }
        }
    }
}

Write-Progress -Activity "Generating unique images" -Completed
Write-Host "`nImage generation complete!" -ForegroundColor Cyan
Write-Host "Total files processed: $processedCount" -ForegroundColor Yellow
Write-Host "Images generated/updated: $updatedCount" -ForegroundColor Green
Write-Host "Images are saved in: $OutputPath" -ForegroundColor Blue
