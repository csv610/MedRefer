.PHONY: help install install-dev test test-all test-coverage test-fast lint format clean run check-syntax

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
PROJECT_NAME := medrefer

# Default target
help:
	@echo "MedRefer - Medical Specialist Recommendation System"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install all dependencies (including dev/test)"
	@echo "  make test             - Run all tests"
	@echo "  make test-coverage    - Run tests with coverage report"
	@echo "  make test-fast        - Run tests without verbose output"
	@echo "  make test-specialists - Run specialist coverage tests only"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make lint             - Check code syntax and style"
	@echo "  make format           - Format code (if formatter available)"
	@echo "  make clean            - Remove generated files and caches"
	@echo "  make run              - Run the interactive CLI"
	@echo "  make check-syntax     - Verify Python syntax only"
	@echo "  make all              - Install, check syntax, and run tests"
	@echo ""

# Install production dependencies
install:
	@echo "Installing production dependencies..."
	$(PIP) install -q -r requirements.txt
	@echo "✓ Installation complete"

# Install all dependencies (production + development/testing)
install-dev:
	@echo "Installing development dependencies..."
	$(PIP) install -q -r requirements.txt
	@echo "✓ Installation complete"

# Run all tests
test:
	@echo "Running all tests..."
	$(PYTEST) tests/ -v
	@echo "✓ Tests complete"

# Run all tests with coverage report
test-coverage:
	@echo "Running tests with coverage report..."
	$(PYTEST) tests/ -v --cov=$(PROJECT_NAME) --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "✓ Coverage report generated"
	@echo "  HTML report: htmlcov/index.html"

# Run tests without verbose output (faster)
test-fast:
	@echo "Running tests (fast mode)..."
	$(PYTEST) tests/ -q
	@echo "✓ Tests complete"

# Run specialist coverage tests only
test-specialists:
	@echo "Running specialist coverage tests..."
	$(PYTEST) tests/test_all_specialists.py -v
	@echo "✓ Specialist tests complete"

# Run unit tests only
test-unit:
	@echo "Running unit tests..."
	$(PYTEST) tests/test_medrefer.py -v
	@echo "✓ Unit tests complete"

# Check Python syntax
check-syntax:
	@echo "Checking Python syntax..."
	$(PYTHON) -m py_compile $(PROJECT_NAME).py
	@echo "✓ Main module syntax valid"
	$(PYTHON) -m py_compile tests/test_medrefer.py
	@echo "✓ Unit tests syntax valid"
	$(PYTHON) -m py_compile tests/test_all_specialists.py
	@echo "✓ Specialist tests syntax valid"

# Lint checks
lint: check-syntax
	@echo "Running linting checks..."
	@echo "Note: Install pylint, flake8, or black for additional linting"
	@echo "✓ Linting checks complete"

# Format code (placeholder - uncomment when formatter is installed)
format:
	@echo "Code formatting..."
	@echo "Note: Install black with 'pip install black' for automatic formatting"
	@echo "Then run: black $(PROJECT_NAME).py tests/"
	@echo "✓ Format target ready"

# Clean up generated files and caches
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete"

# Run the interactive CLI
run:
	@echo "Starting MedRefer interactive CLI..."
	@echo "Type 'exit' or 'quit' to exit (or Ctrl+C)"
	@echo ""
	$(PYTHON) $(PROJECT_NAME).py

# Run all checks and tests
all: install-dev check-syntax test
	@echo ""
	@echo "✓ All checks and tests passed!"

# Development setup target
setup: clean install-dev
	@echo "✓ Development environment ready"
	@echo ""
	@echo "To run the application:"
	@echo "  make run"
	@echo ""
	@echo "To run tests:"
	@echo "  make test"
	@echo ""
	@echo "To generate coverage report:"
	@echo "  make test-coverage"

# CI/CD target - strict checks
ci: clean install-dev check-syntax test-coverage
	@echo ""
	@echo "✓ CI pipeline complete"

# Watch mode for development (requires pytest-watch)
watch:
	@echo "Starting test watch mode (requires pytest-watch)..."
	@echo "Install with: pip install pytest-watch"
	ptw tests/

# Show test statistics
test-stats:
	@echo "Test Statistics:"
	@echo "==============="
	@echo "Total test files: $$(find tests/ -name 'test_*.py' | wc -l)"
	@echo "Total test functions: $$(grep -r 'def test_' tests/ | wc -l)"
	@echo "Total assertions: $$(grep -r 'assert ' tests/ | wc -l)"
	@echo ""
	@echo "Specialists covered: $$(grep -c 'def test_' tests/test_all_specialists.py)"
	@echo "Unit tests: $$(grep -c 'def test_' tests/test_medrefer.py)"

.SILENT: help
