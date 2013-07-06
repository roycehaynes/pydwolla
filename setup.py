# -*- coding: utf-8 -*-

import os
import sys
import version

try:
    from setuptools import setup
except ImportError:
    from distutils.core improt setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dwolla'))

setup(
    name='pydwolla',
    version=version.VERSION,
    description='A python Dwolla API client',
    packages=['pydwolla'],
    author='Royce Haynes',
    author_email='royce.haynes@gmail.com',
    url='https://github.com/roycehaynes/pydwolla',
    license='MIT',
    test_suite='test',
    install_requires=['requests']
)