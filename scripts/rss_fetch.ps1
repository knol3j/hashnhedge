param(
  [string]$OutFile = "C:\\Users\\gnul\\hashnhedge\\data\\latest.json",
  [string]$FeedsFile = "C:\\Users\\gnul\\hashnhedge\\data\\rss_sources.txt",
  [int]$PerFeed = 5
)

# Simple RSS/Atom fetcher using PowerShell's Invoke-WebRequest and XML parsing
$all = @()
$feeds = Get-Content -Path $FeedsFile | Where-Object { $_ -and -not $_.StartsWith('#') }
foreach ($url in $feeds) {
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $url -TimeoutSec 20
    [xml]$xml = $resp.Content
    $items = @()
    if ($xml.rss) { # RSS 2.0
      $items = $xml.rss.channel.item | Select-Object -First $PerFeed | ForEach-Object {
        [pscustomobject]@{
          feed = $url
          title = $_.title
          link = $_.link
          pubDate = $_.pubDate
          guid = $_.guid.'#text'
          description = $_.description
        }
      }
    } elseif ($xml.feed) { # Atom
      $items = $xml.feed.entry | Select-Object -First $PerFeed | ForEach-Object {
        $linkNode = $_.link | Where-Object { $_.rel -eq 'alternate' } | Select-Object -First 1
        [pscustomobject]@{
          feed = $url
          title = $_.title.'#text'
          link = $linkNode.href
          pubDate = $_.updated
          guid = $_.id
          description = $_.summary.'#text'
        }
      }
    }
    $all += $items
  } catch {
    Write-Warning ("Failed to fetch {0}: {1}" -f $url, $_)
  }
}

$all | ConvertTo-Json -Depth 5 | Set-Content -Path $OutFile -Encoding UTF8
Write-Output "Saved $($all.Count) items to $OutFile"

