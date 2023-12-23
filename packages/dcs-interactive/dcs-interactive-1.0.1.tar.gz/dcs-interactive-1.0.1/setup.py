#!/usr/bin/env python

#  SPDX-License-Identifier: MPL-2.0
#    Copyright (c) 2022 Philipp Le <philipp@philipple.de>.
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

setup(
    name='dcs-interactive',
    version='1.0.1',
    description='Interactive Simulations and Visualizations for the Lecture in Digital Communication Systems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Philipp Le',
    author_email='philipp@philipple.de',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dcs-interactive=dcs.main:main'
        ]
    },
    install_requires=[
        'numpy~=1.26.2',
        'scipy~=1.11.4',
        'matplotlib~=3.8.2',
        'toml~=0.10.2',
        'pydantic>=1.0.0,<2.0.0',
        'appdirs~=1.4.4',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Typing :: Typed',
    ],
)
