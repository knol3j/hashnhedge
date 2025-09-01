Write-Host "Moving August 2025 posts temporarily for clean build..." -ForegroundColor Green

# Create backup directory
$backupDir = "C:\Users\gnul\hashnhedge\site\content\posts-august-backup"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

# Move August 2025 posts
$augustPath = "C:\Users\gnul\hashnhedge\site\content\posts\2025\08"
if (Test-Path $augustPath) {
    Move-Item -Path $augustPath -Destination "$backupDir\08" -Force
    Write-Host "Moved August 2025 posts to backup" -ForegroundColor Yellow
}

Write-Host "Ready for clean build" -ForegroundColor Green
