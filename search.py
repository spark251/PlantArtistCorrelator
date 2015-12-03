"""
Takes a search query and searches google for the top results.
Take those top results and search each page for the occurrences of each
artist. Keep track of how many times those artist's names occur for all
of the pages.
"""
import json, urllib, sys, re, socket, csv, time, argparse, http.client
from urllib import request
from bs4 import BeautifulSoup

# Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def formatSeconds(sec) :
    """ Takes a number of seconds and converts it into hrs, mins, secs """
    # Convert the seconds to hours and minutes
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)

    # Get the correct word to go along with each string
    secStr = addS("second", "seconds", s)
    minStr = addS("minute", "minutes", m)
    hrStr = addS("hour", "hours", h)

    # Don't have unnecessary times displayed
    if h < 1.0 :
        if m < 1.0 :
            return format("%d %s" % (s, secStr))
        else :
            return format("%d %s %d %s" % (m, minStr, s, secStr))
    else :
        return format("%d %s %d %s %d %s" % (h, hrStr, m, minStr, s, secStr))

def addS(sing, plur, aNum) :
    """ Determines whether we need a singular or plural version of a word
    Ex: 1 minute, 2 minutes, 0 minutes, etc.

    Keyword arguments:
    sing -- The singular version of the word
    plur -- The plural version of the word
    aNum -- The number that determines which version of word to use
    """
    if aNum >= 1.0 and aNum < 2.0 :
        return sing
    else:
        return plur

def getUrls(query, engine = "google", startValue = 0, verbose=False) :
    """ Get's the urls from a given search engine for a query

    Keyword arguments:
    query -- The search query
    engine -- Which search engine to use (default: "google")
    startValue -- Used only for google. Determines what starting result google returns (default: 0)
    verbose -- Do you want verbose output or not? (default: False)
    """
    try:
        query = query.replace(" ", "+")
        if engine == "google" : # Google Search API (Depreciated, we must pray that it works)
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
            return []
    except (KeyboardInterrupt, SystemExit): # Let the program quit
        raise
    # But for God's sake catch everything else so the program does't randomly
    # crap out before it's finish.
    except Exception:
        if verbose :
            print(FAIL + "Couldn't get: " + ENDC + url)
        return []

def getPageText(url, verbose=False, timeout=10) :
    """ Gets the text from the page and returns it as a string

    Keyword Arguments:
    url -- The url of the page
    verbose -- Do you want it verbose? (default: False)
    timeout -- How long should we wait to try and get the page (default: 10)
    """
    try :
        if verbose :
            printurl = (url[:72] + '...') if len(url) > 75 else url
            print("Downloading... " + printurl)
        html = urllib.request.urlopen(url, timeout=timeout).read()
        return getVisibleText(html)
    except (KeyboardInterrupt, SystemExit): # Let the program quit
        raise
    # But for God's sake catch everything else so the program does't randomly
    # crap out before it's finish.
    except Exception:
        if verbose :
            print(FAIL + "Couldn't get: " + ENDC + url)
        return " "

def getVisibleText(readHTML) :
    """ Takes the page html and removes everything that isn't visible text
    on the page

    Keyword Arguemnts:
    readHTML -- The html to search
    """
    soup = BeautifulSoup(readHTML, "html.parser")
    texts = soup.findAll(text=True)
    paragraphs = ""
    for x in texts:
        paragraphs += str(x)
    return paragraphs

def printOccurrences(counter, artists) :
    """ Nicely prints the artists and the corresponding number of occurrences

    Keyword Arguments:
    counter -- The counter array of occurrences
    artists -- The artists array corresponding to number of occurrences
    """
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

def resultsToCsv(counter, artists, query, plantString, resultsFile) :
    """ Prints out everything to a CSV file

    Keyword Arguments:
    counter -- The counter array of occurrences
    artists -- The artists array corresponding to number of occurrences
    query -- The query that was originally searched for the plant
    plantString -- The plant that was searched
    resultsFile -- An csv file that has already been opened
    """
    # Format the data
    results = [plantString]

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

    resultsFile.write(resultString + "\n")
