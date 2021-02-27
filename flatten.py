#! /usr/bin/env python3
from argparse import ArgumentParser
import os
import shutil
import sys
import re
from itertools import chain

__version__ = "0.1"

HELP = """
Flattens directory structure based on path pattern into single directory.
Pattern is bsically regular expession with folowwing additional logic:
- first pattern is split (by / or relevant path separator) into segments - each segment is then 
    considered separately with file path segment - all file segments must match and matching result will be included to flattened file name


"""


class Pattern:

    def __init__(self, pattern, sep, path_sep=None):
        self.path_sep = path_sep or os.sep
        p = pattern.split(self.path_sep)
        self.segments = list(map(lambda s: re.compile(s, re.UNICODE), p))
        self.sep = sep

    def _process_segment(self,m):
        res = m.group(0)
        for idx in range(1, (m.lastindex or 0)+1):
            res = res[0:m.start(idx)] + res[m.end(idx):]
        return res

    def new_name(self, path):
        segments = list(path.split(self.path_sep))
        res = []
        pos = 0
        while pos < len(segments):
            s = segments[pos]
            p = self.segments[pos]
            m = p.match(s)
            if m:
                res.append(self._process_segment(m))
                pos += 1
            else:
                return None
        return self.sep.join(res)


def parse_args():
    p = ArgumentParser(description=HELP)
    p.add_argument("-b", "--base", default=".",
                   help="Base directory, default current")
    p.add_argument("-r", "--replace-separator", default="-",
                   help="String to replace path separator with")
    p.add_argument("-d", "--destination", required=True,
                   help="destination directory")
    p.add_argument("--dry", action="store_true",
                   help="Dry run - just print command, but do not execute them, nothing should change on disk")
    p.add_argument("--move", action="store_true", help="Move files instead of copying them")

    p.add_argument("--version", action="version", version=__version__)

    p.add_argument("path_pattern", metavar="PATH_PATTERN",
                   help="path pattern to flatten")
    args = p.parse_args()
    return args


def main():
    args = parse_args()
    dest = args.destination

    def dry(fn, *local_args, **kwargs):
        if args.dry:
            if local_args or kwargs:
                ps = chain(local_args, map(lambda item: "{}={}".format(
                    item[0], item[1]), kwargs.items()))
                print("{}({})".format(fn.__name__, ", ".join(ps)))
            else:
                print("{}()", fn.__name__)
        else:
            fn(*args, **kwargs)

    pattern = Pattern(args.path_pattern, args.replace_separator)

    if not os.path.exists(dest):
        dry(os.makedirs, dest)
    if not os.path.isdir(dest):
        print("destination must be directory", file=sys.stderr)
        sys.exit(1)
    for (path, _, files) in os.walk(args.base,):
        if path == args.base:  # we just interested in subdirectories
            continue
        for f in files:
            full_path = os.path.join(path, f)
            p = os.path.join(path[len(args.base)+1:], f)
            fname = pattern.new_name(p)
            if fname:
                target_path =  os.path.join(dest, fname)
                if args.move:
                    dry(shutil.move, full_path, target_path)
                else:
                    dry(shutil.copy, full_path, target_path)


if __name__ == "__main__":
    main()
