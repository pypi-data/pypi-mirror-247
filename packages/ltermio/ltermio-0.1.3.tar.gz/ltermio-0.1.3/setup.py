#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme_md = f.read()

setup(
    name='ltermio',
    version='0.1.3',
    description='Lightweight POSIX terminal I/O library',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    license='Apache Software License',

    author='brookssu',
    author_email='yipeng00@gmail.com',
    url='https://github.com/brookssu/ltermio',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'cursor-demo = cursor:_test_cursor',
            'color256-demo = color256:_test_color256',
            'termkey-demo = termkey:_test_termkey',
        ]
    },
    keywords=[
        'ltermio',
        'termios',
        'cursor',
        'termkey',
        'color256',
        'keyboard',
        'CSI',
        'text composing',
        'ESC sequence',
        'POSIX terminal',
        'character terminal',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
