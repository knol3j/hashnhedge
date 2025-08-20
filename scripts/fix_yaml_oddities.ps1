param(
  [Parameter(Mandatory=$false)][string]$Root = "C:\Users\gnul\hashnhedge\site\content\posts"
)

function Fix-Yaml-Oddities {
  param([string]$text)
  $text = $text -replace "\r?\n", "`r`n"
  if ($text -notmatch "^---\r\n") { return $text }
  $parts = $text -split "`r`n---`r`n", 2
  if ($parts.Count -lt 2) { return $text }
  $front = $parts[0] -replace "^---\r?\n", ""
  $body = $parts[1]

  # Remove quote-only lines and stray pipe fragments
  $front = $front -replace '(?m)^\s*"\s*$', ''
  $front = $front -replace '(?m)^\s*\|\s*Hash n Hedge"\s*$', ''

  # Normalize key:"value" and key:'value' forms to ensure a space after colon
  $front = $front -replace '(?m)^(\s*[A-Za-z_][A-Za-z0-9_\-]*\s*:)\s*"(.*)"\s*$', '$1 "$2"'
  $front = $front -replace "(?m)^(\s*[A-Za-z_][A-Za-z0-9_\-]*\s*:)\s*'(.*)'\s*$", "$1 '$2'"

  # Normalize title spacing (remove leading spaces inside quoted value)
  $front = $front -replace '(?m)^(\s*title\s*:\s*)(["'']?)\s+(.*)$', '$1$2$3'

  # Ensure empty summary/description are explicit
  $front = $front -replace '(?m)^(\s*(summary|description)\s*:)\s*$', "$1 ''"

  # Fix slug leading dashes
  $front = $front -replace '(?m)^(\s*slug\s*:\s*)-+', '$1'

  $newFront = $front
  return "---`r`n$newFront`r`n---`r`n$body"
}

$files = Get-ChildItem -Path $Root -Filter index.md -Recurse -File
$fixed = 0
foreach ($f in $files) {
  try {
    $txt = Get-Content -Raw -LiteralPath $f.FullName -Encoding UTF8
    $new = Fix-Yaml-Oddities $txt
    if ($new -ne $txt) {
      $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
      [System.IO.File]::WriteAllText($f.FullName, $new, $utf8NoBom)
      $fixed++
    }
  } catch {
    Write-Host "Skip $($f.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
  }
}
Write-Host "YAML oddities fixed in $fixed files" -ForegroundColor Green

