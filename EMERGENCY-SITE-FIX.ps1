# COMPREHENSIVE SITE UNFUCKER SCRIPT
# Because your shit's more tangled than Christmas lights in a tornado

Write-Host "=== HASH & HEDGE EMERGENCY SITE REPAIR ===" -ForegroundColor Red
Write-Host "Fixing your broken-ass site..." -ForegroundColor Yellow

# 1. FIX THE CONFIG - Remove the cancer permalink structure
$configPath = "C:\Users\gnul\hashnhedge\config.toml"
$config = Get-Content $configPath -Raw
$config = $config -replace '\[permalinks\][\s\r\n]*posts = "/:year/:month/:title/"', '# Permalinks removed - using default'
Set-Content -Path $configPath -Value $config -Encoding UTF8

Write-Host "✓ Fixed permalink cancer in config.toml" -ForegroundColor Green

# 2. CONVERT DIRECTORY POSTS TO PROPER MARKDOWN FILES
$postsDir = "C:\Users\gnul\hashnhedge\content\posts"
$directories = Get-ChildItem -Path $postsDir -Directory

foreach ($dir in $directories) {
    $indexFile = Join-Path $dir.FullName "index.md"
    if (Test-Path $indexFile) {
        # Move index.md to parent as directory-name.md
        $newPath = Join-Path $postsDir "$($dir.Name).md"
        if (-not (Test-Path $newPath)) {
            Move-Item -Path $indexFile -Destination $newPath -Force
            Write-Host "✓ Converted: $($dir.Name)" -ForegroundColor Green
        }
    }
}

Write-Host "`n✓ Converted directory posts to proper markdown files" -ForegroundColor Green

# 3. SAVE YOUR POSTER IMAGES TO THE STATIC FOLDER
$posterDir = "C:\Users\gnul\hashnhedge\static\images\posters"
if (!(Test-Path $posterDir)) {
    New-Item -ItemType Directory -Force -Path $posterDir | Out-Null
}

Write-Host "`nPoster images saved to: $posterDir" -ForegroundColor Cyan
Write-Host "Upload your 4 poster images there as:" -ForegroundColor Yellow
Write-Host "  - poster1.jpg" -ForegroundColor Yellow
Write-Host "  - poster2.jpg" -ForegroundColor Yellow
Write-Host "  - poster3.jpg" -ForegroundColor Yellow
Write-Host "  - poster4.jpg" -ForegroundColor Yellow

# 4. CREATE A HERO SECTION FOR YOUR INDEX PAGE
$heroHTML = @'
{{ define "hero" }}
<section class="hero-posters">
  <div class="poster-grid">
    <img src="/images/posters/poster1.jpg" alt="Hash and Hedge Revolutionary Poster 1" class="poster">
    <img src="/images/posters/poster2.jpg" alt="Hash and Hedge Revolutionary Poster 2" class="poster">
    <img src="/images/posters/poster3.jpg" alt="Hash and Hedge Revolutionary Poster 3" class="poster">
    <img src="/images/posters/poster4.jpg" alt="Hash and Hedge Revolutionary Poster 4" class="poster">
  </div>
  <style>
    .hero-posters {
      padding: 2rem 0;
      background: #f5f5f5;
    }
    .poster-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2rem;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 2rem;
    }
    .poster {
      width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease;
    }
    .poster:hover {
      transform: scale(1.05);
    }
  </style>
</section>
{{ end }}
'@

$heroPath = "C:\Users\gnul\hashnhedge\layouts\partials\hero.html"
$layoutDir = Split-Path $heroPath -Parent
if (!(Test-Path $layoutDir)) {
    New-Item -ItemType Directory -Force -Path $layoutDir | Out-Null
}
Set-Content -Path $heroPath -Value $heroHTML -Encoding UTF8

Write-Host "`n✓ Created hero section partial for posters" -ForegroundColor Green

# 5. CREATE CUSTOM INDEX LAYOUT
$indexHTML = @'
{{ define "main" }}
  {{ partial "hero.html" . }}
  
  <div class="wrap mt">
    <div class="posts">
      {{ $paginator := .Paginate (where site.RegularPages "Type" "posts") 15 }}
      {{ range $paginator.Pages }}
      <article class="post">
        <a href="{{ .RelPermalink }}" class="post-link">
          {{ if .Params.featured_image }}
          <img src="{{ .Params.featured_image }}" alt="{{ .Title }}" class="post-image">
          {{ else if .Params.image }}
          <img src="{{ .Params.image }}" alt="{{ .Title }}" class="post-image">
          {{ end }}
          <div class="post-content">
            <time class="post-date">{{ .Date.Format "January 2, 2006" }}</time>
            <h2 class="post-title">{{ .Title }}</h2>
            {{ with .Summary }}
            <p class="post-summary">{{ . | truncate 150 }}</p>
            {{ end }}
          </div>
        </a>
      </article>
      {{ end }}
    </div>
    {{ partial "pager.html" . }}
  </div>
  
  <style>
    .posts {
      display: grid;
      gap: 2rem;
    }
    .post {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      overflow: hidden;
      transition: box-shadow 0.3s ease;
    }
    .post:hover {
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .post-link {
      display: block;
      text-decoration: none;
      color: inherit;
    }
    .post-image {
      width: 100%;
      height: 200px;
      object-fit: cover;
    }
    .post-content {
      padding: 1.5rem;
    }
    .post-date {
      color: #666;
      font-size: 0.9rem;
    }
    .post-title {
      margin: 0.5rem 0;
      color: #333;
    }
    .post-summary {
      color: #666;
      line-height: 1.5;
    }
  </style>
{{ end }}
'@

$indexLayoutPath = "C:\Users\gnul\hashnhedge\layouts\index.html"
Set-Content -Path $indexLayoutPath -Value $indexHTML -Encoding UTF8

Write-Host "✓ Created custom index layout with proper image handling" -ForegroundColor Green

# 6. FIX IMAGE PATHS IN POSTS
$mdFiles = Get-ChildItem -Path "$postsDir\*.md"
foreach ($file in $mdFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Fix image paths that might be broken
    $content = $content -replace 'featured_image:\s*/images/([^/]+)/hero\.webp', 'featured_image: /images/posts/$1.webp'
    $content = $content -replace 'images:\s*\n-\s*/images/([^/]+)/', 'image: /images/posts/$1.webp'
    
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
}

Write-Host "`n✓ Fixed image paths in all posts" -ForegroundColor Green

Write-Host "`n=== SITE REPAIR COMPLETE ===" -ForegroundColor Green
Write-Host "`nNEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Save your 4 poster images to: C:\Users\gnul\hashnhedge\static\images\posters\" -ForegroundColor Cyan
Write-Host "2. Name them: poster1.jpg, poster2.jpg, poster3.jpg, poster4.jpg" -ForegroundColor Cyan
Write-Host "3. Run: hugo server -s . --disableFastRender" -ForegroundColor Cyan
Write-Host "4. Your site should now fucking work" -ForegroundColor Green

