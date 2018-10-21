#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setup(name='pyflogd',
      version='1.0.0',
      description='File system access monitoring daemon',
      long_description=long_description,
      author='Izzy Kulbe',
      author_email='pyflogd@unikorn.me',
      license='MIT',
      packages=['pyflogd'],
      entry_points = {
        "console_scripts": [
          "pyflogd = pyflogd.pyflogd:main",
        ],
      },
      install_requires=[
        'pyinotify',
        'docopt',
        'schema',
        'python-daemon',
        'lockfile',
      ],
    )
