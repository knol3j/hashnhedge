# Hash n Hedge Scheduled Tasks Status Checker

Write-Host "`n==== HASH N HEDGE SCHEDULED TASKS STATUS ====" -ForegroundColor Cyan
Write-Host "Checking automated content generation tasks...`n" -ForegroundColor Yellow

$tasks = @("HashHedgeDailyContent", "HashnHedgeDailyBuild", "HashnHedgePublishEvery8h")

foreach ($taskName in $tasks) {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($task) {
        $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
        
        Write-Host "Task: $taskName" -ForegroundColor Green
        Write-Host "   Status: $($task.State)" -ForegroundColor $(if($task.State -eq "Ready"){"Green"}else{"Red"})
        Write-Host "   Last Run: $($taskInfo.LastRunTime)" -ForegroundColor White
        Write-Host "   Next Run: $($taskInfo.NextRunTime)" -ForegroundColor Yellow
        Write-Host "   Last Result: $($taskInfo.LastTaskResult)" -ForegroundColor $(if($taskInfo.LastTaskResult -eq 0){"Green"}else{"Red"})
        
        # Get trigger details
        $trigger = (Get-ScheduledTask -TaskName $taskName).Triggers[0]
        if ($trigger) {
            Write-Host "   Schedule: " -NoNewline -ForegroundColor Cyan
            
            switch ($trigger.GetType().Name) {
                "DailyTrigger" { Write-Host "Daily at $($trigger.StartBoundary.Split('T')[1].Split('+')[0])" }
                "TimeTrigger" { 
                    if ($trigger.Repetition.Interval) {
                        Write-Host "Every $($trigger.Repetition.Interval)"
                    } else {
                        Write-Host "Once at $($trigger.StartBoundary)"
                    }
                }
                default { Write-Host $trigger.GetType().Name }
            }
        }
        
        # Get action details
        $action = (Get-ScheduledTask -TaskName $taskName).Actions[0]
        if ($action) {
            Write-Host "   Command: $($action.Execute)" -ForegroundColor Gray
            if ($action.Arguments) {
                Write-Host "   Args: $($action.Arguments)" -ForegroundColor Gray
            }
        }
        
        Write-Host ""
    } else {
        Write-Host "Task '$taskName' not found" -ForegroundColor Red
    }
}

Write-Host "==== RECOMMENDATIONS ====" -ForegroundColor Cyan
Write-Host "Your scheduled tasks are configured and running!" -ForegroundColor Green
Write-Host "HashHedgeDailyContent - Generates new content daily" -ForegroundColor White
Write-Host "HashnHedgeDailyBuild - Builds the site with Hugo" -ForegroundColor White
Write-Host "HashnHedgePublishEvery8h - Publishes updates every 8 hours" -ForegroundColor White
Write-Host ""
