# Developer Quick Reference

Quick commands and tips for developing ACG-FolderClean.

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd ACG-FolderClean

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Testing

```bash
# Run all tests
pytest test_file_cleaner.py -v

# Run with coverage
pytest test_file_cleaner.py --cov=file_cleaner --cov-report=html

# Run specific test class
pytest test_file_cleaner.py::TestRemoveFiles -v

# Run quick tests (stop at first failure)
python run_tests.py quick

# Run all test modes
python run_tests.py all
python run_tests.py coverage
python run_tests.py verbose
```

## Code Quality

```bash
# Format code with black
black file_cleaner.py app_build.py test_file_cleaner.py

# Check with flake8
flake8 file_cleaner.py --max-line-length=127

# Run pylint
pylint file_cleaner.py
```

## Building

```bash
# Build with patch version bump (1.0.0 → 1.0.1)
python app_build.py --patch

# Build with minor version bump (1.0.1 → 1.1.0)
python app_build.py --minor

# Build with major version bump (1.1.0 → 2.0.0)
python app_build.py --major
```

## Running the Application

```bash
# Run from source
python file_cleaner.py "C:\path\to\files\*" 30

# Run with exclusions
python file_cleaner.py "C:\path\to\files\*" 30 -e

# Run the compiled executable
./dist/ACG-FolderClean "C:\path\to\files\*" 30
```

## Project Structure

```
ACG-FolderClean/
├── src/
│   ├── file_cleaner.py          # Main application
│   ├── app_build.py             # Build script
│   └── app_year.txt             # Copyright year
├── tests/
│   ├── test_file_cleaner.py     # Test suite
│   ├── conftest.py              # Pytest fixtures
│   └── run_tests.py             # Test runner
├── assets/
│   └── ACG.ico                  # Application icon
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest config
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # Documentation
```

## Common Tasks

### Adding a New Feature

1. Write tests first (TDD approach)
2. Implement the feature
3. Run tests to ensure they pass
4. Update documentation
5. Format code with black
6. Create pull request

### Fixing a Bug

1. Write a test that reproduces the bug
2. Fix the bug
3. Verify the test passes
4. Check for regressions
5. Update version with patch bump

### Release Process

1. Ensure all tests pass
2. Update CHANGELOG (if exists)
3. Bump version appropriately (major/minor/patch)
4. Build the executable
5. Tag the release in git
6. Create GitHub release with binaries

## Debugging

```bash
# Run with verbose output
python file_cleaner.py "path" 30 -v

# Check logs
tail -f ACG-FolderClean_logs/ACG-FolderClean.log

# Run specific test with debugging
pytest test_file_cleaner.py::TestRemoveFiles::test_remove_old_files -vv --pdb
```

## Environment Variables

None required. Configuration is handled through:
- Command-line arguments
- `app_version.txt` (optional)
- `app_year.txt` (optional)

## Tips

- Use `--patch` for bug fixes
- Use `--minor` for new features (backward compatible)
- Use `--major` for breaking changes
- Always run tests before committing
- Keep log files under 7 days (automatic rotation)
- Test on Windows, Linux, and macOS when possible

## Troubleshooting

### Tests Failing

```bash
# Clear pytest cache
pytest --cache-clear

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Build Issues

```bash
# Clean build artifacts
rm -rf build/ dist/ *.spec

# Rebuild from scratch
python app_build.py --patch
```

### Import Errors

```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [PyInstaller documentation](https://pyinstaller.org/)
- [Python docopt](http://docopt.org/)
- [Black code formatter](https://black.readthedocs.io/)

## Contact

For questions or issues, please open an issue on GitHub or contact Application Consulting Group, Inc.

---

Copyright © 2025 Application Consulting Group, Inc.  
Licensed under the MIT License