# Hash & Hedge SEO Optimization Script
# Implements advanced SEO strategies for rapid ranking growth

param(
    [string]$SitePath = "C:\Users\gnul\hashnhedge"
)

Write-Host "[SEARCH] Hash and Hedge SEO Optimization Starting..." -ForegroundColor Cyan

# Create robots.txt for optimal crawling
$robotsContent = @"
User-agent: *
Allow: /
Sitemap: https://hashnhedge.com/sitemap.xml

User-agent: Googlebot
Crawl-delay: 0
Allow: /

User-agent: Bingbot
Crawl-delay: 0
Allow: /

# Block bad bots
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Crawl-delay: 10
"@

Set-Content -Path "$SitePath\static\robots.txt" -Value $robotsContent
Write-Host "[OK] Created optimized robots.txt" -ForegroundColor Green

# Create structured data for rich snippets
$structuredDataTemplate = @'
{{ $title := .Title | default .Site.Title }}
{{ $description := .Description | default .Site.Params.description }}
{{ $image := .Params.image | default "/images/default-og.jpg" | absURL }}
{{ $url := .Permalink }}
{{ $date := .Date.Format "2006-01-02T15:04:05-07:00" }}

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "{{ $title }}",
  "description": "{{ $description }}",
  "image": "{{ $image }}",
  "url": "{{ $url }}",
  "datePublished": "{{ $date }}",
  "dateModified": "{{ $date }}",
  "author": {
    "@type": "Organization",
    "name": "Hash & Hedge",
    "url": "https://hashnhedge.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Hash & Hedge",
    "logo": {
      "@type": "ImageObject",
      "url": "https://hashnhedge.com/images/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ $url }}"
  }
}
</script>

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://hashnhedge.com"
    },
    {{ if .Section }}
    {
      "@type": "ListItem",
      "position": 2,
      "name": "{{ .Section | humanize }}",
      "item": "https://hashnhedge.com/{{ .Section }}/"
    },
    {{ end }}
    {
      "@type": "ListItem",
      "position": {{ if .Section }}3{{ else }}2{{ end }},
      "name": "{{ $title }}",
      "item": "{{ $url }}"
    }
  ]
}
</script>
'@

Set-Content -Path "$SitePath\layouts\partials\structured-data.html" -Value $structuredDataTemplate
Write-Host "[OK] Created structured data templates" -ForegroundColor Green

# Generate XML sitemap configuration
$sitemapConfig = @"
# Sitemap configuration
[sitemap]
  changefreq = 'daily'
  filename = 'sitemap.xml'
  priority = 0.5
"@

Add-Content -Path "$SitePath\config.toml" -Value "`n$sitemapConfig"
Write-Host "[OK] Configured XML sitemap generation" -ForegroundColor Green

# Create internal linking script
Write-Host "[LINK] Building internal link structure..." -ForegroundColor Yellow

$internalLinkingScript = @'
# Internal Linking Optimizer
$posts = Get-ChildItem -Path "content\posts" -Filter "*.md" -Recurse
$linkMap = @{}

# Build keyword map
foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw
    if ($content -match "tags:\s*\[(.*?)\]") {
        $tags = $matches[1] -split "," | ForEach-Object { $_.Trim().Trim('"') }
        foreach ($tag in $tags) {
            if (!$linkMap.ContainsKey($tag)) {
                $linkMap[$tag] = @()
            }
            $linkMap[$tag] += $post.BaseName
        }
    }
}

# Add contextual internal links
foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw
    $modified = $false
    
    foreach ($keyword in $linkMap.Keys) {
        if ($linkMap[$keyword].Count -gt 1) {
            # Find other posts with same keyword
            $relatedPosts = $linkMap[$keyword] | Where-Object { $_ -ne $post.BaseName } | Select-Object -First 3
            
            if ($relatedPosts -and $content -notmatch "## Related Articles") {
                $relatedSection = "`n`n## Related Articles`n`n"
                foreach ($related in $relatedPosts) {
                    $relatedSection += "- [Read more about $keyword](/posts/$related/)`n"
                }
                $content += $relatedSection
                $modified = $true
            }
        }
    }
    
    if ($modified) {
        Set-Content -Path $post.FullName -Value $content
    }
}
'@

Set-Content -Path "$SitePath\optimize-internal-links.ps1" -Value $internalLinkingScript
Write-Host "[OK] Created internal linking optimizer" -ForegroundColor Green

Write-Host "`n[SUCCESS] SEO optimization complete!" -ForegroundColor Green
