"""
Takes a search query and searches google for the top results.
Take those top results and search each page for the occurrences of each
artist. Keep track of how many times those artist's names occur for all
of the pages.
"""
import json, urllib, sys, re, socket, csv, time, argparse, http
from urllib import request
from bs4 import BeautifulSoup


availableEngines = ["google", "duckduckgo"]

def getUrls(query, engine = "google", startValue = 0, verbose=False) :
    """
      Get's the urls from a given search engine for a query
    """
    query = query.replace(" ", "+")
    try:
        if engine == "google" : # Google Search API (Depreciated)
            url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&q="+ query +"&start=" + str(startValue)
            if verbose :
                print("Search query: ", url)
            time.sleep(5)
            req = urllib.request.urlopen(url)
            reqtxt = req.read().decode(req.info().get_param('charset') or 'utf-8')
            rJson = json.loads(reqtxt)
            urls = []
            for result in rJson["responseData"]["results"] :
                urls.append(result["unescapedUrl"])
            return urls

        elif engine == "duckduckgo" : # DuckDuckGo parsing
            url = "http://duckduckgo.com/html/?q=" + query
            if verbose :
                print("Search query: ", url)
            data = urllib.request.urlopen(url)
            parsed = BeautifulSoup(data, "html.parser")
            urls = []
            for i in parsed.findAll('div', {'class': re.compile('links_main*')}):
                urls.append(i.a['href'])
            return urls
        else:
            print("Invalid engine. Quitting...")
            exit()
    except (urllib.error.HTTPError, ValueError) :
        print("The query you entered is not valid. Quitting...")
        exit()

def getPageText(url, verbose=False, timeout=10) :
    """
    Gets the text from the page and returns it as a string
    """
    try :
        if verbose :
            printurl = (url[:75] + '..') if len(url) > 75 else url
            print("Searching... ", printurl)
        html = urllib.request.urlopen(url, timeout=timeout).read()
        soup = BeautifulSoup(html, "html.parser")
        texts = soup.findAll(text=True)
        paragraphs = ""
        for x in texts:
            paragraphs += str(x)
        return paragraphs
    except (socket.timeout, ConnectionRefusedError, urllib.error.URLError,
            ValueError, http.client.BadStatusLine) :
        if verbose :
            print("Couldn't get: ", url)
        return " "

def printOccurrences(counter, artists) :
    ## The maximum number of occurrences of any given name
    maxOccurrences = max(counter)
    if maxOccurrences is 0 :
        print("No results");
    else :
        ## Print out all the artists that matched the search
        for occurrences in reversed(range(1, maxOccurrences + 1)) :
            # Index of counter array with the max value
            theIndex = [i for i, x in enumerate(counter) if x == occurrences]

            # Print out the results
            if occurrences == 0 :
                print("No results");
            else :
                if len(theIndex) != 0 :
                    print("Occurrences: ", occurrences)
                    for x in theIndex :
                        print(" - Artist: ", artists[x])
                        #print("Index: ", x)
