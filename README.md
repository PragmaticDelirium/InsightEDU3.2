# InsightEDU3.2

Early Identification & Support for Learning Differences

## 📚 Documentation

Comprehensive documentation is available for different audiences:

- **[Project Report](PROJECT_REPORT.md)** - Comprehensive project overview, features, and analysis
- **[Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Technical specifications, API reference, and architecture
- **[Installation Guide](INSTALLATION_GUIDE.md)** - Step-by-step installation and setup instructions
- **[User Manual](USER_MANUAL.md)** - End-user guide for using the system
- **[Documentation Index](DOCUMENTATION_INDEX.md)** - Complete documentation index and quick reference

**Quick Links:**
- 🚀 **New to the project?** Start with [Project Report](PROJECT_REPORT.md)
- 👨‍💻 **Developer?** See [Technical Documentation](TECHNICAL_DOCUMENTATION.md) and [Installation Guide](INSTALLATION_GUIDE.md)
- 👤 **End User?** See [User Manual](USER_MANUAL.md)
- 🔧 **Setting up?** Follow [Installation Guide](INSTALLATION_GUIDE.md)
- 🔗 **Technology Stack?** See [Technology Stack & Integration](TECHNOLOGY_STACK_AND_INTEGRATION.md)

## Development Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Activate your virtual environment:**
   ```bash
   # Windows
   env\Scripts\activate
   
   # Linux/Mac
   source env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   pip install -r requirements-dev.txt
   ```

3. **Setup development tools:**
   ```bash
   # Windows
   setup-dev-tools.bat
   
   # Linux/Mac
   chmod +x setup-dev-tools.sh
   ./setup-dev-tools.sh
   ```

   Or manually:
   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

## Code Quality Tools

This project uses several tools to maintain code quality:

### Black (Code Formatter)
Automatically formats Python code to a consistent style.

**Usage:**
```bash
# Format all files
black .

# Check what would be changed
black --check .

# Format specific file/directory
black AppClassificationOfLD/views.py
```

**Configuration:** `pyproject.toml`

### Flake8 (Linter)
Checks for style guide violations and programming errors.

**Usage:**
```bash
# Check all files
flake8 .

# Check specific directory
flake8 AppClassificationOfLD/

# Show statistics
flake8 --statistics .
```

**Configuration:** `.flake8`

### Pylint (Code Analyzer)
Performs deeper code analysis and provides detailed reports.

**Usage:**
```bash
# Check entire project
pylint AppClassificationOfLD/

# Check specific file
pylint AppClassificationOfLD/views.py

# Generate HTML report
pylint --output-format=html AppClassificationOfLD/ > pylint_report.html
```

**Configuration:** `.pylintrc`

### Pre-commit Hooks
Automatically runs code quality checks before each commit.

**Usage:**
```bash
# Install hooks (done during setup)
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run hooks on staged files only (automatic on commit)
pre-commit run

# Skip hooks for a commit (not recommended)
git commit --no-verify
```

**Configuration:** `.pre-commit-config.yaml`

## Pre-commit Hooks Included

The following checks run automatically before each commit:

1. **Trailing whitespace** - Removes trailing whitespace
2. **End of file fixer** - Ensures files end with newline
3. **YAML/JSON/TOML checker** - Validates configuration files
4. **Large file checker** - Prevents committing large files
5. **Merge conflict checker** - Detects merge conflict markers
6. **Black** - Formats Python code
7. **isort** - Sorts imports
8. **Flake8** - Lints Python code
9. **Pylint** - Analyzes code quality
10. **MyPy** - Type checking (optional)

## Running All Checks Manually

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Analyze code
pylint AppClassificationOfLD/

# Or run all pre-commit hooks
pre-commit run --all-files
```

## Configuration Files

- `.flake8` - Flake8 configuration
- `.pylintrc` - Pylint configuration
- `pyproject.toml` - Black and isort configuration
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `requirements-dev.txt` - Development dependencies

## IDE Integration

### VS Code
Install these extensions:
- Python (Microsoft)
- Black Formatter
- Pylint
- Flake8

Add to `.vscode/settings.json`:
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### PyCharm
1. Go to Settings → Tools → Black
2. Enable "Use Black"
3. Set line length to 100
4. Enable "On code reformat" and "On save"

## Continuous Integration

To use these tools in CI/CD, add to your pipeline:

```yaml
# Example GitHub Actions
- name: Run pre-commit
  run: pre-commit run --all-files
```

## Troubleshooting

### Pre-commit hooks not running
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Flake8 errors after Black formatting
This is normal - Black and Flake8 have some conflicting rules. The configuration ignores these conflicts (E203, W503, E501).

### Pylint too strict
Edit `.pylintrc` to disable specific checks or adjust thresholds.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=AppClassificationOfLD --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m model         # Model tests only
pytest -m view          # View tests only

# Run specific test file
pytest tests/unit/test_models.py

# Or use the test runner script
# Windows: run_tests.bat
# Linux/Mac: ./run_tests.sh
```

### Test Coverage

```bash
# Generate HTML coverage report
pytest --cov=AppClassificationOfLD --cov-report=html
# Open htmlcov/index.html in browser

# Terminal coverage report
pytest --cov=AppClassificationOfLD --cov-report=term-missing
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── test_models.py      # Model tests
│   ├── test_views_auth.py  # Authentication view tests
│   └── test_views_tests.py # Test functionality view tests
└── integration/             # Integration tests
    └── test_user_flow.py   # End-to-end user flows
```

See `TEST_STATUS_REPORT.md` for detailed test documentation.

## Contributing

Before committing:
1. Run `black .` to format code
2. Run `flake8 .` to check for issues
3. Run `pytest` to ensure all tests pass
4. Fix any errors
5. Commit (pre-commit hooks will run automatically)
