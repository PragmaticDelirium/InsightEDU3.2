# InsightEDU 3.2 Test Suite

This directory contains the comprehensive test suite for the InsightEDU 3.2 learning disability detection platform.

## Quick Start

```bash
# Install test dependencies
pip install -r requirement.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=AppClassificationOfLD --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Directory Structure

```
tests/
├── unit/                   # Unit tests for individual components
│   ├── test_models.py     # Database model tests
│   ├── test_views.py      # View logic tests
│   ├── test_urls.py       # URL routing tests
│   └── test_settings.py   # Django settings tests
│
├── integration/           # Integration tests for workflows
│   └── test_user_flow.py # Complete user journey tests
│
└── fixtures/              # Test data and factories
    └── factories.py       # Factory Boy factories
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **Models**: CRUD operations, field validation, relationships
- **Views**: Request handling, authentication, session management
- **URLs**: Route resolution and configuration
- **Settings**: Django configuration validation

**Run unit tests only**:
```bash
pytest -m unit
```

### Integration Tests (`tests/integration/`)

Test interactions between multiple components:

- User registration and login flows
- Assessment workflows
- Data persistence
- Session management across requests

**Run integration tests only**:
```bash
pytest -m integration
```

## Test Markers

Tests are tagged with markers for selective execution:

```bash
# Run by test level
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only

# Run by component
pytest -m models         # Model tests
pytest -m views          # View tests
pytest -m auth           # Authentication tests
pytest -m database       # Database tests

# Run by speed
pytest -m "not slow"     # Exclude slow tests

# Combine markers
pytest -m "unit and models"    # Unit tests for models
pytest -m "integration or e2e" # Integration or E2E tests
```

## Common Commands

```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test class
pytest tests/unit/test_models.py::TestUserDetailsModel

# Run specific test method
pytest tests/unit/test_models.py::TestUserDetailsModel::test_create_user

# Run tests in parallel (faster)
pytest -n auto

# Reuse database (faster for development)
pytest --reuse-db

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Run last failed tests
pytest --lf

# Run failed first, then others
pytest --ff
```

## Coverage

Generate and view coverage reports:

```bash
# Run tests with coverage
pytest --cov=AppClassificationOfLD --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Check coverage meets threshold
coverage report --fail-under=70
```

## Writing Tests

### Test Structure (AAA Pattern)

```python
def test_something(self):
    # Arrange - Set up test data
    user_data = {'username': 'test', 'email': 'test@example.com'}

    # Act - Perform the action
    user = UserDetails.objects.create(**user_data)

    # Assert - Verify the result
    assert user.id is not None
    assert user.email == 'test@example.com'
```

### Using Fixtures

Fixtures are defined in `conftest.py`:

```python
def test_with_user(user_details):
    """user_details fixture provides a test user"""
    assert user_details.id is not None

def test_with_authenticated_client(authenticated_client):
    """authenticated_client fixture provides logged-in client"""
    response = authenticated_client.get('/some-protected-page/')
    assert response.status_code == 200
```

### Using Factories

Factory Boy factories are available in `tests/fixtures/factories.py`:

```python
from tests.fixtures.factories import UserDetailsFactory

def test_with_factory():
    # Create a user with random data
    user = UserDetailsFactory.create()

    # Create a user with specific data
    user = UserDetailsFactory.create(
        Username='specificuser',
        Email='specific@example.com'
    )

    # Create multiple users
    users = UserDetailsFactory.create_batch(10)
```

## Available Fixtures

Defined in `conftest.py`:

- `api_client`: Django test client
- `authenticated_client`: Logged-in test client
- `user_details`: Test user instance
- `admin_user`: Test admin instance
- `disability_test_data`: Sample disability test
- `test_result`: Sample test result
- `sample_test_session`: Client with session data
- `mock_ml_model`: Mocked ML model

## Best Practices

1. **Use descriptive test names**: `test_user_login_with_valid_credentials`
2. **Keep tests independent**: Don't rely on test execution order
3. **Test one thing**: Each test should verify one behavior
4. **Use fixtures**: Avoid duplicating setup code
5. **Mock external dependencies**: Use `pytest-mock` for external APIs
6. **Tag your tests**: Use markers for organization
7. **Document complex tests**: Add comments for non-obvious logic

## CI/CD Integration

Tests run automatically on:
- Push to `main`, `develop`, or `claude/*` branches
- Pull requests to `main` or `develop`
- Weekly schedule (coverage reports)

View results in the GitHub Actions tab.

## Troubleshooting

### Tests fail with database errors
```bash
# Recreate test database
pytest --create-db
```

### Tests are slow
```bash
# Run in parallel
pytest -n auto

# Reuse database
pytest --reuse-db

# Skip migrations
pytest --nomigrations
```

### Import errors
```bash
# Ensure you're in the project root
cd /path/to/InsightEDU3.2

# Set DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=ClassificationOfLD.settings

# Reinstall dependencies
pip install -r requirement.txt
```

### Coverage not showing
```bash
# Make sure pytest-cov is installed
pip install pytest-cov

# Run with explicit coverage flags
pytest --cov=AppClassificationOfLD --cov-report=term-missing
```

## Resources

- [TESTING_STRATEGY.md](../TESTING_STRATEGY.md) - Comprehensive testing strategy
- [pytest.ini](../pytest.ini) - Pytest configuration
- [.coveragerc](../.coveragerc) - Coverage configuration
- [conftest.py](../conftest.py) - Shared fixtures

## Support

For questions or issues:
1. Check [TESTING_STRATEGY.md](../TESTING_STRATEGY.md)
2. Review example tests in this directory
3. Consult pytest documentation: https://docs.pytest.org/
4. Ask team members

---

**Remember**: Good tests are the foundation of maintainable code. Write them often, keep them clean, and run them always!
