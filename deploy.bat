@echo off
echo Device Monitor - Deployment Tool
echo ==============================
echo.

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

echo Choose deployment option:
echo 1. Create executable only
echo 2. Create Windows installer (requires Inno Setup)
echo 3. Build both executable and installer
echo.

set /p option="Enter option (1-3): "

if "%option%"=="1" (
    echo Creating executable...
    python build.py
) else if "%option%"=="2" (
    echo Creating Windows installer...
    python create_installer.py
) else if "%option%"=="3" (
    echo Creating executable and installer...
    python create_installer.py
) else (
    echo Invalid option. Please run again and select options 1-3.
    exit /b 1
)

echo.
echo Deployment complete!
pause 