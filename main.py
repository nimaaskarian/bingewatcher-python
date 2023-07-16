#!/bin/python3

import argparse, os
from typing import List

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

def percentage(progress,all):
    return round(progress*100*100/all)/100
class Season:
    watched_episodes: int
    all_episodes: int
    def __init__(self, watched_episodes: int, all_episodes: int) -> None:
        self.watched_episodes = watched_episodes
        self.all_episodes = all_episodes
    def is_finished(self) -> bool:
        return self.watched_episodes >= self.all_episodes
    def is_empty(self) -> bool:
        return self.watched_episodes == 0
    def add_watched_episodes_and_return_extra(self, episodes_count: int) -> int:
        self.watched_episodes += episodes_count
        if (self.watched_episodes > self.all_episodes):
            output = self.watched_episodes - self.all_episodes
            self.watched_episodes = self.all_episodes
            return output
        return 0
    def remove_watched_episodes_and_return_extra(self, episodes_count: int) -> int:
        self.watched_episodes -= episodes_count
        if (self.watched_episodes < 0):
            output = -self.watched_episodes
            self.watched_episodes = 0
            return output
        return 0

class Serie:
    name: str
    seasons: List[Season]
    def __init__(self, name: str) -> None:
        self.name = name
        self.seasons = []
    def __str__(self):
        return f"""Name: {self.name}
    Episodes: {self.all_episodes()}
    Progress: {percentage(self.watched_episodes(),self.all_episodes())}%
    """
    def add_watched_episodes(self, episodes_count: int) -> None:
        while (episodes_count):
            for season in self.seasons:
                if not season.is_finished():
                    episodes_count = season.add_watched_episodes_and_return_extra(episodes_count)
                    break
            if (self.is_finished()): 
                return 
    def remove_watched_episodes(self, episodes_count: int) -> None: 
        while (episodes_count):
            for season in reversed(self.seasons):
                if not season.is_empty():
                    episodes_count = season.remove_watched_episodes_and_return_extra(episodes_count)
                    break
            if (self.is_empty()):
                return
    def add_season(self, season: Season)->None:
        self.seasons.append(season)
    def replace_season_with_index(self, season: Season, index:int)->None:
        self.seasons[index] = season
    def all_episodes(self) -> int:
        sum = 0
        for season in self.seasons:
            sum+=season.all_episodes
        return sum
    def watched_episodes(self) -> int:
        sum = 0
        for season in self.seasons:
            sum+=season.watched_episodes
        return sum
    def is_finished(self) -> bool:
        for season in self.seasons:
            if not season.is_finished():
                return False
        return True
    def is_empty(self) -> bool:
        for season in self.seasons:
            if not season.is_empty():
                return False
        return True


args = parser.parse_args()
default_dir = os.path.join(os.path.expanduser("~"), ".cache/bingewatcher")
# print(os.path.exists(default_dir))

mySerie = Serie("Breaking Bad")
mySerie.add_season(Season(0,7))
mySerie.add_season(Season(0,13))
mySerie.add_season(Season(0,13))
print(mySerie)
mySerie.add_watched_episodes(8)
mySerie.add_watched_episodes(19)
mySerie.add_watched_episodes(8)
print(mySerie)
mySerie.remove_watched_episodes(34)
print(mySerie)
