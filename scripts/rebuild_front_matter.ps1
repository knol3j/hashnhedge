param(
  [Parameter(Mandatory=$false)][string]$Root = "C:\Users\gnul\hashnhedge\site\content\posts"
)

function Derive-Title {
  param([string]$front, [string]$path)
  $m = [regex]::Match($front, "(?m)^\s*title\s*:\s*(.*)$")
  if ($m.Success) {
    $v = $m.Groups[1].Value.Trim()
    $v = $v.Trim('"').Trim("'")
    if ($v) { return $v }
  }
  $dir = Split-Path -Path (Split-Path -Path $path -Parent) -Leaf
  $dir = ($dir -replace '-', ' ').Trim()
  if ($dir) { return ($dir.Substring(0,1).ToUpper() + $dir.Substring(1)) }
  return 'Untitled'
}

function Extract-FirstUrl {
  param([string]$text)
  $m = [regex]::Match($text, "https?://\S+")
  if ($m.Success) { return $m.Value }
  return $null
}

function Get-Value {
  param([string]$front, [string]$key)
  $m = [regex]::Match($front, "(?m)^\s*" + [regex]::Escape($key) + "\s*:\s*(.*)$")
  if ($m.Success) {
    $v = $m.Groups[1].Value.Trim()
    $v = $v.Trim('"').Trim("'")
    return $v
  }
  return $null
}

function Rebuild-FM {
  param([string]$raw, [string]$path)
  $text = $raw -replace "\r?\n", "`r`n"
  if ($text -notmatch "^---\r\n") { return $null }
  $parts = $text -split "`r`n---`r`n", 2
  if ($parts.Count -lt 2) { return $null }
  $front = $parts[0] -replace "^---\r?\n", ''
  $body = $parts[1]

  # Extract values tolerantly
  $title = Derive-Title -front $front -path $path
  $date = Get-Value -front $front -key 'date'
  $category = Get-Value -front $front -key 'category'
  if (-not $category) { $category = 'Markets' }
  $summary = Get-Value -front $front -key 'summary'
  if ($null -eq $summary) { $summary = '' }
  $slug = Get-Value -front $front -key 'slug'
  if (-not $slug) {
    $slug = (Split-Path -Path (Split-Path -Path $path -Parent) -Leaf).ToLower()
  }

  # Collect source_urls
  $source = $null
  # Try list under source_urls
  $m = [regex]::Match($front, "(?s)source_urls\s*:\s*(?:\[(.*?)\]|(\r?\n\s*-\s*\S+.*))")
  if ($m.Success) {
    if ($m.Groups[1].Success) {
      $inside = $m.Groups[1].Value
      $um = [regex]::Match($inside, "https?://\S+")
      if ($um.Success) { $source = $um.Value }
    } elseif ($m.Groups[2].Success) {
      $um = [regex]::Match($m.Groups[2].Value, "https?://\S+")
      if ($um.Success) { $source = $um.Value }
    }
  }
  if (-not $source) { $source = Extract-FirstUrl -text $body }

  $sb = New-Object System.Text.StringBuilder
  [void]$sb.AppendLine('---')
  [void]$sb.AppendLine("title: '" + ($title -replace "'","''") + "'")
  if ($date) { [void]$sb.AppendLine("date: \"$date\"") }
  [void]$sb.AppendLine("category: \"$category\"")
  [void]$sb.AppendLine("summary: ''")
  [void]$sb.AppendLine("slug: " + $slug)
  if ($source) {
    [void]$sb.AppendLine("source_urls:")
    [void]$sb.AppendLine("  - \"$source\"")
  } else {
    [void]$sb.AppendLine("source_urls: []")
  }
  [void]$sb.AppendLine("seo:")
  [void]$sb.AppendLine("  title: '" + ($title -replace "'","''") + " | Hash n Hedge'")
  [void]$sb.AppendLine("  description: ''")
  [void]$sb.AppendLine("  keywords: ['news','markets','brief']")
  [void]$sb.AppendLine('---')
  $new = $sb.ToString() + ($body -replace "^\r?\n","\r\n")
  return $new
}

$files = Get-ChildItem -Path $Root -Filter index.md -Recurse -File
$updated = 0
foreach ($f in $files) {
  try {
    $raw = Get-Content -Raw -LiteralPath $f.FullName -Encoding UTF8
    $rebuilt = Rebuild-FM -raw $raw -path $f.FullName
    if ($rebuilt) {
      $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
      [System.IO.File]::WriteAllText($f.FullName, $rebuilt, $utf8NoBom)
      $updated++
    }
  } catch {
    Write-Host "Failed: $($f.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
  }
}
Write-Host "Rebuilt front matter for $updated files" -ForegroundColor Green

