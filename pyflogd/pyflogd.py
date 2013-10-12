#!/usr/bin/env python
"""
pyflogd - File system access monitoring daemon written in Python

Usage:
  pyflogd.py [-f | --only-files] [-d | --daemonize] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
  pyflogd.py (-h | --help)
  pyflogd.py (-v | --version)

Options:
  -h --help                 Show this screen
  -v --version              Show version
  -d --daemonize            Run in background
  -r --recursive            Watch a folder recursivly
  -f --only-files           Don't report events for folders
  -o FILE --outfile=FILE    Write to file instead of stdout

"""

from __future__ import print_function

import os
import pyinotify
import json

from docopt import docopt
from schema import Schema, SchemaError

pyflogd_version='0.0.1'
arguments = docopt(__doc__, help=True, version='pyflogd '+pyflogd_version)

def pyflogd_run():
    wdd      = {}
    wm       = pyinotify.WatchManager()
    mask     = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_OPEN | pyinotify.IN_CLOSE_NOWRITE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MODIFY | pyinotify.IN_ACCESS

    handler  = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    for path in arguments['<folder>']:
        wdd[path] = wm.add_watch(path, mask, rec=arguments['--recursive'])

    notifier.loop()

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
        print('Path "' + path + '" does not exist')

if arguments['--outfile']:
    try:
        Schema(os.path.exists).validate(arguments['--outfile'])
    except SchemaError:
        print('Path "' + arguments['--outfile'] + '"')

if arguments['--daemonize']:
    import daemon
    import signal
    import lockfile
    import hashlib

    proc_hash = hashlib.md5(json.dumps(arguments['<folder>'], sort_keys=True))
    pid_file = '/var/run/pyflogd_' + proc_hash + '.pid'

    context = daemon.DaemonContext(
        pidfile = lockfile.FileLock(pid_file)
    )
    context.signal_map = {
        signal.SIGTERM: pyflogd.cleanup,
        signal.SIGHUP:  'terminate',
        signal.SIGUSR1: pyflogd.print_status
    }

    with context:
        pyflogd_run()
else:
    pyflogd_run()

