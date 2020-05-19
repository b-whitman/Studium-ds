#!/usr/bin/python3

"""
    opensearch.py
    MediaWiki API Demos
    Demo of `Opensearch` module: Search the wiki and obtain
	results in an OpenSearch (http://www.opensearch.org) format
    MIT License
"""
def retrieve_definition(term):
    import requests

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exchars": "300",
        "titles": "Dog",
        "format": "json",
        "explaintext": 1,
        "exintro": 1,
        "exlimit": 1
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    return DATA