# Setup-HugoScheduler.ps1
# Sets up automated content generation for Hash & Hedge Hugo site

Write-Host "=== Hash & Hedge Hugo Automated Content Setup ===" -ForegroundColor Cyan
Write-Host "Setting up scheduled tasks for content generation..." -ForegroundColor Gray
Write-Host ""

$projectPath = "C:\Users\gnul\hashnhedge"
$scriptPath = "$projectPath\pipeline\hugo_scheduler.bat"

# Check if running as admin
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "This script needs admin rights. Please run as Administrator." -ForegroundColor Red
    Write-Host "Right-click on PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit
}

# Create scheduled tasks
$schedules = @(
    @{Name = "HashHedge-Morning-Post"; Time = "09:00"},
    @{Name = "HashHedge-Afternoon-Post"; Time = "15:00"},
    @{Name = "HashHedge-Evening-Post"; Time = "21:00"}
)

foreach ($schedule in $schedules) {
    $taskName = $schedule.Name
    $triggerTime = $schedule.Time
    
    Write-Host "Creating task: $taskName at $triggerTime" -ForegroundColor Green
    
    # Remove existing task if it exists
    try {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    } catch {}
    
    # Create the action
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`"" -WorkingDirectory $projectPath
    
    # Create the trigger 
    $trigger = New-ScheduledTaskTrigger -Daily -At $triggerTime
    
    # Create principal
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
        -LogonType Interactive -RunLevel Limited
    
    # Settings
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -MultipleInstances IgnoreNew `
        -RestartCount 3 `
        -RestartInterval (New-TimeSpan -Minutes 5)
    
    # Register the task
    try {
        Register-ScheduledTask -TaskName $taskName `
            -Action $action `
            -Trigger $trigger `
            -Principal $principal `
            -Settings $settings `
            -Description "Automated content generation for Hash & Hedge Hugo site" `
            -Force
        
        Write-Host "  -> Task created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "  -> Failed to create task: $_" -ForegroundColor Red
    }
}

# Create a manual trigger task
Write-Host "`nCreating manual content generation task..." -ForegroundColor Yellow
$manualTaskName = "HashHedge-Generate-Content-Now"

try {
    Unregister-ScheduledTask -TaskName $manualTaskName -Confirm:$false -ErrorAction SilentlyContinue
} catch {}

$manualAction = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`""
Register-ScheduledTask -TaskName $manualTaskName `
    -Action $manualAction `
    -Description "Manual content generation for Hash & Hedge" `
    -Force

Write-Host "  -> Manual task created!" -ForegroundColor Green

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Green
Write-Host "Scheduled tasks created for: 9:00 AM, 3:00 PM, and 9:00 PM daily" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run content generation manually:" -ForegroundColor Yellow
Write-Host "  1. Open Task Scheduler" 
Write-Host "  2. Find 'HashHedge-Generate-Content-Now'"
Write-Host "  3. Right-click and select 'Run'"
Write-Host ""
Write-Host "Or run directly from command line:" -ForegroundColor Yellow
Write-Host "  $scriptPath"
Write-Host ""
pause