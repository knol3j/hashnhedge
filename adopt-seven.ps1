Param(
  [string]$SitePath = 'C:\Users\gnul\hashnhedge',
  [string]$ThemeRepo = 'https://github.com/mrhelloboy/seven.git',
  [switch]$SkipRestorePoint
)

$ErrorActionPreference = 'Stop'

function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

function Ensure-Tool {
  param([string]$TestCmd, [string]$InstallArgs)
  $ok = $true
  try { Invoke-Expression $TestCmd | Out-Null } catch { $ok = $false }
  if (-not $ok) {
    Info "Installing via winget: $InstallArgs"
    try {
      Start-Process -FilePath winget -ArgumentList $InstallArgs -Verb RunAs -Wait -NoNewWindow
    } catch {
      Err "winget installation failed: $($_.Exception.Message)"
      throw
    }
  }
}

Info "Working directory: $SitePath"
if (-not (Test-Path $SitePath)) { throw "Site path not found: $SitePath" }

if (-not $SkipRestorePoint) {
  Info "Attempting to create a System Restore Point (Windows PowerShell)..."
  try {
    Start-Process -FilePath powershell.exe -Verb RunAs -Wait -NoNewWindow -ArgumentList '-NoProfile','-Command','try { Enable-ComputerRestore -Drive "C:\\"; Checkpoint-Computer -Description "Pre-Hugo-seven-adoption" -RestorePointType "MODIFY_SETTINGS"; Write-Host "Restore point created." } catch { Write-Host "Restore point creation failed or System Protection disabled. Continuing..."; }'
  } catch { Warn "Skipping restore point: $($_.Exception.Message)" }
}

Set-Location $SitePath

Info "Verifying prerequisites (Git, Hugo Extended)..."
Ensure-Tool -TestCmd 'git --version' -InstallArgs 'install -e --id Git.Git --source winget --accept-source-agreements --accept-package-agreements'
$hugoVersion = $null
try { $hugoVersion = (hugo version) } catch { }
if (-not $hugoVersion -or ($hugoVersion -notmatch 'extended')) {
  Ensure-Tool -TestCmd 'hugo version' -InstallArgs 'install -e --id Hugo.Hugo.Extended --source winget --accept-source-agreements --accept-package-agreements'
}

Info "Ensuring Git repository is initialized..."
if (-not (Test-Path .git)) {
  git init
  git add -A
  git commit -m "chore: baseline snapshot before adopting theme seven" | Out-Null
}

$branch = "feat/theme-seven-" + (Get-Date -Format "yyyyMMddHHmmss")
Info "Creating feature branch $branch"
git checkout -b $branch | Out-Null

# Themes: add 'seven' and purge others
if (-not (Test-Path .\\themes)) { New-Item -ItemType Directory -Path .\\themes | Out-Null }

Info "Removing other themes (if any)..."
Get-ChildItem .\\themes -Directory -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -ne 'seven' } |
  ForEach-Object {
    $p = $_.FullName
    git rm -r --ignore-unmatch $p | Out-Null
    Remove-Item -Recurse -Force $p
  }

if (Test-Path .git\\modules\\themes) {
  Get-ChildItem .git\\modules\\themes -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -ne 'seven' } |
    Remove-Item -Recurse -Force
}

if (Test-Path .\\themes\\seven) {
  Info "Cleaning existing themes/seven before re-adding submodule..."
  git submodule deinit -f themes/seven | Out-Null
  git rm -f themes/seven | Out-Null
  Remove-Item -Recurse -Force .git\\modules\\themes\\seven -ErrorAction SilentlyContinue
  Remove-Item -Recurse -Force .\\themes\\seven -ErrorAction SilentlyContinue
}

Info "Adding seven theme as a git submodule..."
git submodule add $ThemeRepo themes/seven

# Config: consolidate to a single file and set theme
Info "Consolidating configuration and setting theme = 'seven'..."
$configFiles = @('hugo.toml','hugo.yaml','hugo.yml','hugo.json','config.toml','config.yaml','config.yml','config.json')
$existing = $configFiles | Where-Object { Test-Path $_ }
$primary = $null
foreach ($f in @('hugo.toml','config.toml','hugo.yaml','config.yaml','hugo.json','config.json','hugo.yml','config.yml')) {
  if ($existing -contains $f) { $primary = $f; break }
}
if (-not $primary) {
  $primary = 'hugo.toml'
  Set-Content -Path $primary -Value "title = `"hashnhedge`"`nbaseURL = `"`/`"`nlanguageCode = `"en-us`"`ntheme = `"seven`"`n" -Encoding UTF8
} else {
  $ext = [IO.Path]::GetExtension($primary).ToLowerInvariant()
  $content = Get-Content -Path $primary -Raw
  if ($ext -eq '.toml') {
    if ($content -match '(?m)^\s*theme\s*=') {
      $content = [regex]::Replace($content,'(?m)^\s*theme\s*=.*$','theme = "seven"')
    } else {
      $content += "`n`ntheme = `"seven`"`n"
    }
    Set-Content -Path $primary -Value $content -Encoding UTF8
  } elseif ($ext -eq '.yaml' -or $ext -eq '.yml') {
    if ($content -match '(?m)^\s*theme\s*:') {
      $content = [regex]::Replace($content,'(?m)^\s*theme\s*:.*$','theme: seven')
    } else {
      $content += "`n`ntheme: seven`n"
    }
    Set-Content -Path $primary -Value $content -Encoding UTF8
  } elseif ($ext -eq '.json') {
    try {
      $obj = $content | ConvertFrom-Json
      $obj.theme = 'seven'
      $json = $obj | ConvertTo-Json -Depth 64
      Set-Content -Path $primary -Value $json -Encoding UTF8
    } catch {
      Add-Content -Path $primary -Value "`n`n`"theme`": `"`seven`"`n"
    }
  }
}
$toRemove = $existing | Where-Object { $_ -ne $primary }
foreach ($f in $toRemove) {
  git rm -f --ignore-unmatch $f | Out-Null
  Remove-Item -Force $f -ErrorAction SilentlyContinue
}
if (Test-Path .\\config) {
  git rm -r -f --ignore-unmatch config | Out-Null
  Remove-Item -Recurse -Force .\\config -ErrorAction SilentlyContinue
}

# Clean generated artifacts
Info "Cleaning generated artifacts..."
Remove-Item -Recurse -Force .\\public -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .\\resources -ErrorAction SilentlyContinue

# Build and validate
Info "Building site with Hugo..."
hugo --minify
if ($LASTEXITCODE -ne 0) {
  Err "Hugo build failed; will not commit or push."
  exit 1
}

# Commit and push if build succeeded
Info "Commit changes and push only if remote 'origin' is configured..."
git add -A
git commit -m "feat(theme): adopt mrhelloboy/seven; purge other themes/config variants; verified clean build" | Out-Null

$origin = $null
try { $origin = git remote 2>$null | Select-String '^origin$' } catch { }
if ($origin) {
  git push -u origin $branch
  Info "Pushed branch $branch to origin."
} else {
  Warn "No 'origin' remote configured; commit created locally and not pushed."
}

Info "Completed successfully."
