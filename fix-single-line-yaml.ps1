Write-Host "Fixing YAML formatting issues (fields on single line)..." -ForegroundColor Green

$contentPath = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08"
$files = Get-ChildItem -Path $contentPath -Filter "index.md" -Recurse
$fixedCount = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check if the file has improperly formatted YAML (all on one line)
        if ($content -match '^---\s*\n(.+?)---') {
            $yamlSection = $matches[1]
            
            # Check if YAML has multiple fields on the same line
            if ($yamlSection -match 'title:.*date:' -or $yamlSection -match 'date:.*category:') {
                # This YAML is all on one line, need to fix it
                
                # Extract the body content
                $bodyStart = $content.IndexOf('---', 4) + 3
                $bodyContent = $content.Substring($bodyStart).Trim()
                
                # Try to parse the single-line YAML
                $yamlLine = $yamlSection.Trim()
                
                # Extract fields using regex
                $title = if ($yamlLine -match 'title:\s*"([^"]+)"') { $matches[1] } else { "" }
                $date = if ($yamlLine -match 'date:\s*"([^"]+)"') { $matches[1] } else { "" }
                $category = if ($yamlLine -match 'category:\s*"([^"]+)"') { $matches[1] } else { "" }
                $summary = if ($yamlLine -match 'summary:\s*"([^"]*)"') { $matches[1] } else { "" }
                $slug = if ($yamlLine -match 'slug:\s*"([^"]+)"') { $matches[1] } else { "" }
                
                # Extract source URLs
                $sourceUrls = @()
                if ($yamlLine -match 'source_urls:\s*-\s*"([^"]+)"') {
                    $sourceUrls += $matches[1]
                }
                
                # Extract SEO fields
                $seoTitle = if ($yamlLine -match 'seo:.*title:\s*"([^"]+)"') { $matches[1] } else { "" }
                
                # Build proper YAML
                $newYaml = @"
---
title: "$title"
date: "$date"
category: "$category"
summary: "$summary"
slug: "$slug"
source_urls:
  - "$($sourceUrls[0])"
seo:
  title: "$seoTitle"
  description: ""
  keywords: ["news", "markets", "brief"]
---
"@
                
                # Combine with body
                $newContent = $newYaml + "`n" + $bodyContent
                
                # Save the file
                Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
                $fixedCount++
                Write-Host "  Fixed: $($file.Name)" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "  Error: $($file.Name) - $_" -ForegroundColor Red
    }
}

Write-Host "`nFixed $fixedCount files with single-line YAML issues" -ForegroundColor Cyan
