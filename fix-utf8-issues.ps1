# Script to find and remove/fix files with UTF-8 issues

$briefsPath = "content\briefs"
$badFiles = @()

Get-ChildItem -Path $briefsPath -Filter "*.md" -Recurse | ForEach-Object {
    try {
        $content = Get-Content $_.FullName -Raw -Encoding UTF8 -ErrorAction Stop
        # Try to parse just the first line to check for UTF-8 issues
        if ($content -match "^[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]") {
            Write-Host "Bad characters in: $($_.FullName)" -ForegroundColor Red
            $badFiles += $_.FullName
        }
    } catch {
        Write-Host "UTF-8 error in: $($_.FullName)" -ForegroundColor Red
        $badFiles += $_.FullName
    }
}

Write-Host "`nFound $($badFiles.Count) problematic files" -ForegroundColor Yellow

if ($badFiles.Count -gt 0) {
    Write-Host "Removing problematic files..." -ForegroundColor Cyan
    foreach ($file in $badFiles) {
        Remove-Item $file -Force
        Write-Host "Removed: $file" -ForegroundColor Green
    }
}
