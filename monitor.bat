@echo off
echo 🚀 HashNHedge Site Monitor
echo ========================

if "%1"=="" (
    echo Usage: monitor.bat [check^|monitor^|status]
    echo.
    echo Commands:
    echo   check   - Run single check
    echo   monitor - Start continuous monitoring
    echo   status  - Generate status page
    echo.
    goto :end
)

if "%1"=="check" (
    echo Running single monitoring check...
    powershell -ExecutionPolicy Bypass -File "%~dp0hashnhedge-monitor-simple.ps1" -Action check
    goto :end
)

if "%1"=="monitor" (
    echo Starting continuous monitoring...
    powershell -ExecutionPolicy Bypass -File "%~dp0hashnhedge-monitor-simple.ps1" -Action monitor
    goto :end
)

if "%1"=="status" (
    echo Generating monitoring report...
    powershell -ExecutionPolicy Bypass -File "%~dp0hashnhedge-monitor-simple.ps1" -Action check
    if exist "%~dp0monitoring-log.json" (
        echo.
        echo Latest monitoring data saved to: monitoring-log.json
        echo You can view the detailed JSON report in that file.
    )
    goto :end
)

echo Invalid command: %1
echo Use: monitor.bat [check^|monitor^|status]

:end
pause
