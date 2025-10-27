"""
Unit tests for ACG-FolderClean file_cleaner.py

Copyright © 2025 Application Consulting Group, Inc.
Licensed under the MIT License - see LICENSE file for details.
"""

import calendar
import logging
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

import pytest

# Import the module to test
import sys
# Add parent directory (src) to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'src'))
import file_cleaner


class TestResolvePaths:
    """Tests for resolve_paths function"""

    def test_resolve_paths_not_frozen(self):
        """Test path resolution when running as script"""
        with patch.object(sys, 'frozen', False, create=True):
            with patch('os.path.abspath') as mock_abspath:
                with patch('os.path.dirname') as mock_dirname:
                    with patch('os.chdir') as mock_chdir:
                        mock_dirname.return_value = '/test/dir'
                        mock_abspath.return_value = '/test/dir'

                        app_path, source_path, log_file = file_cleaner.resolve_paths()

                        assert app_path == '/test/dir'
                        assert source_path == '/test/dir'
                        assert log_file.endswith('ACG-FolderClean.log')
                        mock_chdir.assert_called_once_with('/test/dir')

    def test_resolve_paths_frozen(self):
        """Test path resolution when running as compiled executable"""
        with patch.object(sys, 'frozen', True, create=True):
            with patch.object(sys, 'executable', '/exe/path/app.exe'):
                with patch.object(sys, '_MEIPASS', '/temp/meipass', create=True):
                    with patch('os.path.dirname', return_value='/exe/path'):
                        with patch('os.chdir') as mock_chdir:
                            app_path, source_path, log_file = file_cleaner.resolve_paths()

                            assert app_path == '/temp/meipass'
                            assert source_path == '/exe/path'
                            # On Windows, os.path.join uses backslashes
                            assert log_file.endswith('ACG-FolderClean.log')
                            assert 'ACG-FolderClean.log' in log_file
                            mock_chdir.assert_called_once_with('/exe/path')


class TestGetFileVersion:
    """Tests for get_file_version function"""

    def test_get_file_version_file_exists(self):
        """Test reading version from app_version.txt"""
        version_content = "FileVersion', '1.2.3'\n"
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=version_content)):
                version = file_cleaner.get_file_version('/test/path')
                assert version == '1.2.3'

    def test_get_file_version_file_not_exists(self):
        """Test fallback to VERSION constant when file doesn't exist"""
        with patch('os.path.exists', return_value=False):
            version = file_cleaner.get_file_version('/test/path')
            assert version == file_cleaner.VERSION

    def test_get_file_version_no_match(self):
        """Test fallback when version pattern not found"""
        version_content = "Some other content\n"
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=version_content)):
                version = file_cleaner.get_file_version('/test/path')
                assert version == file_cleaner.VERSION

    def test_get_file_version_exception(self):
        """Test fallback when exception occurs"""
        with patch('os.path.exists', side_effect=Exception("Test error")):
            version = file_cleaner.get_file_version('/test/path')
            assert version == file_cleaner.VERSION


class TestGetYear:
    """Tests for get_year function"""

    def test_get_year_file_exists(self):
        """Test reading year from app_year.txt"""
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='2025')):
                year = file_cleaner.get_year('/test/path')
                assert year == '2025'

    def test_get_year_file_not_exists(self):
        """Test fallback to current year when file doesn't exist"""
        with patch('os.path.exists', return_value=False):
            year = file_cleaner.get_year('/test/path')
            assert year == str(datetime.now().year)

    def test_get_year_with_whitespace(self):
        """Test reading year with whitespace"""
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data='  2026  \n')):
                year = file_cleaner.get_year('/test/path')
                assert year == '2026'

    def test_get_year_exception(self):
        """Test fallback when exception occurs"""
        with patch('os.path.exists', side_effect=Exception("Test error")):
            year = file_cleaner.get_year('/test/path')
            assert year == str(datetime.now().year)


