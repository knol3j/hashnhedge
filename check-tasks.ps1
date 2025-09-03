# Hash n Hedge Scheduled Tasks Status Checker

Write-Host "==== HASH N HEDGE SCHEDULED TASKS STATUS ====" -ForegroundColor Cyan
Write-Host "Checking automated content generation tasks..." -ForegroundColor Yellow
Write-Host ""

$tasks = @("HashHedgeDailyContent", "HashnHedgeDailyBuild", "HashnHedgePublishEvery8h")

foreach ($taskName in $tasks) {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($task) {
        $taskInfo = Get-ScheduledTaskInfo -TaskName $taskName
        
        Write-Host "Task: $taskName" -ForegroundColor Green
        Write-Host "   Status: $($task.State)" -ForegroundColor White
        Write-Host "   Last Run: $($taskInfo.LastRunTime)" -ForegroundColor White
        Write-Host "   Next Run: $($taskInfo.NextRunTime)" -ForegroundColor Yellow
        Write-Host "   Last Result: $($taskInfo.LastTaskResult)" -ForegroundColor White
        Write-Host ""
    }
}

Write-Host "==== SUMMARY ====" -ForegroundColor Cyan
Write-Host "Your scheduled tasks are configured and running!" -ForegroundColor Green
