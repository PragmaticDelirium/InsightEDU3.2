#!/bin/bash
# Setup script for development tools (linting, formatting, pre-commit hooks)

echo "Setting up development tools for InsightEDU3.2..."

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Virtual environment not detected."
    echo "Please activate your virtual environment first:"
    echo "  Windows: env\\Scripts\\activate"
    echo "  Linux/Mac: source env/bin/activate"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo ""
echo "Setup complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Run 'pre-commit run --all-files' to check all files"
echo "2. Run 'black .' to format all Python files"
echo "3. Run 'flake8 .' to check for linting issues"
echo "4. Run 'pylint AppClassificationOfLD' to check code quality"
echo ""
echo "Pre-commit hooks will now run automatically on git commit."


