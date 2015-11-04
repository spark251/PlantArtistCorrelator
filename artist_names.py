import urllib2
import urllib
import sys
import re
from bs4 import BeautifulSoup # To get everything

# Remove the html tags
def remove_tags(text):
    return re.sub('<[^>]*>', '', text)

# Read the links file into string
html = ""
with open ("links.html", "r") as myfile:
    html=myfile.read().replace('\n', '')

soup = BeautifulSoup(html, "html.parser")
results = soup.findAll('a') # Find all 'a' tags

# For each result remove the html tags and print them out
for result in results:
    print remove_tags(str(result)).lstrip()
