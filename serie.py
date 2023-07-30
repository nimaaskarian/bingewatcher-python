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
    seasons: List[Season]
    def __init__(self, name: str) -> None:
        self.name = name
        self.seasons = []
    def __str__(self):
        return f"""Name: {self.name}
    Episodes: {self.allEpisodes()}
    Progress: {round(self.progressPercentage(),2)}%
    """
    def findCurrentSeason(self)->Season:
        for season in self.seasons:
            if season.watchedEpisodes != season.allEpisodes:
                return season
        raise Exception("Series is finished")
    def nextEpisodeString(self)->str:
        try:
            s = self.findCurrentSeason()
        except Exception:
            return ""
        # Season index+1 is the number of the season. Because index is from 0, len(self.seasons)
        # Same goes for watchedEpisodes. We want the NEXT episode. So we add 1
        return f"S{s.index+1:02d}E{s.watchedEpisodes+1:02d}"
    def progressPercentage(self):
        return self.watchedEpisodes()*100/self.allEpisodes()
    def addWatchedEpisodes(self, episodesCount: int) -> None:
        while (episodesCount):
            try:
                currentSeason = self.findCurrentSeason()
                currentSeason.watchedEpisodes += episodesCount
                episodesCount = 0
                if (currentSeason.watchedEpisodes > currentSeason.allEpisodes):
                    episodesCount = currentSeason.watchedEpisodes - currentSeason.allEpisodes
                    currentSeason.watchedEpisodes = currentSeason.allEpisodes
            except Exception:
                print(f"Warning: Your show is finished. But you have still {episodesCount} episodes to add.")
                return 
    def removeWatchedEpisodes(self, episodesCount: int) -> None: 
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
