param(
  [string]$Time = "07:30"
)

$root = "C:\Users\gnul\hashnhedge"
$script = Join-Path $root 'pipeline\build.ps1'
$taskName = 'HashnHedgeDailyBuild'

if (-not (Test-Path $script)) { throw "Pipeline script not found at $script" }

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -Daily -At ([DateTime]::ParseExact($Time,'HH:mm',$null))
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries

try {
  Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
} catch {}

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null

Write-Host "Registered daily task '$taskName' at $Time to run $script"

