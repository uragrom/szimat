@echo off
setlocal
cd /d "%~dp0"

REM Check admin rights
net session >nul 2>&1
if not %errorlevel%==0 (
    echo ERROR: Run as Administrator! Right-click install.bat - Run as administrator
    pause
    exit /b 1
)

python install_runner.py
set PY_ERR=%errorlevel%
if not %PY_ERR%==0 (
    echo.
    echo Installation failed. Check messages above.
)

pause
endlocal
exit /b %PY_ERR%
