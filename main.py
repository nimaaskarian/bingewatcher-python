#!/home/nima/Documents/Other/bingewatcher-python3/bin/python3

import argparse, os, json, sys

import requests
from iterfzf import iterfzf
from serie import Serie, Season

parser = argparse.ArgumentParser( prog='bw.py', description="Keeps track of series that you're watching.")
parser.add_argument('seriesIndexes',action="extend", nargs="*", type=int, default=[])
parser.add_argument('-s', '--search', action="extend", nargs="+",type=str, default=[])
parser.add_argument('-S', '--exact-match', action="extend", nargs="+", type=str, default=[])

parser.add_argument('-f', '--include-finished', action='store_true')
parser.add_argument('-F', '--only-finished', action='store_true')
parser.add_argument('-E', '--extended', action='store_true')
parser.add_argument('-e', '--next-episode', action='store_true')
parser.add_argument('-D', '--delete-serie', action="store_true")

parser.add_argument('-n', '--new-serie', action="append", type=str, default=[])
parser.add_argument('-o', '--new-online', action="append", type=str, default=[])

parser.add_argument('-a', '--add-watched', action="store", type=int)
parser.add_argument('-A', '--add-season', action="append", type=str, default = [])
parser.add_argument('-r', '--remove-watched', action="store", type=int)
parser.add_argument('-d', '--directory', action="store", type=str)

default_dir = os.path.expanduser("~/.cache/bingewatcher")
args = parser.parse_args()
basenames = [name for name in os.listdir(default_dir) if name.endswith(".bw")]


def main():
    series = []
    for basename in basenames:
        file_path =  os.path.join(default_dir,basename)
        if os.path.isdir(file_path):
            continue
        try:
            # serie = Serie(basename.replace(".bw",""))
            serie = Serie.factory(basename[:-3], args.extended, args.next_episode)
            serie.load(file_path)
            series.append(serie)
        except:
            pass
    for name in args.new_serie:
        serie = Serie(name)
        series.append(serie)
        index = len(series)
        args.seriesIndexes.append(index)

    for query in args.new_online:
        search_url=f"https://www.episodate.com/api/search?q={query}&page=1"
        try:
            search_res = requests.get(search_url)
        except:
            raise Exception("Network error: couldn't access the API")
        search_json = json.loads(search_res.text)
        if not search_json["pages"]:
            raise Exception(f"Error! couldn't find the series {query}")
        def iterate_pages(pages):
            for page in range(1,pages+1):
                search_url=f"https://www.episodate.com/api/search?q={query}&page={page}"
                search_res = requests.get(search_url)
                search_json = json.loads(search_res.text)
                for serie in search_json["tv_shows"]:
                    # yield f'Name: {serie["name"]}; URL: {serie["permalink"]}'
                    yield json.dumps(serie)
        if int(search_json["total"]) == 1:
            show=search_json["tv_shows"][0]
        else:
            show=json.loads(iterfzf(iterate_pages(search_json["pages"]),exact=True))
        show_url=f"https://episodate.com/api/show-details?q={show['permalink']}"
        try:
            details = requests.get(show_url)
        except:
            raise Exception("Network error: couldn't access the API")
        details_json = json.loads(details.text)

        serie = Serie.factory(show["name"], args.extended, args.next_episode)
        series.append(serie)
        index = len(series)
        args.seriesIndexes.append(index)

        seasons_count = []
        for episode in details_json["tvShow"]["episodes"]:
            season = episode["season"]
            if season > len(seasons_count):
                seasons_count.append(1)
            else:
                seasons_count[season-1]+=1

        for season_count in seasons_count:
            serie.addSeason(Season(0,season_count))
        print(serie)

    for index,serie in enumerate(series):
        for match in args.exact_match:
            if (serie.match(match)):
                args.seriesIndexes.append(index+1)
        for search in args.search:
            if (serie.search(search)):
                args.seriesIndexes.append(index+1)
        
    if (args.exact_match or args.search) and not len(args.seriesIndexes):
        exit(1)

    for index in args.seriesIndexes:
        serie = series[index-1]
        file_path =  os.path.join(default_dir,serie.name+".bw")
        if (args.delete_serie):
            print(f"Warning: You sure you want to remove '{serie.name}' [y/N]", end=" ")
            sys.stdout.flush()
            try:
                ch = sys.stdin.read(1)
            except KeyboardInterrupt:
                ch = 'n'

            if (ch.lower()=='y'):
                os.remove(file_path)
                print(f"Info: '{serie.name}' removed")
            else:
                print("Info: Remove canceled.")
            continue

        serie.addWatchedEpisodes(args.add_watched)
        serie.removeWatchedEpisodes(args.remove_watched)
        for allString in args.add_season:
            serie.addSeason(Season(0, int(allString)))

        print(serie)

        if serie.isFinished():
            os.remove(file_path)
            file_path =  os.path.join(default_dir,"finished",serie.name+".bw")

        serie.write(file_path);

    if not len(args.seriesIndexes):
        for index,serie in enumerate(series):
            print(f"{ index+1}) ", end="")
            print(serie)

if __name__ == "__main__":
    main()