class TestSetupLogging:
    """Tests for setup_logging function"""

    def test_setup_logging_creates_logger(self):
        """Test that setup_logging creates a logger with correct name"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            log_file = tmp.name

        try:
            logger = file_cleaner.setup_logging(log_file)
            assert logger.name == file_cleaner.APP_NAME
            assert logger.level == logging.INFO
            assert len(logger.handlers) == 2  # File and stream handlers
        finally:
            # Cleanup
            logger.handlers.clear()
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_setup_logging_handlers(self):
        """Test that logger has both file and stream handlers"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            log_file = tmp.name

        try:
            logger = file_cleaner.setup_logging(log_file)

            handler_types = [type(h).__name__ for h in logger.handlers]
            assert 'TimedRotatingFileHandler' in handler_types
            assert 'StreamHandler' in handler_types
        finally:
            logger.handlers.clear()
            if os.path.exists(log_file):
                os.remove(log_file)


class TestIsLastDayOfMonth:
    """Tests for is_last_day_of_month function"""

    def test_is_last_day_january(self):
        """Test last day of January (31st)"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Set modification time to January 31, 2025
            jan_31 = datetime(2025, 1, 31, 12, 0, 0).timestamp()
            os.utime(tmp_path, (jan_31, jan_31))

            assert file_cleaner.is_last_day_of_month(tmp_path) is True
        finally:
            os.remove(tmp_path)

    def test_is_not_last_day_january(self):
        """Test not last day of January (30th)"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Set modification time to January 30, 2025
            jan_30 = datetime(2025, 1, 30, 12, 0, 0).timestamp()
            os.utime(tmp_path, (jan_30, jan_30))

            assert file_cleaner.is_last_day_of_month(tmp_path) is False
        finally:
            os.remove(tmp_path)

    def test_is_last_day_february_leap_year(self):
        """Test last day of February in leap year (29th)"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Set modification time to February 29, 2024 (leap year)
            feb_29 = datetime(2024, 2, 29, 12, 0, 0).timestamp()
            os.utime(tmp_path, (feb_29, feb_29))

            assert file_cleaner.is_last_day_of_month(tmp_path) is True
        finally:
            os.remove(tmp_path)

    def test_is_last_day_february_non_leap_year(self):
        """Test last day of February in non-leap year (28th)"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Set modification time to February 28, 2025 (non-leap year)
            feb_28 = datetime(2025, 2, 28, 12, 0, 0).timestamp()
            os.utime(tmp_path, (feb_28, feb_28))

            assert file_cleaner.is_last_day_of_month(tmp_path) is True
        finally:
            os.remove(tmp_path)


