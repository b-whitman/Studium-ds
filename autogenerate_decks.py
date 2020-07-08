import requests
from retrieve_definition import retrieve_definition, open_search, text_wrangle


def autogenerate(term):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"  # this is the base API URL for Wikipedia

    params = {
        "action": "parse",
        "prop": "links",
        "page": term,
        "format": "json",
    }
    # Parameter set to query the Wikipedia page for a given term and retrieve up to 250 links to other articles -
    # namespace 0 - from that page in JSON format.

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
    articles = batch_search(article_links)
    cards = {}
    articles = [item for elem in articles for item in elem]
    # this turns the nested list returned by batch_search function into a flat list
    for article in articles:
        definition = retrieve_definition(article)
        cards.update({article: definition})

    S.close()
    return cards


def batch_search(terms_list):
    search_string = ""
    batch_size = 50
    large_articles = []
    if len(terms_list) > batch_size:
        while len(terms_list) > batch_size:
            for item in terms_list[:batch_size]:
                search_string = search_string + "|" + item
                search_string = search_string[1:]
            large_articles.append(get_article_size(search_string))
            terms_list = terms_list[batch_size:]
            search_string = ""
    if len(terms_list) < batch_size:
        for item in terms_list:
            search_string = search_string + "|" + item
        search_string = search_string[1:]
        large_articles.append(get_article_size(search_string))

    return large_articles


def get_article_size(search_string):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"  # this is the base API URL for Wikipedia

    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "size",
        "titles": search_string,
        "format": "json",
    }
    # Parameter set to query the Wikipedia pages for a list of terms and retrieve links from that page in JSON format.

    response = S.get(url=URL, params=params)
    data = response.json()
    page_ids = data["query"]["pages"].keys()
    articles = []
    for page_id in page_ids:
        if page_id != "-1":
            b_size = data["query"]["pages"][page_id]["revisions"][0]
            b_size = b_size["size"]
            if b_size > 50000:
                articles.append(data["query"]["pages"][page_id]["title"])
    S.close()
    return articles
