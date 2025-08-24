Write-Host "Comprehensive YAML fix for all remaining issues..." -ForegroundColor Green

$contentPath = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08"
$files = Get-ChildItem -Path $contentPath -Filter "index.md" -Recurse
$fixedCount = 0
$errorCount = 0

foreach ($file in $files) {
    try {
        # Read raw bytes to handle encoding issues
        $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
        $content = [System.Text.Encoding]::UTF8.GetString($bytes)
        
        # Remove BOM if present
        if ($content.StartsWith([char]0xFEFF)) {
            $content = $content.Substring(1)
        }
        
        # Extract YAML front matter and body separately
        if ($content -match '(?s)^---\s*\r?\n(.+?)\r?\n---\s*\r?\n(.*)$') {
            $yamlContent = $matches[1]
            $bodyContent = $matches[2]
            
            # Clean YAML by removing ALL non-ASCII characters
            $cleanYaml = ""
            for ($i = 0; $i -lt $yamlContent.Length; $i++) {
                $char = $yamlContent[$i]
                $ascii = [int]$char
                
                if ($ascii -lt 32 -and $ascii -ne 9 -and $ascii -ne 10 -and $ascii -ne 13) {
                    # Skip control characters except tab, newline, carriage return
                    continue
                } elseif ($ascii -ge 32 -and $ascii -le 126) {
                    # Keep printable ASCII
                    $cleanYaml += $char
                } elseif ($ascii -eq 8216 -or $ascii -eq 8217) {
                    # Smart single quotes
                    $cleanYaml += "'"
                } elseif ($ascii -eq 8220 -or $ascii -eq 8221) {
                    # Smart double quotes  
                    $cleanYaml += '"'
                } elseif ($ascii -eq 8211) {
                    # En dash
                    $cleanYaml += '-'
                } elseif ($ascii -eq 8212) {
                    # Em dash
                    $cleanYaml += '--'
                } elseif ($ascii -eq 160) {
                    # Non-breaking space
                    $cleanYaml += ' '
                } else {
                    # Replace any other non-ASCII with space
                    $cleanYaml += ' '
                }
            }
            
            # Rebuild the file
            $newContent = "---`n$cleanYaml`n---`n$bodyContent"
            
            # Write the file
            [System.IO.File]::WriteAllText($file.FullName, $newContent, [System.Text.Encoding]::UTF8)
            $fixedCount++
            Write-Host "  Fixed: $($file.Name)" -ForegroundColor Green
        }
    } catch {
        $errorCount++
        Write-Host "  Error: $($file.Name) - $_" -ForegroundColor Red
    }
}

Write-Host "`nFixed $fixedCount files, $errorCount errors" -ForegroundColor Cyan
