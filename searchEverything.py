import json, urllib, sys, re, socket, csv, time, argparse, http, search

startTime = time.time()

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

artists = []
try:
    reader = csv.reader(open(ARTISTS_CSV, 'r'))
    tempArtists = list(reader)
    for artist in tempArtists:
        artists.append(artist[0])
except FileNotFoundError :
    print("The artists file is not found. Quitting...")
    exit()

try:
    results_file = open(RESULTS_CSV, 'w')
    results_file.write("Plants, Artists (Ranking: higher = better), \n")
except FileNotFoundError :
    print("The results file is not found. Quitting...")
    exit()

for index, plant in enumerate(plants) :
    plantStartTime = time.time()

    queryAdd = " art artist painting"

    query = plant + queryAdd
    print(index+1, "out of", len(plants), ":", plant)

    url1 = search.getUrls(query, "google", verbose=True)
    #url1=[]
    url2 = search.getUrls(query, "duckduckgo", verbose=True)

    in_first = set(url1)
    in_second = set(url2)
    in_second_but_not_in_first = in_second - in_first

    urls = url1 + list(in_second_but_not_in_first)
    #urls = ["http://google.com/","http://facebook.com"]
    ## Open ARTISTS_LIST as a list called artists


    # Search the urls for occurrences of artist names

    ## Open each url and add to one string HTMLOfPages
    HTMLOfPages = ""
    for url in urls :
        html = search.getPageText(url, verbose=True, timeout=3)
        HTMLOfPages += html
    print()
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

    #search.printOccurrences(counter, artists)
    search.resultsToCsv(counter, artists, query, plant, results_file)
    plantFinishTime = time.time()
    plantElapsedTime = (plantFinishTime - plantStartTime)
    totalElapsedTime = (plantFinishTime - startTime)
    print("Successfully added " + plant + " to results file in " + search.formatSeconds(plantElapsedTime) + ".")
    print("Total elapsed time: " + search.formatSeconds(totalElapsedTime))
