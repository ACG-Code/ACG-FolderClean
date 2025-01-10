# ACG_FileCleaner
A tool that cleans out a directory based on file type and time since creation.

Usage:
  file_cleaner.py [--directory <directory>] [--regex <regex>] [--time <time>]
  file_cleaner.py [-d <d>] [-r <r>] [-t <t>]
  file_cleaner.py (-h | --help)
  
Options: 
  -h,--help                Display help.
  --directory, -d          The path to the directory.
  --filename, -f           The regular expresion to filter files, '*' for all. 
  --time, t <t>            Time in number of days.
