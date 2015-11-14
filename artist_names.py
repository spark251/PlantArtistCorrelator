
import urllib
import sys
import re
from lxml import html

# Remove the html tags
def remove_tags(text):
    return re.sub('<[^>]*>', '', text)

with open('artists.csv', 'w') as fp:
    # Read the links file into string
    txt = ""
    with open ("links.html", "r") as myfile:
        txt=myfile.read().replace('\n', '')

    tree = html.fromstring(txt)
    first_names = tree.xpath('//a')
    first_names_array = []
    first_names_array = first_names


    for x in range(0, len(first_names_array)) :
        if isinstance(first_names_array[x].text, basestring) :
            fp.write(str(first_names_array[x].text + first_names_array[x].find('b').text).strip()+",\n")
        else:
            fp.write(str(first_names_array[x].find('b').text).strip()+",\n")
