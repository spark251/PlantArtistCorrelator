# top_results.py
# usage: python3 top_results.py <flower> [csv]
#
# Takes a search query <flower> and searches google for the top results.
# Take those top results and search each page for the occurrences of each
# artist. Keep track of how many times those artist's names occur for all
# of the pages.
import json
import urllib
from urllib import request
import sys
from bs4 import BeautifulSoup
import re
import socket
import csv
import time

ARTIST_LIST = "artists.csv" # Default artist list

# Generate a list of the top 10(-ish) Google result urls for the query
try :
    query = sys.argv[1].replace(" ", "+")
except IndexError :
    print("You forgot to put in a search. Quitting...")
    exit()

def getSearch(searchQuery, startValue) :
    """
    # Google Search API (Depreciated)
    try:
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&q="+ query +"&start=" + str(startValue)
        #url = "apisearchsample.html"
        print(url)
        time.sleep(15)
        r = urllib.request.urlopen(url)
        rJson = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
        urls = []
        for result in rJson["responseData"]["results"] :
            urls.append(result["unescapedUrl"])
        return urls
    except (urllib.error.HTTPError, ValueError) :
        print("The query you entered is not valid. Quitting...")
        exit()
    """
    # DuckDuckGo parsing
    try:
        url = "http://duckduckgo.com/html/?q=" + query
        data = urllib.request.urlopen(url)
        parsed = BeautifulSoup(data, "html.parser")
        urls = []
        for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
            urls.append(i.a['href'])
        return urls
    except (urllib.error.HTTPError, ValueError) :
        print("The query you entered is not valid. Quitting...")
        exit()

urls = getSearch(query, 0)


# Search the urls for occurrences of artist names

## Open each url and add to one string HTMLOfPages
HTMLOfPages = ""
for url in urls :
    try :
        html = urllib.request.urlopen(url, timeout=1).read()
        soup = BeautifulSoup(html, "html.parser")
        texts = soup.findAll(text=True)
        paragraphs = ""
        for x in texts:
            paragraphs += str(x)
        HTMLOfPages += paragraphs
        print("Searching... ", url)
    except (socket.timeout, ConnectionRefusedError, urllib.error.URLError, ValueError) :
        print("Couldn't get: ", url)

## Open ARTISTS_LIST as a list called artists
try:
    artists_list = sys.argv[2]
except IndexError :
    artists_list = ARTISTS_LIST
try:
    reader = csv.reader(open(artists_list, 'r'))
    tempArtists = list(reader)
    artists = []
    for artist in tempArtists:
        artists.append(artist[0])
except FileNotFoundError :
    print("The artists file is not found. Quitting...")
    exit()
#print (artists)

## For each artist, count the number of occurrences that artist has in the
## file and add it to an array (counter) with it's index corresponding to
## the index of that artist

counter = []
for index, artist in enumerate(artists, start=0):
    count = HTMLOfPages.count(artist)
    counter.append(count)

## The maximum number of occurrences of any given name
maxOccurrences = max(counter)

## Print out all the artists that matched the search
for occurrences in reversed(range(1, maxOccurrences + 1)) :
    # Index of counter array with the max value
    theIndex = [i for i, x in enumerate(counter) if x == occurrences]

    # Print out the results
    if occurrences == 0 :
        print("No results");
    else :
        if len(theIndex) != 0 :
            print("Occurrences: ", occurrences)
            for x in theIndex :
                print(" - Artist: ", artists[x])
                #print("Index: ", x)
