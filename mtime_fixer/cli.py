#!/usr/bin/env python3
import argparse
import sys
from typing import Sequence

from .core import MtimeFixer

__all__ = [
    "main",
    "parse_args",
]


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    description = "A tool for fixing inconsistent timestamp metadata (atime, ctime, and mtime)."
    epilog = "For more information: https://github.com/simsekhalit/mtime-fixer"
    parser = argparse.ArgumentParser("mtime-fixer", description=description, epilog=epilog)
    parser.add_argument("-c", "--fix-ctimes", action="store_true",
                        help="change ctimes as well (requires root priviledges)")
    parser.add_argument("-f", "--fix-files", action="store_true", help="change timestamps of files as well")
    parser.add_argument("paths", metavar="PATH", nargs="+")

    return parser.parse_args(args)


def main(args: Sequence[str]) -> None:
    args = parse_args(args)
    mtime_fixer = MtimeFixer(args.fix_ctimes, args.fix_files)
    mtime_fixer.fix(args.paths)


if __name__ == "__main__":
    main(sys.argv[1:])
