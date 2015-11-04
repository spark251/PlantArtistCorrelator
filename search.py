import urllib2
import re
from bs4 import BeautifulSoup # To get everything

url = "http://www.google.com/search?q=query"
req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
response = urllib2.urlopen(req)
html = response.read()

soup = BeautifulSoup(html, "html.parser")

num = soup.find_all(attrs={'id' : 'resultStats'})[0] # Find the element with id="resultStats"
num_string = "" + str(num) # Make it a string
num_string = re.sub("[^0-9]", "", num_string) # Take out everything except numbers
num_final = int(num_string) # Convert to an int
print num_final
