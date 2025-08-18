param(
  [switch]$SkipSummarize,
  [switch]$Drafts
)

$ErrorActionPreference = 'Stop'

$root = "C:\Users\gnul\hashnhedge"
$site = Join-Path $root 'site'
$dataDir = Join-Path $root 'data'
$scripts = Join-Path $root 'scripts'
$outJson = Join-Path $dataDir 'latest.json'
$briefsDir = Join-Path $root 'content\briefs'
$hugoExe = "C:\Users\gnul\AppData\Local\Microsoft\WinGet\Packages\Hugo.Hugo_Microsoft.Winget.Source_8wekyb3d8bbwe\hugo.exe"

Write-Host "[1/4] Fetching RSS feeds..."
& powershell -NoProfile -File (Join-Path $scripts 'rss_fetch.ps1') -OutFile $outJson -PerFeed 8

if (-not $SkipSummarize) {
  Write-Host "[2/4] Generating briefs with local LLM (Ollama)..."
  try {
    & powershell -NoProfile -File (Join-Path $scripts 'summarize.ps1') -Input "$outJson" -OutDir "$briefsDir"
  } catch {
    Write-Warning "Summarization step failed (is Ollama installed and model pulled?). Continuing with existing content."
  }
} else {
  Write-Host "[2/4] Skipping summarize step (per flag)."
}

# Sync briefs into Hugo content structure (posts/YYYY/MM/slug)
Write-Host "[3/4] Syncing briefs into Hugo content tree..."
$today = Get-Date
$year = $today.ToString('yyyy')
$month = $today.ToString('MM')
$hugoPostsDir = Join-Path $site (Join-Path 'content\posts' (Join-Path $year $month))
if (-not (Test-Path $hugoPostsDir)) { New-Item -ItemType Directory -Path $hugoPostsDir -Force | Out-Null }

function Sanitize-Name([string]$name){
  if (-not $name) { return $name }
  $n = $name.Trim().ToLowerInvariant()
  $n = $n -replace "[^a-z0-9]+","-"
  $n = $n.Trim('-')
  if ($n.Length -gt 80) { $n = $n.Substring(0,80).Trim('-') }
  return $n
}

Get-ChildItem -Path (Join-Path $briefsDir $today.ToString('yyyy-MM-dd')) -Filter *.md -ErrorAction SilentlyContinue | ForEach-Object {
  $raw = [IO.Path]::GetFileNameWithoutExtension($_.Name)
  $slug = Sanitize-Name $raw
  if ([string]::IsNullOrWhiteSpace($slug)) { return }
  $dest = Join-Path $hugoPostsDir $slug
  if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest -Force | Out-Null }
  Copy-Item -Path $_.FullName -Destination (Join-Path $dest 'index.md') -Force
}

# Build the site
Write-Host "[4/4] Building site with Hugo..."
$hugoArgs = @('--gc','--minify','-s', $site, '-d', (Join-Path $root 'public'))
if ($Drafts) { $hugoArgs = @('-D') + $hugoArgs }
& $hugoExe @hugoArgs
if ($LASTEXITCODE -ne 0) { throw "Hugo build failed with code $LASTEXITCODE" }

# Verify sitemap and robots exist
$publicDir = Join-Path $root 'public'
$sitemap = Join-Path $publicDir 'sitemap.xml'
$robots = Join-Path $publicDir 'robots.txt'
if (Test-Path $sitemap) { Write-Host "Verified: sitemap.xml present" } else { Write-Warning "Missing sitemap.xml" }
if (Test-Path $robots) { Write-Host "Verified: robots.txt present" } else { Write-Warning "Missing robots.txt" }

Write-Host "Done. Output at: " $publicDir

