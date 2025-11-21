@echo off
REM Test runner script for Windows

echo ========================================
echo InsightEDU3.2 Test Runner
echo ========================================
echo.

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo Warning: Virtual environment not detected.
    echo Please activate your virtual environment first:
    echo   env\Scripts\activate
    echo.
    pause
    exit /b 1
)

echo Running tests...
echo.

REM Run tests with coverage
pytest -v --cov=AppClassificationOfLD --cov-report=html --cov-report=term-missing

echo.
echo ========================================
echo Test execution complete!
echo.
echo Coverage report generated in: htmlcov\index.html
echo.
pause

