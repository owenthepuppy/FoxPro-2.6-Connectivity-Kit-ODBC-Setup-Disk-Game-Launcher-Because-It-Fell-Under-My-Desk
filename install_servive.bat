@echo off
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

schtasks /create /tn "FoxPro 2.6 Connectivity Kit ODBC Setup Disk Game Launcher Because It Fell Under My Desk" /tr "pythonw.exe \"%~dp0main.py\"" /sc onlogon /rl highest /f
echo If there's no errors above, the install probably worked
pause