class TestFindFilesNotLastDayOfMonth:
    """Tests for find_files_not_last_day_of_month function"""

    def test_find_files_filters_correctly(self):
        """Test that files modified on last day are filtered out"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = os.path.join(tmpdir, 'file1.txt')
            file2 = os.path.join(tmpdir, 'file2.txt')
            file3 = os.path.join(tmpdir, 'file3.txt')

            for f in [file1, file2, file3]:
                Path(f).touch()

            # Set different modification dates
            jan_31 = datetime(2025, 1, 31, 12, 0, 0).timestamp()
            jan_30 = datetime(2025, 1, 30, 12, 0, 0).timestamp()
            jan_15 = datetime(2025, 1, 15, 12, 0, 0).timestamp()

            os.utime(file1, (jan_31, jan_31))  # Last day - should be filtered
            os.utime(file2, (jan_30, jan_30))  # Not last day - should be included
            os.utime(file3, (jan_15, jan_15))  # Not last day - should be included

            pattern = os.path.join(tmpdir, '*.txt')
            result = file_cleaner.find_files_not_last_day_of_month(pattern)

            assert len(result) == 2
            assert file1 not in result
            assert file2 in result
            assert file3 in result


class TestRemoveFiles:
    """Tests for remove_files function"""

    def test_remove_old_files(self):
        """Test that old files are removed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            old_file = os.path.join(tmpdir, 'old_file.txt')
            recent_file = os.path.join(tmpdir, 'recent_file.txt')

            Path(old_file).touch()
            Path(recent_file).touch()

            # Make one file old (10 days ago)
            old_time = (datetime.now() - timedelta(days=10)).timestamp()
            os.utime(old_file, (old_time, old_time))

            # Create mock logger
            mock_logger = MagicMock()

            # Remove files older than 5 days
            file_cleaner.remove_files([old_file, recent_file], _age=5, logger=mock_logger)

            # Old file should be deleted
            assert not os.path.exists(old_file)
            # Recent file should still exist
            assert os.path.exists(recent_file)

            # Check logging
            mock_logger.info.assert_called()

    def test_remove_no_files_when_all_recent(self):
        """Test that no files are removed when all are recent"""
        with tempfile.TemporaryDirectory() as tmpdir:
            recent_file = os.path.join(tmpdir, 'recent_file.txt')
            Path(recent_file).touch()

            mock_logger = MagicMock()

            # Try to remove files older than 5 days
            file_cleaner.remove_files([recent_file], _age=5, logger=mock_logger)

            # File should still exist
            assert os.path.exists(recent_file)

            # Should log "No files were deleted"
            calls = [str(call) for call in mock_logger.info.call_args_list]
            assert any('No files were deleted' in str(call) for call in calls)

    def test_remove_handles_os_error(self):
        """Test that OSError is handled gracefully"""
        mock_logger = MagicMock()

        # Try to remove a non-existent file
        non_existent = '/path/to/nonexistent/file.txt'

        with patch('pathlib.Path.stat') as mock_stat:
            mock_stat.return_value.st_mtime = 0  # Very old timestamp

            # This should handle the OSError when trying to remove
            file_cleaner.remove_files([non_existent], _age=1, logger=mock_logger)

            # Should log error
            mock_logger.error.assert_called()

    def test_remove_uses_default_logger_if_none(self):
        """Test that function uses default logger if none provided"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            # Make file old
            old_time = (datetime.now() - timedelta(days=10)).timestamp()
            os.utime(test_file, (old_time, old_time))

            # Call without logger parameter
            file_cleaner.remove_files([test_file], _age=5)

            # File should be deleted
            assert not os.path.exists(test_file)


class TestIntegration:
    """Integration tests"""

    def test_full_cleanup_workflow(self):
        """Test complete file cleanup workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files with different ages
            files = []
            for i in range(5):
                file_path = os.path.join(tmpdir, f'file_{i}.txt')
                Path(file_path).touch()
                files.append(file_path)

            # Set different ages
            ages = [20, 15, 10, 5, 1]  # days old
            for file_path, age in zip(files, ages):
                old_time = (datetime.now() - timedelta(days=age)).timestamp()
                os.utime(file_path, (old_time, old_time))

            mock_logger = MagicMock()

            # Remove files older than 7 days
            file_cleaner.remove_files(files, _age=7, logger=mock_logger)

            # Files 0, 1, 2 should be deleted (20, 15, 10 days old)
            assert not os.path.exists(files[0])
            assert not os.path.exists(files[1])
            assert not os.path.exists(files[2])

            # Files 3, 4 should remain (5, 1 days old)
            assert os.path.exists(files[3])
            assert os.path.exists(files[4])

    def test_exclude_last_day_workflow(self):
        """Test workflow with last day of month exclusion"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files
            file1 = os.path.join(tmpdir, 'file1.txt')
            file2 = os.path.join(tmpdir, 'file2.txt')

            Path(file1).touch()
            Path(file2).touch()

            # Set file1 to last day of month, old enough to delete
            jan_31 = datetime(2025, 1, 31, 12, 0, 0).timestamp()
            os.utime(file1, (jan_31, jan_31))

            # Set file2 to not last day, old enough to delete
            jan_15 = datetime(2025, 1, 15, 12, 0, 0).timestamp()
            os.utime(file2, (jan_15, jan_15))

            # Find files not on last day
            pattern = os.path.join(tmpdir, '*.txt')
            filtered_files = file_cleaner.find_files_not_last_day_of_month(pattern)

            # Only file2 should be in the list
            assert file1 not in filtered_files
            assert file2 in filtered_files

            mock_logger = MagicMock()

            # Remove old files (today is way past January 2025)
            file_cleaner.remove_files(filtered_files, _age=1, logger=mock_logger)

            # file1 should still exist (excluded by last day filter)
            assert os.path.exists(file1)

            # file2 should be deleted
            assert not os.path.exists(file2)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])