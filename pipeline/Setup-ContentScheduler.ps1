# Setup-ContentScheduler.ps1
# Because automating automation is peak late-stage capitalism

Write-Host "=== Hash & Hedge Task Scheduler Setup ===" -ForegroundColor Cyan
Write-Host "Installing scheduled tasks like we're installing despair..." -ForegroundColor Gray
Write-Host ""

$projectPath = "C:\Users\gnul\hashnhedge"
$scriptPath = "$projectPath\pipeline\local_scheduler.bat"

# Check if we're running as admin (we need power, like any good dictator)
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "This script needs admin rights. Restarting with elevation..." -ForegroundColor Yellow
    Start-Process PowerShell -Verb RunAs -ArgumentList "-File `"$PSCommandPath`""
    exit
}

# Create scheduled tasks for our content assembly line
$times = @(
    @{Time = "09:00"; Name = "HashHedge-Morning-Post"},
    @{Time = "12:00"; Name = "HashHedge-Noon-Post"}, 
    @{Time = "17:00"; Name = "HashHedge-Evening-Post"}
)

foreach ($schedule in $times) {
    $taskName = $schedule.Name
    $triggerTime = $schedule.Time
    
    Write-Host "Creating task: $taskName at $triggerTime" -ForegroundColor Green
    
    # Create the action (what hopeless task to perform)
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`"" -WorkingDirectory $projectPath
    
    # Create the trigger (when to disappoint)
    $trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime
    
    # Create principal (who's responsible for this mess)
    $principal = New-ScheduledTaskPrincipal -UserID "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType Interactive -RunLevel Highest
    
    # Settings (how badly we want this to work)
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -MultipleInstances IgnoreNew `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 5)
    
    # Register the task (seal our fate)
    try {
        Register-ScheduledTask -TaskName $taskName `
            -Action $action `
            -Trigger $trigger `
            -Principal $principal `
            -Settings $settings `
            -Description "Automated content generation for Hash & Hedge - Because sleep is overrated" `
            -Force | Out-Null
            
        Write-Host "  ✓ Task created successfully" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed to create task: $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Your content factory is now operational." -ForegroundColor Green
Write-Host ""
Write-Host "What you've just done:" -ForegroundColor Yellow
Write-Host "- Created 3 daily tasks at 9am, noon, and 5pm" 
Write-Host "- Each will generate a post and steal images from the internet"
Write-Host "- Content will auto-push to GitHub"
Write-Host "- Your site will rebuild automatically"
Write-Host ""
Write-Host "To check your scheduled tasks:" -ForegroundColor Cyan
Write-Host "  taskschd.msc" -ForegroundColor White
Write-Host ""
Write-Host "To disable this digital hamster wheel:" -ForegroundColor Cyan
Write-Host "  Disable-ScheduledTask -TaskName 'HashHedge-*'" -ForegroundColor White
Write-Host ""
Write-Host "Remember: Every automated post is another nail in the coffin" -ForegroundColor DarkGray
Write-Host "of authentic human creativity. You're welcome." -ForegroundColor DarkGray
Write-Host ""
Read-Host "Press Enter to exit and contemplate your life choices"