#!/bin/bash
# Test runner script for Linux/Mac

echo "========================================"
echo "InsightEDU3.2 Test Runner"
echo "========================================"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Virtual environment not detected."
    echo "Please activate your virtual environment first:"
    echo "  source env/bin/activate"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Running tests..."
echo ""

# Run tests with coverage
pytest -v --cov=AppClassificationOfLD --cov-report=html --cov-report=term-missing

echo ""
echo "========================================"
echo "Test execution complete!"
echo ""
echo "Coverage report generated in: htmlcov/index.html"
echo ""

