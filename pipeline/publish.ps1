Param(
  [switch]$SkipPush,
  [string]$Branch = "main",
  [switch]$OptimizeImages = $true
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
Set-Location $RepoRoot

$logs = Join-Path $RepoRoot "logs"
New-Item $logs -ItemType Directory -Force | Out-Null
$logFile = Join-Path $logs ("publish-" + (Get-Date -Format "yyyyMMdd-HHmmss") + ".log")

Start-Transcript -Path $logFile -Append

try {
  Write-Host "Running build pipeline..."
  & "$RepoRoot\pipeline\build.ps1"
  if ($LASTEXITCODE -ne 0) { throw "build.ps1 failed with exit code $LASTEXITCODE" }

  if ($OptimizeImages -and (Test-Path "$RepoRoot\scripts\optimize_images.ps1")) {
    Write-Host "Optimizing images..."
    & "$RepoRoot\scripts\optimize_images.ps1"
  }

  if (Test-Path "$RepoRoot\pipeline\fetch_images.py") {
    Write-Host "Fetching hero images..."
    if (Test-Path "$RepoRoot\.venv\Scripts\Activate.ps1") { . "$RepoRoot\.venv\Scripts\Activate.ps1" }
    python -m pip install -q -r "$RepoRoot\pipeline\requirements.txt" 2> $null
    python "$RepoRoot\pipeline\fetch_images.py"
  }

  Write-Host "Staging changes..."
  # Stage all tracked/untracked changes (respects .gitignore)
  git add -A

  $status = git status --porcelain
  if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit."
  } else {
    $msg = "chore: auto publish " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    git commit -m $msg

    if (-not $SkipPush) {
      git pull --rebase origin $Branch
      git push origin $Branch
      Write-Host "Pushed to $Branch."
    } else {
      Write-Host "SkipPush is set; not pushing."
    }
  }

  if (Test-Path "$RepoRoot\scripts\ping_search_engines.ps1") {
    Write-Host "Pinging search engines with sitemap..."
    & "$RepoRoot\scripts\ping_search_engines.ps1"
  }

  Write-Host "Publish pipeline completed."
} catch {
  Write-Error $_
  exit 1
} finally {
  Stop-Transcript | Out-Null
}

exit 0
