# Daily content generator
$topics = @(
    "bitcoin price analysis",
    "ethereum news today",
    "crypto market update",
    "defi opportunities",
    "nft trends"
)

$topic = $topics | Get-Random
$date = Get-Date -Format "yyyy-MM-dd"
$slug = "$date-$($topic -replace ' ', '-')"

# Build content with proper escaping
$frontMatter = "---`n"
$frontMatter += "title: `"$topic - $(Get-Date -Format 'MMMM d, yyyy')`"`n"
$frontMatter += "date: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss-05:00')`n"
$frontMatter += "draft: false`n"
$frontMatter += "categories: [`"crypto`"]`n"
$frontMatter += "tags: [`"$topic`", `"daily update`", `"market analysis`"]`n"
$frontMatter += "image: `"/images/posts/$slug.jpg`"`n"
$frontMatter += "---`n`n"

$body = "## Today's Market Overview`n`n"
$body += "[AI-generated daily content about $topic]`n`n"
$body += "## Key Metrics`n"
$body += "- Price: `$[PRICE]`n"
$body += "- 24h Change: [CHANGE]%`n"
$body += "- Volume: `$[VOLUME]`n`n"
$body += "## Analysis`n"
$body += "[Detailed analysis]`n`n"
$body += "## What This Means For You`n"
$body += "[Actionable insights]"

$content = $frontMatter + $body

New-Item -Path "content\posts\$slug.md" -Value $content -Force
