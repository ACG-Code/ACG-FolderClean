import os
import json
import glob
from re import I
from docopt import docopt
from datetime import datetime, timedelta

# TODO: Replace this import with one relevant to client
from tm1py_config_connect import ConfigConnector

usage = """
file_cleaner.py
Run this with a chore every hour.
Get every error log in the past hour or time specified.

Usage:
  file_cleaner.py [--directory <directory>] [--regex <regex>] [--days <days>]
  file_cleaner.py [-d <d>] [-r <r>] [-d <d>]
  file_cleaner.py (-h | --help)

Options: 
  -h,--help                Display help.
  --directory, -d          The path to the directory.
  --filename, -f           The regular expresion to filter files, '*' for all. 
  --days, d <d>   Number of days ago.
"""

arguments = docopt(usage)

directory = float(arguments['--directory'])
regex = float(arguments['--regex'])
days = float(arguments['--days'])

if not os.path.exists(directory):
    raise FileNotFoundError()

current_datetime = datetime.now()

full_regex = os.path.join(directory, regex)
matching_files = glob.glob(full_regex)

for file in matching_files:
    mtime = os.path.getmtime(file)
    creation_datetime = datetime.fromtimestamp(mtime)
    delta_time = current_datetime - creation_datetime
    
    if delta_time.days > days:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except:
            print(f"ERROR, failed to delete: {file}")