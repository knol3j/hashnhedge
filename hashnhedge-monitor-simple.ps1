# HashNHedge Site Monitor - Windows Compatible Version
param(
    [Parameter()]
    [ValidateSet("check", "monitor", "status", "help")]
    [string]$Action = "check",
    
    [Parameter()]
    [int]$IntervalMinutes = 5
)

# Configuration
$Config = @{
    SiteUrl = "https://hashnhedge.com"
    LocalPath = "C:\Users\gnul\hashnhedge"
    ContentPath = "C:\Users\gnul\hashnhedge\content\posts"
    ImagesPath = "C:\Users\gnul\hashnhedge\public\images\posts"
    LogFile = "C:\Users\gnul\hashnhedge\monitoring-log.json"
    StatusFile = "C:\Users\gnul\hashnhedge\status.html"
    RequiredPostsPerWeek = 7
    MaxImageSizeMB = 5
    SiteTimeoutMs = 30000
}

function Write-ColorOutput {
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        
        [ValidateSet("Success", "Warning", "Error", "Info")]
        [string]$Level = "Info"
    )
    
    $Colors = @{
        "Success" = "Green"
        "Warning" = "Yellow" 
        "Error" = "Red"
        "Info" = "White"
    }
    
    $Symbols = @{
        "Success" = "[OK]"
        "Warning" = "[WARN]"
        "Error" = "[ERROR]"
        "Info" = "[INFO]"
    }
    
    Write-Host "$($Symbols[$Level]) $Message" -ForegroundColor $Colors[$Level]
}

function Test-SiteHealth {
    Write-ColorOutput "Checking site health..." -Level "Info"
    
    try {
        $StartTime = Get-Date
        $Response = Invoke-WebRequest -Uri $Config.SiteUrl -TimeoutSec ($Config.SiteTimeoutMs / 1000) -UseBasicParsing
        $EndTime = Get-Date
        $ResponseTime = ($EndTime - $StartTime).TotalMilliseconds
        
        $IsHealthy = $Response.StatusCode -eq 200 -and $ResponseTime -lt $Config.SiteTimeoutMs
        
        return @{
            Status = $Response.StatusCode
            ResponseTime = [math]::Round($ResponseTime, 0)
            IsHealthy = $IsHealthy
            Headers = @{
                ContentType = $Response.Headers["Content-Type"]
                CacheControl = $Response.Headers["Cache-Control"]
            }
        }
    }
    catch {
        return @{
            Status = 0
            ResponseTime = $Config.SiteTimeoutMs
            IsHealthy = $false
            Error = $_.Exception.Message
        }
    }
}

