# ACG_FileCleaner

Copyright © 2025 Application Consulting Group, Inc.

A tool that cleans out a directory based on file type and time since creation.

*: All.\
**: All recursive.

#### Usage:
  file_cleaner.py --directory <directory> --regex <regex> --time <time>\
  file_cleaner.py -d <directory> -r <regex> -t <time>\
  file_cleaner.py (-h | --help)
  
#### Options:
  --directory -d        The path to the directory.\
  --regex -r            The regular expresion to filter files.\
  --time -t             Time in number of days.\
  -h --help             Display help.
  
#### Examples:
  file_cleaner.py --directory C:\Users\John\Documents\ --regex **/*.txt --time 5\
  file_cleaner.py -d C:\Users\John\Documents\ --r *.csv -t 1

## Logging File Locations
-Linux: /home/\<username\>/.FileCleaner/\
-Windows: C:\Users\\<username\>\AppData\Roaming\FileCleaner\\<br>
-MacOs: /Users/\<username\>/Library/Logs/FileCleaner/