@echo off
REM Setup script for development tools (linting, formatting, pre-commit hooks) - Windows

echo Setting up development tools for InsightEDU3.2...

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo Warning: Virtual environment not detected.
    echo Please activate your virtual environment first:
    echo   env\Scripts\activate
    pause
    exit /b 1
)

REM Install development dependencies
echo Installing development dependencies...
pip install -r requirements-dev.txt

REM Install pre-commit hooks
echo Installing pre-commit hooks...
pre-commit install

echo.
echo Setup complete! ^_^
echo.
echo Next steps:
echo 1. Run 'pre-commit run --all-files' to check all files
echo 2. Run 'black .' to format all Python files
echo 3. Run 'flake8 .' to check for linting issues
echo 4. Run 'pylint AppClassificationOfLD' to check code quality
echo.
echo Pre-commit hooks will now run automatically on git commit.
pause


