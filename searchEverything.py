import json, urllib, sys, re, socket, csv, time, argparse, http, search

startTime = time.time() # Start time of script execution

ARTISTS_CSV = "artists.csv"
RESULTS_CSV = "result.csv"
PLANTS_CSV = "plants.csv"

# Get an array of plants
plants = []
try:
    reader = csv.reader(open(PLANTS_CSV, 'r'))
    tempPlants = list(reader)
    for plant in tempPlants:
        plants.append(plant[0])
except FileNotFoundError :
    print("The plants file is not found. Quitting...")
    exit()

# Get the array of artists
artists = []
try:
    reader = csv.reader(open(ARTISTS_CSV, 'r'))
    tempArtists = list(reader)
    for artist in tempArtists:
        artists.append(artist[0])
except FileNotFoundError :
    print("The artists file is not found. Quitting...")
    exit()

# Open the results file
try:
    results_file = open(RESULTS_CSV, 'w')
    results_file.write("Plants, Artists (Ranking: higher = better), \n")
except FileNotFoundError :
    print("The results file is not found. Quitting...")
    exit()

for index, plant in enumerate(plants) :
    plantStartTime = time.time() # Start time for execution of script for current plant

    # The search query used
    queryAdd = " art artist painting"
    query = plant + queryAdd

    # Prints: "1 out of 427 : PLANT_NAME"
    print(index+1, "out of", len(plants), ":", plant)

    # Get a list of urls
    url1 = search.getUrls(query, "google", verbose=True)
    url2 = search.getUrls(query, "duckduckgo", verbose=True)
    urlList = [url1, url2]
    urls = list(set().union(*urlList)) # union() removes duplicates

    # Search the urls for occurrences of artist names

    ## Open each url and add to one string HTMLOfPages
    HTMLOfPages = ""
    for url in urls :
        html = search.getPageText(url, verbose=True, timeout=3)
        HTMLOfPages += html
    print("Finished downloading all pages. Searching for artists...")

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

    # Figure out how long the program's been running and print it out
    plantFinishTime = time.time()
    plantElapsedTime = (plantFinishTime - plantStartTime)
    totalElapsedTime = (plantFinishTime - startTime)
    print("Successfully added " + plant + " to results file in " + search.formatSeconds(plantElapsedTime) + ".")
    print("Total elapsed time: " + search.formatSeconds(totalElapsedTime))
    print("------------------------")
    print("")
