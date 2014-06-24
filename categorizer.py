'''
TODO : disambiguishing error
'''
import urllib
import xmltodict
import wikipedia
import operator
#http://wikipedia-miner.cms.waikato.ac.nz/services/compare?term1=kiwi&term2=takahe

def get_correlation(t1,t2):
	'''
	Get correlation between two terms.

	NOTE : the two terms need to be exact wikipediac terms
	'''
	service_url = 'http://wikipedia-miner.cms.waikato.ac.nz/services/compare'
	params = {
	  'term1': t1,
	  'term2': t2
	}

	url = service_url + '?' + urllib.urlencode(params)
	HTTP_GET_DATA = urllib.urlopen(url).read()
	doc = xmltodict.parse(HTTP_GET_DATA)
	
	return doc['message']['@relatedness']

def get_correlation_by_id(id1,id2):
	'''
	utilizes the wikipedia module to figure out pageIDs..... it auto
	utilizes the auto-suggest feature so as to tackle common synonym issues
	'''
	service_url = 'http://wikipedia-miner.cms.waikato.ac.nz/services/compare'
	params = {
	  'id1': id1,
	  'id2': id2
	}

	url = service_url + '?' + urllib.urlencode(params)
	HTTP_GET_DATA = urllib.urlopen(url).read()
	doc = xmltodict.parse(HTTP_GET_DATA)
	
	return doc['message']['@relatedness']

def categorize(term):
	#print "categorizing term : ", term
	list_of_cats = ["Entertainment", "Technology", "People", "Science", "History", "Kids", "Arts", "Games"]
	try:
		term_page_id = wikipedia.page(term).pageid
		cat_corr = []
		for category in list_of_cats:
			#print '\t', category,
			cat_correlation = get_correlation_by_id(wikipedia.page(category).pageid, term_page_id)
			if (cat_correlation is None) or (len(cat_correlation) == 0):
				cat_corr.append(0)
			else:
				cat_corr.append(float(cat_correlation))
			cat_correlation
		max_index, max_value = max(enumerate(cat_corr), key=operator.itemgetter(1))
		return list_of_cats[max_index]
	except:
		return 'Disambiguish_cat'

if __name__ == '__main__':
	print categorize("Galileo")
	#categorize("Nexus 5")