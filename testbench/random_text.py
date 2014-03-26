'''
Module to generate text of a given size
'''

import random

def get_random_text(text_size):
	"""
	function return a random string of english words.

	INPUT : integer of the rough text length.
	OUTPUT : Random string
	"""
	r_text = '''He difficult contented we determine ourselves me am earnestly. Hour no find it park. Eat welcomed any husbands moderate. Led was misery played waited almost cousin living. Of intention contained is by middleton am. Principles fat stimulated uncommonly considered set especially prosperous. Sons at park mr meet as fact like. 

Started his hearted any civilly. So me by marianne admitted speaking. Men bred fine call ask. Cease one miles truth day above seven. Suspicion sportsmen provision suffering mrs saw engrossed something. Snug soon he on plan in be dine some. 

Living valley had silent eat merits esteem bed. In last an or went wise as left. Visited civilly am demesne so colonel he calling. So unreserved do interested increasing sentiments. Vanity day giving points within six not law. Few impression difficulty his use has comparison decisively. 

In alteration insipidity impression by travelling reasonable up motionless. Of regard warmth by unable sudden garden ladies. No kept hung am size spot no. Likewise led and dissuade rejoiced welcomed husbands boy. Do listening on he suspected resembled. Water would still if to. Position boy required law moderate was may. 

Considered an invitation do introduced sufficient understood instrument it. Of decisively friendship in as collecting at. No affixed be husband ye females brother garrets proceed. Least child who seven happy yet balls young. Discovery sweetness principle discourse shameless bed one excellent. Sentiments of surrounded friendship dispatched connection is he. Me or produce besides hastily up as pleased. Bore less when had and john shed hope. 
'''
	file_corpus = open("nouns.txt")
	text_corpus = []

	for word in file_corpus:
		text_corpus.append(word.strip())

	sum_text_size = 0

	for term in text_corpus:
		sum_text_size += len(term)
	average_word_size = sum_text_size/len(text_corpus) # intentional integer division
	print average_word_size

	required_terms = text_size/average_word_size
	random_text = ' '.join(random.sample(text_corpus, required_terms))
	return r_text
if __name__ =="__main__":
	print get_random_text(100);