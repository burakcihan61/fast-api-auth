# Contributing Guide

Thank you for considering contributing to the project! This document details the standards and procedures for contributing.

## 🛠️ Development Setup

Refer to [Setup Guide](docs/setup.md) for instructions on setting up your local environment.

## 🧪 Testing Policy

All new features and bug fixes must include tests.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 📊 Code Quality Standards

We enforce strict code quality using `ruff` and `pre-commit`.

### Pre-commit Hooks
Install hooks to automatically check your code before committing:
```bash
pre-commit install
```

### Manual Checks
Run these commands locally before pushing:

```bash
# specialized linting
ruff check .

# formatting
ruff format .

# strict type checking
mypy app
```

## 📝 Commit Conventions

We follow Conventional Commits:
- `feat: add new feature`
- `fix: resolve issue`
- `docs: update documentation`
- `style: formatting changes`
- `refactor: code restructuring`
- `test: adding tests`
- `chore: maintenance`

## 🔄 Pull Request Process

1. Fork the repository
2. Create a feature branch (`feat/username/feature-name`)
3. Commit your changes
4. Push to the branch
5. Create a Pull Request targeting `main`
