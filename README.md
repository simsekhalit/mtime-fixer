# Mtime Fixer
Mtime Fixer is a tool for fixing inconsistent timestamp metadata (atime, ctime, and mtime).
Sometimes timestamp metadata of folders are inconsistent with files inside them.
Mtime Fixer is a program for setting mtime (modification time) timestamp of folders according to files inside them.
Additionally, it can set ctime (change time) metadata as the same as mtime as well (with root privileges).

## Requirements
Python >= 3.8 is required. (CPython and PyPy are both supported)

## Installation
Mtime Fixer can be either installed directly via pip:
```shell
pip install mtime-fixer
```
Or it can be installed from the source:
```shell
git clone https://github.com/simsekhalit/mtime-fixer.git
python3 -m pip install ./mtime-fixer
```

## Manual
```
$ python3 -m mtime_fixer --help
usage: mtime-fixer [-h] [-c] [-f] PATH [PATH ...]

A tool for fixing inconsistent timestamp metadata (atime, ctime, and mtime).

positional arguments:
  PATH

optional arguments:
  -h, --help        show this help message and exit
  -c, --fix-ctimes  change ctimes as well (requires root priviledges)
  -f, --fix-files   change timestamps of files as well

For more information: https://github.com/simsekhalit/mtime-fixer
```
