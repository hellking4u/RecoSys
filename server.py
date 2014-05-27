#server.py
#import categorizer as cat_mod
import dmoz
phase_one = __import__("Phase 1")
import search_module as sm
from google import search
import string
import numpy as np
import pickle

favorite_color = { "lion": "yellow", "kitty": "red" }
source_probs = {}
source_probs['general'] = [0.25150121, 0.42066945, 0.32782934]
source_probs['technology'] = source_prob = np.array([1.0/3 for i in range(3)])
#source_probs = pickle.load( open( "source_probabilities.sp", "rb" ) )
pickle.dump( source_probs, open( "source_probabilities.sp", "wb" ) )


#maintain a hashmap for the sources

uri_list = []

def get_uri(kw, source_list, source_prob, n):
    global uri_list
    print "Current bucket of URIs :", str(len(uri_list))
    for index, provider in enumerate(source_list):
	    search_url_generator =  search(kw[0]+" "+provider[1], stop=n)
	    for i in range(n):
	    	try:
	    		uri_list.append((search_url_generator.next(),kw[1]*source_prob[index]))
	    	except:
	    		pass

def print_uri():
    for link in uri_list:
		print link

def run_server(kw_list,log = None):
	global source_probs
	global uri_list
	cat_list = {}
	cat_list['general'] = wiki_list = [("Wikipedia", "site:wikipedia.org"), ("Citizendium", "site:citizendium.org"), ("Britannica", "site:britannica.com")]
	cat_list['technology'] = [("gizmodo","gizmodo"), ("theverge","theverge"), ("engadget","engadget")]

	source_probs['general'] = phase_one.phase1_update(source_probs['general'], cat_list['general'], [item[0] for item in kw_list], 1, True, log = log)

	pickle.dump( source_probs, open( "source_probabilities.sp", "wb" ) )

	for kw in kw_list:
		kw_category = string.lower(dmoz.categorize(kw[0]))
		print kw, kw_category
		get_uri(kw,cat_list['general'], source_probs['general'], 2)
		if kw_category in cat_list.keys():
			source_probs[kw_category] = phase_one.phase1_update(source_probs[kw_category], cat_list[kw_category], [item[0] for item in kw_list], 1, True, log = log)
			get_uri(kw,cat_list[kw_category], source_probs[kw_category], 2)
	print_uri()
	return uri_list
		#source_probs = phase_one.phase1_update(source_prob, wiki_list, [kw[0]], n_iter, verbosity, log, mode_of_operation = 4):
		
if __name__ == '__main__':
	kw = [(u'hubble', 0.029575473945260247), (u'space', 0.020182425516724098), (u'telescope', 0.019276098609193208)]
	run_server(kw,"test_server_run")
