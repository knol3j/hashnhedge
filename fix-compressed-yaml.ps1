Write-Host "Fixing files with compressed YAML format..." -ForegroundColor Green

$contentPath = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08"
$files = Get-ChildItem -Path $contentPath -Filter "index.md" -Recurse
$fixedCount = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check if file starts with BOM and YAML marker
        if ($content -match '^(?:\xEF\xBB\xBF)?---\s*\n') {
            # Get the first few lines
            $lines = $content -split "`n"
            
            # Check if line 2 has multiple YAML fields compressed together
            if ($lines.Count -gt 1 -and $lines[1] -match 'title:.*date:') {
                # This is a compressed YAML file
                $compressedYaml = $lines[1]
                
                # Find where the body starts (after second ---)
                $bodyStartIndex = -1
                for ($i = 2; $i -lt $lines.Count; $i++) {
                    if ($lines[$i] -match '^---') {
                        $bodyStartIndex = $i + 1
                        break
                    }
                }
                
                # Get body content
                $bodyContent = ""
                if ($bodyStartIndex -gt 0 -and $bodyStartIndex -lt $lines.Count) {
                    $bodyContent = ($lines[$bodyStartIndex..($lines.Count-1)] -join "`n").Trim()
                }
                
                # Parse the compressed YAML using spaces between fields
                $title = ""
                $date = ""
                $category = ""
                $summary = ""
                $slug = ""
                $sourceUrl = ""
                $seoTitle = ""
                
                # Split by double spaces which seem to separate fields
                $parts = $compressedYaml -split '  +'
                
                foreach ($part in $parts) {
                    if ($part -match 'title:\s*"([^"]+)"') { $title = $matches[1] }
                    if ($part -match 'date:\s*"([^"]+)"') { $date = $matches[1] }
                    if ($part -match 'category:\s*"([^"]+)"') { $category = $matches[1] }
                    if ($part -match 'summary:\s*"([^"]*)"') { $summary = $matches[1] }
                    if ($part -match 'slug:\s*"([^"]+)"') { $slug = $matches[1] }
                    if ($part -match 'source_urls:.*-\s*"([^"]+)"') { $sourceUrl = $matches[1] }
                    if ($part -match 'title:\s*"([^|]+)\|') { $seoTitle = $matches[1] + "| Hash n Hedge" }
                }
                
                # Clean up slug - remove extra spaces
                $slug = $slug -replace '\s+', '-'
                
                # Build proper YAML
                $newContent = @"
---
title: "$title"
date: "$date"
category: "$category"
summary: "$summary"
slug: "$slug"
source_urls:
  - "$sourceUrl"
seo:
  title: "$title | Hash n Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---
$bodyContent
"@
                
                # Save the file
                [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
                $fixedCount++
                Write-Host "  Fixed: $($file.Name)" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "  Error: $($file.Name) - $_" -ForegroundColor Red
    }
}

Write-Host "`nFixed $fixedCount files with compressed YAML" -ForegroundColor Cyan
