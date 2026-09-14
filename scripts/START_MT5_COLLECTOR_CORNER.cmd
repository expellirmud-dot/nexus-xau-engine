@echo off
cd /d D:\nexus-xau-engine-repo
start "" powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -Command "$root='D:\nexus-xau-engine-repo'; $py=Join-Path $root '.venv\Scripts\python.exe'; if (-not (Get-NetTCPConnection -State Listen -LocalPort 8765 -ErrorAction SilentlyContinue)) { Start-Process -FilePath $py -ArgumentList 'scripts\mt5_collector_dashboard.py' -WorkingDirectory $root -WindowStyle Hidden }; Start-Process -FilePath $py -ArgumentList 'scripts\mt5_collector_corner.py' -WorkingDirectory $root -WindowStyle Hidden"
exit /b 0
