#!/usr/bin/env python2
"""
pyflogd - File system access monitoring daemon written in Python

Usage:
  pyflogd run [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
  pyflogd start [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
  pyflogd stop <folder> ...
  pyflogd -h | --help
  pyflogd -v | --version

Options:
  -h --help                 Show this screen
  -v --version              Show version
  -r --recursive            Watch a folder recursivly
  -f --only-files           Don't report events for folders
  -o FILE --outfile=FILE    Write to file instead of stdout

"""

from __future__ import print_function

import os
import pyinotify
import json

from docopt import docopt, DocoptExit
from schema import Schema, SchemaError

pyflogd_version='0.1.1'
arguments = docopt(__doc__, help=True, version='pyflogd '+pyflogd_version)

def pyflogd_run(pid_file=None):
    if pid_file:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))

    wdd      = {}
    wm       = pyinotify.WatchManager()
    mask     = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_OPEN | pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MODIFY | pyinotify.IN_ACCESS

    handler  = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    for path in arguments['<folder>']:
        wdd[path] = wm.add_watch(path, mask, rec=arguments['--recursive'])

    notifier.loop()

def pyflog_cleanup(pid_file):
    try:
        with open(pid_file, 'r') as f:
            os.kill(int(f.read()), signal.SIGTERM)
        os.unlink(pid_file)
    except OSError as e:
        print('Could not stop daemon with lockfile' + pid_file)
    exit(255)

class EventHandler(pyinotify.ProcessEvent):
    def create_event_info(self, event, event_type):
        if arguments['--only-files'] and event.dir:
            return

        info = json.dumps({
            'type': event_type,
            'path': event.pathname
        })

        if arguments['--outfile']:
            with open(arguments['--outfile'], 'a') as f:
                f.write(info + '\n')
        else:
            print(info)

    def process_IN_CREATE(self, event):
        self.create_event_info(event, 'create')

    def process_IN_DELETE(self, event):
        self.create_event_info(event, 'delete')

    def process_IN_OPEN(self, event):
        self.create_event_info(event, 'open')

    def process_IN_CLOSE_NOWRITE(self, event):
        self.create_event_info(event, 'close_nowrite')

    def process_IN_CLOSE_WRITE(self, event):
        self.create_event_info(event, 'close_write')

    def process_IN_MODIFY(self, event):
        self.create_event_info(event, 'modify')

    def process_IN_ACCESS(self, event):
        self.create_event_info(event, 'access')


for path in arguments['<folder>']:
    try:
        Schema(os.path.exists).validate(path)
    except SchemaError:
        print('\nPath "' + path + '" does not exist\n')
        raise DocoptExit

if arguments['--outfile']:
    try:
        Schema(os.path.exists).validate(arguments['--outfile'])
    except SchemaError:
        print('Path "' + arguments['--outfile'] + '"')

if arguments['start'] or arguments['stop']:
    import daemon
    import signal
    import lockfile
    import hashlib

    m = hashlib.md5()
    m.update(json.dumps(arguments['<folder>'], sort_keys=True))
    proc_hash = m.hexdigest()
    lock_file = '/tmp/pyflogd_' + str(proc_hash)
    pid_file = lock_file + '.pid'

    if arguments['stop']:
        if not os.path.isfile(pid_file):
            print('There is no process running for the supplied directories.')
            exit(255)

        pyflog_cleanup(pid_file)
    else:
        if os.path.isfile(pid_file) and os.path.isfile(lock_file + '.lock'):
            print('There is already a pyflogd process for these directories '
                  'running.')
            exit(255)
                
        context = daemon.DaemonContext(
            pidfile = lockfile.FileLock(lock_file),
            working_directory = os.getcwd()
        )
        with context:
            pyflogd_run(pid_file)
else:
    pyflogd_run()

