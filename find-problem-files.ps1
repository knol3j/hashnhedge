# Find all markdown files with potential YAML issues
$path = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08"
$files = Get-ChildItem -Path $path -Filter "index.md" -Recurse

$problemFiles = @()

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        # Check for common problematic characters
        if ($content -match '[^\x00-\x7F]') {
            $problemFiles += $file.FullName
            Write-Host "Found issues in: $($file.FullName)"
        }
    } catch {
        Write-Host "Error reading: $($file.FullName)"
    }
}

Write-Host "`nTotal problematic files found: $($problemFiles.Count)"
$problemFiles | Out-File "C:\Users\gnul\hashnhedge\problem-files.txt"
