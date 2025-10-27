"""
Pytest configuration and shared fixtures for ACG-FolderClean tests

Copyright © 2025 Application Consulting Group, Inc.
Licensed under the MIT License - see LICENSE file for details.
"""

import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    # Cleanup
    import shutil
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    yield tmp_path
    # Cleanup
    if os.path.exists(tmp_path):
        os.remove(tmp_path)


@pytest.fixture
def old_file(temp_dir):
    """Create a file that is 30 days old"""
    file_path = os.path.join(temp_dir, 'old_file.txt')
    Path(file_path).touch()

    # Set modification time to 30 days ago
    old_time = (datetime.now() - timedelta(days=30)).timestamp()
    os.utime(file_path, (old_time, old_time))

    return file_path


@pytest.fixture
def recent_file(temp_dir):
    """Create a file that is 1 day old"""
    file_path = os.path.join(temp_dir, 'recent_file.txt')
    Path(file_path).touch()

    # Set modification time to 1 day ago
    recent_time = (datetime.now() - timedelta(days=1)).timestamp()
    os.utime(file_path, (recent_time, recent_time))

    return file_path


@pytest.fixture
def last_day_file(temp_dir):
    """Create a file modified on the last day of a month"""
    file_path = os.path.join(temp_dir, 'last_day_file.txt')
    Path(file_path).touch()

    # Set modification time to January 31, 2025
    last_day = datetime(2025, 1, 31, 12, 0, 0).timestamp()
    os.utime(file_path, (last_day, last_day))

    return file_path


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing"""
    from unittest.mock import MagicMock
    return MagicMock()


@pytest.fixture
def sample_files(temp_dir):
    """Create multiple sample files with different ages"""
    files = []
    ages = [1, 5, 10, 15, 30]  # days old

    for i, age in enumerate(ages):
        file_path = os.path.join(temp_dir, f'file_{i}.txt')
        Path(file_path).touch()

        old_time = (datetime.now() - timedelta(days=age)).timestamp()
        os.utime(file_path, (old_time, old_time))

        files.append(file_path)

    return files


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration after each test"""
    yield
    # Clear all handlers
    import logging
    logger = logging.getLogger('ACG-FolderClean')
    logger.handlers.clear()