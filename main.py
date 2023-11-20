#!/home/nima/Documents/Other/bingewatcher-python3/bin/python3

import argparse, os, json, sys
import numpy as np

from typing import List
import requests
from iterfzf import iterfzf
from serie import Serie, Season

default_dir = os.path.expanduser("~/.cache/bingewatcher")
parser = argparse.ArgumentParser( prog='bw.py', description="Keeps track of series that you're watching.")
parser.add_argument('seriesIndexes',action="extend", nargs="*", type=int, default=[])
parser.add_argument('-s', '--search', action="append", type=str, default=[])
parser.add_argument('-S', '--exact-match', action="append", type=str, default=[])

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
parser.add_argument('-d', '--directory', action="store", type=str, default=default_dir)

args = parser.parse_args()

def read_dir_for_series(dir_name:str)-> List[Serie]:
    series = []
    basenames = [name for name in os.listdir(dir_name) if name.endswith(".bw")]
    for basename in basenames:
        file_path =  os.path.join(dir_name,basename)
        if os.path.isdir(file_path):
            continue
        try:
            # serie = Serie(basename.replace(".bw",""))
            serie = Serie.factory(basename[:-3], args.extended, args.next_episode)
            serie.load(file_path)
            series.append(serie)
        except:
            pass
    return series


def findSerieInList(series:List[Serie],find:Serie) -> bool:
    for serie in series:
        if serie.match(find.name):
            return True;
    return False;

def get_online_serie(query:str, args)->Serie:
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

    seasons_count = []
    for episode in details_json["tvShow"]["episodes"]:
        season = episode["season"]
        if season > len(seasons_count):
            seasons_count.append(1)
        else:
            seasons_count[season-1]+=1

    for season_count in seasons_count:
        serie.addSeason(Season(0,season_count))
    return serie

def delete_serie(serie):
    print(f"Warning: You sure you want to remove '{serie.name}' [y/N]", end=" ",flush=True)
    try:
        ch = input()
    except KeyboardInterrupt:
        ch = 'n'

    if (ch.lower()=='y'):
        os.remove(serie.path)
        print(f"Info: '{serie.name}' removed")
    else:
        print("Info: Remove canceled.")

def get_max_length(length_string:List[int]):
    SPACES_AFTER_NAME = 4
    return np.max(length_string)+SPACES_AFTER_NAME

def main():
    series = read_dir_for_series(args.directory)

    if args.include_finished:
        series += read_dir_for_series(os.path.join(args.directory, "finished"))
    if args.only_finished:
        series = read_dir_for_series(os.path.join(args.directory, "finished"))

    def add_new_serie(serie:Serie):
        if not findSerieInList(series, serie):
            return series.append(serie)
        raise Exception(f"Error: You already have serie '{serie.name}'. But you tried to add it again.")

    for new_serie in args.new_serie:
        serie = Serie(new_serie)
        add_new_serie(serie)
        index = len(series)
        args.seriesIndexes.append(index)

    for query in args.new_online:
        serie = get_online_serie(query, args)
        add_new_serie(serie)
        index = len(series)
        args.seriesIndexes.append(index)

    should_exit_failure = False
    for exact_match in args.exact_match:
        matched = False
        for index,serie in enumerate(series):
            if (serie.match(exact_match)):
                args.seriesIndexes.append(index+1)
                matched = True
        if not matched:
            print(f"Couldn't find a serie named '{exact_match}'")
            should_exit_failure = True

    for search in args.search:
        found = False
        for index,serie in enumerate(series):
            if (serie.search(search)):
                args.seriesIndexes.append(index+1)
                found = True
        if not found:
            print(f"Couldn't find a serie that matches '{search}'")
            should_exit_failure = True

    for index in args.seriesIndexes:
        if index-1 >= len(series):
            print(f"Couldn't find a serie with index '{index}'")
            should_exit_failure=True

    selected_series = [series[index-1] for index in args.seriesIndexes if index-1 < len(series)]
    if (len(selected_series)):
        for serie in selected_series:
            if (args.delete_serie):
                delete_serie(serie)
                serie.path = None
                continue

            serie.addWatchedEpisodes(args.add_watched)
            serie.removeWatchedEpisodes(args.remove_watched)
            for allString in args.add_season:
                serie.addSeason(Season(0, int(allString)))

            if serie.path is None:
                serie.path=os.path.join(args.directory,serie.name+ ".bw")
            serie.write();

        max_name_size = get_max_length([len(serie.name) for serie in selected_series])
        if (not args.extended and not args.next_episode) and not args.delete_serie:
            print("NAME", " "*(max_name_size-4), "EP\t","PROG\t", "NEXT", sep="")

        for serie in selected_series:
            if serie.path is None:
                continue
            serie.print(max_name_size)

    for serie in series:
        if serie.isFinished() and os.path.dirname(serie.path)==args.directory:
            os.remove(serie.path)
            serie.path = os.path.join(args.directory,"finished",serie.name+".bw")
            serie.write()
        if not serie.isFinished() and os.path.dirname(serie.path)==os.path.join(args.directory, "finished"):
            os.remove(serie.path)
            serie.path = os.path.join(args.directory,serie.name+".bw")
            serie.write()

    if should_exit_failure:
        exit(1)
    if not len(selected_series):
        max_name_size = get_max_length([len(serie.name) for serie in series])
        if (not args.extended and not args.next_episode):
            print("INDEX\t","NAME", " "*(max_name_size-4), "EP\t","PROG\t", "NEXT", sep="")
        for index,serie in enumerate(series):
            print(index+1,"\t", sep="", end="")
            serie.print(max_name_size)
        

if __name__ == "__main__":
    main()
