param(
  [Parameter(Mandatory=$true)][string]$File
)

function Derive-TitleFromPath {
  param([string]$p)
  $dir = Split-Path -Path (Split-Path -Path $p -Parent) -Leaf
  if (-not $dir -or $dir -eq 'index.md') { $dir = Split-Path -Leaf $p }
  $dir = $dir -replace '-', ' '
  if ($dir.Length -gt 0) { return ($dir.Substring(0,1).ToUpper() + $dir.Substring(1)) }
  return 'Untitled'
}

$raw = Get-Content -Raw -LiteralPath $File -Encoding UTF8
$raw = $raw -replace "\r?\n", "`r`n"
if ($raw -notmatch "^---\r\n") { return }
$parts = $raw -split "`r`n---`r`n", 2
if ($parts.Count -lt 2) { return }
$front = $parts[0] -replace "^---\r?\n", ''
$body = $parts[1]

$lines = $front -split "`r`n"
# remove stray quote-only and pipe suffix lines
$lines = $lines | Where-Object { $_ -notmatch "^\s*""\s*$" -and $_ -notmatch '^\s*\|\s*Hash n Hedge"\s*$' }
# normalize key: value spacing and quotes as needed
$normalized = @()
foreach ($ln in $lines) {
  if ($ln -match '^(\s*)([A-Za-z_][A-Za-z0-9_\-]*)\s*:\s*(.*)$') {
    $pre,$key,$val = $matches[1],$matches[2],$matches[3]
    $val = $val.Trim()
    if ($val -eq '' -or $val -eq '""' -or $val -eq "''") {
      if ($key -in @('summary','description')) { $val = "''" } else { $val = "''" }
    }
    # quote titles/descriptions
    if ($key -in @('title','description','summary')) {
      $val = $val.Trim('"').Trim("'")
      $val = "'${val}'"
    }
    $normalized += ("${pre}${key}: ${val}")
  } else {
    $normalized += $ln
  }
}
# ensure title exists
if (-not ($normalized -match '^\s*title\s*:')) {
  $title = Derive-TitleFromPath -p $File
  $normalized = @("title: '${title}'") + $normalized
}
# ensure seo block consistency
$hasSeo = $normalized -match '^\s*seo\s*:\s*$'
if ($hasSeo) {
  $out = @()
  $inSeo = $false
  $addedTitle = $false
  foreach ($ln in $normalized) {
    if ($ln -match '^\s*seo\s*:\s*$') { $inSeo = $true; $addedTitle = $false; $out += $ln; continue }
    if ($inSeo) {
      if (-not $addedTitle -and $ln -notmatch '^\s*title\s*:') {
        $t = ($normalized | Where-Object { $_ -match '^\s*title\s*:' } | Select-Object -First 1)
        $tval = ($t -replace '^\s*title\s*:\s*', '')
        $out += ("  title: ${tval}")
        $addedTitle = $true
      }
      if ($ln -match '^\s*\w+\s*:\s*') { $out += $ln; $inSeo = $false; continue }
      # skip stray lines within seo
      continue
    }
    $out += $ln
  }
  $normalized = $out
}

$newFront = ($normalized -join "`r`n").TrimEnd()
$new = "---`r`n$newFront`r`n---`r`n$body"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($File, $new, $utf8NoBom)

