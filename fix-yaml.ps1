# PowerShell script to fix YAML issues in markdown files
$path = "C:\Users\gnul\hashnhedge\site\content"
$files = Get-ChildItem -Path $path -Filter "*.md" -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Replace problematic characters
    $content = $content -replace 'â€™', "'"
    $content = $content -replace 'â€œ', '"'
    $content = $content -replace 'â€', '"'
    $content = $content -replace 'â€"', '-'
    $content = $content -replace 'â€"', '--'
    $content = $content -replace 'â€¦', '...'
    $content = $content -replace 'â', "'"
    $content = $content -replace '"', '"'
    $content = $content -replace '"', '"'
    
    # Save the file
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
}

Write-Host "Fixed YAML issues in all markdown files"
