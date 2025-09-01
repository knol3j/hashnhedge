Write-Host "Starting markdown file cleanup..." -ForegroundColor Green

$contentPath = "C:\Users\gnul\hashnhedge\site\content"
$fixedCount = 0
$errorCount = 0

# Get all markdown files
$files = Get-ChildItem -Path $contentPath -Filter "*.md" -Recurse
$totalFiles = $files.Count

Write-Host "Found $totalFiles markdown files to process" -ForegroundColor Cyan

foreach ($file in $files) {
    try {
        # Read file content
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Simple ASCII-only replacement approach
        # Remove or replace all non-ASCII characters
        $cleanContent = ""
        for ($i = 0; $i -lt $content.Length; $i++) {
            $char = $content[$i]
            $charCode = [int]$char
            
            # Map common Unicode characters to ASCII equivalents
            switch ($charCode) {
                # Single quotes
                {$_ -in 8216,8217,8218,8219,8220,8221,8222,8223} {
                    if ($charCode -in 8220,8221,8222,8223) {
                        $cleanContent += '"'
                    } else {
                        $cleanContent += "'"
                    }
                }
                # Dashes
                8211 { $cleanContent += '-' }  # En dash
                8212 { $cleanContent += '--' } # Em dash
                # Ellipsis
                8230 { $cleanContent += '...' }
                # Non-breaking space
                160 { $cleanContent += ' ' }
                # Regular ASCII characters
                {$_ -lt 128} { $cleanContent += $char }
                # Skip other non-ASCII characters
                default { }
            }
        }
        
        # Only write if content changed
        if ($cleanContent -ne $originalContent) {
            # Save the cleaned content
            Set-Content -Path $file.FullName -Value $cleanContent -Encoding UTF8 -NoNewline
            $fixedCount++
            Write-Host "  Fixed: $($file.Name)" -ForegroundColor Green
        }
        
    } catch {
        $errorCount++
        Write-Host "  Error: $($file.Name) - $_" -ForegroundColor Red
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "Total files: $totalFiles"
Write-Host "Fixed: $fixedCount" -ForegroundColor Green
Write-Host "Errors: $errorCount" -ForegroundColor Red
