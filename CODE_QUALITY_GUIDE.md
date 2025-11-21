# Code Quality Quick Reference Guide

## Quick Commands

### Format Code
```bash
black .                    # Format all Python files
black AppClassificationOfLD/views.py  # Format specific file
black --check .            # Check without making changes
```

### Lint Code
```bash
flake8 .                   # Check all files
flake8 AppClassificationOfLD/        # Check specific directory
flake8 --statistics .      # Show statistics
```

### Analyze Code
```bash
pylint AppClassificationOfLD/         # Analyze entire app
pylint AppClassificationOfLD/views.py # Analyze specific file
```

### Sort Imports
```bash
isort .                    # Sort all imports
isort --check-only .       # Check without making changes
```

### Run All Checks
```bash
pre-commit run --all-files  # Run all hooks on all files
```

## Common Issues and Fixes

### Issue: "Black and Flake8 conflict"
**Solution:** Already configured in `.flake8` to ignore conflicting rules (E203, W503, E501)

### Issue: "Too many pylint errors"
**Solution:** 
- Start with `--disable=all --enable=errors` to see only critical issues
- Gradually enable more checks as you fix issues
- Adjust thresholds in `.pylintrc`

### Issue: "Pre-commit hooks are slow"
**Solution:**
- Hooks only run on changed files by default
- Use `SKIP=flake8 git commit` to skip specific hooks (not recommended)
- Consider running `pre-commit run --all-files` separately before committing

### Issue: "Import errors in pylint"
**Solution:** 
- Ensure Django is in `known-third-party` in `.pylintrc` (already configured)
- Install `pylint-django` (included in requirements-dev.txt)

## Configuration Customization

### Adjust Line Length
Edit `pyproject.toml`:
```toml
[tool.black]
line-length = 120  # Change from 100 to 120
```

Also update `.flake8`:
```ini
max-line-length = 120
```

### Disable Specific Pylint Checks
Edit `.pylintrc` under `[MESSAGES CONTROL]`:
```ini
disable=
    missing-module-docstring,
    your-check-here
```

### Add Custom Flake8 Rules
Edit `.flake8`:
```ini
# Ignore specific error codes
ignore = E501, E203, W503, E402, F401, C901

# Per-file ignores
per-file-ignores =
    __init__.py:F401
    migrations/*:E501
    tests/*:F811
```

## Best Practices

1. **Run checks before committing:**
   ```bash
   black . && isort . && flake8 . && pylint AppClassificationOfLD/
   ```

2. **Fix issues incrementally:**
   - Don't try to fix everything at once
   - Focus on one type of issue at a time
   - Use `--disable` flags to temporarily ignore non-critical issues

3. **Use pre-commit hooks:**
   - They catch issues before you commit
   - Can be bypassed with `--no-verify` but avoid this

4. **IDE Integration:**
   - Configure your IDE to run formatters on save
   - This prevents most formatting issues

5. **CI/CD Integration:**
   - Run checks in your CI pipeline
   - Fail builds on linting errors
   - This ensures code quality in the repository

## File Exclusions

The following are automatically excluded from checks:
- `migrations/` - Django migration files
- `env/`, `venv/`, `.venv/` - Virtual environments
- `assets/`, `media/` - Static/media files
- `__pycache__/` - Python cache files
- `*.pyc` - Compiled Python files

## Integration with Git

### Pre-commit Hook Workflow
1. You make changes and stage them: `git add .`
2. You commit: `git commit -m "message"`
3. Pre-commit hooks run automatically
4. If hooks pass → commit succeeds
5. If hooks fail → commit is blocked, fix issues and try again

### Bypassing Hooks (Not Recommended)
```bash
git commit --no-verify -m "message"
```

Only use this in emergencies. The whole point is to catch issues early!

## Performance Tips

1. **Use pre-commit cache:**
   - Hooks cache results for unchanged files
   - Much faster on subsequent runs

2. **Run checks on specific files:**
   ```bash
   # Instead of checking everything
   flake8 AppClassificationOfLD/views.py
   ```

3. **Disable slow checks during development:**
   - Comment out pylint in `.pre-commit-config.yaml` during active development
   - Run it manually before final commit

4. **Use parallel execution:**
   ```bash
   pylint -j 4 AppClassificationOfLD/  # Use 4 processes
   ```

