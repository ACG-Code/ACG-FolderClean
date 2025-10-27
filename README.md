# ACG_FileCleaner

Copyright © 2025 Application Consulting Group, Inc.

A tool that removes files filtered by a regular expression and time since creation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Features

- Delete files based on age (days since last modification)
- Support for glob patterns and recursive directory scanning
- Optional exclusion of files modified on the last day of the month
- Automatic log rotation (keeps 7 days of logs)
- Dynamic version and copyright year management
- Dual output logging (file and console)

## Glob Pattern Support

- `*`: Matches files in a single directory
- `**`: Recursively matches files in directories and subdirectories

## Usage

```
ACG-FolderClean <expression> <age> [options]
ACG-FolderClean (-h | --version)
```

## Arguments

- `<expression>` - The path pattern to match files (supports glob patterns)
- `<age>` - Age in days; files older than this will be deleted

## Options

- `-e` - Exclude files modified on the last day of a month from deletion
- `-h` - Display help screen
- `--version` - Display version information

## Examples

### Basic Usage

Delete all files in a directory older than 5 days:
```
ACG-FolderClean "C:\Users\John\Documents\*" 5
```

Delete all files recursively in directory and subdirectories older than 5 days:
```
ACG-FolderClean "C:\Users\John\Documents\**" 5
```

### Pattern Matching

Delete files matching a pattern in a directory older than 5 days:
```
ACG-FolderClean "C:\Users\John\Documents\File*" 5
```

Delete files matching a pattern recursively older than 5 days:
```
ACG-FolderClean "C:\Users\John\Documents\File**" 5
```

### Exclude End-of-Month Files

Delete all files older than 30 days, but keep files modified on the last day of any month:
```
ACG-FolderClean "C:\Users\John\Reports\**" 30 -e
```

This is useful for preserving end-of-month reports or snapshots while cleaning up other files.

## Logging

The application creates logs in the `ACG-FolderClean_logs` directory:
- Logs are automatically rotated at midnight
- Keeps 7 days of log history
- Logs are output to both file and console
- Each log entry includes timestamp, level, and message

## Building Executable

The project includes an automated build script (`app_build.py`) that handles version management and PyInstaller compilation.

### Prerequisites

```bash
pip install pyinstaller docopt
```

### Build Commands

Bump and build with patch version (1.0.0 → 1.0.1):
```bash
python app_build.py --patch
```

Bump and build with minor version (1.0.1 → 1.1.0):
```bash
python app_build.py --minor
```

Bump and build with major version (1.1.0 → 2.0.0):
```bash
python app_build.py --major
```

### Build Process

The build script automatically:
1. Increments the build number
2. Updates version information
3. Generates PyInstaller spec file
4. Compiles the executable with embedded version info
5. Outputs to the `dist` directory

### Directory Structure

```
project/
├── src/
│   ├── file_cleaner.py
│   ├── app_build.py
│   ├── app_build_number.txt (auto-generated)
│   ├── app_version.txt (auto-generated)
│   └── app_year.txt
├── assets/
│   └── ACG.ico
├── dist/           (executables)
└── build/          (temp build files)
```

## Testing

The project includes comprehensive unit and integration tests using pytest.

### Install Test Dependencies

```bash
pip install -r requirements.txt
```

Or install testing packages directly:
```bash
pip install pytest pytest-cov pytest-mock
```

### Running Tests

Run all tests:
```bash
pytest test_file_cleaner.py -v
```

Run with coverage report:
```bash
pytest test_file_cleaner.py --cov=file_cleaner --cov-report=html
```

Run specific test class:
```bash
pytest test_file_cleaner.py::TestRemoveFiles -v
```

Run specific test:
```bash
pytest test_file_cleaner.py::TestRemoveFiles::test_remove_old_files -v
```

### Test Coverage

The test suite covers:
- **Path resolution** - Both frozen and non-frozen execution modes
- **Version management** - Reading from external files and fallbacks
- **Logging setup** - Logger configuration and handlers
- **Date checking** - Last day of month detection (including leap years)
- **File filtering** - Pattern matching and date-based filtering
- **File removal** - Age-based deletion with error handling
- **Integration tests** - Complete workflows with exclusions

### Continuous Integration

To run tests in CI/CD pipelines:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest test_file_cleaner.py --cov=file_cleaner --cov-report=xml

# Generate coverage badge (optional)
coverage-badge -o coverage.svg
```

## Version Management

The application supports dynamic version and copyright year:
- Place `app_version.txt` in the application directory to override the default version
- Place `app_year.txt` in the application directory to override the copyright year
- If these files don't exist, defaults from the script are used

## Notes

- Files are evaluated based on their last modification time
- The `-e` option checks if the file was modified on the last day of the month (e.g., Jan 31, Feb 28/29, etc.)
- Use caution with recursive patterns (`**`) as they can affect many files
- Always test with non-critical files first
- Check the log file for detailed information about deleted files