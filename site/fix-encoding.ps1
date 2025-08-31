# Fix encoding issues in all markdown files
$ContentPath = "C:\Users\gnul\hashnhedge\site\content"

Write-Host "🔧 Fixing encoding issues in markdown files..." -ForegroundColor Yellow

$fixedCount = 0
$errorCount = 0

Get-ChildItem -Path $ContentPath -Recurse -Filter "*.md" | ForEach-Object {
    try {
        $file = $_
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check if content has problematic characters
        if ($content -match '[^\x00-\x7F]') {
            # Clean up common problematic characters
            $cleanContent = $content -replace 'â', '-'
            $cleanContent = $cleanContent -replace 'â€™', "'"
            $cleanContent = $cleanContent -replace 'â€œ', '"'
            $cleanContent = $cleanContent -replace 'â€', '"'
            $cleanContent = $cleanContent -replace '[^\u0000-\u007F]', '-'
            
            # Write back with clean UTF8
            Set-Content -Path $file.FullName -Value $cleanContent -Encoding UTF8
            
            Write-Host "✅ Fixed: $($file.Name)" -ForegroundColor Green
            $fixedCount++
        }
    }
    catch {
        Write-Host "❌ Error with: $($file.Name)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host "`n🎉 Encoding fix complete!" -ForegroundColor Magenta
Write-Host "Fixed: $fixedCount files" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "Errors: $errorCount files" -ForegroundColor Red
}