# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dwolla'))
import version

setup(
    name='pydwolla',
    version=version.VERSION,
    description='An elegant Dwolla python wrapper',
    long_description='Pydwolla is an elegant API wrapper for Dwolla. You can do tasks like register new user, add a new bank account, transfer funds and more.',
    packages=['dwolla', 'dwolla.test'],
    author='Royce Haynes',
    author_email='royce.haynes@gmail.com',
    url='https://github.com/roycehaynes/pydwolla',
    license='MIT',
    test_suite='dwolla.test',
    install_requires=['requests>=1.1.0']
)