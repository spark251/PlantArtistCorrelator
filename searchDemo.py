import json, urllib, sys, re, socket, csv, time, argparse, http, search

if __name__ == '__main__':
    helpText = """
    Takes a search query and searches google for the top results.
    Take those top results and search each page for the occurrences of each
    artist. Keep track of how many times those artist's names occur for all
    of the pages.
    """
    parser = argparse.ArgumentParser(description=helpText)
    parser.add_argument("-v", "--verbose",
                action="store_true", dest="verbose", default=True,
                help="run with lots of info [default]")
    parser.add_argument("-q", "--quiet",
                action="store_false", dest="verbose",
                help="run quietly")
    parser.add_argument("-t", "--timeout", metavar="TIME",
                action="store", dest="timeout", default=10, type=float,
                help="set the timeout for searching each page [default=10s]")
    parser.add_argument("-e", "--engine", action="store", dest="engine",
                default="duckduckgo", type=str, choices=search.availableEngines,
                help="the search engine you want to use to get results")
    parser.add_argument("-f", "--file", action="store", type=str,
                dest="csv", default="artists.csv",
                help="specify the artists.csv file [default=artists.csv]")
    parser.add_argument('query', type=str,
                help='what to search for')

    args = parser.parse_args()

    # Show user that their request is "Loading..."
    if args.verbose is False :
         sys.stdout.write('\rLoading... ')

    url1 = search.getUrls(args.query, "google", verbose=args.verbose)
    url2 = search.getUrls(args.query, "duckduckgo", verbose=args.verbose)

    in_first = set(url1)
    in_second = set(url2)
    in_second_but_not_in_first = in_second - in_first

    urls = url1 + list(in_second_but_not_in_first)
    ## Open ARTISTS_LIST as a list called artists
    try:
        artists_list = args.csv
    except IndexError :
        parser.print_help()
        exit()

    try:
        reader = csv.reader(open(artists_list, 'r'))
        tempArtists = list(reader)
        artists = []
        for artist in tempArtists:
            artists.append(artist[0])
    except FileNotFoundError :
        print("The artists file is not found. Quitting...")
        exit()

    # Search the urls for occurrences of artist names

    ## Open each url and add to one string HTMLOfPages
    HTMLOfPages = ""
    for url in urls :
        html = search.getPageText(url, verbose=args.verbose, timeout=args.timeout)
        HTMLOfPages += html

    # There is an artist named "Erro" and he get's matched for every single
    # "error" in the site text. Since no artist has "error" in their name
    # we can safely get rid of "error" strings without messing up the results.
    pattern = re.compile("error", re.IGNORECASE)
    HTMLOfPages = pattern.sub("", HTMLOfPages.lower())

    ## For each artist, count the number of occurrences that artist has in the
    ## file and add it to an array (counter) with it's index corresponding to
    ## the index of that artist

    counter = []
    for index, artist in enumerate(artists, start=0):
        count = HTMLOfPages.count(artist.lower())
        counter.append(count)
    #print(len(counter))


    # Remove "Loading..."
    if args.verbose is False :
        sys.stdout.write("\r")

    search.printOccurrences(counter, artists)
