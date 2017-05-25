#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
phototeller setup
@version 0.0.1
"""

from setuptools import setup

setup(
    name='phototeller',
    version='0.0.1',
    author='guessme',
    packages=['phototeller'],
    install_requires=[
        'tornado'
    ],
    entry_points={
        'console_scripts': [
            'phototeller=app:main'
        ]
    }
)