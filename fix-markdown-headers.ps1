# Fix the fucked up double YAML headers in all markdown files
$mdFiles = Get-ChildItem -Path "C:\Users\gnul\hashnhedge\content\posts\*.md"
$fixedCount = 0

foreach ($file in $mdFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Check for double headers with BOM
    if ($content -match '^---[\s\S]*?---[\s\S]*?﻿---') {
        Write-Host "Fixing: $($file.Name)"
        
        # Remove the first header and BOM, keep the second (complete) header
        $content = $content -replace '^---[\s\S]*?---[\s\r\n]*﻿', ''
        
        # Write back without BOM
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.UTF8Encoding]::new($false))
        $fixedCount++
    }
}

Write-Host "`nFixed $fixedCount markdown files"
