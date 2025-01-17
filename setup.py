from setuptools import setup, find_packages

setup(
    name='ACG_FileCleaner',
    version='1.0.0',
    author='Application Consulting Group, Inc.',
    author_email='info@acg.com',
    description='A tool that removes files filtered by a regular expression and time since creation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ACG-Code/ACG_FileCleaner',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'docopt',
    ],
    entry_points={
        'console_scripts': [
            'file_cleaner=src.file_cleaner:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)