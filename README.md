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
