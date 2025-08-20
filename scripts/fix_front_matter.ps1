param(
  [Parameter(Mandatory=$false)][string]$Root = "C:\Users\gnul\hashnhedge\site\content\posts"
)

function Remove-ControlChars {
  param([string]$s)
  if ($null -eq $s) { return $s }
  return [regex]::Replace($s, "[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "")
}

function Quote-YamlIfNeeded {
  param([string]$val)
  if ($null -eq $val) { return $val }
  $needs = $val -match "(^\s|\s$|:|#|\-|\[|\]|\{|\}|,|\&|\*|!|\?|\||>|')"
  if ($needs -or $val -match '"') {
    $escaped = $val -replace "'", "''"
    return "'${escaped}'"
  }
  return $val
}

function Fix-FrontMatterInText {
  param([string]$text)
  $text = $text -replace "\r?\n", "`r`n"
  if ($text -notmatch "^---\r\n") { $text = "---`r`n" + $text }
  $parts = $text -split "`r`n---`r`n", 2
  if ($parts.Count -lt 2) { return $text }
  $front = $parts[0] -replace "^---\r?\n", ""
  $body = $parts[1]

  $front = Remove-ControlChars $front

  $lines = $front -split "`r`n"
  $out = @()
  $inSeo = $false
  foreach ($line in $lines) {
    $l = $line
    if ($l -match '^\s*$') { $out += $l; continue }
    if ($l -match '^\s*seo\s*:\s*$') { $inSeo = $true; $out += $l; continue }
    if ($inSeo -and $l -match '^\s*\w+\s*:\s*$') { $inSeo = $false }

    if ($l -match '^(\s*)(title|description|summary|slug)\s*:\s*(.*)$') {
      $pre = $matches[1]; $key = $matches[2]; $val = ($matches[3]).Trim()
      $val = $val.Trim('"').Trim("'")
      if ($key -eq 'slug') {
        $val = ($val -replace '[^a-zA-Z0-9\- ]','' -replace '\s+','-').ToLower()
        $out += ("${pre}${key}: ${val}")
      } else {
        $val = Quote-YamlIfNeeded $val
        $out += ("${pre}${key}: ${val}")
      }
      continue
    }
    if ($inSeo -and $l -match '^(\s*)(title)\s*:\s*(.*)$') {
      $pre = $matches[1]; $val = ($matches[3]).Trim('"').Trim("'")
      $val = Quote-YamlIfNeeded $val
      $out += ("${pre}title: ${val}")
      continue
    }
    $out += $l
  }

  $newFront = ($out -join "`r`n")
  return "---`r`n$newFront`r`n---`r`n$body"
}

$files = Get-ChildItem -Path $Root -Filter index.md -Recurse -File
$fixed = 0
foreach ($f in $files) {
  try {
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
      $bytes = $bytes[3..($bytes.Length-1)]
    }
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $new = Fix-FrontMatterInText $text
    if ($new -ne $text) {
      $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
      [System.IO.File]::WriteAllText($f.FullName, $new, $utf8NoBom)
      $fixed++
    }
  } catch {
    Write-Host "Failed: $($f.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
  }
}
Write-Host "Processed $($files.Count) files, fixed: $fixed" -ForegroundColor Green

