#!/bin/python3

import argparse, os

parser = argparse.ArgumentParser( prog='bw.py', description="Keeps track of series that you're watching.")
parser.add_argument('seriesIndexes',action="extend", nargs="*", type=int, default=[])
parser.add_argument('-s', '--search', action="append", type=str, default=[])
parser.add_argument('-S', '--exact-match', action="append", type=str, default=[])

parser.add_argument('-f', '--include-finished', action='store_true')
parser.add_argument('-F', '--only-finished', action='store_true')
parser.add_argument('-E', '--extended', action='store_true')
parser.add_argument('-e', '--next-episode', action='store_true')

args = parser.parse_args()
print(os.path.expanduser("~"))
print(args)
