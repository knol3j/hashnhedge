param(
  [Parameter(Mandatory=$false)][string]$Root = "C:\Users\gnul\hashnhedge\site\content\posts"
)

$files = Get-ChildItem -Path $Root -Filter index.md -Recurse -File
$changed = 0
foreach ($f in $files) {
  try {
    & "C:\Users\gnul\hashnhedge\scripts\fix_one_front_matter.ps1" -File $f.FullName
    $changed++
  } catch {
    Write-Host "Failed to process $($f.FullName): $($_.Exception.Message)" -ForegroundColor Yellow
  }
}
Write-Host "Ran fix_one_front_matter on $changed files" -ForegroundColor Green

