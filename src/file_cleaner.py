import os
import glob
import logging
import calendar
import platform
from tkinter import CURRENT
from docopt import docopt
from datetime import datetime, timedelta

usage = """
file_cleaner

Copyright \u00A9 2025 Application Consulting Group, Inc.

A tool that removes files filtered by a regular expression and time since creation.

*: All files deleted in a directory.
**: All files recursively deleted; directories and subdirectories.

Usage:
  file_cleaner.py --regex <regex> --time <time> [--exclude-month-end | -e]
  file_cleaner.py -r <regex> -t <time> [--exclude-month-end | -e]
  file_cleaner.py (-h | --help)
  
Options: 
  --regex -r                 The regular expresion to filter files.
  --time, -t                 Time in number of days.
  --exclude-month-end, -e   Exclude files created on the last day of a month from deletion.
  -h --help                  Display help.
  
Examples:
  file_cleaner --directory C:\\Users\\John\\Documents\\ --regex **\*.txt --time 5
  file_cleaner -d C:\\Users\\John\\Documents\\ --r *.csv -t 1 -e
"""

def is_last_day_of_month(datetime):
    last_day = calendar.monthrange(datetime.year, datetime.month)
    return datetime.day == last_day

def logging_file_directory():
    if platform.system() == 'Linux':  
        log_path = os.path.join(os.path.expanduser('~'), '.FileCleaner')
    elif platform.system() == 'Windows':
        log_path = os.path.join(os.environ['APPDATA'], 'FileCleaner')
    else:
        log_path = os.path.join(os.path.expanduser('~'), 'Library', 'Logs', 'FileCleaner')
    
    os.makedirs(log_path, exist_ok=True)
    return log_path

arguments = docopt(usage)

regex = arguments['<regex>']
days = float(arguments['<time>'])
check_is_last_of_month = arguments['--exclude-month-end'] or arguments['-e']

print(f"Exclude month end was {check_is_last_of_month}")

current_datetime = datetime.now()
year = current_datetime.year
month = current_datetime.month
day = current_datetime.day
hour = current_datetime.hour
minute = current_datetime.minute
second = current_datetime.second

logging_directory = logging_file_directory()
logging_filename = f"FileCleaner_Log_{year}-{month}-{day}_H{hour}-M{minute}-S{second}.log"
logging_filename = os.path.join(logging_directory, logging_filename)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",  # Custom time format
                    filename=logging_filename,
                    filemode='w')

console_handler = logging.StreamHandler()

logger = logging.getLogger()
logger.addHandler(console_handler)

matching_files = glob.glob(regex, recursive = True)
delete_count = 0

for file in matching_files:
    mtime = os.path.getmtime(file)
    creation_datetime = datetime.fromtimestamp(mtime)
    delta_time = current_datetime - creation_datetime
    
    if check_is_last_of_month and is_last_day_of_month(creation_datetime):
        month_number = creation_datetime.month
        month_name = calendar.month_name[month_number]
        logger.info(f"Skipped file made at the end of {month_name} - {file}")
        continue

    if days >= abs(delta_time.days):
        try:
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                continue

            delete_count += 1
            logger.info(f"Deleted {file}")
        except:
            logger.error(f"Failed to delete {file}")

if delete_count == 0:
    logger.info(f"No files were created within {days} days matching the regular expression: {regex}")
else:
    logger.info(f"{delete_count} files deleted, created within {days} days, matching the regular expression: {regex}")
    
print (f"Log file path: {logging_filename}")