"""
Setup script for ACG-FolderClean

Copyright © 2025 Application Consulting Group, Inc.
Licensed under the MIT License - see LICENSE file for details.
"""

from setuptools import setup, find_packages
import os

# Read the version from file if it exists
version = '1.0.0'
version_file = os.path.join('src', 'app_version.txt')
if os.path.exists(version_file):
    with open(version_file, 'r') as f:
        for line in f:
            if 'FileVersion' in line:
                import re
                match = re.search(r"'([\d.]+)'", line)
                if match:
                    version = match.group(1)
                    break

# Read the README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='acg-folderclean',
    version=version,
    author='Application Consulting Group, Inc.',
    author_email='info@acgconsulting.com',
    description='A tool that removes files filtered by a regular expression and time since creation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/your-org/ACG-FolderClean',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=['file_cleaner'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.8',
    install_requires=[
        'docopt>=0.6.2',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-mock>=3.10.0',
            'pytest-timeout>=2.1.0',
            'flake8>=6.0.0',
            'black>=23.0.0',
            'pylint>=2.17.0',
        ],
        'build': [
            'pyinstaller>=5.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'acg-foldercean=file_cleaner:main',
        ],
    },
    license='MIT',
)