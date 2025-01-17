import os
import tempfile
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from src.file_cleaner import main


class TestFileCleaner(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = self.test_dir.name

        # Create some test files
        self.old_file = os.path.join(self.test_dir_path, 'old_file.txt')
        self.new_file = os.path.join(self.test_dir_path, 'new_file.txt')
        self.last_day_file = os.path.join(self.test_dir_path, 'last_day_file.txt')

        with open(self.old_file, 'w') as f:
            f.write('This is an old file.')

        with open(self.new_file, 'w') as f:
            f.write('This is a new file.')

        with open(self.last_day_file, 'w') as f:
            f.write('This is a file modified on the last day of the month.')

        # Set the modification times
        old_time = datetime.now() - timedelta(days=10)
        new_time = datetime.now() - timedelta(days=1)
        last_day_time = datetime(datetime.now().year, datetime.now().month, 1) - timedelta(days=1)

        os.utime(self.old_file, (old_time.timestamp(), old_time.timestamp()))
        os.utime(self.new_file, (new_time.timestamp(), new_time.timestamp()))
        os.utime(self.last_day_file, (last_day_time.timestamp(), last_day_time.timestamp()))

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    @patch('sys.argv', ['file_cleaner.py', self.test_dir_path + '/*.txt', '5', '-e'])
    def test_file_cleaner(self):
        # Run the file cleaner
        main()

        # Check that the old file was deleted and the new file was not
        self.assertFalse(os.path.exists(self.old_file))
        self.assertTrue(os.path.exists(self.new_file))
        self.assertTrue(os.path.exists(self.last_day_file))


if __name__ == '__main__':
    unittest.main()