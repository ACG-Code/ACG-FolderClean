"""
PyInstaller Build Script for ACG-FolderClean

Automates version management and executable building using PyInstaller.

Usage:
    build.py [--major | --minor | --patch]
    build.py (-h | --help)

Options:
    --major     Bump major version (resets minor and patch)
    --minor     Bump minor version (resets patch)
    --patch     Bump patch version
    -h --help   Show this help message

Copyright © 2025 Application Consulting Group, Inc.
Licensed under the MIT License - see LICENSE file for details.
"""

import os
import subprocess
import sys
from docopt import docopt

APP_NAME = 'ACG-FolderClean'
SCRIPT_NAME = 'file_cleaner.py'
BUILD_FILE = 'app_build_number.txt'
VERSION_FILE = 'app_version.txt'
YEAR_FILE = 'app_year.txt'
SPEC_FILE = 'ACG-FolderClean.spec'
VERSION_BASE = [1, 0, 0]

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
ICON_PATH = os.path.abspath(os.path.join(ROOT_DIR, '.', 'imgs', 'ACG.ico')).replace('\\', '/')
DIST_PATH = os.path.abspath(os.path.join(ROOT_DIR, '..', 'dist')).replace('\\', '/')
WORK_PATH = os.path.abspath(os.path.join(ROOT_DIR, '..', 'build')).replace('\\', '/')

def read_year():
    year = "2025"
    path = os.path.join(ROOT_DIR, YEAR_FILE)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            year = f.read().strip() or year
    return year

def read_build():
    path = os.path.join(ROOT_DIR, BUILD_FILE)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return int(f.read().strip()) + 1
    return 1

def write_build(build):
    path = os.path.join(ROOT_DIR, BUILD_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(build))

def bump_version(args):
    major, minor, patch = VERSION_BASE
    if args['--major']:
        major += 1
        minor = 0
        patch = 0
    elif args['--minor']:
        minor += 1
        patch = 0
    elif args['--patch']:
        patch += 1
    return major, minor, patch

def write_version_file(major, minor, patch, build, year):
    content = f"""# UTF-8
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, {build}),
    prodvers=({major}, {minor}, {patch}, {build}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'Application Consulting Group, Inc.'),
          StringStruct('FileDescription', '{APP_NAME}'),
          StringStruct('FileVersion', '{major}.{minor}.{patch}.{build}'),
          StringStruct('InternalName', '{APP_NAME}'),
          StringStruct('LegalCopyright', '{year} Application Consulting Group, Inc.'),
          StringStruct('OriginalFilename', '{SCRIPT_NAME}'),
          StringStruct('ProductName', '{APP_NAME}'),
          StringStruct('ProductVersion', '{major}.{minor}.{patch}.{build}')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"""
    path = os.path.join(ROOT_DIR, VERSION_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def write_spec_file():
    version_path = os.path.abspath(os.path.join(ROOT_DIR, VERSION_FILE)).replace('\\', '/')
    year_path = os.path.abspath(os.path.join(ROOT_DIR, YEAR_FILE)).replace('\\', '/')

    for path in [version_path, year_path, ICON_PATH]:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Required file missing: {path}")

    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['{SCRIPT_NAME}'],
    pathex=[],
    binaries=[],
    datas=[
        ('{version_path}', '.'),
        ('{year_path}', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=r'{ICON_PATH}',
    version='{version_path}'
)
"""
    path = os.path.join(ROOT_DIR, SPEC_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(spec_content)

def build_executable():
    spec_path = os.path.join(ROOT_DIR, SPEC_FILE)
    if not os.path.isfile(spec_path):
        raise FileNotFoundError(f"Spec file not found: {spec_path}")

    subprocess.run([
        'pyinstaller',
        spec_path,
        '--distpath', DIST_PATH,
        '--workpath', WORK_PATH,
        '--clean',
        '--noconfirm'
    ], check=True)

def main():
    """Main build process."""
    args = docopt(__doc__)

    print(f"Building {APP_NAME}...")
    print("-" * 50)

    year = read_year()
    build = read_build()
    major, minor, patch = bump_version(args)

    version_string = f"{major}.{minor}.{patch}.{build}"
    print(f"Version: {version_string}")
    print(f"Copyright Year: {year}")

    write_build(build)
    print("✓ Build number updated")

    write_version_file(major, minor, patch, build, year)
    print("✓ Version file created")

    write_spec_file()
    print("✓ Spec file created")

    print("-" * 50)
    print(f"{APP_NAME} build {version_string} © {year} Application Consulting Group")
    print("Building executable with PyInstaller...")
    print("-" * 50)

    try:
        build_executable()
        print("-" * 50)
        print(f"✓ Build completed successfully!")
        print(f"Executable location: {DIST_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())