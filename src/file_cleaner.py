"""
A tool that removes files filtered by a regular expression and time since creation.

*: All files deleted in a directory.
**: All files recursively deleted; directories and subdirectories.

Usage:
    ACG-FolderClean <expression> <age> [options]
    ACG-FolderClean (-h | --version)

Positional Arguments:
    <expression>               Directory to search for files.
    <age>                      Age in number of days.

Options:
    -e                          Exclude files created on the last day of a month from deletion.
    -h                          Display this screen.
    --version                   Show version information.

Licensed under the MIT License - see LICENSE file for details.
"""

import calendar
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta
from glob import glob
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Tuple

from docopt import docopt

APP_NAME = 'ACG-FolderClean'
VERSION = '1.0.0'
APP_VERSION = '1.0.0'
APP_YEAR = '2025'
APP_COPYRIGHT = f'Copyright © {APP_YEAR} Application Consulting Group, Inc.'
APP_HELP = f'{APP_NAME}\nVersion: {APP_VERSION}\n{APP_COPYRIGHT}'
LOG_FILE = APP_NAME + '.log'
APP_PATH = ''


def resolve_paths() -> Tuple[str, str, str]:
    """
    Resolve application paths for both frozen and non-frozen execution.

    Returns:
        Tuple of (app_path, source_path, log_file)
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable (PyInstaller)
        source_path = os.path.dirname(sys.executable)
        app_path = getattr(sys, '_MEIPASS', source_path)
    else:
        # Running as script
        source_path = os.path.abspath(os.path.dirname(__file__))
        app_path = source_path

    # Change to source directory
    os.chdir(source_path)

    log_file = os.path.join(source_path, f'{APP_NAME}.log')
    return app_path, source_path, log_file


def get_file_version(app_path: str) -> str:
    """
    Get version from app_version.txt file if it exists.

    Args:
        app_path: Path to application directory

    Returns:
        Version string or VERSION constant
    """
    try:
        version_file = os.path.join(app_path, 'app_version.txt')
        if os.path.exists(version_file):
            with open(version_file, 'r') as file:
                for line in file:
                    match = re.search(r"FileVersion',\s*'([\d.]+)'", line)
                    if match:
                        return match.group(1)
    except Exception:
        pass
    return VERSION


def get_year(app_path: str) -> str:
    """
    Get copyright year from app_year.txt file if it exists.

    Args:
        app_path: Path to application directory

    Returns:
        Year string or current year
    """
    try:
        year_file = os.path.join(app_path, 'app_year.txt')
        if os.path.exists(year_file):
            with open(year_file, 'r') as file:
                return file.read().strip()
    except Exception:
        pass
    return str(datetime.now().year)


def setup_logging(log_file: str) -> logging.Logger:
    """
    Setup logging with rotation and both file and console handlers.

    Args:
        log_file: Path to log file

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # File handler with rotation (keeps 7 days of logs)
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )

    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    )

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def set_current_directory() -> None:
    global LOG_FILE
    global APP_PATH
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    APP_PATH = application_path
    _directory = os.path.dirname(application_path)
    LOG_FILE = os.path.join(application_path, fr'{APP_NAME}_logs\{LOG_FILE}')
    os.chdir(_directory)


def configure_logging() -> None:
    if not os.path.exists(os.path.join(APP_PATH, fr'{APP_NAME}_logs')):
        os.makedirs(os.path.join(APP_PATH, fr'{APP_NAME}_logs'))
        open(LOG_FILE, 'w').close()
    logging.basicConfig(
        filename=LOG_FILE,
        format="%(asctime)s - " + APP_NAME + " - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # Also log to stdout
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def is_last_day_of_month(file_path):
    # Get the last modified time of the file
    mtime = os.path.getmtime(file_path)
    modified_date = datetime.fromtimestamp(mtime)

    # Get the last day of the month
    last_day = calendar.monthrange(modified_date.year, modified_date.month)[1]

    # Check if the modified date is the last day of the month
    return modified_date.day == last_day


def find_files_not_last_day_of_month(_expression: str) -> list:
    no_end_date = []
    _files = glob(_expression, recursive=True)
    for _file in _files:
        if not is_last_day_of_month(_file):
            no_end_date.append(_file)
    return no_end_date


def remove_files(_files: list, _age: int = 1, logger=None):
    if logger is None:
        logger = logging.getLogger(APP_NAME)
    deleted_files = 0
    cutoff_date = datetime.now() - timedelta(days=_age)
    for _file in _files:
        if Path(_file).stat().st_mtime < cutoff_date.timestamp():
            try:
                os.remove(_file)
                deleted_files += 1
                logger.info(f"Removed: {_file}")
            except OSError:
                logger.error(f"Error removing: {_file}")
    if deleted_files > 0:
        logger.info(f"Deleted {deleted_files} files.")
    else:
        logger.info("No files were deleted.")


if __name__ == '__main__':
    start_time = time.perf_counter()

    # Setup paths and logging first
    app_path, source_path, log_file = resolve_paths()
    logger = setup_logging(log_file)

    # Get version info
    version = get_file_version(app_path)
    year = get_year(app_path)

    # Log startup information
    logger.info(f"{APP_NAME} Version: {version} | © {year} Application Consulting Group, Inc.")

    files = []
    cmd_args = docopt(__doc__, version=APP_HELP)
    logger.info(f"{APP_NAME} started.  Parameters: {cmd_args}")
    expression = cmd_args['<expression>']
    age = int(cmd_args['<age>'])
    exclude_last_day = cmd_args['-e']
    if exclude_last_day:
        files = find_files_not_last_day_of_month(_expression= expression)
    else:
        for file in glob(expression, recursive=True):
            files.append(file)
    remove_files(_files=files, _age=age, logger=logger)
    logger.info(f"Execution complete in: {time.perf_counter() - start_time:0.4f} seconds")