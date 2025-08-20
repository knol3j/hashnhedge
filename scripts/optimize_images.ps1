Param(
  [string]$Root = (Resolve-Path ".").Path,
  [int]$JpegQuality = 85,
  [switch]$DryRun
)

if (-not (Get-Command magick.exe -ErrorAction SilentlyContinue)) {
  Write-Warning "ImageMagick not found. Install with: winget install ImageMagick.ImageMagick"
  exit 1
}

$paths = @(
  Join-Path $Root "site\static",
  Join-Path $Root "site\content\posts"
) | Where-Object { Test-Path $_ }

$images = Get-ChildItem -Path $paths -Recurse -File -Include *.jpg, *.jpeg, *.png
foreach ($img in $images) {
  $ext = $img.Extension.ToLowerInvariant()
  if ($DryRun) { Write-Host "[DRY] $($img.FullName)"; continue }
  if ($ext -in @(".jpg",".jpeg")) {
    & magick mogrify -strip -interlace Plane -sampling-factor 4:2:0 -quality $JpegQuality $img.FullName
  } elseif ($ext -eq ".png") {
    & magick mogrify -strip -define png:compression-level=9 -define png:compression-filter=5 $img.FullName
  }
}
