# ACG_FileCleaner

Copyright © 2025 Application Consulting Group, Inc.

A tool that removes files filtered by a regular expression and time since creation.

*: All files deleted in a directory.\
**: All files recursively deleted; directories and subdirectories.`

## Usage:
  `ACG-FolderClean <expression> <age> [options]`\
  `ACG-FolderClean (-h | --version)`
  
## Options:
  `<expression>`        The path to the directory.\
   `<age>`              Age in days to keep files.\
  `-h --help`           Display this screen.\
  `--version `          Display version information.
  
## Examples:
`ACG-FolderClean "C:\Users\John\Documents\*"  5`  Delete all file in the directory older than 5 days.\
`ACG-FolderClean "C:\Users\John\Documents\**"  5`  Delete all files in the directory and subdirectories older than 5 days.\
`ACG-FolderClean "C:\Users\John\Documents\File*"  5` Delete all files in the directory that match the expression (File*) older than 5 days.\
`ACG-FolderClean "C:\Users\John\Documents\File**"  5` Delete all files in the directory and subdirectories that match the expression (File*) older than 5 days.
