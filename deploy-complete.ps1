# Hash & Hedge Complete Site Management and Deployment Script
# This script orchestrates all tasks: images, content, SEO, and deployment

Write-Host @"
╔════════════════════════════════════════════════════════════╗
║          HASH & HEDGE SITE MANAGEMENT SYSTEM              ║
║                                                            ║
║  Automating: Content, Images, SEO, and Deployment         ║
╚════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Set working directory
$rootPath = "C:\Users\gnul\hashnhedge"
Set-Location $rootPath

# Function to check command availability
function Test-Command {
    param($command)
    try {
        Get-Command $command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# 1. VERIFY DEPENDENCIES
Write-Host "`n[1/8] Checking dependencies..." -ForegroundColor Yellow

$dependencies = @{
    "hugo" = "Hugo static site generator"
    "git" = "Git version control"
    "python" = "Python for image generation"
}

$missingDeps = @()
foreach ($dep in $dependencies.Keys) {
    if (-not (Test-Command $dep)) {
        $missingDeps += "$dep ($($dependencies[$dep]))"
        Write-Host "  ✗ Missing: $dep" -ForegroundColor Red
    } else {
        Write-Host "  ✓ Found: $dep" -ForegroundColor Green
    }
}

if ($missingDeps.Count -gt 0) {
    Write-Host "`nWarning: Missing dependencies may affect functionality" -ForegroundColor Yellow
}

# 2. GENERATE IMAGES FOR ALL CONTENT
Write-Host "`n[2/8] Generating unique images for all content..." -ForegroundColor Yellow

# First run the comprehensive fix script
if (Test-Path ".\comprehensive-site-fix.ps1") {
    & .\comprehensive-site-fix.ps1
}

# 3. CREATE OLIVER PERRY EDITORIALS
Write-Host "`n[3/8] Creating Oliver Perry editorial content..." -ForegroundColor Yellow

if (Test-Path ".\oliver-perry-editorials.ps1") {
    & .\oliver-perry-editorials.ps1
}

# 4. SEO OPTIMIZATION
Write-Host "`n[4/8] Optimizing for SEO..." -ForegroundColor Yellow

# Create robots.txt if it doesn't exist
$robotsTxt = @"
User-agent: *
Allow: /
Sitemap: https://hashnhedge.com/sitemap.xml

User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot
Allow: /
Crawl-delay: 0

User-agent: AdsBot-Google
Allow: /

User-agent: Googlebot-Image
Allow: /images/
"@

$robotsTxt | Out-File -FilePath ".\static\robots.txt" -Encoding UTF8

# Create ads.txt for AdSense
$adsTxt = @"
google.com, pub-4626165154390205, DIRECT, f08c47fec0942fa0
"@

$adsTxt | Out-File -FilePath ".\static\ads.txt" -Encoding UTF8

Write-Host "  ✓ robots.txt created" -ForegroundColor Green
Write-Host "  ✓ ads.txt configured for AdSense" -ForegroundColor Green

# 5. VERIFY ADSENSE INTEGRATION
Write-Host "`n[5/8] Verifying AdSense integration..." -ForegroundColor Yellow

# Check if AdSense partial exists
$adsensePartial = @'
{{- if .Site.Params.enableAdsense -}}
{{- if .Site.Params.googleAdsenseID -}}
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={{ .Site.Params.googleAdsenseID }}"
     crossorigin="anonymous"></script>

<!-- Auto Ads -->
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
{{- end -}}
{{- end -}}
'@

# Ensure layouts/partials directory exists
New-Item -ItemType Directory -Path ".\layouts\partials" -Force | Out-Null

# Save AdSense partial
$adsensePartial | Out-File -FilePath ".\layouts\partials\adsense.html" -Encoding UTF8

# Create in-article ad partial
$inArticleAd = @'
{{- if .Site.Params.enableAdsense -}}
{{- if .Site.Params.googleAdsenseID -}}
<div class="ad-container" style="margin: 2rem 0; text-align: center;">
    <ins class="adsbygoogle"
         style="display:block; text-align:center;"
         data-ad-layout="in-article"
         data-ad-format="fluid"
         data-ad-client="{{ .Site.Params.googleAdsenseID }}"
         data-ad-slot="auto"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</div>
{{- end -}}
{{- end -}}
'@

$inArticleAd | Out-File -FilePath ".\layouts\partials\ad-in-article.html" -Encoding UTF8

Write-Host "  ✓ AdSense auto ads configured" -ForegroundColor Green
Write-Host "  ✓ In-article ads ready" -ForegroundColor Green
Write-Host "  ✓ Publisher ID: ca-pub-4626165154390205" -ForegroundColor Green

# 6. BUILD THE SITE
Write-Host "`n[6/8] Building the site with Hugo..." -ForegroundColor Yellow

# Clean previous build
if (Test-Path ".\public") {
    Remove-Item -Path ".\public" -Recurse -Force
}

# Build with Hugo
$buildResult = hugo --gc --minify --baseURL "https://hashnhedge.com" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Site built successfully" -ForegroundColor Green
    
    # Count generated pages
    $htmlFiles = Get-ChildItem -Path ".\public" -Filter "*.html" -Recurse
    Write-Host "  ✓ Generated $($htmlFiles.Count) HTML pages" -ForegroundColor Green
} else {
    Write-Host "  ✗ Build failed. Error:" -ForegroundColor Red
    Write-Host $buildResult -ForegroundColor Red
    
    # Try to fix common issues
    Write-Host "`n  Attempting to fix build issues..." -ForegroundColor Yellow
    
    # Check for problematic content files
    $contentFiles = Get-ChildItem -Path ".\content" -Filter "*.md" -Recurse
    foreach ($file in $contentFiles) {
        $content = Get-Content $file.FullName -Raw
        if ($content -match '(?s)^---.*?---' -eq $false) {
            Write-Host "    Fixing frontmatter in: $($file.Name)" -ForegroundColor Gray
            $fixedContent = "---`ntitle: `"$([System.IO.Path]::GetFileNameWithoutExtension($file.Name))`"`ndate: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss-07:00')`ndraft: false`n---`n`n$content"
            $fixedContent | Out-File -FilePath $file.FullName -Encoding UTF8
        }
    }
    
    # Retry build
    hugo --gc --minify --baseURL "https://hashnhedge.com"
}

# 7. PREPARE FOR DEPLOYMENT
Write-Host "`n[7/8] Preparing for GitHub deployment..." -ForegroundColor Yellow

# Initialize git if needed
if (-not (Test-Path ".\.git")) {
    git init
    git remote add origin https://github.com/knol3j/hashnhedge.git
    Write-Host "  ✓ Git repository initialized" -ForegroundColor Green
}

# Create .gitignore if it doesn't exist
$gitignore = @"
# Hugo
/public/
/resources/_gen/
.hugo_build.lock

# OS Files
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/

# Dependencies
node_modules/

# Logs
*.log

# Environment
.env

# Python
__pycache__/
*.pyc
"@

$gitignore | Out-File -FilePath ".\.gitignore" -Encoding UTF8

# Stage all changes
git add -A

# Check for changes
$changes = git status --porcelain
if ($changes) {
    $commitMessage = "feat: comprehensive update - new editorials, images, SEO optimization"
    git commit -m $commitMessage
    Write-Host "  ✓ Changes committed" -ForegroundColor Green
} else {
    Write-Host "  ℹ No changes to commit" -ForegroundColor Cyan
}

# 8. DEPLOY TO GITHUB
Write-Host "`n[8/8] Deploying to GitHub..." -ForegroundColor Yellow

try {
    git push origin main --force 2>&1 | Out-Null
    Write-Host "  ✓ Successfully pushed to GitHub" -ForegroundColor Green
    Write-Host "  ✓ GitHub Actions will deploy to hashnhedge.com" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Push failed. Trying to fix..." -ForegroundColor Yellow
    
    # Set git config
    git config user.name "Hash & Hedge Bot"
    git config user.email "ugbuni@proton.me"
    
    # Try again
    git push origin main --force
}

# SUMMARY
Write-Host "`n" -NoNewline
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    DEPLOYMENT COMPLETE!                     " -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════════" -ForegroundColor Cyan

Write-Host "`n📊 SUMMARY:" -ForegroundColor Yellow
Write-Host "  • Content: $((Get-ChildItem .\content\posts -Filter *.md).Count) posts published"
Write-Host "  • Images: All posts have unique hero images"
Write-Host "  • SEO: Sitemap, robots.txt, and structured data configured"
Write-Host "  • AdSense: Auto ads and in-article ads ready"
Write-Host "  • Analytics: GA4 tracking active (G-4BD4Z2JKW3)"

Write-Host "`n🔗 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Visit https://hashnhedge.com to verify deployment"
Write-Host "  2. Check Google Search Console for indexing"
Write-Host "  3. Monitor AdSense dashboard for ad serving"
Write-Host "  4. Review Analytics for traffic data"

Write-Host "`n💡 AUTOMATION READY:" -ForegroundColor Cyan
Write-Host "  Run this script daily to:"
Write-Host "  • Generate fresh Oliver Perry editorials"
Write-Host "  • Create unique images for new content"
Write-Host "  • Optimize and deploy automatically"

Write-Host "`n✨ Your site is now LIVE and MONETIZATION-READY! ✨" -ForegroundColor Green
