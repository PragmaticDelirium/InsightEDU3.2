# Testing Strategy for InsightEDU 3.2

## Table of Contents
1. [Overview](#overview)
2. [Testing Philosophy](#testing-philosophy)
3. [Test Structure](#test-structure)
4. [Testing Levels](#testing-levels)
5. [Coverage Goals](#coverage-goals)
6. [Running Tests](#running-tests)
7. [CI/CD Integration](#cicd-integration)
8. [Best Practices](#best-practices)
9. [Maintenance](#maintenance)

## Overview

InsightEDU 3.2 is a comprehensive learning disability detection and assessment platform built with Django. This document outlines the testing strategy to ensure reliability, maintainability, and quality of the application.

### Technology Stack
- **Framework**: Django 4.1.7
- **Testing Framework**: Pytest 7.2.2
- **Coverage Tool**: Coverage.py 7.2.2
- **Additional Tools**: pytest-django, pytest-cov, factory-boy, faker

## Testing Philosophy

Our testing approach follows these core principles:

1. **Test Pyramid**: Focus on unit tests (70%), integration tests (20%), and end-to-end tests (10%)
2. **Fast Feedback**: Tests should run quickly to encourage frequent execution
3. **Isolated Tests**: Each test should be independent and not rely on other tests
4. **Readable Tests**: Tests serve as documentation; write them clearly
5. **Continuous Testing**: Integrate testing into the development workflow

## Test Structure

```
InsightEDU3.2/
├── tests/
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   ├── test_models.py      # Model tests
│   │   ├── test_views.py       # View tests
│   │   ├── test_urls.py        # URL routing tests
│   │   └── test_settings.py    # Settings tests
│   ├── integration/             # Integration tests
│   │   ├── __init__.py
│   │   └── test_user_flow.py   # User journey tests
│   └── fixtures/                # Test data
│       ├── __init__.py
│       └── factories.py         # Factory Boy factories
├── conftest.py                  # Pytest configuration and fixtures
├── pytest.ini                   # Pytest settings
└── .coveragerc                  # Coverage configuration
```

## Testing Levels

### 1. Unit Tests

**Purpose**: Test individual components in isolation

**Location**: `tests/unit/`

**Coverage Areas**:
- **Models** (`test_models.py`): Database models, field validation, relationships
- **Views** (`test_views.py`): View logic, authentication, session management
- **URLs** (`test_urls.py`): URL routing and resolution
- **Settings** (`test_settings.py`): Django configuration

**Example**:
```python
@pytest.mark.unit
@pytest.mark.models
@pytest.mark.django_db
def test_create_user(self):
    user = UserDetails.objects.create(
        Firstname='John',
        Lastname='Doe',
        Email='john@example.com',
        Username='johndoe',
        Password='password123'
    )
    assert user.id is not None
    assert user.Email == 'john@example.com'
```

### 2. Integration Tests

**Purpose**: Test interactions between components

**Location**: `tests/integration/`

**Coverage Areas**:
- Complete user flows (registration → login → assessment)
- Data persistence across requests
- Session management
- Multi-step processes

**Example**:
```python
@pytest.mark.integration
@pytest.mark.django_db
def test_complete_registration_and_login_flow(self):
    # Register user
    response = client.post('/UserRegisteration/', {...})
    assert UserDetails.objects.filter(Username='user').exists()

    # Login
    response = client.post('/UserLogin/', {...})
    assert response.status_code == 302
```

### 3. Future: End-to-End Tests

**Purpose**: Test complete user scenarios with real browsers

**Tools**: Selenium, Playwright (to be implemented)

**Coverage Areas**:
- Complete assessment workflows
- Video test interactions
- Memory test interactions
- Admin dashboard operations

## Coverage Goals

### Target Metrics
- **Overall Coverage**: Minimum 70%
- **Models**: 90%+ (critical data layer)
- **Views**: 75%+ (business logic)
- **Integration**: 60%+ (workflows)

### Coverage Exclusions
The following are excluded from coverage metrics:
- Migration files (`*/migrations/*`)
- Test files themselves
- Virtual environment files
- WSGI/ASGI configuration
- Django admin configuration

### Measuring Coverage

```bash
# Run tests with coverage
pytest --cov=AppClassificationOfLD --cov=ClassificationOfLD --cov-report=html --cov-report=term-missing

# View HTML report
open htmlcov/index.html

# Check coverage threshold
coverage report --fail-under=70
```

## Running Tests

### Quick Start

```bash
# Install dependencies
pip install -r requirement.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test class
pytest tests/unit/test_models.py::TestUserDetailsModel

# Run specific test
pytest tests/unit/test_models.py::TestUserDetailsModel::test_create_user
```

### Using Test Markers

Tests are marked for selective execution:

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only model tests
pytest -m models

# Run only view tests
pytest -m views

# Exclude slow tests
pytest -m "not slow"

# Combine markers
pytest -m "unit and models"
```

### Parallel Execution

Run tests in parallel for faster execution:

```bash
# Run on 4 CPUs
pytest -n 4

# Run on auto-detected CPU count
pytest -n auto
```

### Test Database

Tests use a separate test database:
- Django automatically creates `test_<database_name>`
- Use `--reuse-db` flag to reuse test database between runs
- Use `--create-db` to force recreation

```bash
# Reuse database (faster)
pytest --reuse-db

# Recreate database
pytest --create-db
```

## CI/CD Integration

### GitHub Actions Workflows

#### 1. Main Test Pipeline (`.github/workflows/tests.yml`)

**Triggers**:
- Push to `main`, `develop`, `claude/*` branches
- Pull requests to `main`, `develop`

**Jobs**:
- **Test Matrix**: Python 3.8, 3.9, 3.10
- **Database**: MySQL 8.0
- **Steps**:
  1. Install dependencies
  2. Run migrations
  3. Run linting (flake8)
  4. Run unit tests with coverage
  5. Run integration tests with coverage
  6. Upload coverage to Codecov
  7. Generate coverage reports

#### 2. PR Tests (`.github/workflows/pr-tests.yml`)

**Triggers**: Pull request events

**Purpose**: Quick feedback on PRs

**Features**:
- Fast unit test execution
- Automated PR comments with results

#### 3. Coverage Reports (`.github/workflows/coverage-report.yml`)

**Triggers**:
- Push to `main`, `develop`
- Weekly schedule (Sunday midnight)

**Purpose**: Track coverage trends

**Features**:
- Full coverage analysis
- Coverage threshold enforcement (50%)
- Codecov integration
- HTML report artifacts

### Additional CI Jobs

#### Security Scanning
- **Safety**: Check for known vulnerabilities in dependencies
- **Bandit**: Static security analysis for Python code

#### Code Quality
- **Black**: Code formatting verification
- **isort**: Import sorting verification
- **Pylint**: Code quality linting

## Best Practices

### Writing Tests

1. **Use Descriptive Names**
   ```python
   # Good
   def test_user_login_with_valid_credentials(self):

   # Bad
   def test_login(self):
   ```

2. **Follow AAA Pattern**: Arrange, Act, Assert
   ```python
   def test_create_user(self):
       # Arrange
       user_data = {...}

       # Act
       user = UserDetails.objects.create(**user_data)

       # Assert
       assert user.id is not None
   ```

3. **Use Fixtures for Common Setup**
   ```python
   @pytest.fixture
   def user_details(db):
       return UserDetails.objects.create(...)

   def test_something(user_details):
       assert user_details.id is not None
   ```

4. **Test Edge Cases**
   - Empty inputs
   - Maximum length strings
   - Invalid data types
   - Boundary conditions

5. **Keep Tests Independent**
   - Don't rely on test execution order
   - Clean up after each test
   - Use database transactions (automatic with pytest-django)

### Test Data Management

1. **Use Factories** (factory_boy) for complex objects
   ```python
   from tests.fixtures.factories import UserDetailsFactory

   user = UserDetailsFactory.create()
   ```

2. **Use Fixtures** for reusable test data
   ```python
   @pytest.fixture
   def authenticated_client(user_details):
       client = Client()
       client.session['Users_id'] = user_details.id
       return client
   ```

3. **Mock External Dependencies**
   ```python
   def test_ml_prediction(mock_ml_model):
       mock_ml_model.predict.return_value = [[0.8]]
       # Test code using mocked model
   ```

### Performance Optimization

1. **Use `--reuse-db`** for faster test runs during development
2. **Mark slow tests**: `@pytest.mark.slow`
3. **Run parallel tests**: `pytest -n auto`
4. **Use `--nomigrations`** if migrations aren't needed
5. **Cache dependencies** in CI/CD

## Maintenance

### Regular Tasks

**Daily/Per Commit**:
- Run relevant tests before committing
- Review test failures in CI/CD

**Weekly**:
- Review coverage reports
- Address failing tests
- Update test data as needed

**Monthly**:
- Review and refactor test code
- Update dependencies
- Analyze test performance

**Quarterly**:
- Comprehensive test suite review
- Update testing strategy
- Evaluate new testing tools

### Adding New Tests

When adding new features:

1. **Write tests first** (TDD approach)
2. **Update fixtures** if needed
3. **Add appropriate markers**
4. **Document complex test scenarios**
5. **Update this strategy document** if adding new patterns

### Handling Test Failures

1. **Investigate immediately**: Don't let broken tests linger
2. **Reproduce locally**: Use same Python version and dependencies
3. **Check CI logs**: Review complete error traces
4. **Fix or skip**: Fix the issue or mark as `@pytest.mark.skip` with reason
5. **Document**: Add comments for complex failure scenarios

## Test Metrics Dashboard

Track these metrics over time:

- **Total Test Count**: Target 200+ tests
- **Overall Coverage**: Target 70%+
- **Test Execution Time**: Keep under 2 minutes
- **Failure Rate**: Keep below 5%
- **Flaky Tests**: Identify and fix tests that fail intermittently

## Future Enhancements

### Short Term (1-3 months)
- [ ] Add end-to-end tests with Selenium/Playwright
- [ ] Implement visual regression testing
- [ ] Add performance/load testing
- [ ] Create test data generation scripts

### Medium Term (3-6 months)
- [ ] Machine learning model testing framework
- [ ] API integration tests (if REST API added)
- [ ] Accessibility testing
- [ ] Mobile responsiveness testing

### Long Term (6-12 months)
- [ ] Automated security testing
- [ ] Chaos engineering experiments
- [ ] Production monitoring integration
- [ ] A/B testing framework

## Resources

### Documentation
- [Pytest Documentation](https://docs.pytest.org/)
- [Django Testing](https://docs.djangoproject.com/en/4.1/topics/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)

### Commands Reference

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=AppClassificationOfLD --cov-report=html

# Run specific markers
pytest -m unit
pytest -m integration
pytest -m "unit and models"

# Run with verbosity
pytest -v -s

# Run in parallel
pytest -n auto

# Reuse database
pytest --reuse-db

# Stop on first failure
pytest -x

# Show local variables in traceback
pytest -l

# Run only failed tests from last run
pytest --lf

# Run failed tests first, then others
pytest --ff
```

## Contact & Support

For questions about testing:
- Review this document
- Check test examples in `tests/` directory
- Consult team members
- Refer to official documentation

---

**Last Updated**: 2025-11-15
**Version**: 1.0
**Author**: InsightEDU Development Team
