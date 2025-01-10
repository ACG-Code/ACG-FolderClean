import os
import glob
from docopt import docopt
from datetime import datetime, timedelta

usage = """
file_cleaner.py

A tool that cleans out a directory based on file type and time since creation.

Usage:
  file_cleaner.py --directory <directory> --regex <regex> --time <time>
  file_cleaner.py -d <directory> -r <regex> -t <time>
  file_cleaner.py (-h | --help)
  
Options: 
  --directory -d        The path to the directory.
  --regex -r            The regular expresion to filter files, '*' for all. 
  --time -t             Time in number of days.
  -h --help             Display help.
"""

arguments = docopt(usage)

directory = arguments['<directory>']
regex = arguments['<regex>']
days = float(arguments['<time>'])

if not os.path.exists(directory):
    raise FileNotFoundError()

current_datetime = datetime.now()

full_regex = os.path.join(directory, regex)
matching_files = glob.glob(full_regex)
delete_count = 0

print(len(matching_files))

for file in matching_files:
    mtime = os.path.getmtime(file)
    creation_datetime = datetime.fromtimestamp(mtime)
    delta_time = current_datetime - creation_datetime

    if days >= abs(delta_time.days):
        try:
            os.remove(file)
            delete_count += 1
            print(f"Deleted: {file}")
        except:
            print(f"ERROR, failed to delete: {file}")

if delete_count == 0:
    print(f"No files created within {days} days matched the regular expression: {full_regex}")
else:
    print(f"{delete_count} files deleted, created within {days} days, matching the regular expression: {full_regex}")