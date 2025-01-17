"""
A tool that removes files filtered by a regular expression and time since creation.

*: All files deleted in a directory.
**: All files recursively deleted; directories and subdirectories.

Usage:
    ACG-FolderClean <expression> <age> [options]
    ACG-FolderClean (-h | --version)

Positional Arguments:
    <expression>                Directory to search for files.
    <age>                      Age in number of days.

Options:
    -e                          Exclude files created on the last day of a month from deletion.
    -h                          Display this screen.
    --version                   Show version information.

Copyright © 2025 Application Consulting Group, Inc.
"""

import calendar
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from glob import glob
from pathlib import Path

from docopt import docopt

APP_NAME = 'ACG-FolderClean'
APP_VERSION = '1.0.0'
APP_YEAR = '2025'
APP_COPYRIGHT = f'Copyright © {APP_YEAR} Application Consulting Group, Inc.'
APP_HELP = f'{APP_NAME}\nVersion: {APP_VERSION}\n{APP_COPYRIGHT}'
LOG_FILE = APP_NAME + '.log'
APP_PATH = ''


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


def remove_files(_files: list, _age: int = 1):
    deleted_files = 0
    cutoff_date = datetime.now() - timedelta(days=_age)
    for _file in _files:
        if Path(_file).stat().st_mtime < cutoff_date.timestamp():
            try:
                os.remove(_file)
                deleted_files += 1
                logging.info(f"Removed: {_file}")
            except OSError:
                logging.error(f"Error removing: {_file}")
    if deleted_files > 0:
        logging.info(f"Deleted {deleted_files} files.")
    else:
        logging.info("No files were deleted.")


if __name__ == '__main__':
    start_time = time.perf_counter()
    set_current_directory()
    configure_logging()
    files = []
    cmd_args = docopt(__doc__, version=APP_HELP)
    logging.info(f"{APP_NAME} started.  Parameters: {cmd_args}")
    expression = cmd_args['<expression>']
    age = int(cmd_args['<age>'])
    exclude_last_day = cmd_args['-e']
    if exclude_last_day:
        files = find_files_not_last_day_of_month(_expression= expression)
    else:
        for file in glob(expression, recursive=True):
            files.append(file)
    remove_files(_files=files, _age=age)
    logging.info(f"Execution complete in: {time.perf_counter() - start_time:0.4f} seconds")
