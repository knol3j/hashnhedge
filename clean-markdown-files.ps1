# PowerShell script to fix all special character encoding issues in markdown files
Write-Host "Starting comprehensive markdown file cleanup..." -ForegroundColor Green
Write-Host "This will fix special characters in all content files" -ForegroundColor Yellow

$contentPath = "C:\Users\gnul\hashnhedge\site\content"
$fixedCount = 0
$errorCount = 0
$logFile = "C:\Users\gnul\hashnhedge\cleanup-log.txt"

# Clear log file
"Markdown Cleanup Log - $(Get-Date)" | Out-File $logFile

# Get all markdown files
$files = Get-ChildItem -Path $contentPath -Filter "*.md" -Recurse
$totalFiles = $files.Count

Write-Host "`nFound $totalFiles markdown files to process" -ForegroundColor Cyan

foreach ($file in $files) {
    try {
        # Read file content as bytes to handle encoding issues
        $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
        
        # Convert to UTF8 string
        $content = [System.Text.Encoding]::UTF8.GetString($bytes)
        $originalContent = $content
        
        # Remove BOM if present
        if ($content.StartsWith([char]0xFEFF)) {
            $content = $content.Substring(1)
        }
        
        # Replace problematic characters using character codes
        # Smart quotes
        $content = $content -replace [char]0x2018, "'"  # Left single quote
        $content = $content -replace [char]0x2019, "'"  # Right single quote
        $content = $content -replace [char]0x201C, '"'  # Left double quote
        $content = $content -replace [char]0x201D, '"'  # Right double quote
        
        # Dashes
        $content = $content -replace [char]0x2013, '-'  # En dash
        $content = $content -replace [char]0x2014, '--' # Em dash
        
        # Ellipsis
        $content = $content -replace [char]0x2026, '...'
        
        # Non-breaking space
        $content = $content -replace [char]0x00A0, ' '
        
        # Additional cleanup for common UTF-8 encoding issues
        # These patterns often appear when UTF-8 is misinterpreted
        $replacements = @{
            'â€™' = "'"
            'â€œ' = '"'
            'â€' = '"'
            'â€"' = '--'
            'â€"' = '-'
            'â€¦' = '...'
            'Â' = ''
            'â' = "'"
            'âÂ' = ''
            '–' = '-'
            '—' = '--'
            ''' = "'"
            ''' = "'"
            '"' = '"'
            '"' = '"'
            '…' = '...'
        }
        
        foreach ($key in $replacements.Keys) {
            $content = $content -replace [regex]::Escape($key), $replacements[$key]
        }
        
        # Clean up any remaining non-ASCII characters in titles and slugs
        $lines = $content -split "`n"
        $newLines = @()
        
        foreach ($line in $lines) {
            if ($line -match '^(title:|slug:)') {
                # For title and slug lines, be more aggressive about cleaning
                $cleanLine = $line -replace '[^\x00-\x7F]', ''
                $cleanLine = $cleanLine -replace '\s+', ' '
                $newLines += $cleanLine
            } else {
                $newLines += $line
            }
        }
        
        $content = $newLines -join "`n"
        
        # Only write if content changed
        if ($content -ne $originalContent) {
            # Save the cleaned content
            [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
            $fixedCount++
            
            $logEntry = "FIXED: $($file.FullName)"
            Write-Host "  Fixed: $($file.Name)" -ForegroundColor Green
        } else {
            $logEntry = "UNCHANGED: $($file.FullName)"
        }
        
        $logEntry | Add-Content $logFile
        
    } catch {
        $errorCount++
        $errorMsg = "ERROR: $($file.FullName) - $($_.Exception.Message)"
        Write-Host "  Error: $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
        $errorMsg | Add-Content $logFile
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Cleanup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total files processed: $totalFiles"
Write-Host "Files fixed: $fixedCount" -ForegroundColor Green
Write-Host "Files unchanged: $($totalFiles - $fixedCount - $errorCount)" -ForegroundColor Yellow
Write-Host "Errors: $errorCount" -ForegroundColor Red
Write-Host "`nLog file saved to: $logFile" -ForegroundColor Cyan
