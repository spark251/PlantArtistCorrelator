import json, urllib, sys, re, socket, csv, time, argparse, http, search

ARTISTS_CSV = "artists.csv"
RESULTS_CSV = "result.csv"
PLANTS_CSV = "plants.csv"

plants = []
try:
    reader = csv.reader(open(PLANTS_CSV, 'r'))
    tempPlants = list(reader)
    for plant in tempPlants:
        plants.append(plant[0])
except FileNotFoundError :
    print("The plants file is not found. Quitting...")
    exit()

try:
    reader = csv.reader(open(ARTISTS_CSV, 'r'))
    tempArtists = list(reader)
    artists = []
    for artist in tempArtists:
        artists.append(artist[0])
except FileNotFoundError :
    print("The artists file is not found. Quitting...")
    exit()

for plant in plants :
    query = plant + " art artist painting"

    url1 = search.getUrls(query, "google", verbose=False)
    url2 = search.getUrls(query, "duckduckgo", verbose=False)

    in_first = set(url1)
    in_second = set(url2)
    in_second_but_not_in_first = in_second - in_first

    urls = url1 + list(in_second_but_not_in_first)
    ## Open ARTISTS_LIST as a list called artists


    # Search the urls for occurrences of artist names

    ## Open each url and add to one string HTMLOfPages
    HTMLOfPages = ""
    for url in urls :
        html = search.getPageText(url, verbose=False, timeout=3)
        HTMLOfPages += html

    # There is an artist named "Erro" and he get's matched for every single
    # "error" in the site text. Since no artist has "error" in their name
    # we can safely get rid of "error" strings without messing up the results.
    pattern = re.compile("error", re.IGNORECASE)
    HTMLOfPages = pattern.sub("", HTMLOfPages.lower())

    ## For each artist, count the number of occurrences that artist has in the
    ## file and add it to an array (counter) with it's index corresponding to
    ## the index of that artist

    counter = []
    for index, artist in enumerate(artists, start=0):
        count = HTMLOfPages.count(artist.lower())
        counter.append(count)
    #print(len(counter))

    search.printOccurrences(counter, artists)
