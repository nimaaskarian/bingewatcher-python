from typing import List
class Season:
    watchedEpisodes: int
    allEpisodes: int
    index: int
    def __init__(self, watchedEpisodes: int, allEpisodes: int) -> None:
        self.index = -1
        self.watchedEpisodes = watchedEpisodes
        self.allEpisodes = allEpisodes

class Serie:
    name: str
    path: str
    seasons: List[Season]

    def search(self, search:str) -> bool:
        return search.lower() in self.name.lower()

    def match(self, search:str) -> bool:
        return search == self.name

    def __init__(self, name: str) -> None:
        self.name = name
        self.seasons = []
        self.path = None

    def __str__(self) -> str:
        return self.info()

    def print(self,spaces_after_name):
        print(f"{self.name}{(spaces_after_name-len(self.name))*' '}{self.info()}")

    def info(self) -> str:
        if not self.allEpisodes():
            return ""
        return f"{self.allEpisodes()}\t{self.progressPercentage():.{1}f}%\t{self.nextEpisodeString() or '-'}"
        # if self.isFinished():
        #     return info+"\n"
        # else:
        #     return f"""{info} Next: {self.nextEpisodeString()}\n"""

    def extendedString(self):
        seasonString = "".join([f"\tSeason {index+1}: {season.watchedEpisodes}/{season.allEpisodes}\n" for index,season in enumerate(self.seasons)])
        return f"""Name: {self.name}
\tEpisodes {self.allEpisodes()}
\tProgress {self.progressPercentage():.{3}f}%
\tNext: {self.nextEpisodeString()}
{seasonString}"""

    def load(self,path=None):
        if path is not None:
            self.path=path
        f = open(self.path)
        times_called = 0
        for line in f.readlines():
            times_called+=1
            [watched, all] = line.split("+")
            if all:
                self.addSeason(Season(int(watched),int(all)))
        if times_called < 1:
            raise Exception("This file is empty")

    def write(self,path=None):
        if path is None:
            path=self.path
        f = open(path, "w")
        for season in self.seasons:
            f.write(f"{ season.watchedEpisodes }+{ season.allEpisodes }\n")

    def currentSeason(self)->Season:
        for season in self.seasons:
            if season.watchedEpisodes != season.allEpisodes:
                return season
        raise Exception("Series is finished")

    def nextEpisodeString(self)->str:
        try:
            s = self.currentSeason()
        except Exception:
            return ""
        # Season index+1 is the number of the season. Because index is from 0, len(self.seasons)
        # Same goes for watchedEpisodes. We want the NEXT episode. So we add 1
        return f"S{s.index+1:02d}E{s.watchedEpisodes+1:02d}"

    def progressPercentage(self) -> float:
        if self.allEpisodes():
            return self.watchedEpisodes()*100/self.allEpisodes()
        return 0

    def addWatchedEpisodes(self, episodesCount: int) -> None:
        if not episodesCount:
            return
        if episodesCount < 0:
            return self.removeWatchedEpisodes(-episodesCount)
        print(f"Added {episodesCount} episodes to '{self.name}'.")
        while (episodesCount):
            try:
                currentSeason = self.currentSeason()
                currentSeason.watchedEpisodes += episodesCount
                episodesCount = 0
                if (currentSeason.watchedEpisodes > currentSeason.allEpisodes):
                    episodesCount = currentSeason.watchedEpisodes - currentSeason.allEpisodes
                    currentSeason.watchedEpisodes = currentSeason.allEpisodes
            except Exception:
                print(f"Warning: Your show is finished. But you have still {episodesCount} episodes to add.")
                return 

    def removeWatchedEpisodes(self, episodesCount: int) -> None: 
        if not episodesCount:
            return
        if episodesCount < 0:
            return self.addWatchedEpisodes(-episodesCount)
        print(f"Removed {episodesCount} episodes from '{self.name}'.")
        while (episodesCount):
            for season in reversed(self.seasons):
                if not season.watchedEpisodes: 
                    continue
                season.watchedEpisodes -= episodesCount 
                episodesCount = 0
                if season.watchedEpisodes < 0:
                    episodesCount = -season.watchedEpisodes
                    season.watchedEpisodes = 0
                break
            if (self.isEmpty()):
                return

    def addSeason(self, season: Season)->None:
        season.index=len(self.seasons)
        self.seasons.append(season)

    def replaceSeasonWithIndex(self, season: Season, index:int)->None:
        self.seasons[index] = season

    def allEpisodes(self) -> int:
        sum = 0
        for season in self.seasons:
            sum+=season.allEpisodes
        return sum

    def watchedEpisodes(self) -> int:
        sum = 0
        for season in self.seasons:
            sum+=season.watchedEpisodes
        return sum

    def isFinished(self) -> bool:
        for season in self.seasons:
            if season.watchedEpisodes != season.allEpisodes:
                return False
        return True

    def isEmpty(self) -> bool:
        for season in self.seasons:
            if season.watchedEpisodes:
                return False
        return True

    @staticmethod
    def factory(name:str,extended=False, nextEpisode=False):
        if (extended):
            return ExtendedSerie(name)
        if (nextEpisode):
            return EpisodeSerie(name)
        return Serie(name)

class ExtendedSerie(Serie):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    def print(self,spaces_after_name):
        print(self.extendedString())

class EpisodeSerie(Serie):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    def print(self,spaces_after_name):
        print(self.nextEpisodeString())