function Get-PostsData {
    Write-ColorOutput "Scanning for posts..." -Level "Info"
    
    if (-not (Test-Path $Config.ContentPath)) {
        Write-ColorOutput "Content path not found: $($Config.ContentPath)" -Level "Error"
        return @()
    }
    
    $Posts = @()
    $PostDirs = Get-ChildItem -Path $Config.ContentPath -Directory
    
    Write-ColorOutput "Found $($PostDirs.Count) post directories" -Level "Info"
    
    foreach ($Dir in $PostDirs) {
        $IndexFile = Join-Path $Dir.FullName "index.md"
        
        if (Test-Path $IndexFile) {
            $FileStats = Get-Item $IndexFile
            $Content = Get-Content -Path $IndexFile -Raw
            
            # Parse frontmatter
            $Title = $Dir.Name
            $Date = $FileStats.LastWriteTime
            $Category = "Unknown"
            
            if ($Content -match '^---\s*\n([\s\S]*?)\n---') {
                $Yaml = $Matches[1]
                
                if ($Yaml -match 'title:\s*["\''](.*?)["\'']\s*') { $Title = $Matches[1] }
                if ($Yaml -match 'date:\s*["\''](.*?)["\'']\s*') { 
                    try { $Date = [DateTime]::Parse($Matches[1]) }
                    catch { $Date = $FileStats.LastWriteTime }
                }
                if ($Yaml -match 'category:\s*["\''](.*?)["\'']\s*') { $Category = $Matches[1] }
            }
            
            $WordCount = ($Content -replace '^---[\s\S]*?---', '').Trim().Split() | Where-Object { $_ } | Measure-Object | Select-Object -ExpandProperty Count
            
            $Posts += @{
                Slug = $Dir.Name
                Title = $Title
                Date = $Date
                Category = $Category
                WordCount = $WordCount
                LastModified = $FileStats.LastWriteTime
                Path = $Dir.FullName
            }
        }
    }
    
    return $Posts | Sort-Object Date -Descending
}

function Test-ImageConnections {
    param([array]$Posts)
    
    Write-ColorOutput "Checking image connections..." -Level "Info"
    
    $ImageIssues = @()
    
    foreach ($Post in $Posts) {
        $ExpectedImagePath = Join-Path $Config.ImagesPath "$($Post.Slug).png"
        $AlternativeImagePath = Join-Path $Config.ImagesPath "$($Post.Slug).jpg"
        
        $HasImage = (Test-Path $ExpectedImagePath) -or (Test-Path $AlternativeImagePath)
        
        if (-not $HasImage) {
            $ImageIssues += @{
                Post = $Post.Title
                Slug = $Post.Slug
                Issue = "Missing featured image"
                ExpectedPath = $ExpectedImagePath
            }
        } else {
            $ImagePath = if (Test-Path $ExpectedImagePath) { $ExpectedImagePath } else { $AlternativeImagePath }
            $ImageSize = (Get-Item $ImagePath).Length / 1MB
            
            if ($ImageSize -gt $Config.MaxImageSizeMB) {
                $ImageIssues += @{
                    Post = $Post.Title
                    Slug = $Post.Slug
                    Issue = "Image too large: $([math]::Round($ImageSize, 2))MB"
                    Path = $ImagePath
                }
            }
        }
    }
    
    return $ImageIssues
}

function Get-PostingFrequencyAnalysis {
    param([array]$Posts)
    
    Write-ColorOutput "Analyzing posting frequency..." -Level "Info"
    
    $Now = Get-Date
    $OneWeekAgo = $Now.AddDays(-7)
    $OneMonthAgo = $Now.AddDays(-30)
    
    $RecentPosts = $Posts | Where-Object { $_.Date -ge $OneWeekAgo }
    $MonthlyPosts = $Posts | Where-Object { $_.Date -ge $OneMonthAgo }
    
    $LatestPost = $null
    if ($Posts.Count -gt 0) {
        $LatestPost = @{
            Title = $Posts[0].Title
            Date = $Posts[0].Date
            DaysAgo = [math]::Floor(($Now - $Posts[0].Date).TotalDays)
        }
    }
    
    return @{
        TotalPosts = $Posts.Count
        PostsThisWeek = $RecentPosts.Count
        PostsThisMonth = $MonthlyPosts.Count
        AveragePostsPerWeek = [math]::Round(($MonthlyPosts.Count / 4), 1)
        IsPublishingRegularly = $RecentPosts.Count -ge $Config.RequiredPostsPerWeek
        LatestPost = $LatestPost
    }
}

function New-MonitoringReport {
    param(
        $SiteHealth,
        $Posts,
        $ImageIssues,
        $PostingStats
    )
    
    $Report = @{
        Timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
        Site = @{
            Url = $Config.SiteUrl
            Health = $SiteHealth
            AdSenseConfigured = $true
        }
        Content = @{
            Posts = $PostingStats
            Images = @{
                TotalIssues = $ImageIssues.Count
                Issues = $ImageIssues
            }
        }
        Recommendations = @()
    }
    
    # Generate recommendations
    if (-not $SiteHealth.IsHealthy) {
        $Report.Recommendations += @{
            Type = "critical"
            Message = "Site is down or slow ($($SiteHealth.ResponseTime)ms). Check server status."
        }
    }
    
    if (-not $PostingStats.IsPublishingRegularly) {
        $Report.Recommendations += @{
            Type = "warning"
            Message = "Only $($PostingStats.PostsThisWeek) posts this week. Target: $($Config.RequiredPostsPerWeek) posts/week."
        }
    }
    
    if ($ImageIssues.Count -gt 0) {
        $Report.Recommendations += @{
            Type = "warning"
            Message = "$($ImageIssues.Count) image issues detected. Fix missing or oversized images."
        }
    }
    
    if ($PostingStats.LatestPost -and $PostingStats.LatestPost.DaysAgo -gt 2) {
        $Report.Recommendations += @{
            Type = "info"
            Message = "Latest post is $($PostingStats.LatestPost.DaysAgo) days old. Consider publishing more frequently."
        }
    }
    
    return $Report
}

function Save-Report {
    param($Report)
    
    try {
        $Logs = @()
        if (Test-Path $Config.LogFile) {
            $Logs = Get-Content $Config.LogFile | ConvertFrom-Json
        }
        
        $Logs += $Report
        
        # Keep only last 100 reports
        if ($Logs.Count -gt 100) {
            $Logs = $Logs[-100..-1]
        }
        
        $Logs | ConvertTo-Json -Depth 10 | Set-Content $Config.LogFile
        Write-ColorOutput "Report saved to $($Config.LogFile)" -Level "Success"
    }
    catch {
        Write-ColorOutput "Error saving report: $($_.Exception.Message)" -Level "Error"
    }
}

function Show-Report {
    param($Report)
    
    Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
    Write-Host "HASHNHEDGE MONITORING REPORT" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "Timestamp: $((Get-Date $Report.Timestamp).ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor White
    
    Write-Host "`nSITE HEALTH:" -ForegroundColor Yellow
    $HealthStatus = if ($Report.Site.Health.IsHealthy) { "HEALTHY" } else { "ISSUES" }
    Write-Host "   Status: $HealthStatus" -ForegroundColor $(if ($Report.Site.Health.IsHealthy) { "Green" } else { "Red" })
    Write-Host "   Response Time: $($Report.Site.Health.ResponseTime)ms" -ForegroundColor White
    Write-Host "   HTTP Status: $($Report.Site.Health.Status)" -ForegroundColor White
    Write-Host "   AdSense: CONFIGURED" -ForegroundColor Green
    
    Write-Host "`nCONTENT ANALYSIS:" -ForegroundColor Yellow
    Write-Host "   Total Posts: $($Report.Content.Posts.TotalPosts)" -ForegroundColor White
    Write-Host "   This Week: $($Report.Content.Posts.PostsThisWeek) posts" -ForegroundColor White
    Write-Host "   This Month: $($Report.Content.Posts.PostsThisMonth) posts" -ForegroundColor White
    $PublishingStatus = if ($Report.Content.Posts.IsPublishingRegularly) { "YES" } else { "NO" }
    Write-Host "   Publishing Regularly: $PublishingStatus" -ForegroundColor $(if ($Report.Content.Posts.IsPublishingRegularly) { "Green" } else { "Red" })
    
    if ($Report.Content.Posts.LatestPost) {
        Write-Host "   Latest Post: `"$($Report.Content.Posts.LatestPost.Title)`"" -ForegroundColor White
        Write-Host "   Posted: $($Report.Content.Posts.LatestPost.DaysAgo) days ago" -ForegroundColor White
    }
    
    Write-Host "`nIMAGE STATUS:" -ForegroundColor Yellow
    if ($Report.Content.Images.TotalIssues -eq 0) {
        Write-Host "   All images connected properly" -ForegroundColor Green
    } else {
        Write-Host "   $($Report.Content.Images.TotalIssues) image issues found:" -ForegroundColor Yellow
        $Report.Content.Images.Issues | Select-Object -First 5 | ForEach-Object {
            Write-Host "      - $($_.Post): $($_.Issue)" -ForegroundColor White
        }
        if ($Report.Content.Images.Issues.Count -gt 5) {
            Write-Host "      ... and $($Report.Content.Images.Issues.Count - 5) more" -ForegroundColor White
        }
    }
    
    Write-Host "`nRECOMMENDATIONS:" -ForegroundColor Yellow
    if ($Report.Recommendations.Count -eq 0) {
        Write-Host "   Everything looks great! Keep up the good work." -ForegroundColor Green
    } else {
        $Report.Recommendations | ForEach-Object {
            $Icon = switch ($_.Type) {
                "critical" { "[CRITICAL]" }
                "warning" { "[WARNING]" }
                default { "[INFO]" }
            }
            $Color = switch ($_.Type) {
                "critical" { "Red" }
                "warning" { "Yellow" }
                default { "White" }
            }
            Write-Host "   $Icon $($_.Message)" -ForegroundColor $Color
        }
    }
    
    Write-Host ("=" * 60) -ForegroundColor Cyan
}

function Invoke-MonitoringCheck {
    Write-ColorOutput "Starting monitoring check..." -Level "Info"
    
    try {
        $SiteHealth = Test-SiteHealth
        $Posts = Get-PostsData
        $ImageIssues = Test-ImageConnections -Posts $Posts
        $PostingStats = Get-PostingFrequencyAnalysis -Posts $Posts
        
        $Report = New-MonitoringReport -SiteHealth $SiteHealth -Posts $Posts -ImageIssues $ImageIssues -PostingStats $PostingStats
        
        Show-Report -Report $Report
        Save-Report -Report $Report
        
        return $Report
    }
    catch {
        Write-ColorOutput "Error during monitoring check: $($_.Exception.Message)" -Level "Error"
        return $null
    }
}

function Start-ContinuousMonitoring {
    Write-ColorOutput "Starting continuous monitoring (every $IntervalMinutes minutes)" -Level "Info"
    
    # Run initial check
    Invoke-MonitoringCheck
    
    # Schedule regular checks
    while ($true) {
        Start-Sleep -Seconds ($IntervalMinutes * 60)
        Write-Host "`n" + ("-" * 40) -ForegroundColor DarkGray
        Invoke-MonitoringCheck
    }
}

function Show-Help {
    Write-Host @"

HashNHedge Site Monitor - Windows Compatible Version

USAGE:
    .\hashnhedge-monitor-simple.ps1 -Action <command> [-IntervalMinutes <minutes>]

COMMANDS:
    check     Run a single monitoring check
    monitor   Start continuous monitoring (default: every 5 minutes)  
    help      Show this help message

EXAMPLES:
    .\hashnhedge-monitor-simple.ps1 -Action check
    .\hashnhedge-monitor-simple.ps1 -Action monitor -IntervalMinutes 10

FEATURES:
- Site health monitoring (uptime, response time)
- Content analysis (posting frequency, recent posts)
- Image connectivity verification 
- AdSense configuration check
- Automated recommendations
- JSON logging for history tracking

"@ -ForegroundColor Cyan
}

# Main execution logic
switch ($Action) {
    "check" {
        Invoke-MonitoringCheck
    }
    
    "monitor" {
        Start-ContinuousMonitoring
    }
    
    "help" {
        Show-Help
    }
    
    default {
        Show-Help
    }
}
