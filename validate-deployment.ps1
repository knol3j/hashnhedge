# Hash & Hedge Deployment Validation System
param([switch]$Verbose = $false)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   DEPLOYMENT VALIDATION FRAMEWORK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Phase 1: Structure Check
Write-Host "`n[PHASE 1] STRUCTURAL INTEGRITY" -ForegroundColor Yellow
$checks = @{
    "Hugo" = (Get-Command hugo -ErrorAction SilentlyContinue)
    "Theme" = (Test-Path "site\themes\newsroom\layouts")
    "Content" = (Test-Path "site\content\posts")
    "Workflow" = (Test-Path ".github\workflows\deploy.yml")
}

foreach ($check in $checks.GetEnumerator()) {
    if ($check.Value) {
        Write-Host "  [OK] $($check.Key)" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $($check.Key)" -ForegroundColor Red
    }
}

# Phase 2: Build Test
Write-Host "`n[PHASE 2] BUILD VERIFICATION" -ForegroundColor Yellow
Set-Location "site"
$buildResult = hugo --quiet --destination ../test-build 2>&1
Set-Location ".."

if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Build successful" -ForegroundColor Green
    $files = (Get-ChildItem -Path "test-build" -Recurse -File).Count
    Write-Host "  [INFO] Generated $files files" -ForegroundColor Gray
    Remove-Item -Path "test-build" -Recurse -Force
} else {
    Write-Host "  [FAIL] Build failed" -ForegroundColor Red
}

# Phase 3: Deployment Ready
Write-Host "`n[PHASE 3] DEPLOYMENT STATUS" -ForegroundColor Yellow
$ready = $true

# Check git status
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "  [WARN] Uncommitted changes detected" -ForegroundColor Yellow
    $ready = $false
} else {
    Write-Host "  [OK] Git status clean" -ForegroundColor Green
}

# Final Assessment
Write-Host "`n========================================" -ForegroundColor Cyan
if ($ready -and $LASTEXITCODE -eq 0) {
    Write-Host "RESULT: READY FOR DEPLOYMENT" -ForegroundColor Green
    Write-Host "Next: git add -A && git commit -m 'fix: deployment' && git push" -ForegroundColor White
} else {
    Write-Host "RESULT: NOT READY" -ForegroundColor Red
    Write-Host "Fix issues above before deploying" -ForegroundColor Yellow
}
Write-Host "========================================" -ForegroundColor Cyan