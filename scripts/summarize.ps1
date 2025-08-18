param(
  [string]$Input = "C:\\Users\\gnul\\hashnhedge\\data\\latest.json",
  [string]$OutDir = "C:\\Users\\gnul\\hashnhedge\\content\\briefs"
)

# Requires a running local model via Ollama (e.g., llama3.1:8b or qwen2.5:7b)
# Install: https://ollama.com/ (then `ollama pull llama3.1:8b`)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

if (-not (Test-Path $Input)) { Write-Warning "Input JSON not found at $Input. Skipping summarization."; return }
$items = Get-Content -Raw -Path $Input | ConvertFrom-Json
$today = Get-Date -Format 'yyyy-MM-dd'
$outToday = Join-Path $OutDir $today
if (-not (Test-Path $outToday)) { New-Item -ItemType Directory -Path $outToday | Out-Null }

function New-Slug($text) {
  $t = $text.ToLowerInvariant()
  $t = -join ($t.ToCharArray() | ForEach-Object { if (([char]::IsLetterOrDigit($_)) -or ($_ -eq ' ')) { $_ } })
  $t = ($t -replace '\\s+', '-').Trim('-')
  return $t.Substring(0, [Math]::Min(60, $t.Length))
}

foreach ($item in $items) {
  $title = [string]$item.title
  if ([string]::IsNullOrWhiteSpace($title)) { continue }
  $slug = New-Slug $title
  $outfile = Join-Path $outToday ("$slug.md")
  if (Test-Path $outfile) { continue }

  $prompt = @"
You are an editor writing a concise, original news brief. Using the source below, produce:
- A headline under 60 chars
- A 120–160 char summary meta description
- 3–5 bullet key points
- 2 short takeaways with light analysis
- Include the source link in a Sources section
- Tone: neutral, factual, with a line of original context

SOURCE TITLE: $($item.title)
SOURCE LINK: $($item.link)
SOURCE SNIPPET: $($item.description)
"@

  # Locate Ollama executable and ensure server is running
  $ollPaths = @(
    'C:\\Users\\gnul\\AppData\\Local\\Programs\\Ollama\\ollama.exe',
    'C:\\Program Files\\Ollama\\ollama.exe'
  )
  $oll = $ollPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $oll) { Write-Warning "Ollama executable not found. Skipping '$title'"; continue }
  try {
    Start-Process -FilePath $oll -ArgumentList 'serve' -WindowStyle Hidden -ErrorAction SilentlyContinue
  } catch {}

  # Wait for Ollama server readiness (up to 60 seconds)
  $ready = $false
  for ($i=0; $i -lt 30; $i++) {
    try {
      $respPing = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:11434/api/version' -TimeoutSec 2
      if ($respPing.StatusCode -ge 200 -and $respPing.StatusCode -lt 300) { $ready = $true; break }
    } catch {}
    Start-Sleep -Seconds 2
  }
  if (-not $ready) { Write-Warning "Ollama server not ready. Skipping '$title'"; continue }

  try {
    $resp =  $oll run llama3.1:8b $prompt 2$null
  } catch {
    Write-Warning "Ollama run failed or model missing. Skipping '$title'"
    continue
  }

  $nowIso = (Get-Date).ToString('s')
  $frontMatter = @"
---
title: "$title"
date: "$nowIso"
category: "Markets"
summary: ""
slug: "$slug"
source_urls:
  - "$($item.link)"
seo:
  title: "$title | Hash n Hedge"
  description: ""
  keywords: ["news", "markets", "brief"]
---
"@

  $content = $frontMatter + "`r`n" + $resp
  Set-Content -Path $outfile -Value $content -Encoding UTF8
  Write-Output "Wrote $outfile"
}

