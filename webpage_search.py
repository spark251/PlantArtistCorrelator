import csv
import urllib.request
import urllib.parse
from urllib.parse import quote
import sys
import subprocess
from bs4 import BeautifulSoup
import json

ARTISTS_LIST = "artists.csv"

# Open the url as flowerHTML
try:
    html = urllib.request.urlopen(sys.argv[1]).read()
    soup = BeautifulSoup(html, "html.parser")
    texts = soup.findAll(text=True)
    paragraphs = ""
    for x in texts:
        paragraphs += str(x)
    flowerHTML = paragraphs
except (urllib.error.HTTPError, ValueError) :
    #flowerHTML = open(DEFAULT_FILE, 'r').read()
    print("The url you entered is not valid. Quitting...")
    exit()

#print(flowerHTML)

# Open ARTISTS_LIST as a list called artists
try:
    reader = csv.reader(open(ARTISTS_LIST, 'r'))
    artists = list(reader)
except FileNotFoundError :
    print("The artists file is not found. Quitting...")
    exit()

# For each artist, count the number of occurrences that artist has in the
# file and add it to an array (counter) with it's index corresponding to
# the index of that artist
counter = []
for index, artist in enumerate(artists, start=0):
    count = flowerHTML.count(artist[0])
    counter.append(count)

# The maximum number of occurrences of any given name
maxOccurrences = max(counter)

# Index of counter array with the max value
theIndex = [i for i, x in enumerate(counter) if x == maxOccurrences]

# Print out the results
if maxOccurrences == 0 :
    print("Sorry, no results");
else :
    print("Occurrences: ", maxOccurrences)
    for x in theIndex :
        print(" - Artist: ", artists[x][0])
        #print("Index: ", x)
