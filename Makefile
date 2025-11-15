.PHONY: help test test-unit test-integration test-fast test-verbose coverage clean install lint format

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install --upgrade pip
	pip install -r requirement.txt

test:  ## Run all tests
	pytest

test-unit:  ## Run unit tests only
	pytest -m unit -v

test-integration:  ## Run integration tests only
	pytest -m integration -v

test-fast:  ## Run tests in parallel (fast)
	pytest -n auto --reuse-db

test-verbose:  ## Run tests with verbose output
	pytest -v -s

test-models:  ## Run model tests only
	pytest -m models -v

test-views:  ## Run view tests only
	pytest -m views -v

test-failed:  ## Run only failed tests from last run
	pytest --lf -v

coverage:  ## Run tests with coverage report
	pytest --cov=AppClassificationOfLD --cov=ClassificationOfLD --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

coverage-report:  ## Open coverage report in browser
	pytest --cov=AppClassificationOfLD --cov-report=html
	@which xdg-open > /dev/null && xdg-open htmlcov/index.html || open htmlcov/index.html

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf coverage.xml
	@echo "Cleaned up generated files"

lint:  ## Run linting checks
	@echo "Running flake8..."
	flake8 AppClassificationOfLD --count --select=E9,F63,F7,F82 --show-source --statistics || true
	@echo ""
	@echo "Running pylint..."
	pylint AppClassificationOfLD --exit-zero || true

format:  ## Format code with black and isort
	@echo "Formatting with black..."
	black AppClassificationOfLD/ tests/
	@echo ""
	@echo "Sorting imports with isort..."
	isort AppClassificationOfLD/ tests/

format-check:  ## Check code formatting without modifying
	@echo "Checking black formatting..."
	black --check AppClassificationOfLD/ tests/
	@echo ""
	@echo "Checking isort..."
	isort --check-only AppClassificationOfLD/ tests/

migrate:  ## Run database migrations
	python manage.py migrate

migrations:  ## Create new migrations
	python manage.py makemigrations

runserver:  ## Start development server
	python manage.py runserver

shell:  ## Start Django shell
	python manage.py shell

test-db-create:  ## Force recreate test database
	pytest --create-db

test-db-reuse:  ## Reuse test database (faster)
	pytest --reuse-db

security-check:  ## Run security checks
	@echo "Running safety check..."
	safety check --file=requirement.txt || true
	@echo ""
	@echo "Running bandit..."
	bandit -r AppClassificationOfLD/ || true

ci-test:  ## Run tests as in CI/CD pipeline
	pytest --cov=AppClassificationOfLD --cov=ClassificationOfLD --cov-report=xml --cov-report=term-missing -v

all: clean install test coverage  ## Clean, install, test, and generate coverage
