#!/usr/bin/env python

__all__ = ['main']

import os
import sys
import argparse

def main(argv=None):

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser('trim')
    parser.add_argument("chars", nargs='?', default=None)
    parser.add_argument("file", nargs="?", default=None)
    parser.add_argument('-l', '--left', action='store_true')
    parser.add_argument('-r', '--right', action='store_true')
    args = parser.parse_args(sys.argv[1:])

    if args.file:
        file = open(args.file)
    else:
        file = sys.stdin

    if args.left:
        strip = str.lstrip
    elif args.right:
        strip = str.rstrip
    else:
        strip = str.strip

    import signalhandlers
    signalhandlers.install_exit_on_sigpipe_handler()

    for line in file:
        line = line[:-1] # don't operate on trailing newline
        output = strip(line, args.chars)
        print(output)

if __name__ == '__main__':
    main(sys.argv[1:])
