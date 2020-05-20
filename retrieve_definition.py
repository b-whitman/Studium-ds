#!/usr/bin/python3

"""
    Pull first 300 characters from Wikipedia article for a given term
"""
def retrieve_definition(term):
    import requests
    import json

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

    if extract == '...':
        pass
        #exceptions function goes here

    return extract

def open_search(term):
