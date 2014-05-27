'''
Module to generate text of a given size.

Function:
get_random_text
'''

import random

def get_random_text(text_size):
	"""
	function return a random string of english words.

	INPUT : integer of the rough text length.
	OUTPUT : Random string
	"""
	
	file_corpus = open("nouns.txt")
	text_corpus = []

	for word in file_corpus:
		text_corpus.append(word.strip())

	sum_text_size = 0

	for term in text_corpus:
		sum_text_size += len(term)
	average_word_size = sum_text_size/len(text_corpus) # intentional integer division

	required_terms = text_size/(average_word_size*2)
	random_text = ' '.join(random.sample(text_corpus, required_terms))
	return random_text

if __name__ =="__main__":
	print get_random_text(1000);
