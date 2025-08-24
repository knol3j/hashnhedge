#!/usr/bin/env pwsh

# Script to fix YAML front matter issues in Hugo content files
Write-Host "Fixing YAML issues in Hugo content files..."

$siteRoot = "C:\Users\gnul\hashnhedge\site\content"
$files = Get-ChildItem -Path $siteRoot -Name "*.md" -Recurse

$fixedCount = 0

foreach ($file in $files) {
    $fullPath = Join-Path $siteRoot $file
    
    try {
        $content = Get-Content $fullPath -Encoding UTF8 -Raw
        $originalContent = $content
        
        # Fix the most common issue: unescaped quotes in title fields
        # Match pattern: title: "text with "quoted" text"
        if ($content -match 'title:\s*"([^"]*)"([^"]*)"([^"]*)"') {
            $content = $content -replace 'title:\s*"([^"]*)"([^"]*)"([^"]*)"', 'title: "$1`'$2`'$3"'
            Write-Host "Fixed quotes in: $file"
        }
        
        # Also check SEO titles
        if ($content -match '\s+title:\s*"([^"]*)"([^"]*)"([^"]*)"') {
            $content = $content -replace '(\s+title:\s*)"([^"]*)"([^"]*)"([^"]*)"', '$1"$2`'$3`'$4"'
            Write-Host "Fixed SEO quotes in: $file"
        }
        
        # Fix problematic em-dash characters that appear as â
        if ($content -match '[â]') {
            $content = $content -replace 'â', '-'
            Write-Host "Fixed em-dash in: $file"
        }
        
        # Check if we made any changes
        if ($content -ne $originalContent) {
            Set-Content $fullPath -Value $content -Encoding UTF8
            $fixedCount++
        }
    }
    catch {
        Write-Host "Error processing $file : $($_.Exception.Message)"
    }
}

Write-Host "Fixed $fixedCount files total."
Write-Host "Testing Hugo build..."

# Test the build
Set-Location "C:\Users\gnul\hashnhedge\site"
$buildResult = & hugo --gc --minify 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Hugo build completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Build failed. Here are the first few errors:" -ForegroundColor Red
    $buildResult | Select-Object -First 10 | ForEach-Object { Write-Host $_ }
}
