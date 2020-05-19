#!/usr/bin/python3

"""
    Pull first 300 terms from Wikipedia article for a given term
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

    return DATA
