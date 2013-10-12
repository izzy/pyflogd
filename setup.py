#!/usr/bin/env python

from distutils.core import setup

setup(name='pyflogd',
      version='0.0.1',
      description='File system access monitoring daemon',
      author='Izzy Kulbe',
      author_email='pyflogd@unikorn.me',
      packages=['pyflogd'],
      license='MIT',
      requires=['inotifyx', 'docopt', 'schema'],
      )
