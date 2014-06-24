"""
Module for the server side of the recomender system application of source prioritization.

Functions :
get_uri
print_uri
run_server
"""

#server.py
#import categorizer as cat_mod
import dmoz
phase_one = __import__("Phase 1")
import search_module as sm
from google import search
import string
import numpy as np
import globalsfile as gl

#maintain a hashmap for the sources

uri_list = []

def get_uri(kw, cat, n):
    """
        Updates the global variable 'uri_list' based on the urls suggested from a keyword and a source list.

        Input:
            kw - Keywords
            cat - Category
            n - # of results to fetch
    """

    print "Current bucket of URIs :", str(len(uri_list))
    for index, provider in enumerate(gl.cat_list[cat]):
	    search_url_generator =  search(kw[0]+" "+provider[1], stop=n)
	    for i in range(n):
	    	try:
	    		uri_list.append((search_url_generator.next(),kw[1]*gl.source_probs[cat][index]))
	    	except:
	    		pass

def print_uri():
    """
        Prints the urls stored in the global variable 'uri_list'.
    """
    
    for link in uri_list:
        print link

def run_server(kw_list, log = None):
    """
        Runs the server based on the 'kw_list' given.

        Input:
            kw_list - List of keywords

        Output:
            uri_list - List of URLs related to the keywords
    """

    global uri_list
    
    gl.source_probs['general'] = phase_one.phase1_update('general', [item[0] for item in kw_list], verbosity = True, log = log, run_mean_mode = True)

    for kw in kw_list:
        kw_category = string.lower(dmoz.categorize(kw[0]))
        print kw, kw_category
        get_uri(kw, 'general', 1)
        if kw_category in gl.cat_list.keys():
            gl.source_probs[kw_category] = phase_one.phase1_update(kw_category, [item[0] for item in kw_list], verbosity = True, log = log, run_mean_mode = True)
            get_uri(kw, kw_category, 1)

    uri_list.sort(key = lambda x: x[-1], reverse = True)
    return uri_list
    #gl.source_probs = phase_one.phase1_update(gl.source_probs, wiki_list, [kw[0]], n_iter, verbosity, log, mode_of_operation = 4):

if __name__ == '__main__':
    """
        A test run for the module.
    """

    gl.init()

    kw_list = [(u'hubble', 0.029575473945260247), (u'space', 0.020182425516724098), (u'telescope', 0.019276098609193208)]
    run_server(kw_list, "test_server_run")
