'''
API for the DMOZ : The Open Directory Project
'''

#url = http://www.dmoz.org/search?q=test

import urllib2
from bs4 import BeautifulSoup
import operator

# Using the dmoz search library
# 
def categorize(term):
	url = 'http://www.dmoz.org/search?q=' + term 

	conn = urllib2.urlopen(url)
	html = conn.read()

	soup = BeautifulSoup(html)
	list_of_cat = soup.findAll("ol", { "class" : "dir" })[0].findAll("li")
	ordered_list_of_cat = []
	for elem in list_of_cat:
		elem = elem.get_text().strip()
		elem = elem.replace(":","%&^*")
		elem = elem.replace("\t","")
		elem = elem.replace("\n","")
		elem = elem.replace("\r","")
		elem = elem.replace("   ","%&^*")
		elem = elem.split("%&^*")
		elem[-1] = int(elem[-1][1:-1])
		ordered_list_of_cat.append(elem)

	ordered_list_of_cat.sort(key=lambda x: x[-1], reverse=True)
	return ordered_list_of_cat[0][0]

if __name__=="__main__":
	print categorize("iPhone")