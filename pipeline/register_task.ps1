param(
  [string]$Time = "07:30",
  [int]$EveryHours = 0
)

$root = "C:\Users\gnul\hashnhedge"
$script = Join-Path $root 'pipeline\publish.ps1'
$taskName = if ($EveryHours -gt 0) { 'HashnHedgePublishEvery' + $EveryHours + 'h' } else { 'HashnHedgeDailyPublish' }

if (-not (Test-Path $script)) { throw "Pipeline script not found at $script" }

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`""

if ($EveryHours -gt 0) {
  $start = (Get-Date).AddMinutes(5)
  # Use a long but finite repetition duration (1 year) to avoid XML out-of-range issues
  $duration = [TimeSpan]::FromDays(365)
  $trigger = New-ScheduledTaskTrigger -Once -At $start -RepetitionInterval (New-TimeSpan -Hours $EveryHours) -RepetitionDuration $duration
  Write-Host "Configuring repeating trigger every $EveryHours hours (starts at $($start.ToString('u')))"
} else {
  $at = [DateTime]::ParseExact($Time,'HH:mm',$null)
  $trigger = New-ScheduledTaskTrigger -Daily -At $at
}

# Configure to run whether user is logged on or not without storing password (S4U)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest -LogonType S4U
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries

try {
  Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
} catch {}

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null

if ($EveryHours -gt 0) {
  Write-Host "Registered task '$taskName' to run every $EveryHours hours"
} else {
  Write-Host "Registered daily task '$taskName' at $Time"
}

