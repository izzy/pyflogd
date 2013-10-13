# pyflogd

pyflogd is a monitoring tool to support you when tracking down 
potential file system bottlenecks. It uses the inotify kernel API.

## Requirements

- Python
  - pyinotify
  - json
  - daemon
  - signal
  - lockfile
  - hashlib

### Notes on using pyflogd on Ubuntu

When pyinotify is installed via apt you will get an old version that has a 
known bug regarding recursive watching. When using this version it is not 
possible to track files and folders in folders that are created after pyflogd 
has started. To solve this, you can run `pip install --upgrade pyinotify`.

## Installation

The setup.py is currently untested and unfinished. At this point to use 
pyflogd just start the script `pyflogd/pyflogd.py` from your commandline. 

## Usage

> Usage:
>   pyflogd.py run [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
>   pyflogd.py start [-f | --only-files] [-r | --recursive] [-o <file> | --outfile=<file>] <folder> ...
>   pyflogd.py stop <folder> ...
>   pyflogd.py -h | --help
>   pyflogd.py -v | --version
> 
> Options:
>   -h --help                 Show this screen
>   -v --version              Show version
>   -r --recursive            Watch a folder recursivly
>   -f --only-files           Don't report events for folders
>   -o FILE --outfile=FILE    Write to file instead of stdout

### run

The `run` command starts pyflogd in foreground and outputs events to 
stdout when no `outfile` is supplied. 

Example:
```
pyflogd.py run --outfile=/tmp/pyflogd.log --recursive /path/to/folder1 \
           /path/to/folder2 /path/to/folder3
```

### start/stop

The `start` command starts a pyflogd daemon in the background and outputs 
events to the supplied `outfile`. To stop the daemon use the same folders
as for the start command and omit all other options like `outfile` or 
`recursive`.

Example:
```
pyflogd.py start --outfile=/tmp/pyflogd.log --recursive /path/to/folder1 \
           /path/to/folder2 /path/to/folder3

pyflogd.py stop /path/to/folder1 /path/to/folder2 /path/to/folder3
```
