@echo off
echo ============================================================
echo COMP 3603 Research Symposium - Virtual Research Gallery
echo ============================================================
echo.
echo Choose an option:
echo 1. Initialize database and start app (flask init + flask run)
echo 2. Just start the app (flask run)
echo 3. Run with Python directly (python run.py)
echo.
echo ============================================================
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Initializing database...
    flask init
    echo.
    echo Starting application with Flask CLI...
    flask run
) else if "%choice%"=="2" (
    echo.
    echo Starting application with Flask CLI...
    flask run
) else if "%choice%"=="3" (
    echo.
    echo Starting application with Python...
    python run.py
) else (
    echo Invalid choice. Starting with Flask CLI...
    flask run
)

pause
