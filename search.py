"""
Takes a search query and searches google for the top results.
Take those top results and search each page for the occurrences of each
artist. Keep track of how many times those artist's names occur for all
of the pages.
"""
import json, urllib, sys, re, socket, csv, time, argparse, http.client
from urllib import request
from bs4 import BeautifulSoup

def formatSeconds(sec) :
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    secStr = addS("second", "seconds", s)
    minStr = addS("minute", "minutes", m)
    hrStr = addS("hour", "hours", h)
    if h < 1.0 :
        if m < 1.0 :
            return format("%d %s" % (s, secStr))
        else :
            return format("%d %s %d %s" % (m, minStr, s, secStr))
    else :
        return format("%d %s %d %s %d %s" % (h, hrStr, m, minStr, s, secStr))

def addS(sing, plur, aNum) :
    if aNum >= 1.0 and aNum < 2.0 :
        return sing
    else:
        return plur

availableEngines = ["google", "duckduckgo"]

def getUrls(query, engine = "google", startValue = 0, verbose=False) :
    """
      Get's the urls from a given search engine for a query
    """
    query = query.replace(" ", "+")
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

def oneLinePrint(printStr, lines=60) :
    sys.stdout.flush()
    for x in range(0, lines) :
        sys.stdout.write(" ")
    sys.stdout.write('\r')
    sys.stdout.write((printStr[:lines-1] + '..') if len(printStr) > lines-1 else printStr)

def getPageText(url, verbose=False, timeout=10) :
    """
    Gets the text from the page and returns it as a string
    """
    try :
        if verbose :
            printurl = (url[:75] + '..') if len(url) > 75 else url
            oneLinePrint("Searching... " + url, 75)
        html = urllib.request.urlopen(url, timeout=timeout).read()
        return getVisibleText(html)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        if verbose :
            oneLinePrint("Couldn't get: " + url, 75)
        return " "

def getVisibleText(readUrl) :
    soup = BeautifulSoup(readUrl, "html.parser")
    texts = soup.findAll(text=True)
    paragraphs = ""
    for x in texts:
        paragraphs += str(x)
    return paragraphs

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

def resultsToCsv(counter, artists, query, plant_string, results_file) :
    # Format the data
    results = [plant_string]

    firstRun = True

    ## The maximum number of occurrences of any given name
    maxOccurrences = max(counter)
    if maxOccurrences <= 3 :
        results.append("No results");
    else :
        ## Print out all the artists that matched the search
        for occurrences in reversed(range(1, maxOccurrences + 1)) :
            # Index of counter array with the max value
            theIndexes = [i for i, x in enumerate(counter) if x == occurrences]
            if len(theIndexes) != 0 :
                for x in theIndexes :
                    if firstRun :
                        results.append(query + " " + artists[x])
                        firstRun = False
                    if occurrences > 3 :
                        results.append(artists[x] + " (" + str(occurrences) + ")")

    # Write data to file in a new row in csv format
    resultString = ""
    for result in results :
        resultString += result + ", "

    results_file.write(resultString + "\n")
