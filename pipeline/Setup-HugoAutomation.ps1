# Setup scheduled tasks for Hugo content generation
Write-Host "Setting up Hash & Hedge content automation..." -ForegroundColor Cyan

$taskPath = "C:\Users\gnul\hashnhedge\pipeline\hugo_content_scheduler.bat"

# Create 3 daily tasks
$times = @("08:00", "14:00", "20:00")
foreach ($time in $times) {
    $taskName = "HashHedge-Post-$($time.Replace(':', ''))"
    
    # Remove existing
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Create new
    $action = New-ScheduledTaskAction -Execute $taskPath
    $trigger = New-ScheduledTaskTrigger -Daily -At $time
    $principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings
    Write-Host "[OK] Created task: $taskName at $time" -ForegroundColor Green
}

Write-Host "`nSetup complete! Content will be generated 3 times daily." -ForegroundColor Green
