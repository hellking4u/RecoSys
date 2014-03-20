__author__ = 'nikhil'
"""
Wrapper for the pygoogle search module,

Uses get_articles for extracting content from search_list set.
"""
from google import search
import content_extractor

default_list = ["Wikipedia", "site:citizendium.org", "Britannica"]

def get_wiki_article(search_term, verbose=False, search_list=default_list):
    content_list = []
    if verbose:
        print "Begin Search Algorithm for keyword : ", search_term
    for provider in search_list:
        search_url_generator =  search(search_term+" "+provider, stop=1)
        root_url = search_url_generator.next()
        if verbose:
            print "Looking at Encyclopedia Article :", root_url
        term = content_extractor.get_content(root_url)
        if verbose:
            print term['meta'].encode('utf-8', errors='replace')
        content_list.append(term['content'])
    return content_list

if __name__ == "__main__":
    get_wiki_article("Dog", verbose = True)