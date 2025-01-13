# ACG_FileCleaner

Copyright © 2025 Application Consulting Group, Inc.

A tool that removes files filtered by a regular expression and time since creation.

*: All files deleted in a directory.\
**: All files recursively deleted; directories and subdirectories.

#### Usage:
  file_cleaner --directory <directory> --regex <regex> --time <time>\
  file_cleaner -d <directory> -r <regex> -t <time>\
  file_cleaner (-h | --help)
  
#### Options:
  --directory -d        The path to the directory.\
  --regex -r            The regular expresion to filter files.\
  --time -t             Time in number of days.\
  -h --help             Display help.
  
#### Examples:
  file_cleaner --directory C:\Users\John\Documents\ --regex **/*.txt --time 5\
  file_cleaner -d C:\Users\John\Documents\ --r *.csv -t 1

## Logging File Locations
-Linux: /home/\<username\>/.FileCleaner/\
-Windows: C:\Users\\<username\>\AppData\Roaming\FileCleaner\\<br>
-MacOs: /Users/\<username\>/Library/Logs/FileCleaner/