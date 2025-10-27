#!/usr/bin/env python
"""
Test runner script for ACG-FolderClean

Provides convenient commands for running tests with different options.

Copyright © 2025 Application Consulting Group, Inc.
Licensed under the MIT License - see LICENSE file for details.
"""

import sys
import subprocess
import argparse


def run_command(cmd):
    """Run a command and return the exit code"""
    print(f"\n{'=' * 60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'=' * 60}\n")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description='Run tests for ACG-FolderClean')
    parser.add_argument(
        'mode',
        choices=['all', 'unit', 'integration', 'coverage', 'quick', 'verbose'],
        default='all',
        nargs='?',
        help='Test mode to run'
    )

    args = parser.parse_args()

    base_cmd = ['pytest', 'test_file_cleaner.py']

    if args.mode == 'all':
        # Run all tests with coverage
        cmd = base_cmd + ['-v', '--cov=file_cleaner', '--cov-report=html', '--cov-report=term']

    elif args.mode == 'unit':
        # Run only unit tests
        cmd = base_cmd + ['-v', '-m', 'unit']

    elif args.mode == 'integration':
        # Run only integration tests
        cmd = base_cmd + ['-v', '-m', 'integration']

    elif args.mode == 'coverage':
        # Run with detailed coverage report
        cmd = base_cmd + [
            '--cov=file_cleaner',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=xml'
        ]

    elif args.mode == 'quick':
        # Run without coverage for speed
        cmd = base_cmd + ['-v', '-x']  # Stop at first failure

    elif args.mode == 'verbose':
        # Maximum verbosity
        cmd = base_cmd + ['-vv', '--tb=long']

    return run_command(cmd)


if __name__ == '__main__':
    sys.exit(main())