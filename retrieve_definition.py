#!/usr/bin/python3

"""
    Pull first 300 characters from Wikipedia article for a given term
"""


def retrieve_definition(term):
    import requests

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"  # this is the base API URL for Wikipedia

    PARAMS = {
        "action": "query",
        "prop": "extracts",
        "exchars": "300",
        "titles": term,
        "format": "json",
        "explaintext": 1,
        "exlimit": 1
    }

    # parameters set to query for an extract of 300 characters for the given term, in JSON format. Explaintext strips out
    # Wikipedia's special formatting. Exlimit says to only return 1 extract.

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    pageid = list(DATA['query']['pages'].keys())[0]
    try:
        extract = DATA['query']['pages'][pageid]['extract']
    # this selects the extract from within the JSON object returned by the API call. Two steps are necessary because one
    # of the dictionary keys is the page ID for that term.

        if len(extract) == 3:
            return text_wrangle(term)

        else:
            return extract
    except KeyError:
        #sometimes instead of an empty string as an extract the API call returns a "missing" key in JSON, this accounts
        #for that
        return text_wrangle(term)


def open_search(term):
    """
    function to use opensearch on Wikipedia API and return most likely related articles for a given term. opensearch
    is a Wikimedia API feature which returns similarly-titled articles within the wiki.
    """
    import requests
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "opensearch",
        "search": term,
        "redirects": "resolve",
        "format": "json"
    }

    # Parameters set tells API to use opensearch on the given term and return the results as a JSON object.
    # Resolve means to return redirects as the page they point to.

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    suggests = DATA[1]
    return f"Did you mean {suggests[0]}, {suggests[1]}, {suggests[2]}?"

def text_wrangle(term):
    """
    Check text for various edge cases and re-run
    """
    if term.isupper():
        return retrieve_definition(term.lower())
    elif (term[0:4] == 'the ') | (term[0:4] == 'The '):
        return retrieve_definition(term[4:])
        #sends term back through function minus 'the'
    elif term[-1:] == 's':
        return retrieve_definition(term[:-1])
        #sends terms back through function without final 's'
    elif term[-1:] == 'e':
        #this accounts for cases of "es" plural, the previous cycle would have removed the 's'
        term = term[:-1]
        return retrieve_definition(term[:-1])
    else:
        return open_search(term)
        #all of the test cases have failed, function will return suggestions instead
