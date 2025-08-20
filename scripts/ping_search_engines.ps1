Param(
  [string]$SitemapUrl = "https://hashnhedge.com/sitemap.xml"
)

$targets = @(
  "https://www.google.com/ping?sitemap=$SitemapUrl",
  "https://www.bing.com/ping?sitemap=$SitemapUrl"
)

foreach ($u in $targets) {
  try {
    $r = Invoke-WebRequest -Uri $u -Method Get -UseBasicParsing -TimeoutSec 30
    Write-Host "Pinged $u -> $($r.StatusCode)"
  } catch {
    Write-Warning "Ping to $u failed: $_"
  }
}
