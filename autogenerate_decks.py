import requests
from retrieve_definition import retrieve_definition, open_search, text_wrangle


def get_params_autogen(term):
    """Sets the parameters for the API call for the initial user-entered term"""
    params = {
        "action": "parse",
        "prop": "links",
        "page": term,
        "format": "json",
    }
    # Parameter set to query the Wikipedia page for a given term and retrieve up to 250 links to other articles -
    # namespace 0 - from that page in JSON format.
    return params


def get_params_size(search_string):
    """Set parameters for API call that gets the article sizes for everything linked to the initial term article"""
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "size",
        "titles": search_string,
        "format": "json",
    }
    # Parameter set to query the Wikipedia pages for a list of terms and retrieve links from that page in JSON format.
    return params


def autogenerate(term):
    """Function to generate a set of extracts from a single user-entered term using the Wikipedia API"""
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"  # this is the base API URL for Wikipedia
    params = get_params_autogen(term)
    response = S.get(url=URL, params=params)
    data = response.json()
    if "error" in data.keys():
        return open_search(term)
    # if the term does not match a Wikipedia entry, the open_search function runs and suggests a different term
    links = data['parse']['links']
    # getting the list of links from the JSON object returned from the API call
    article_links = []
    count = 0
    # counter to track number of links being added to list
    exclude_types = ["List of", "History of", "Timeline of", "Glossary of"]
    for item in links:
        if (item['ns'] == 0) & ("exists" in item.keys()) & ~ any(excluded in item["*"] for excluded in exclude_types):
            # includes only titles that are namespace: 0 (articles only), exist,
            # and don't contain the listed exclusion phrases
            article_links.append(item["*"])
            count += 1
    if count < 2:
        return open_search(term)
    # if the term entered doesn't return any articles, suggest a different term
    articles = batch_search(article_links)
    cards = {}
    articles = [item for elem in articles for item in elem]
    # this turns the nested list returned by batch_search function into a flat list
    for article in articles:
        definition = retrieve_definition(article)
        cards.update({article: definition})

    S.close()
    return cards


def batch_search(terms_list, batch_size=50):
    """Function to break longer sets of related terms into groups of 50, the max allowed by the Wikipedia API call"""
    large_articles = []
    if len(terms_list) > batch_size:
        while len(terms_list) > batch_size:
            search_string = get_search_string(terms_list, batch_size)
            large_articles.append(get_article_size(search_string))
            terms_list = terms_list[batch_size:]
    if len(terms_list) < batch_size:
        search_string = get_search_string(terms_list, batch_size)
        large_articles.append(get_article_size(search_string))

    return large_articles


def get_article_size(search_string):
    """Function to get the size of each article connected to the initial search term"""
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"  # this is the base API URL for Wikipedia
    params = get_params_size(search_string)
    response = S.get(url=URL, params=params)
    data = response.json()
    page_ids = data["query"]["pages"].keys()
    articles = []
    for page_id in page_ids:
        if page_id != "-1":
            # a -1 page_id means that the page does not exist
            b_size = data["query"]["pages"][page_id]["revisions"][0]
            b_size = b_size["size"]
            if b_size > 50000:
                # article size is measured in bytes, this filters for only articles larger than 50k bytes using
                # article size as a rough approximation of whether a topic/title is important enough to have a card
                articles.append(data["query"]["pages"][page_id]["title"])
    S.close()
    return articles


def get_search_string(terms_list, batch_size=50):
    """Function to create a search string from the list of related terms"""
    search_string = ""
    for item in terms_list[:batch_size]:
        search_string = search_string + "|" + item
    search_string = search_string[1:]
    # creates string of titles separated by pipeline character in order to send through API
    return search_string
