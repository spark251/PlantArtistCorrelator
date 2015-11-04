import urllib2
import urllib
import sys
import re
from bs4 import BeautifulSoup # To get everything

def remove_tags(text):
    return re.sub('<[^>]*>', '', text)

html = ""
with open ("links.html", "r") as myfile:
    html=myfile.read().replace('\n', '')



soup = BeautifulSoup(html, "html.parser")
results = soup.findAll('a')

for result in results:
    print remove_tags(str(result)).lstrip()
