param(
  [Parameter(Mandatory=$false)][string]$Root = "C:\Users\gnul\hashnhedge\site\content\posts"
)

$files = Get-ChildItem -Path $Root -Filter index.md -Recurse -File
$changed = 0
foreach ($f in $files) {
  try {
    $txt = Get-Content -Raw -LiteralPath $f.FullName -Encoding UTF8
    $txt = $txt -replace "\r?\n","`r`n"
    if ($txt -notmatch "^---\r\n") { continue }
    $parts = $txt -split "`r`n---`r`n", 2
    if ($parts.Count -lt 2) { continue }
    $front = $parts[0] -replace "^---\r?\n",""
    $body = $parts[1]
    $lines = $front -split "`r`n"
    $out = @()
    for ($i=0; $i -lt $lines.Length; $i++) {
      $line = $lines[$i]
      if ($line -match "^\s*''\s*$") { continue }
      if ($line -match "^\s*source_urls:\s*''\s*$") { $out += "source_urls:"; continue }
      if ($line -match "^\s*seo:\s*''\s*$") { $out += "seo:"; continue }
      $out += $line
    }
    $newFront = ($out -join "`r`n").TrimEnd()
    $new = "---`r`n$newFront`r`n---`r`n$body"
    if ($new -ne $txt) {
      $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
      [System.IO.File]::WriteAllText($f.FullName, $new, $utf8NoBom)
      $changed++
    }
  } catch {
    Write-Host "Skip $($f.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
  }
}
Write-Host "Simple pattern fixes applied to $changed files" -ForegroundColor Green

