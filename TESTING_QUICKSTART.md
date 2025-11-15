# Testing Quick Start Guide

Get up and running with testing in 5 minutes!

## Setup (First Time Only)

```bash
# 1. Install test dependencies
pip install -r requirement.txt

# 2. Verify pytest is installed
pytest --version
# Should show: pytest 7.2.2 (or similar)
```

## Run Your First Test

```bash
# Run all tests
pytest

# Expected output:
# ======================== test session starts ========================
# collected 50+ items
#
# tests/unit/test_models.py ..............................
# tests/unit/test_views.py ................................
# tests/integration/test_user_flow.py ....................
#
# ======================== 50+ passed in 5.00s ========================
```

## Common Testing Commands

```bash
# 🚀 Quick tests (parallel, fast)
make test-fast

# 📊 Tests with coverage report
make coverage

# 🔍 Unit tests only
make test-unit

# 🔗 Integration tests only
make test-integration

# 📝 Verbose output
make test-verbose

# ❌ Run only failed tests
make test-failed
```

## View Coverage Report

```bash
# Generate and open coverage report
make coverage-report

# OR manually:
pytest --cov=AppClassificationOfLD --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Writing Your First Test

Create a new test file in `tests/unit/`:

```python
# tests/unit/test_my_feature.py
import pytest
from AppClassificationOfLD.models import UserDetails

@pytest.mark.unit
@pytest.mark.django_db
class TestMyFeature:
    """Test my awesome new feature"""

    def test_something_works(self):
        """Test that something works as expected"""
        # Arrange
        user = UserDetails.objects.create(
            Firstname='Test',
            Username='testuser',
            Email='test@example.com',
            Password='password'
        )

        # Act
        result = user.Firstname

        # Assert
        assert result == 'Test'
```

Run your test:
```bash
pytest tests/unit/test_my_feature.py -v
```

## Test Markers

Use markers to organize tests:

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.models        # Model test
@pytest.mark.views         # View test
@pytest.mark.slow          # Slow test
@pytest.mark.django_db     # Requires database
```

Run tests by marker:
```bash
pytest -m unit              # Only unit tests
pytest -m "unit and models" # Unit tests for models
pytest -m "not slow"        # Exclude slow tests
```

## Using Fixtures

Fixtures provide reusable test data (defined in `conftest.py`):

```python
def test_with_user(user_details):
    """user_details fixture provides a test user"""
    assert user_details.Username == 'testuser'

def test_authenticated_request(authenticated_client):
    """authenticated_client provides logged-in client"""
    response = authenticated_client.get('/TestDisability/')
    assert response.status_code == 200
```

## Debugging Tests

```bash
# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Extra verbose
pytest -vv

# Use Python debugger
pytest --pdb
```

## CI/CD

Tests run automatically on:
- ✅ Push to main/develop/claude branches
- ✅ Pull requests
- ✅ Weekly schedule

View results in GitHub Actions tab.

## Common Issues

### Database errors
```bash
pytest --create-db  # Recreate test database
```

### Tests are slow
```bash
pytest -n auto --reuse-db  # Parallel + reuse DB
```

### Import errors
```bash
# Set Django settings
export DJANGO_SETTINGS_MODULE=ClassificationOfLD.settings

# Verify you're in project root
pwd  # Should show: /path/to/InsightEDU3.2
```

## Next Steps

1. ✅ Read [TESTING_STRATEGY.md](TESTING_STRATEGY.md) for detailed strategy
2. ✅ Read [tests/README.md](tests/README.md) for test suite documentation
3. ✅ Explore existing tests in `tests/` directory
4. ✅ Write tests for your features
5. ✅ Run tests before committing: `make test`

## Cheat Sheet

```bash
# Development workflow
make test-fast        # Quick test during development
make test-verbose     # Debug test failures
make coverage         # Check coverage before commit

# Pre-commit checks
make test             # Run all tests
make lint             # Check code style
make coverage         # Verify coverage

# CI/CD simulation
make ci-test          # Run tests like CI/CD does

# Maintenance
make clean            # Clean up generated files
make install          # Reinstall dependencies
```

## Getting Help

- 📖 [TESTING_STRATEGY.md](TESTING_STRATEGY.md) - Comprehensive strategy
- 📚 [tests/README.md](tests/README.md) - Test suite details
- 🔧 [Makefile](Makefile) - Available make commands
- 🌐 [Pytest Docs](https://docs.pytest.org/) - Official documentation

---

**Pro Tip**: Use `make help` to see all available commands!

```bash
make help
```

Happy Testing! 🎉
