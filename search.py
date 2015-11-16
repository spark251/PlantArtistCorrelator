import urllib
import urllib.parse
import urllib.request
import sys
import re
from bs4 import BeautifulSoup # To get everything

# Get the HTML from the search
query = { 'q' : sys.argv[1]}
url = "http://www.google.com/search?" + urllib.parse.urlencode(query)
print ("Search Query: ", url)
req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
response = urllib.request.urlopen(req)
html = response.read()

soup = BeautifulSoup(html, "html.parser")

num = soup.find_all(attrs={'id' : 'resultStats'})[0] # Find the element with id="resultStats"
num_string = "" + str(num) # Make it a string
num_string = re.sub("[^0-9]", "", num_string) # Take out everything except numbers
num_final = int(num_string) # Convert to an int
print ("Number of Results: ", str(num_final))
