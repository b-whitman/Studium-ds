#!/usr/bin/python3

"""
    Pull first 300 characters from Wikipedia article for a given term
"""
def retrieve_definition(term):
    import requests

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exchars": "300",
        "titles": term,
        "format": "json",
        "explaintext": 1,
        "exintro": 1,
        "exlimit": 1
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    key = list(DATA['query']['pages'].keys())[0]
    extract = DATA['query']['pages'][key]['extract']

    if len(extract) == 3:
        return open_search(term)

        #exceptions function goes here

    else:
        return extract

def open_search(term):
    import requests
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "opensearch",
        "search": term,
        "redirects": "resolve",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    suggests = DATA[1]
    return suggests