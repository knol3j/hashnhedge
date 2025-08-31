# Simple encoding fix for markdown files
$ContentPath = "C:\Users\gnul\hashnhedge\site\content"

Write-Host "🔧 Fixing encoding issues..." -ForegroundColor Yellow

$fixedCount = 0

Get-ChildItem -Path $ContentPath -Recurse -Filter "*.md" | ForEach-Object {
    try {
        $file = $_
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Replace common problematic characters
        $cleanContent = $content
        $cleanContent = $cleanContent -replace 'â', '-'
        $cleanContent = $cleanContent -replace 'â€™', "'"
        $cleanContent = $cleanContent -replace 'â€œ', '"'
        $cleanContent = $cleanContent -replace 'â€', '"'
        $cleanContent = $cleanContent -replace 'Ã¢â‚¬â„¢', "'"
        
        # Only update if content changed
        if ($cleanContent -ne $content) {
            Set-Content -Path $file.FullName -Value $cleanContent -Encoding UTF8
            Write-Host "✅ Fixed: $($file.Name)" -ForegroundColor Green
            $fixedCount++
        }
    }
    catch {
        Write-Host "❌ Error with: $($file.Name)" -ForegroundColor Red
    }
}

Write-Host "`n🎉 Fixed $fixedCount files" -ForegroundColor Magenta