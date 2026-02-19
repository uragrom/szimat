@echo off
setlocal
cd /d "%~dp0"

net session >nul 2>&1
if not %errorlevel%==0 (
    echo ERROR: Run as Administrator!
    pause
    exit /b 1
)

echo Removing context menu entries...
python install_runner.py --remove
pause
endlocal
