"""
Module for global variables that has to be accessed by more than one file.

Function:
init
"""
import numpy as np
import pickle
cache = {}

def save_cache():
    global cache
    pickle.dump( cache, open( "cache.p", "wb" ) )

def load_cache():
    global cache
    cache = pickle.load(open("cache.p", "rb" ))
    return cache

def init():
    """
        Initialize all the global variables.
        Should be called only once.
        Should be called only in the file in which it is used for the first time, eg. gui file.
    """
    global count
    global source_probs
    global cat_list
    global cache
    cache = load_cache()
    #print cache.keys()

    random_source = ("random","random")
    cat_list = {}
    cat_list['general'] = wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com")]
    for i in range(1):
        cat_list['general'].append(random_source)
    cat_list['technology'] = [("Gizmodo","gizmodo"), ("The Verge","theverge"), ("Engadget","engadget")]
    cat_list['computers'] = [("Gizmodo","gizmodo"), ("The Verge","theverge"), ("Engadget","engadget")]

    source_probs = {}
    count = {}

    for category in cat_list.keys():
        source_probs[category] = np.array([1.0/len(cat_list[category]) for i in range(len(cat_list[category]))])
        count[category] = 0
