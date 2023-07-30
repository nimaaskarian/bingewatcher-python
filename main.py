#!/bin/python3

import argparse, os
from serie import Serie, Season

parser = argparse.ArgumentParser( prog='bw.py', description="Keeps track of series that you're watching.")
parser.add_argument('seriesIndexes',action="extend", nargs="*", type=int, default=[])
parser.add_argument('-s', '--search', action="append", type=str, default=[])
parser.add_argument('-S', '--exact-match', action="append", type=str, default=[])

parser.add_argument('-f', '--include-finished', action='store_true')
parser.add_argument('-F', '--only-finished', action='store_true')
parser.add_argument('-E', '--extended', action='store_true')
parser.add_argument('-e', '--next-episode', action='store_true')
parser.add_argument('-D', '--delete-series', action="store_true")

parser.add_argument('-a', '--add-watched', action="store", type=int)
parser.add_argument('-r', '--delete-watched', action="store", type=int)
parser.add_argument('-d', '--directory', action="store", type=str)



args = parser.parse_args()
default_dir = os.path.join(os.path.expanduser("~"), ".cache/bingewatcher")

f = open("main.py")
print(f)
mySerie = Serie("Breaking Bad")
mySerie.addSeason(Season(0,7))
mySerie.addSeason(Season(0,13))
mySerie.addSeason(Season(0,13))
print(mySerie)
# mySerie.addWatchedEpisodes(8)
mySerie.addWatchedEpisodes(35)
# mySerie.addWatchedEpisodes(8)
print(mySerie)
mySerie2 = Serie("Sopranos")
path = os.path.expanduser("~/.cache/bingewatcher/the sopranos")
mySerie2.load(path)
print(mySerie2)
mySerie2.addWatchedEpisodes(1)
print(mySerie2)
mySerie2.write(path)
# mySerie.removeWatchedEpisodes(28)
# print(mySerie.nextEpisodeString())
# print(mySerie)
