# Testing Guide - InsightEDU3.2

## Quick Start

### 1. Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### 2. Run Tests

```bash
# Quick test run
pytest

# With coverage
pytest --cov=AppClassificationOfLD --cov-report=html

# Or use the script
# Windows: run_tests.bat
# Linux/Mac: ./run_tests.sh
```

## Test Organization

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures and configuration
├── unit/                          # Unit tests
│   ├── __init__.py
│   ├── test_models.py            # Model unit tests
│   ├── test_views_auth.py        # Authentication view tests
│   └── test_views_tests.py       # Test functionality view tests
└── integration/                   # Integration tests
    ├── __init__.py
    └── test_user_flow.py         # End-to-end user flow tests
```

### Test Categories

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests (isolated component tests)
- `@pytest.mark.integration` - Integration tests (multi-component tests)
- `@pytest.mark.model` - Model tests
- `@pytest.mark.view` - View tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.test_disability` - Disability test functionality

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test
pytest tests/unit/test_models.py::TestUserDetails::test_create_user_details
```

### Running by Category

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Model tests only
pytest -m model

# View tests only
pytest -m view

# Authentication tests only
pytest -m auth
```

### Coverage Reports

```bash
# HTML report (opens in browser)
pytest --cov=AppClassificationOfLD --cov-report=html
# Then open htmlcov/index.html

# Terminal report
pytest --cov=AppClassificationOfLD --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov=AppClassificationOfLD --cov-report=xml

# Minimum coverage threshold
pytest --cov=AppClassificationOfLD --cov-fail-under=80
```

## Test Fixtures

### Available Fixtures (in `conftest.py`)

- `factory` - Django RequestFactory for creating test requests
- `user_details` - Test user instance
- `admin_user` - Test admin user instance
- `disability_test_data` - Test disability test data
- `test_result` - Test result instance
- `authenticated_request` - Authenticated request object
- `admin_request` - Admin authenticated request object
- `anonymous_request` - Anonymous request object

### Using Fixtures

```python
def test_example(user_details, authenticated_request):
    """Example test using fixtures"""
    assert user_details.Username == "johndoe"
    assert authenticated_request.session['UserId'] == user_details.id
```

## Writing Tests

### Unit Test Example

```python
@pytest.mark.django_db
@pytest.mark.unit
@pytest.mark.model
class TestUserDetails:
    """Test cases for UserDetails model"""

    def test_create_user_details(self):
        """Test creating a user details instance"""
        user = UserDetails.objects.create(
            Firstname="Jane",
            Lastname="Smith",
            Phone="9876543210",
            Email="jane.smith@example.com",
            Username="janesmith",
            Password="password123"
        )
        assert user.id is not None
        assert user.Firstname == "Jane"
```

### View Test Example

```python
@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.auth
def test_user_login_success(client, user_details):
    """Test successful user login"""
    response = client.post('/UserLogin/', {
        'U_name': 'johndoe',
        'U_pwds': 'testpass123'
    })
    assert response.status_code == 302  # Redirect
    assert response.url == '/'
```

### Integration Test Example

```python
@pytest.mark.django_db
@pytest.mark.integration
def test_user_registration_to_login(client):
    """Test user can register and then login"""
    # Register
    response = client.post('/UserRegisteration/', {
        'fname': 'Integration',
        'lname': 'Test',
        'phone': '5551112222',
        'Eid': 'integration@test.com',
        'uname': 'integrationtest',
        'pwd': 'testpass123'
    })
    assert response.status_code == 200
    assert UserDetails.objects.filter(Username='integrationtest').exists()

    # Login
    response = client.post('/UserLogin/', {
        'U_name': 'integrationtest',
        'U_pwds': 'testpass123'
    })
    assert response.status_code == 302
    assert response.url == '/'
```

## Test Best Practices

### 1. Use Descriptive Test Names

```python
# Good
def test_user_login_with_valid_credentials_redirects_to_home():
    pass

# Bad
def test_login():
    pass
```

### 2. One Assertion Per Test (When Possible)

```python
# Good - Clear what failed
def test_user_has_correct_email(user_details):
    assert user_details.Email == "john.doe@example.com"

def test_user_has_correct_username(user_details):
    assert user_details.Username == "johndoe"

# Acceptable - Related assertions
def test_user_creation(user_details):
    assert user_details.id is not None
    assert user_details.Firstname == "John"
```

### 3. Use Fixtures for Common Setup

```python
# Good - Reusable fixture
@pytest.fixture
def user_details():
    return UserDetails.objects.create(...)

# Bad - Repeated setup
def test_one(user_details):
    user = UserDetails.objects.create(...)  # Repeated
    ...

def test_two(user_details):
    user = UserDetails.objects.create(...)  # Repeated
    ...
```

### 4. Test Edge Cases

```python
def test_user_registration_duplicate_email(client, user_details):
    """Test registration with duplicate email fails"""
    response = client.post('/UserRegisteration/', {
        'Eid': 'john.doe@example.com',  # Duplicate
        ...
    })
    assert response.status_code == 200
    # Should show error or redirect
```

### 5. Use Appropriate Markers

```python
@pytest.mark.django_db      # Required for database access
@pytest.mark.unit           # Categorize test
@pytest.mark.slow           # Mark slow tests
```

## Debugging Tests

### Run with Verbose Output

```bash
pytest -v -s
```

### Run Specific Test

```bash
pytest tests/unit/test_models.py::TestUserDetails::test_create_user_details -v
```

### Use Print Statements

```python
def test_example():
    result = some_function()
    print(f"Result: {result}")  # Will show with -s flag
    assert result == expected
```

### Use PDB Debugger

```python
def test_example():
    result = some_function()
    import pdb; pdb.set_trace()  # Drop into debugger
    assert result == expected
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirement.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest --cov=AppClassificationOfLD --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### Tests Not Finding Django Settings

```bash
# Set Django settings module
export DJANGO_SETTINGS_MODULE=ClassificationOfLD.settings
pytest
```

### Database Issues

```bash
# Use in-memory database for tests (already configured)
# Or create test database
python manage.py test
```

### Import Errors

```bash
# Ensure you're in the project root
# Activate virtual environment
# Install dependencies
pip install -r requirements-dev.txt
```

### Coverage Not Working

```bash
# Install coverage
pip install pytest-cov

# Run with coverage
pytest --cov=AppClassificationOfLD
```

## Test Coverage Goals

| Component | Target | Current |
|-----------|--------|---------|
| Models | 90% | 0% |
| Views | 80% | 0% |
| Utils | 70% | 0% |
| **Overall** | **80%** | **0%** |

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- `TEST_STATUS_REPORT.md` - Detailed test status and statistics

---

**Happy Testing! 🧪**

