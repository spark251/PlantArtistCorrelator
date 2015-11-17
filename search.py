import urllib
import urllib.parse
import urllib.request
import csv
import sys
import re
import time
from bs4 import BeautifulSoup # To get everything

artist_filename = "artists.csv"
# import artists

f = open(artist_filename, 'rt')
artists = []
try:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        artists.append(row)
finally:
    f.close()

print(len(artists))
# Get the HTML from the search

plant = sys.argv[1]
print(plant)
save_filename = plant + ".csv"

numbers_of_results = []
with open(save_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    for artist in artists:
        query = { 'q' : "\"" + plant + "\" \"" + artist[0] + "\" \"artist\" OR \"art\""}
        url = "http://www.google.com/search?" + urllib.parse.urlencode(query)
        # print ("Search Query: ", url)
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        time.sleep(3)
        response = urllib.request.urlopen(req)
        html = response.read()

        soup = BeautifulSoup(html, "html.parser")

        num = soup.find_all(attrs={'id' : 'resultStats'})[0] # Find the element with id="resultStats"
        num_string = "" + str(num) # Make it a string
        num_string = re.sub("[^0-9]", "", num_string) # Take out everything except numbers
        num_final = int(num_string) # Convert to an int]
        row = [artist[0], num_string]
        print(row)
        writer.writerow(row)
    f.close()
