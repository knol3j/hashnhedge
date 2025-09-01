# Final cleanup script for remaining YAML issues
Write-Host "Final cleanup for remaining YAML issues..." -ForegroundColor Green

$problemFiles = @(
    "C:\Users\gnul\hashnhedge\site\content\posts\2025\08\jensen-huang-says-nvidia-is-in-talks-with-china-over-h20-sec\index.md"
)

# Find all files that might still have issues
$allFiles = Get-ChildItem -Path "C:\Users\gnul\hashnhedge\site\content\posts\2025\08" -Filter "index.md" -Recurse

foreach ($file in $allFiles) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check if file has YAML front matter
        if ($content -match '^---') {
            # Extract the YAML front matter
            $yamlMatch = $content -match '(?s)^---(.+?)---'
            
            if ($yamlMatch) {
                $yamlContent = $matches[1]
                $bodyContent = $content.Substring($content.IndexOf('---', 3) + 3)
                
                # Clean the YAML content more aggressively
                # Remove all non-ASCII characters from YAML
                $cleanYaml = ""
                for ($i = 0; $i -lt $yamlContent.Length; $i++) {
                    $char = $yamlContent[$i]
                    $charCode = [int]$char
                    
                    if ($charCode -lt 128) {
                        # Keep ASCII characters
                        $cleanYaml += $char
                    } elseif ($charCode -eq 8217 -or $charCode -eq 8216) {
                        # Single quotes
                        $cleanYaml += "'"
                    } elseif ($charCode -eq 8220 -or $charCode -eq 8221) {
                        # Double quotes
                        $cleanYaml += '"'
                    } elseif ($charCode -eq 8211) {
                        # En dash
                        $cleanYaml += '-'
                    } elseif ($charCode -eq 8212) {
                        # Em dash
                        $cleanYaml += '--'
                    } else {
                        # Skip other non-ASCII
                        $cleanYaml += ' '
                    }
                }
                
                # Reconstruct the file
                $newContent = "---" + $cleanYaml + "---" + $bodyContent
                
                # Save if changed
                if ($newContent -ne $content) {
                    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
                    Write-Host "Fixed: $($file.Name)" -ForegroundColor Green
                }
            }
        }
    } catch {
        Write-Host "Error processing: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "Final cleanup complete!" -ForegroundColor Green
